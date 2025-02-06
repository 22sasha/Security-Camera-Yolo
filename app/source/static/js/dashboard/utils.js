function disableButton(buttonId, duration) {
    const button = document.getElementById(buttonId);
    button.disabled = true;
    setTimeout(() => {
        button.disabled = false;
    }, duration);
}

function toggleButtons(cameraBlockId, isConnected) {
    const connectButton = document.getElementById(`connect-button-${cameraBlockId}`);
    const disconnectButton = document.getElementById(`disconnect-button-${cameraBlockId}`);
    const connectionInput = document.getElementById(`camera-url-${cameraBlockId}`);

    if (isConnected) {
        connectButton.style.display = 'none';
        disconnectButton.style.display = 'inline-block';
        connectionInput.disabled = true;
    } else {
        connectButton.style.display = 'inline-block';
        disconnectButton.style.display = 'none';
        connectionInput.disabled = false;
    }
}

function saveCameraState(cameraBlockId, cameraId, url) {
    const cameras = JSON.parse(localStorage.getItem('cameras') || '{}');
    cameras[cameraBlockId] = { cameraId, url };
    localStorage.setItem('cameras', JSON.stringify(cameras));
}

function removeCameraState(cameraBlockId) {
    const cameras = JSON.parse(localStorage.getItem('cameras') || '{}');
    delete cameras[cameraBlockId];
    localStorage.setItem('cameras', JSON.stringify(cameras));
}

function playAudio() {
    document.getElementById("myAudio").play();
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
