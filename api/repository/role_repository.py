from sqlalchemy.orm import Session
from api.models.role_model import Role
from api.repository.read_write_repository import ReadWriteRepository


class RoleRepository(ReadWriteRepository):
    def get_role_by_name(self, name: str, db: Session) -> Role:
        role = db.query(Role).filter_by(name=name).first()
        return role

