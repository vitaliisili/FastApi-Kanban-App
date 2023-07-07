from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
