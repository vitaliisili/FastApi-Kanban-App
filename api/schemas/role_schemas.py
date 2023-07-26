from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator, Field


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
