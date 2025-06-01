chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendToCalc",
    title: "Send to LibreOffice Calc",
    contexts: ["all"] // Show in all cases, not just selection
  });
});

// Native Messaging: send selected text and URL to native host
function sendToNativeHost(selectedText, pageUrl) {
  chrome.runtime.sendNativeMessage(
    "com.example.browsertocalc",
    { text: selectedText, url: pageUrl || "" },
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

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "sendToCalc") {
    // Use chrome.tabs API to get the active tab's URL
    chrome.tabs.get(tab.id, (tabInfo) => {
      sendToNativeHost(info.selectionText, tabInfo.url || "");
    });
  }
});