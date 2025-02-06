function handleWebSocket(cameraBlockId, cameraId) {
    const ws = new WebSocket(`ws://${window.location.host}/ws/camera/${cameraId}`);
    cameraWebSockets[cameraBlockId] = ws;
    cameraIDs[cameraBlockId] = cameraId;

    ws.onopen = function (event) {
        console.log(`WebSocket connection opened for camera id: ${cameraId}`);
        toggleButtons(cameraBlockId, true);
    }

    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const frame = data.frame;
        const detections = data.detections;

        document.getElementById(`camera-stream-${cameraBlockId}`).src = `data:image/jpeg;base64,${frame}`;
        document.querySelector(`.detect0-${cameraBlockId} img`).src = "/static/images/empty.png";
        document.querySelector(`.detect1-${cameraBlockId} img`).src = "/static/images/empty.png";

        if (detections.length > 0) {
            if (enableSound === 1) { playAudio(); }
            document.querySelector(`.video-container-${cameraBlockId}`).style.boxShadow = '0 0 10px 5px red';
        } else {
            document.querySelector(`.video-container-${cameraBlockId}`).style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
        }

        detections.forEach((detection) => {
            if (detection.class_id === 0) {
                document.querySelector(`.detect0-${cameraBlockId} img`).src = "/static/images/fire.png";
            } else if (detection.class_id === 1) {
                document.querySelector(`.detect1-${cameraBlockId} img`).src = "/static/images/smoke.png";
            }
        });
    };

    ws.onerror = function (event) {
        disconnectWebsocket(cameraBlockId);
        console.error(`WebSocket error for camera id: ${cameraId}`, event);
    };

    ws.onclose = function (event) {
        disconnectCamera(cameraBlockId);
        console.log(`WebSocket connection closed for camera id: ${cameraId}`);
    };
}

async function disconnectWebsocket(cameraBlockId) {
    const disconnectButtonId = `disconnect-button-${cameraBlockId}`;
    disableButton(disconnectButtonId, 5000);

    if (cameraWebSockets[cameraBlockId] && cameraIDs[cameraBlockId]) {
        cameraWebSockets[cameraBlockId].close();
    }
}
