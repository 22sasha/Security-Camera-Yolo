from pydantic import BaseModel


class IPCamera(BaseModel):
    id: int
    ip: str
