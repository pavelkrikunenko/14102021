from __future__ import annotations

from fastapi import Query
from pydantic import BaseModel

from typing import TypeVar, Generic

from fastapi_pagination.default import Page as BasePage, Params as BaseParams

T = TypeVar("T")


class UserBase(BaseModel):
    name: str
    role: str


class User(UserBase):
    id: int
    ctime: int

    class Config:
        orm_mode = True


class Params(BaseParams):
    size: int = Query(5, ge=1, le=1_000, description="Page size")


class Page(BasePage[T], Generic[T]):
    __params_type__ = Params
