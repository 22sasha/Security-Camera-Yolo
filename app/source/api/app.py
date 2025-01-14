from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.requests import Request
import os

from .camera_config import router as camera_config_router
from .dashboard import router as dashboard_router
from .configuration import router as configuration_router

app = FastAPI(title="Security Camera API")

app.include_router(camera_config_router)
app.include_router(dashboard_router)
app.include_router(configuration_router)


templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# @app.get("/dashboard", response_class=HTMLResponse)
# async def read_dashboard(request: Request):
#     return templates.TemplateResponse("dashboard.html", {"request": request})

# @app.get("/configuration", response_class=HTMLResponse)
# async def read_configuration(request: Request):
#     return templates.TemplateResponse("configuration.html", {"request": request})
