from datetime import datetime
from typing import List
from pydantic import BaseModel
from api.schemas.role_schemas import Role


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    roles: List[Role]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
