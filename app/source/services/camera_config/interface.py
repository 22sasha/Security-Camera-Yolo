from shared.schemas.camera_config import response, params, CameraConfig
from abc import ABC, abstractmethod


class CameraConfigServiceInterface(ABC):
    @abstractmethod
    async def create(self, params: params.Create) -> response.Create:
        ...

    @abstractmethod
    async def read(self, params: params.Read) -> response.Read:
        ...
