from typing import List, Type

from sqlalchemy.orm import Session
from api.models.role_model import Role


class RoleRepository:

    def save(self, role_model: Role, db: Session) -> Role:
        db.add(role_model)
        db.commit()
        db.refresh(role_model)
        return role_model

    def get_role_by_name(self, name: str, db: Session) -> Role:
        role = db.query(Role).filter(Role.name == name).first()
        return role

    def get_all(self, db: Session) -> List[Type[Role]]:
        roles = db.query(Role).all()
        return roles