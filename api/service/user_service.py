from typing import List, Type
from sqlalchemy.orm import Session
from api.exception.exception import BadRequestException, EntityAlreadyExistsException, EntityNotFoundException
from api.models.user_model import User
from api.repository.user_repository import UserRepository
from api.schemas.user_schemas import UserCreate, UserUpdate
from api.security.password import HashPassword
from api.service.role_service import RoleService


class UserService:
    def __init__(self):
        self.password = HashPassword()
        self.user_repository = UserRepository(User)
        self.role_service = RoleService()

    def save(self, user_create: UserCreate, db: Session) -> User:

        if not self.password.validate_password(user_create.password):
            raise BadRequestException("Password is not valid")

        check_user = self.user_repository.get_user_by_email(user_create.email, db)
        if check_user is not None:
            raise EntityAlreadyExistsException(f"User with email: {user_create.email} already exists")

        user_create.password = self.password.get_hashed_password(user_create.password)
        new_user: User = User(**user_create.dict())
        new_user.roles = []
        new_user.roles.append(self.role_service.get_role_by_name('USER', db))
        return self.user_repository.save(new_user, db)

    def get_user_by_email(self, email: str, db: Session) -> User:
        user: User = self.user_repository.get_user_by_email(email, db)
        if user is None:
            raise EntityNotFoundException(f"User with email: {email} not found")
        return user

    def get_all(self, db: Session) -> List[Type[User]]:
        users: List[Type[User]] = self.user_repository.get_all(db)
        return users

    def get_user_by_id(self, id: int, db: Session) -> Type[User]:
        user: Type[User] = self.user_repository.get_by_id(id, db)
        if user is None:
            raise EntityNotFoundException(f"User with id: {id} not found")
        return user

    def update_user(self, user_update: UserUpdate, db: Session) -> User:
        check_user_id = self.user_repository.get_by_id(user_update.id, db)

        if check_user_id is None:
            raise EntityNotFoundException(f"User with id: {user_update.id} not found")

        if user_update.email != check_user_id.email:
            check_user_email: User = self.user_repository.get_user_by_email(user_update.email, db)
            if check_user_email is not None:
                raise EntityAlreadyExistsException(f"User with email: {user_update.email} already exists")

        user: User = self.user_repository.update(user_update, db)
        return user

    def delete_user(self, id: int, db: Session) -> None:
        check_user_id: Type[User] = self.user_repository.get_by_id(id, db)
        if check_user_id is None:
            raise EntityNotFoundException(f"User with id: {id} not found")
        self.user_repository.delete(id, db)
