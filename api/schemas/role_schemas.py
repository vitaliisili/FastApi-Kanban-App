from datetime import datetime
from pydantic import BaseModel, validator, Field


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
