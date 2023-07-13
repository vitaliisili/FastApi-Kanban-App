from typing import List, Type
from sqlalchemy.orm import Session
from api.exception.exception import BadRequestException, EntityAlreadyExistsException, EntityNotFoundException
from api.models.user_model import User
from api.repository.user_repository import UserRepository
from api.schemas.user_schemas import UserCreate
from api.security.password import HashPassword
from api.service.role_service import RoleService


class UserService:
    def __init__(self):
        self.password = HashPassword()
        self.user_repository = UserRepository()
        self.role_service = RoleService()

    def save(self, user_create: UserCreate, db: Session) -> User:
        if not self.password.validate_password(user_create.password):
            raise BadRequestException("Password is not valid")

        check_user = self.user_repository.get_user_by_email(user_create.email, db)
        if check_user is not None:
            raise EntityAlreadyExistsException(f"User with email: {user_create.email} already exists")

        user_create.password = self.password.get_hashed_password(user_create.password)
        new_user = User(**user_create.dict())
        new_user.roles = []
        new_user.roles.append(self.role_service.get_role_by_name('USER', db))
        return self.user_repository.save(new_user, db)

    def get_user_by_email(self, email: str, db: Session) -> User:
        user = self.user_repository.get_user_by_email(email, db)
        if user is None:
            raise EntityNotFoundException(f"User with email: {email} not found")
        return user

    def get_all(self, db: Session) -> List[Type[User]]:
        users: List[Type[User]] = self.user_repository.get_all(db)
        return users
