// example.js
// Simple script to prompt for a URL, fetch the content, and print the raw HTTP response or parsed content.

const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter a URL to fetch: ', async (urlStr) => {
  try {
    const response = await fetch(urlStr, {
      headers: {
        'User-Agent': 'Node.js Example Script'
      }
    });
    const data = await response.text();
    // Print the whole response unfiltered
    console.log('\n--- Full Response ---\n');
    console.log(data);
    // Find the first line containing '"name"' and '"image"' and extract their string values
    const lines = data.split(/\r?\n/);
    let nameValue = null;
    let imageValue = null;
    for (let line of lines) {
      if (nameValue === null && line.includes('"name"')) {
        const match = line.match(/"name"\s*:\s*"([^"\r\n]+)"/);
        if (match) {
          nameValue = match[1];
        }
      }
      if (imageValue === null && line.includes('"image"')) {
        const match = line.match(/"image"\s*:\s*"([^"\r\n]+)"/);
        if (match) {
          imageValue = match[1];
        }
      }
      if (nameValue !== null && imageValue !== null) break;
    }
    console.log('Extracted name:', nameValue);
    console.log('Extracted image:', imageValue);
    rl.close();
  } catch (e) {
    console.error('Error fetching URL:', e.message);
    rl.close();
  }
});
