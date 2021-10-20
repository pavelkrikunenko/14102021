from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    role: str


class User(UserBase):
    id: int
    ctime: int

    class Config:
        orm_mode = True
