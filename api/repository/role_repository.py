from typing import List, Type
from sqlalchemy.orm import Session, Query
from api.models.role_model import Role
from api.schemas.role_schemas import RoleUpdate


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

    def get_by_id(self, id: int, db: Session) -> Role:
        role = db.query(Role).filter(Role.id == id).first()
        return role

    def update_role(self, role: RoleUpdate, db: Session):
        role_query = db.query(Role).filter(Role.id == role.id)
        role_query.update(role.dict(), synchronize_session=False)
        db.commit()
        return role_query.first()

    def delete_role(self, id: int, db: Session) -> None:
        role_query: Query = db.query(Role).filter(Role.id == id)
        role_query.delete(synchronize_session=False)
        db.commit()
