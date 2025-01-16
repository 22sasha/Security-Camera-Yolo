from shared.schemas.camera_config import response, params, CameraConfig
from abc import ABC, abstractmethod


class CameraConfigServiceInterface(ABC):
    @abstractmethod
    async def create(self, params: params.Create) -> response.Create:
        ...

    @abstractmethod
    async def read(self, params: params.Read) -> response.Read:
        ...

    # @abstractmethod
    # async def update(self, params: params.Update) -> response.Update:
    #     ...

    @abstractmethod
    async def delete(self, params: params.Delete):
        ...

    @abstractmethod
    async def list(self, params: params.List) -> response.List:
        ...
