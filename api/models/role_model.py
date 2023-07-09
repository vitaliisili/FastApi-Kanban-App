from sqlalchemy import Column, String, text, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from api.db.base_class import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    users = relationship('Users', secondary='user_role', back_populates='roles')
