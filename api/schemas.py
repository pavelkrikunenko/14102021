from pydantic import BaseModel
from typing import List
from fastapi import Depends


class UserBase(BaseModel):
    name: str
    role: str


class User(UserBase):
    id: int
    ctime: int

    class Config:
        orm_mode = True


class Page(BaseModel):
    total: int
    per_page: int
    page: int
    limit: int
    offset: int
    items: List[User]
