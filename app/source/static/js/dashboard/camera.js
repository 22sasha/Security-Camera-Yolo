async function connectCamera(cameraBlockId, cameraId = null) {
    const connectButtonId = `connect-button-${cameraBlockId}`;
    disableButton(connectButtonId, 5000);

    const newCameraId = await connectToCamera(cameraBlockId, cameraId);
    if (newCameraId) {
        const url = document.getElementById(`camera-url-${cameraBlockId}`).value;
        saveCameraState(cameraBlockId, newCameraId, url);
        handleWebSocket(cameraBlockId, newCameraId);
    }
}

async function connectToCamera(cameraBlockId, cameraId = null) {
    const config = await getCameraConfig(cameraBlockId);
    const url = config.url;
    const name = config.name;
    console.log(name);
    const response = await fetch('/connect_camera', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url, cameraId: cameraId })
    });
    if (!response.ok) {
        const errorData = await response.json();
        console.error('Error connecting camera:', errorData);
        toggleButtons(cameraBlockId, false);
        return null;
    }
    const data = await response.json();
    document.getElementById(`camera-name-${cameraBlockId}`).innerText = name;
    return data.camera_id;
}

async function getCameraConfig(cameraBlockId) {
    const cameraConfigID = document.getElementById(`camera-url-${cameraBlockId}`).value;
    const response = await fetch(`/camera_config/${cameraConfigID}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    if (!response.ok) {
        console.error('Error getting camera config:', await response.json());
        return;
    }
    const config = await response.json();
    return config.camera_config;
}

async function disconnectCamera(cameraBlockId) {
    if (cameraWebSockets[cameraBlockId] && cameraIDs[cameraBlockId]) {
        let camera_id = cameraIDs[cameraBlockId];

        if (cameraWebSockets[cameraBlockId].readyState === WebSocket.OPEN) {
            cameraWebSockets[cameraBlockId].close();
        }
        delete cameraWebSockets[cameraBlockId];
        delete cameraIDs[cameraBlockId];

        document.getElementById(`camera-stream-${cameraBlockId}`).src = "/static/images/empty.png";
        document.querySelector(`.detect0-${cameraBlockId} img`).src = "/static/images/empty.png";
        document.querySelector(`.detect1-${cameraBlockId} img`).src = "/static/images/empty.png";
        document.querySelector(`.video-container-${cameraBlockId}`).style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        document.getElementById(`camera-name-${cameraBlockId}`).style.display = 'none';

        const response = await fetch('/disconnect_camera', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ camera_id: camera_id })
        });

        if (!response.ok) {
            console.error('Error disconnecting camera:', await response.json());
        }
        toggleButtons(cameraBlockId, false);
        removeCameraState(cameraBlockId);
    }
}
