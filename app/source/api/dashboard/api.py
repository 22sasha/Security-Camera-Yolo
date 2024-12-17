from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.templating import Jinja2Templates
from common.camera import Camera
from typing import Dict
from uuid import uuid4
import os


router = APIRouter(
    prefix="",
    tags=["Dashboard"]
)
templates = Jinja2Templates(directory="templates")


camera_cache: Dict[str, Camera] = {}
detections_cache: Dict[str, list] = {}


@router.post("/add_camera")
async def add_camera(url: str):
    camera_id = str(uuid4())
    camera = Camera(url=url)
    if not camera.cap.isOpened():
        raise HTTPException(status_code=400, detail="Camera could not be opened")
    
    camera_cache[camera_id] = camera
    detections_cache[camera_id] = []
    return {"camera_id": camera_id}


def get_camera(camera_id: str) -> Camera:
    if camera_id not in camera_cache:
        raise HTTPException(status_code=404, detail="Camera not found")
    return camera_cache[camera_id]


def gen_video(camera: Camera, camera_id: str):
    try:
        while True:
            frame, detections = camera.get_frame() # type: ignore
            detections_cache[camera_id] = detections
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as E:
        clean_camera_cache(camera_id)
        return


def clean_camera_cache(camera_id: str):
    if camera_id in camera_cache:
        del camera_cache[camera_id]
    if camera_id in detections_cache:
        del detections_cache[camera_id]


@router.get('/video_feed')
async def video_feed(camera_id: str):
    try:
        camera = get_camera(camera_id)
        return StreamingResponse(gen_video(camera, camera_id),
                                media_type='multipart/x-mixed-replace; boundary=frame')
    except HTTPException as E:
        clean_camera_cache(camera_id)
        raise E


@router.get('/detections')
async def detections(camera_id: str):
    try:
        if camera_id in detections_cache:
            detection = detections_cache[camera_id]
            return detection
        else:
            raise HTTPException(400, "Camera URL not working")
    except HTTPException as E:
        clean_camera_cache(camera_id)
        raise E


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