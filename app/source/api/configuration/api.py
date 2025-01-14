from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="",
    tags=["Configuration"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/configuration", response_class=HTMLResponse)
async def read_configuration(request: Request):
    return templates.TemplateResponse("configuration.html", {"request": request})
