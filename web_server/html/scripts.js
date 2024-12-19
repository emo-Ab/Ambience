async function fetchData(url) {
    try {
        const response = await fetch(url);
        return await response.text();
    } catch (error) {
        console.error('Error:', error);
    }
}

async function addDeviceName() {
    const data = await fetchData('http://192.168.0.52:8087/');
    document.getElementById('deviceNameTitle').value = data;
}

async function updateColor() {
    const data = await fetchData('http://192.168.0.52:8085/');
    const [r, g, b] = data.split(',').map(Number);
    document.getElementById('colorBox').style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
}

async function updateText() {
    const data = await fetchData('http://192.168.0.52:8086/');
    document.getElementById('singleLineText').value = data;
}

setInterval(updateColor, 5000);
setInterval(updateText, 5000);
setInterval(addDeviceName, 5000);

addDeviceName();
updateColor();
updateText();