from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from api.schemas.role_schemas import RoleOut, RoleUpdate


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: int
    roles: List[RoleUpdate]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserOut(UserBase):
    id: int
    roles: List[RoleOut]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
