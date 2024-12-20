const http = require('http');
const https = require('https');
const url = require('url');
const path = require('path')
const fs = require('fs')
const config = require('config');

const hostname = config.get('webserver-address')

// Http Server to retrieve the latest values for a device on port 8085
const retrieveServer = http.createServer((req, res) => {
    const queryObject = url.parse(req.url, true).query;

    if (queryObject.device) {
        const deviceName = queryObject.device;
        const devicePath = `./data/${deviceName}.txt`;
        // Check if the file exists
        if (fs.existsSync(devicePath)) {
            // Read the file contents
            fs.readFile(devicePath, 'utf8', (err, data) => {
                if (err) {
                    console.error('Error reading file', err);
                    res.writeHead(500, { 'Content-Type': 'text/plain' });
                    res.end('Error reading file');
                } else {
                    // Split the file content into lines and get the first 3 lines
                    const lines = data.split('\n').slice(-3).join('\n');
                    res.writeHead(200, {
                        'Content-Type': 'text/plain',
                        'Access-Control-Allow-Origin' : '*'
                    });
                    res.end(lines);
                }
            });
        } else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('Device is not connected');
        }
    } 
    else if (req.url.startsWith('/alldevices')){
        const devList = './data/devicelist.txt';
        if (fs.existsSync(devList)) {
            fs.readFile(devList, 'utf8', (err, data) => {
                if (err) {
                    console.error('Error reading file', err);
                } else {
                    res.writeHead(200, {
                         'Content-Type': 'text/plain',
                         'Access-Control-Allow-Origin' : '*'
                    });
                    res.end(data);
                }
            });
        }        
    }
    else {
        res.writeHead(400, { 'Content-Type': 'text/plain' });
        res.end('Invalid Query');
    }
});

retrieveServer.listen(config.get('data-port'), () => {
    console.log('Data Server is running on http://' + hostname + ':' + config.get('data-port') + '/');
});

// Read SSL certificate and key
const options = {
    key: fs.readFileSync('./certificates/server-private.pem'),
    cert: fs.readFileSync('./certificates/server.pem')
  };

// Http Server to update the latest values for a device on port 8080
const updateServerHttps = https.createServer(options, (req, res) => {
    const queryObject = url.parse(req.url, true).query;
    /* Check if a device Id exists */
    if (queryObject.device) {
        const params = new URLSearchParams(queryObject.params);
        const deviceName = queryObject.device;
        const rgbValue = queryObject.rgb;
        const speechText = queryObject.text;

        // Check if the file exists
        if (!fs.existsSync(`./data/${deviceName}.txt`)) {
            const addDevice = deviceName + '\n';
            // Append the data to a file named after the device
            fs.appendFile(`./data/devicelist.txt`, deviceName, (err) => {
                if (err) {
                    res.writeHead(400, { 'Content-Type': 'text/plain' });
                    res.end('Device cannot be added');
                }
            });
        }

        // Create a string with the values
        const data = `Device: ${deviceName}\nRGB: ${rgbValue}\nText: ${speechText}\n`;

        console.log(data);
        // Append the data to a file named after the device
        fs.appendFile(`./data/${deviceName}.txt`, data, (err) => {
            if (err) {
                res.writeHead(400, { 'Content-Type': 'text/plain' });
                res.end('Device cannot be stored');
            }
        });

        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('Data Updated');

    } else {
        res.writeHead(400, { 'Content-Type': 'text/plain' });
        res.end('Invalid Query');
    }
});

updateServerHttps.listen(config.get('update-port-https'), () => {
    console.log('Update server running at https://' + hostname + ':' + config.get('update-port-https') + '/');
});