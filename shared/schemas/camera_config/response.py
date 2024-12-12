from pydantic import BaseModel
from .common import CameraConfig


class Create(BaseModel):
    camera_config: CameraConfig


class Read(BaseModel):
    camera_config: CameraConfig


class List(BaseModel):
    items: list[CameraConfig]
    total: int
