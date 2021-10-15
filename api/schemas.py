from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    name: str
    role: str


class User(UserBase):
    id: int
    ctime: int

    class Config:
        orm_mode = True


class PageBase(BaseModel):
    limit: int
    offset: int


class Page(PageBase):
    total: int
    per_page: int
    page: int
    items: List[User] = None


class DeleteUser(BaseModel):
    id: int
