from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    id: int


class RoleOut(RoleBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
