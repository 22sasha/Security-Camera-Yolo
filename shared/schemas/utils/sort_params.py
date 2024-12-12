from pydantic import BaseModel, Field
from enum import Enum


class SortOrder(str, Enum):
    Asc = "asc"
    Desc = "desc"


class SortParams(BaseModel):
    field: str | None = Field(None, validation_alias="sortBy")
    order: SortOrder = Field(SortOrder.Asc, validation_alias="sortOrder")

    def __bool__(self):
        return self.field is not None
