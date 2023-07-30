import re
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator, EmailStr
from api.schemas.role_schemas import RoleOut, RoleUpdate


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

    # type: ignore
    @validator("first_name", "last_name")
    def validation_empty_date(cls, value):  # noqa
        if not value.strip():
            raise ValueError("Empty or blank string is not allowed")
        return value


class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, password):  # noqa
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least 1 digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("Password must contain at least 1 special character")
        return password


class UserUpdate(UserBase):
    id: int
    roles: List[RoleUpdate]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class UserOut(UserBase):
    id: int
    roles: List[RoleOut]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
