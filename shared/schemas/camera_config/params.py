from pydantic import BaseModel
from ..utils import PaginationParams, SortParams
from fastapi import Depends


class Create(BaseModel):
    name: str
    url: str


class Read(BaseModel):
    id: int


class Delete(BaseModel):
    id: int


class List(BaseModel):
    pagination: PaginationParams = Depends()
    sort: SortParams = Depends()
