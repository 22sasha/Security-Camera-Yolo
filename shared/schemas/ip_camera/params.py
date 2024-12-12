from pydantic import BaseModel


class Create(BaseModel):
    ip: str


class Read(BaseModel):
    id: int
