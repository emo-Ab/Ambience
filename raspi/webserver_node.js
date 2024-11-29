const http = require('http');
const url = require('url');
const path = require('path')
const fs = require('fs')

let variableValue = '....';

// Read the HTML file
const htmlFilePath = path.join(__dirname, '/html/index.html');
const htmlContent = fs.readFileSync(htmlFilePath, 'utf8');

// Server to update variable value on port 8080
const updateServer = http.createServer((req, res) => {
    const queryObject = url.parse(req.url, true).query;
    if (queryObject.value) {
        variableValue = queryObject.value;
    }

    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });

    res.end(variableValue);
});

updateServer.listen(8080, () => {
    console.log('Update server running at http://127.0.0.1:8080/');
});


// Server to display html page on Port 3000
const htmlServer = http.createServer((req, res) => {
    const queryObject = url.parse(req.url, true).query;
    if (queryObject.value) {
        variableValue = queryObject.value;
    }

    res.writeHead(200, {
    'Content-Type': 'text/html',
    'Access-Control-Allow-Origin': '*'
    });

    res.end(htmlContent);
});

htmlServer.listen(3000, () => {
    console.log('Server running at http://192.168.0.180:8080/');
});
