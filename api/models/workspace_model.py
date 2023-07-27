from sqlalchemy import Column, String, Integer, func, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from api.db.base_class import Base


class Workspace(Base):
    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    title = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="workspaces")
    members = relationship(
        'User', secondary='workspace_member', back_populates='workspaces_member', passive_deletes=True)
