from pydantic import BaseModel
from .common import IPCamera


class Create(BaseModel):
    ip_camera: IPCamera


class Read(BaseModel):
    ip_camera: IPCamera
