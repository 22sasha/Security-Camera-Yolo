from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import os

from .camera_config import router as camera_config_router


app = FastAPI(title="Security Camera API")

app.include_router(camera_config_router)



templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_page1(request: Request):
    return templates.TemplateResponse("page1.html", {"request": request})

@app.get("/page2", response_class=HTMLResponse)
async def read_page2(request: Request):
    return templates.TemplateResponse("page2.html", {"request": request})

@app.get("/page3", response_class=HTMLResponse)
async def read_page3(request: Request):
    return templates.TemplateResponse("page3.html", {"request": request})
