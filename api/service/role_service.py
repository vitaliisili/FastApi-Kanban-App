from typing import List, Type
from sqlalchemy.orm import Session
from api.exception.exception import EntityNotFoundException, EntityAlreadyExistsException, BadRequestException
from api.models.role_model import Role
from api.repository.role_repository import RoleRepository
from api.schemas.role_schemas import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self):
        self.role_repository = RoleRepository()

    def save(self, role_create: RoleCreate, db: Session):
        if role_create.name.strip() == "":
            raise BadRequestException("Role name must not be blank")

        check_role = self.role_repository.get_role_by_name(role_create.name, db)
        if check_role is not None:
            raise EntityAlreadyExistsException(f"Role with name {role_create.name} already exists")

        new_role: Role = Role(**role_create.dict())
        return self.role_repository.save(new_role, db)

    def get_role_by_name(self, name, db: Session) -> Role:
        role: Role = self.role_repository.get_role_by_name(name, db)
        if role is None:
            raise EntityNotFoundException(f"Role with name {name} not found")
        return role

    def get_all(self, db: Session) -> List[Type[Role]]:
        return self.role_repository.get_all(db)

    def update_role(self, role: RoleUpdate, db: Session) -> Role:
        check_role: Role = self.role_repository.get_by_id(role.id, db)

        if check_role is None:
            raise EntityNotFoundException(f"Role with id: {role.id} not found")

        if role.name != check_role.name:
            check_role_name: Role = self.role_repository.get_role_by_name(role.name, db)
            if check_role_name is not None:
                raise EntityAlreadyExistsException(f"Role with name: {role.name} already exists")

        role: Role = self.role_repository.update_role(role, db)
        return role
