const http = require('http');
const url = require('url');
const path = require('path')
const fs = require('fs')
const config = require('config');

const hostname = config.get('webserver-address')
let variableValue = '10,10,10';
let speechText = 'nothing';
let deviceName = '';

// Read the HTML file
const htmlFilePath = path.join(__dirname, '/html/webui.html');
const htmlContent = fs.readFileSync(htmlFilePath, 'utf8');

// Server to update variable value on port 8080
const updateServer = http.createServer((req, res) => {
    const queryObject = url.parse(req.url, true).query;

    if (queryObject.device) {
        deviceName = queryObject.device;
    }

    if (queryObject.value) {
        variableValue = queryObject.value;
    }

    if (queryObject.text) {
        speechText = queryObject.text;
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
const retrieveRGB = http.createServer((req, res) => {
    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });

    res.end(variableValue);
});

retrieveRGB.listen(config.get('rgb-port'), () => {
    console.log('Retrieve server running at http://' + hostname + ':8085/');
});

// Server to update variable value on port 8080
const retrieveSpeech = http.createServer((req, res) => {
    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });

    res.end(speechText);
});

retrieveSpeech.listen(config.get('speech-port'), () => {
    console.log('Retrieve server running at http://' + hostname + ':8086/');
});

// Server to update variable value on port 8080
const retrieveDevice = http.createServer((req, res) => {
    res.writeHead(200, {
        'Content-Type': 'text/plain',
        'Access-Control-Allow-Origin': '*'
    });

    res.end(deviceName);
});

retrieveDevice.listen(config.get('device-port'), () => {
    console.log('Retrieve server running at http://' + hostname + ':8087/');
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
