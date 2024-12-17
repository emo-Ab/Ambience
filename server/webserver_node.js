const http = require('http');
const url = require('url');
const path = require('path')
const fs = require('fs')
const config = require('config');

const hostname = config.get('webserver-address')
let variableValue = '10,10,10';

// Read the HTML file
const htmlFilePath = path.join(__dirname, '/html/index.html');
const htmlContent = fs.readFileSync(htmlFilePath, 'utf8');

// Server to update variable value on port 8080
const updateServer = http.createServer((req, res) => {
    const queryObject = url.parse(req.url, true).query;
    if (queryObject.value) {
        variableValue = queryObject.value;
        console.log('Update requested');
    }

    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });

    res.end('updated');
});

updateServer.listen(config.get('update-port'), () => {
    console.log('Update server running at http://' + hostname + ':8080/');
});

// Server to update variable value on port 8080
const retrieveServer = http.createServer((req, res) => {
    console.log('Value requested');
    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });

    res.end(variableValue);
});

retrieveServer.listen(config.get('read-port'), () => {
    console.log('Retrieve server running at http://' + hostname + ':8085/');
});

// Server to display html page on Port 3000
const htmlServer = http.createServer((req, res) => {

    console.log('Page requested');
    res.writeHead(200, {
    'Content-Type': 'text/html',
    'Access-Control-Allow-Origin': '*'
    });

    res.end(htmlContent);
});

htmlServer.listen(config.get('webclient-port'), () => {
    console.log('Server running at http://' + hostname + ':3000/');
});
