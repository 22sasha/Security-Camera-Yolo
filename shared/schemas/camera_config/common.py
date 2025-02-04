from pydantic import BaseModel


class CameraConfig(BaseModel):
    id: int
    name: str
    url: str
