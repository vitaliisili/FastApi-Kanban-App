from typing import Type, List

from sqlalchemy.orm import Session
from api.models.role_model import Role
from api.models.user_model import User
from api.schemas.user_schemas import UserUpdate
from api.repository.read_write_repository import ReadWriteRepository


class UserRepository(ReadWriteRepository):
    def get_user_by_email(self, email: str, db: Session) -> Type[User]:  # noqa
        """ Retrieves a user from the database based on their email.
         Parameters:
            email (str): The email of the user to retrieve.
            db (Session): The database session object.
         Returns:
            User: The user object retrieved from the database, if found.
        """
        user: Type[User] = db.query(User).filter_by(email=email).first()
        return user

    def update(self, user_update: UserUpdate, db: Session) -> Type[User]:
        """ Updates a user in the database with the provided user_update data.
        Parameters:
            user_update (UserUpdate): The user update object containing the new user data.
            db (Session): The database session object.
        Returns:
            User: The updated user object.
        """
        user: Type[User] = db.query(User).filter_by(id=user_update.id).first()

        for field, value in user_update.dict(exclude={"roles"}).items():
            if value is not None:
                setattr(user, field, value)

        roles: List[Type[Role]] = db.query(Role).filter(Role.id.in_([role.id for role in user_update.roles])).all()
        user.roles = roles

        db.commit()
        db.refresh(user)
        return user
