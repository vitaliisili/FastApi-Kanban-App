from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from api.schemas.user_schemas import UserUpdate, UserOut


class WorkspaceBase(BaseModel):
    title: str
    owner_id: int


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    id: int
    members: List[UserUpdate]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class WorkspaceOut(WorkspaceBase):
    id: int
    members: List[UserOut]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
