from .pagination_params import PaginationParams
from typing import Generic, TypeVar
from .sort_params import SortParams
from pydantic import BaseModel
from fastapi import Depends


class ListParams(BaseModel):
    pagination: PaginationParams = Depends()
    sort: SortParams = Depends()


T = TypeVar("T")
class ListResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
