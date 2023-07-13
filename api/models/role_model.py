from sqlalchemy import Column, String, text, Integer, func, DateTime
from sqlalchemy.orm import relationship
from api.db.base_class import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    users = relationship('User', secondary='user_role', back_populates='roles')
