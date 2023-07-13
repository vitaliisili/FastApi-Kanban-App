from datetime import datetime
from pydantic import BaseModel, validator, Field


class RoleBase(BaseModel):
    name: str

    # Alternative validation TODO: choose where validate in schemas or in service layer
    # @validator('name')
    # def name_validation(cls, value: str):
    #     if value.strip() == "":
    #         raise ValueError("Name must not be empty")
    #     return value


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
