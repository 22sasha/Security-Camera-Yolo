from shared.schemas.ip_camera import response, params, IPCamera
from abc import ABC, abstractmethod


class IPCameraServiceInterface(ABC):
    @abstractmethod
    async def create(self, params: params.Create) -> response.Create:
        ...

    @abstractmethod
    async def read(self, params: params.Read) -> response.Read:
        ...
