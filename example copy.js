// example.js
// Simple script to prompt for a URL, fetch the content, and print the raw HTTP response or parsed content.

const readline = require('readline');
const https = require('https');
const http = require('http');
const { URL } = require('url');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Enter a URL to fetch: ', (urlStr) => {
  try {
    const url = new URL(urlStr);
    const client = url.protocol === 'https:' ? https : http;
    const options = {
      method: 'GET',
      headers: {
        'User-Agent': 'Node.js Example Script'
      }
    };
    const req = client.request(url, options, (res) => {
      let data = '';
      res.on('data', chunk => { data += chunk; });
      res.on('end', () => {
        console.log('Status:', res.statusCode);
        console.log('Headers:', res.headers);
        console.log('\n--- Content (truncated to 1000 chars) ---\n');
        console.log(data.slice(0, 1000));

        // Find the first line containing '"name"' and extract the next string value
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
        // Values are now available in nameValue and imageValue
        rl.close();
      });
    });
    req.on('error', (e) => {
      console.error('Error fetching URL:', e.message);
      rl.close();
    });
    req.end();
  } catch (e) {
    console.error('Invalid URL:', e.message);
    rl.close();
  }
});
