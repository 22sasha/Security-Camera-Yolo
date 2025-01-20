from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
# from common.camera import Camera
from common.cam_debug import Camera
from typing import Dict
from uuid import uuid4
import os
import asyncio
from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import base64


router = APIRouter(
    prefix="",
    tags=["Dashboard"]
)
templates = Jinja2Templates(directory="templates")
FRAME_DELAY = float(os.getenv("FRAME_DELAY", 0.1))
camera_cache: Dict[str, Camera] = {}


class CameraConnectionRequest(BaseModel):
    url: str
    cameraId: str | None = None


class CameraDisconnectionRequest(BaseModel):
    camera_id: str

@router.post("/connect_camera")
async def connect_camera(request: CameraConnectionRequest):
    print(request)
    if request.cameraId not in camera_cache:
        camera_id = str(uuid4())
        camera = Camera(request.url, camera_id)
        if not camera.cap.isOpened():
            raise HTTPException(status_code=503, detail="Camera could not be opened")    
        await asyncio.sleep(5)
        camera_cache[camera_id] = camera
        print(camera_cache)
        return {"camera_id": camera_id}

    print(camera_cache)
    return {"camera_id": request.cameraId}

@router.websocket("/ws/camera/{camera_id}")
async def websocket_endpoint(websocket: WebSocket, camera_id: str):
    await websocket.accept()
    try:
        while camera_id in camera_cache and camera_cache[camera_id].is_active:
            frame, detections = camera_cache[camera_id].get_frame()
            frame_base64 = base64.b64encode(frame).decode('utf-8')
            await websocket.send_json({"frame": frame_base64, "detections": detections})
            await asyncio.sleep(FRAME_DELAY)
        await websocket.close()
    except WebSocketDisconnect as Error:
        print(f"Client {camera_id} disconnected")


@router.post("/disconnect_camera")
async def disconnect_camera(request: CameraDisconnectionRequest):
    if request.camera_id in camera_cache:
        camera_cache[request.camera_id].stop()
        del camera_cache[request.camera_id]
        return {"message": f"Camera {request.camera_id} disconnected and removed from cache"}
    raise HTTPException(status_code=404, detail="Camera not found")


@router.get("/dashboard", response_class=HTMLResponse)
async def index(request: Request):
    width = int(os.getenv("CAMERA_WIDTH", 640))
    height = int(os.getenv("CAMERA_HEIGHT", 480))
    
    context = {
        "request": request,
        "width": width,
        "height": height
    }
    return templates.TemplateResponse('dashboard.html', context)
