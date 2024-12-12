from fastapi import Depends, HTTPException, status
from database.repos import CameraConfigRepository
from .interface import CameraConfigServiceInterface
from shared.schemas.camera_config import response, params, CameraConfig


class LocalCameraConfigService(CameraConfigServiceInterface):

    def __init__(self,
                 repo: CameraConfigRepository = Depends()):
        self.repo = repo

    async def create(self, params: params.Create) -> response.Create:
        obj = await self.repo.new(**params.model_dump())
        if obj is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database error")  # noqa
        return response.Create(camera_config=CameraConfig.model_validate(obj, from_attributes=True))

    async def read(self, params: params.Read) -> response.Read:
        obj = await self.__get(id=params.id)
        return response.Read(camera_config=CameraConfig.model_validate(obj, from_attributes=True))

    async def __get(self, id: int) -> CameraConfig:
        obj = await self.repo.get(id=id)
        if obj is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Camera config not found")
        return obj
