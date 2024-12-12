from fastapi import Depends, HTTPException, status
from database.repos import IPCameraRepository
from .interface import IPCameraServiceInterface
from shared.schemas.ip_camera import response, params, IPCamera


class LocalIPCameraService(IPCameraServiceInterface):

    def __init__(self,
                 repo: IPCameraRepository = Depends()):
        self.repo = repo

    async def create(self, params: params.Create) -> response.Create:
        obj = await self.repo.new(**params.model_dump())
        if obj is None:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Database error")  # noqa
        return response.Create(ip_camera=IPCamera.model_validate(obj, from_attributes=True))

    async def read(self, params: params.Read) -> response.Read:
        lot = await self.__get(id=params.id)
        return response.Read(ip_camera=IPCamera.model_validate(lot, from_attributes=True))

    async def __get(self, id: int) -> IPCamera:
        lot = await self.repo.get(id=id)
        if lot is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "IP not found")
        return lot
