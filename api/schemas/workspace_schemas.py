from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from api.schemas.user_schemas import UserUpdate, UserOut


class WorkspaceBase(BaseModel):
    title: str = Field(..., description="Workspace name")

    @validator("title")
    def validate_title(cls, title):  # noqa
        if not title.strip():
            raise ValueError("Title cannot be empty or blank")
        return title


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(WorkspaceBase):
    id: int
    members: List[UserUpdate]
    owner_id: int = Field(None, description="Workspace owner")
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class WorkspaceOut(WorkspaceBase):
    id: int
    members: List[UserOut]
    owner_id: int = Field(None, description="Workspace owner")
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
