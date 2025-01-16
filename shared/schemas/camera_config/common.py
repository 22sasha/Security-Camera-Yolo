from pydantic import BaseModel


class CameraConfig(BaseModel):
    id: int
    url: str
