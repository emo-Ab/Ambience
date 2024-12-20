async function fetchDeviceNames() {
    const response = await fetch('http://192.168.0.31:8085/alldevices');
    const text = await response.text();
    return text.split('\r\n');
}

async function fetchDeviceData(deviceName) {
    const response = await fetch(`http://192.168.0.31:8085/?device=${deviceName}`);
    return response.text();
}

async function displayDevices() {
    const deviceContainer = document.getElementById('device-container');
    deviceContainer.innerHTML = ''; // Clear previous data
    const deviceNames = await fetchDeviceNames();

    for (const deviceName of deviceNames) {
        const deviceData = await fetchDeviceData(deviceName);
        const [rgb, speech] = deviceData.split('\n');
        const [r, g, b] = rgb.match(/\d+/g).map(Number);

        const deviceDataElement = document.createElement('div');
        deviceDataElement.className = 'device-section';
        deviceDataElement.innerHTML = `
        <h2>${deviceName}</h2>
        <p>${speech.substring(5)}</p>
        `;
        deviceDataElement.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
        deviceContainer.appendChild(deviceDataElement);
    }    
}


// Fetch and display device data every second
setInterval(displayDevices, 5000);