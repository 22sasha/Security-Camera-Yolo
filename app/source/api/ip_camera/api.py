from .api_settings import PREFIX, Paths
from fastapi import APIRouter, Depends, status
from services.ip_camera import IPCameraServiceInterface, get_ip_camera_service
from shared.schemas.ip_camera import params, response, IPCamera


router = APIRouter(prefix=PREFIX, tags=["IP Camera", ])


@router.put(
    path=Paths.Create,
    name="Save IP for IP Camera",
    responses={
        status.HTTP_201_CREATED: {"model": response.Create},
        status.HTTP_503_SERVICE_UNAVAILABLE: {},
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_lot(params: params.Create, 
                     service: IPCameraServiceInterface = Depends(get_ip_camera_service)) -> response.Create:
    return await service.create(params)


@router.get(
    path=Paths.Read,
    name="Read Lot",
    responses={
        status.HTTP_200_OK: {"model": response.Read},
        status.HTTP_404_NOT_FOUND: {},
    },
    status_code=status.HTTP_200_OK,
)
async def read_lot(params: params.Read = Depends(), 
                   service: IPCameraServiceInterface = Depends(get_ip_camera_service)) -> response.Read:
    return await service.read(params)
