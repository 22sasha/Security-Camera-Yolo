from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from services.camera_config import CameraConfigServiceInterface, get_camera_config_service
from shared.schemas.camera_config import params as CameraConfigParams
from shared.schemas.utils import PaginationParams, SortParams, SortOrder

router = APIRouter(
    prefix="",
    tags=["Configuration"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/configuration", response_class=HTMLResponse)
async def read_configuration(request: Request,
                             service: CameraConfigServiceInterface = Depends(get_camera_config_service)):
    pagination_params = PaginationParams(page=1, perPage=20)
    print(pagination_params)
    sort_params = SortParams(sortBy="id", sortOrder=SortOrder.Desc)
    params = CameraConfigParams.List(pagination=pagination_params, sort=sort_params)
    configs = await service.list(params=params)
    response = templates.TemplateResponse(
        "configuration.html", 
        {"request": request, "configs": configs.items}
    )
    return response
