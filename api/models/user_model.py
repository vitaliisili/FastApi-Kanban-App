from sqlalchemy import Column, String, Integer, func, DateTime
from sqlalchemy.orm import relationship
from api.db.base_class import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    roles = relationship('Role', secondary='user_role', back_populates='users', cascade="all, delete")
    workspaces = relationship("Workspace", back_populates='owner')
    workspaces_member = relationship(
        'Workspace', secondary='workspace_member', back_populates='members', cascade="all, delete")
