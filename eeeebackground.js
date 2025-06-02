// Import Netflix extraction logic from netflix.js
import { extractNetflixTitleAndImage } from './src/netflix.js';

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendToCalc",
    title: "Send to LibreOffice Calc",
    contexts: ["all"] // Show in all cases, not just selection
  });
});

// Native Messaging: send selected text and URL to native host
function sendToNativeHost(selectedText, pageUrl, imageSrc = null) {
  const messageData = { 
    text: selectedText, 
    url: pageUrl || "" 
  };
  
  // Add image source if provided
  if (imageSrc) {
    messageData.imageSrc = imageSrc;
  }
  
  chrome.runtime.sendNativeMessage(
    "com.example.browsertocalc",
    messageData,
    (response) => {
      if (chrome.runtime.lastError) {
        let errorMessage = chrome.runtime.lastError.message;
        if (errorMessage.includes("host not found")) {
          console.error("Native host not found. Please check if Python script is properly registered.");
        } else if (errorMessage.includes("Native host has exited")) {
          // This is normal when the script completes successfully
          console.log("Native host completed successfully");
        } else {
          console.error("Native Messaging Error:", errorMessage);
        }
      } else if (response && response.result === "OK") {
        console.log("Successfully saved to LibreOffice Calc");
      } else if (response && response.result === "ERROR") {
        console.error("Error saving to Calc:", response.error || "Unknown error");
      } else {
        console.warn("Unexpected response:", response);
      }
    }
  );
}

// Function to parse DVD poster image from fsmirror pages
function readActiveTabContent(callback) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    if (tabs.length === 0) {
      console.warn('No active tabs found');
      callback("");
      return;
    }
    
    const tab = tabs[0];
    console.log('Attempting to parse content from tab:', tab.id, tab.url);
    
    // Check if the URL contains "fsmirror"
    if (!tab.url.includes('fsmirror')) {
      console.warn('URL does not contain "fsmirror":', tab.url);
      callback("This function only works on fsmirror URLs");
      return;
    }
    
    // Check if the tab URL is valid for content script injection
    if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://') || 
        tab.url.startsWith('edge://') || tab.url.startsWith('about:')) {
      console.warn('Cannot inject script into system page:', tab.url);
      callback("Cannot read content from system pages");
      return;
    }
    
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      func: () => {
        // Parse the specific DVD poster image from the dvd-container
        try {
          // Find the div with class "dvd-container" and onclick="showDvdPoster()"
          const dvdContainer = document.querySelector('div.dvd-container[onclick="showDvdPoster()"]');
          
          if (!dvdContainer) {
            return {
              success: false,
              error: 'DVD container not found',
              url: window.location.href,
              title: document.title || 'No title'
            };
          }
          
          // Find the img tag inside the dvd-container
          const imgTag = dvdContainer.querySelector('img');
          
          if (!imgTag || !imgTag.src) {
            return {
              success: false,
              error: 'Image tag or src attribute not found in DVD container',
              url: window.location.href,
              title: document.title || 'No title'
            };
          }
          
          return {
            success: true,
            imageSrc: imgTag.src,
            url: window.location.href,
            title: document.title || 'No title',
            altText: imgTag.alt || 'No alt text'
          };
          
        } catch (e) {
          return {
            success: false,
            error: 'Error parsing DVD poster: ' + e.message,
            url: window.location.href,
            title: document.title || 'No title'
          };
        }
      }
    }, (results) => {
      if (chrome.runtime.lastError) {
        console.error('Script injection error:', chrome.runtime.lastError.message);
        callback(`Error reading content: ${chrome.runtime.lastError.message}`);
        return;
      }
      
      if (!results || !results[0]) {
        console.error('No results returned from script execution');
        callback("No results returned from content script");
        return;
      }
      
      const result = results[0].result;
      console.log('DVD poster parsing result:', result);
        if (result.success) {
        // Return only the img src and alt values
        const content = `${result.imageSrc}
${result.altText}`;
        callback(content);
      } else {
        callback(`Error: ${result.error}`);
      }
    });
  });
}

// Function to parse title and image from Netflix pages using external logic
function readNetflixTabContent(callback) {
  chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
    if (tabs.length === 0) {
      console.warn('No active tabs found');
      callback("");
      return;
    }
    const tab = tabs[0];
    console.log('Attempting to parse content from tab:', tab.id, tab.url);
    // Check if the URL contains "netflix"
    if (!tab.url.includes('netflix')) {
      console.warn('URL does not contain "netflix":', tab.url);
      callback("This function only works on netflix URLs");
      return;
    }
    // Check if the tab URL is valid for content script injection
    if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://') || 
        tab.url.startsWith('edge://') || tab.url.startsWith('about:')) {
      console.warn('Cannot inject script into system page:', tab.url);
      callback("Cannot read content from system pages");
      return;
    }
    chrome.scripting.executeScript({
      target: {tabId: tab.id},
      func: extractNetflixTitleAndImage,
    }, (results) => {
      if (chrome.runtime.lastError) {
        console.error('Script injection error:', chrome.runtime.lastError.message);
        callback(`Error reading content: ${chrome.runtime.lastError.message}`);
        return;
      }
      if (!results || !results[0]) {
        console.error('No results returned from script execution');
        callback("No results returned from content script");
        return;
      }
      const result = results[0].result;
      console.log('Netflix parsing result:', result);
      if (result.success) {
        // Return name and image as selected text and imageSrc
        callback({ selectedText: result.name, imageSrc: result.image });
      } else {
        callback({ selectedText: '', imageSrc: '', error: result.error });
      }
    });
  });
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  console.log('Context menu clicked:', info.menuItemId, info, tab);
  if (info.menuItemId === "sendToCalc") {
    chrome.tabs.get(tab.id, (tabInfo) => {
      console.log('sendToCalc triggered');
      if (tabInfo && tabInfo.url) {
        if (tabInfo.url.includes('fsmirror')) {
          // FSMirror page
          console.log('FSMirror page detected, parsing DVD poster info');
          readActiveTabContent((content) => {
            console.log('Parsed DVD poster content:', content);
            const lines = content.split('\n');
            const imageSrc = lines.length > 0 ? lines[0] : '';
            const altText = lines.length > 1 ? lines[1] : content;
            console.log('Sending alt text to Calc:', altText);
            console.log('Sending image src to Calc:', imageSrc);
            sendToNativeHost(altText, tabInfo.url || "", imageSrc);
          });
        } else if (tabInfo.url.includes('netflix')) {
          // Netflix page
          console.log('Netflix page detected, parsing title and image info');
          readNetflixTabContent((content) => {
            console.log('Parsed Netflix content:', content);
            sendToNativeHost(content.selectedText, tabInfo.url || "", content.imageSrc);
          });
        } else {
          // Other pages
          sendToNativeHost(info.selectionText, tabInfo.url || "");
        }
      } else {
        sendToNativeHost(info.selectionText, tabInfo.url || "");
      }
    });
  } else {
    console.warn('Unknown context menu item clicked:', info.menuItemId);
  }
});
