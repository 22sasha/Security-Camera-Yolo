from .api_settings import PREFIX, Paths
from fastapi import APIRouter, Depends, status
from services.camera_config import CameraConfigServiceInterface, get_camera_config_service
from shared.schemas.camera_config import params, response, CameraConfig


router = APIRouter(prefix=PREFIX, tags=["IP Camera", ])


@router.put(
    path=Paths.Create,
    name="Save Camera Config",
    responses={
        status.HTTP_201_CREATED: {"model": response.Create},
        status.HTTP_503_SERVICE_UNAVAILABLE: {},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_camera_config(params: params.Create, 
                     service: CameraConfigServiceInterface = Depends(get_camera_config_service)) -> response.Create:
    return await service.create(params)


@router.get(
    path=Paths.Read,
    name="Read Camera Config",
    responses={
        status.HTTP_200_OK: {"model": response.Read},
        status.HTTP_404_NOT_FOUND: {},
    },
    status_code=status.HTTP_200_OK,
)
async def read_camera_config(params: params.Read = Depends(), 
                   service: CameraConfigServiceInterface = Depends(get_camera_config_service)) -> response.Read:
    return await service.read(params)


@router.delete(
    path=Paths.Delete,
    name="Delete Camera Config",
    responses={
        status.HTTP_200_OK: {},
        status.HTTP_404_NOT_FOUND: {},
    },
    status_code=status.HTTP_200_OK,
)
async def delete_camera_config(params: params.Delete = Depends(), 
                   service: CameraConfigServiceInterface = Depends(get_camera_config_service)):
    return await service.delete(params)


@router.get(
    path=Paths.List,
    name="List Camera Config",
    responses={
        status.HTTP_200_OK: {"model": response.List},
        status.HTTP_404_NOT_FOUND: {},
    },
    status_code=status.HTTP_200_OK,
)
async def read_camera_config(params: params.List = Depends(), 
                   service: CameraConfigServiceInterface = Depends(get_camera_config_service)) -> response.List:
    return await service.list(params)