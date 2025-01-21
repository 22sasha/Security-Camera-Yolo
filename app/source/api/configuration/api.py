from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from services.camera_config import CameraConfigServiceInterface, get_camera_config_service
from shared.schemas.camera_config import params as CameraConfigParams
from shared.schemas.utils import PaginationParams, SortParams, SortOrder
from math import ceil


router = APIRouter(
    prefix="",
    tags=["Configuration"]
)
templates = Jinja2Templates(directory="templates")


@router.get("/camera_config/{camera_id}")
async def get_camera_config(camera_id: int, 
                            service: CameraConfigServiceInterface = Depends(get_camera_config_service)):
    params = CameraConfigParams.Read(id=camera_id)  
    config = await service.read(params=params)
    return config


@router.get("/configuration", response_class=HTMLResponse)
async def read_configuration(request: Request,
                             page: int = 1,
                             per_page: int = 20,
                             service: CameraConfigServiceInterface = Depends(get_camera_config_service)):
    pagination_params = PaginationParams(page=page, perPage=per_page)
    sort_params = SortParams(sortBy="id", sortOrder=SortOrder.Desc)
    params = CameraConfigParams.List(pagination=pagination_params, sort=sort_params)
    configs = await service.list(params=params)

    total_pages = max(1, ceil(configs.total / per_page))

    response = templates.TemplateResponse("configuration.html", 
        {
            "request": request, 
            "configs": configs.items,
            "total_pages": total_pages,
            "current_page": page
        }
    )
    return response
