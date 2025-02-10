let cameraCount = 1;
const cameraWebSockets = {};
const cameraIDs = {};

function addCameraBlock() {
    const cameraBlockId = `camera-${cameraCount}`;
    const cameraBlock = document.createElement('div');
    cameraBlock.classList.add('camera-block');
    cameraBlock.id = cameraBlockId;
    cameraBlock.innerHTML = `
    <button class="camera-disconnect-button" id="disconnect-button-${cameraBlockId}" style="display: none;" onclick="disconnectWebsocket('${cameraBlockId}')">&times;</button>
    <div class="url-block url-block-${cameraCount}">
        <input type="text" id="camera-url-${cameraBlockId}" placeholder="Введите номер конфигурации" size="28">
        <button class="camera-connect-button" id="connect-button-${cameraBlockId}" onclick="connectCamera('${cameraBlockId}')">Подключить</button>
    </div>
    <div class="video-and-detection">
        <div class="video-container video-container-${cameraBlockId}" style="width: ${cameraWidth}px; height: ${cameraHeight}px;">
            <img id="camera-stream-${cameraBlockId}" src="/static/images/empty.png" alt="Camera Stream" style="width: ${cameraWidth}px; height: ${cameraHeight}px;">
        </div>
        <div class="detect-container">
            <div class="detect detect0-${cameraBlockId}">
                <img src="/static/images/empty.png" alt="fire">
            </div>
            <div class="detect detect1-${cameraBlockId}">
                <img src="/static/images/empty.png" alt="smoke">
            </div>
        </div>
        <div class="camera-name" id="camera-name-${cameraBlockId}" style="display: none;"></div>
    </div>
  `;
    document.getElementById('camera-blocks').appendChild(cameraBlock);
    cameraCount++;
}

function initializeCameraBlocks() {
    for (let i = 0; i < 12; i++) {
        addCameraBlock();
    }
}

function restoreCameras() {
    const cameras = JSON.parse(localStorage.getItem('cameras') || '{}');
    Object.keys(cameras).forEach(cameraBlockId => {
        const { cameraId, url } = cameras[cameraBlockId];
        while (!document.getElementById(cameraBlockId)) {
            addCameraBlock();
        }
        document.getElementById(`camera-url-${cameraBlockId}`).value = url;
        connectCamera(cameraBlockId, cameraId);
    });
}

window.onload = function () {
    initializeCameraBlocks();
    restoreCameras();
};
