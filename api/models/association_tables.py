from sqlalchemy import Table, Column, ForeignKey, Integer
from api.db.base import Base

user_role = Table(
    'user_role',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE")),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"))
)

workspace_member = Table(
    'workspace_member',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE")),
    Column('workspace_id', Integer, ForeignKey('workspace.id', ondelete="CASCADE"))
)

