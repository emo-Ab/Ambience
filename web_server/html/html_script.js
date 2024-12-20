async function fetchDeviceNames() {
    const response = await fetch('http://192.168.0.52:8085/alldevices');
    const text = await response.text();
    return text.split('\r\n');
}

async function fetchDeviceData(deviceName) {
    const response = await fetch(`http://192.168.0.52:8085/?device=${deviceName}`);
    return response.text();
}

async function displayDevices() {
    const deviceContainer = document.getElementById('device-container');
    deviceContainer.innerHTML = ''; // Clear previous data
    const deviceNames = await fetchDeviceNames();

    for (const deviceName of deviceNames) {
        const deviceData = await fetchDeviceData(deviceName);
        // Parse the device data
        const [rgb, text] = deviceData.split('\r\n');
        const [r, g, b] = rgb.match(/\d+/g).map(Number);

        const deviceDataElement = document.createElement('div');
        deviceDataElement.className = 'device-section';
        deviceDataElement.innerHTML = `<h2>${deviceName}</h2><p>${deviceData}</p>`;

        // Add styles for the colored box
        deviceDataElement.style.border = '1px solid #ccc';
        deviceDataElement.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        deviceDataElement.style.padding = '10px';
        deviceDataElement.style.margin = '10px 0';
        deviceDataElement.style.borderRadius = '5px';

        deviceContainer.appendChild(deviceDataElement);
    }    
}


// Fetch and display device data every second
setInterval(displayDevices, 1000);