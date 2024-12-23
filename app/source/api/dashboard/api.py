from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.templating import Jinja2Templates
from common.camera import Camera
from typing import Dict
from uuid import uuid4
import os
import asyncio


router = APIRouter(
    prefix="",
    tags=["Dashboard"]
)
templates = Jinja2Templates(directory="templates")


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
