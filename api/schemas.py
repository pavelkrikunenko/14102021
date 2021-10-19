from __future__ import annotations

from pydantic import BaseModel

from typing import TypeVar, Generic
from fastapi_pagination.bases import Sequence, AbstractParams, AbstractPage

from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class Raw:
    limit: int
    offset: int
    per_page: int


class UserBase(BaseModel):
    name: str
    role: str


class User(UserBase):
    id: int
    ctime: int

    class Config:
        orm_mode = True


class Params(BaseModel, AbstractParams):
    limit: int = 5
    offset: int = 0

    def to_raw_params(self) -> Raw:
        return Raw(
            limit=self.limit,
            offset=self.offset,
            per_page=int(self.offset / self.limit),

        )


class Page(AbstractPage[T], Generic[T]):
    total: int
    per_page: int

    limit: int
    offset: int
    items: Sequence[T]

    __params_type__ = Params

    @classmethod
    def create(cls,
               items: Sequence[T],
               total: int,
               params: Params
               ) -> Page[T]:
        return cls(items=items,
                   total=total,
                   limit=params.limit,
                   offset=params.offset,
                   per_page=int(params.offset / params.limit),

                   )
