from pydantic import BaseModel


class CameraConfig(BaseModel):
    id: int
    ip: str
