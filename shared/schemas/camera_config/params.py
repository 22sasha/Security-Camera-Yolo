from pydantic import BaseModel
from ..utils import PaginationParams, SortParams
from fastapi import Depends


class Create(BaseModel):
    ip: str


class Read(BaseModel):
    id: int


class Delete(BaseModel):
    id: int


class List(BaseModel):
    pagination: PaginationParams = Depends()
    sort: SortParams = Depends()
