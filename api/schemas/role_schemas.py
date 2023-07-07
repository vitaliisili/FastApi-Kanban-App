from datetime import datetime
from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str


class Role(RoleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
