import math
from typing import Annotated, Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import asc, desc, Column
from sqlalchemy.orm import Query as SAQuery

T = TypeVar("T")


class PaginationParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, description="Page number (1-indexed)"),
        size: int = Query(20, ge=1, le=100, description="Items per page (max 100)"),
    ):
        self.page = page
        self.size = size
        self.offset = (page - 1) * size


class SortingParams:
    def __init__(
        self,
        sort_by: str = Query("id", description="Field to sort by"),
        sort_order: str = Query("desc", description="Sort order: asc or desc"),
    ):
        self.sort_by = sort_by
        self.sort_order = sort_order

    def apply(self, query: SAQuery, model, allowed_fields: list[str] | None = None):
        field = self.sort_by
        if allowed_fields and field not in allowed_fields:
            field = "id"
        column = getattr(model, field, None)
        if column is None:
            column = model.id
        direction = desc if self.sort_order == "desc" else asc
        return query.order_by(direction(column))


def paginate(query: SAQuery, pagination: PaginationParams) -> dict:
    total = query.count()
    pages = math.ceil(total / pagination.size) if total > 0 else 1
    items = query.offset(pagination.offset).limit(pagination.size).all()
    return {
        "items": items,
        "total": total,
        "page": pagination.page,
        "size": pagination.size,
        "pages": pages,
    }


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T] = Field(..., description="List of records")
    total: int = Field(..., description="Total number of matching records")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Page size")
    pages: int = Field(..., description="Total number of pages")
