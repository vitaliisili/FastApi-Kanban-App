from typing import List, Type
from sqlalchemy.orm import Session
from api.models.role_model import Role
from api.models.user_model import User
from api.schemas.user_schemas import UserUpdate


class UserRepository:

    def save(self, model: User, db: Session) -> User:
        db.add(model)
        db.commit()
        db.refresh(model)
        return model

    def get_user_by_email(self, email: str, db: Session) -> User:
        user: User = db.query(User).filter(User.email == email).first()
        return user

    def get_all(self, db: Session) -> List[Type[User]]:
        users: List[Type[User]] = db.query(User).all()
        return users

    def get_user_by_id(self, id, db):
        user: User = db.query(User).filter(User.id == id).first()
        return user

    def update_user(self, user_update: UserUpdate, db: Session):
        user = db.query(User).filter(User.id == user_update.id).first()

        for field, value in user_update.dict(exclude={"roles"}).items():
            if value is not None:
                setattr(user, field, value)

        roles = db.query(Role).filter(Role.id.in_([role.id for role in user_update.roles])).all()
        user.roles = roles

        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, id: int, db: Session):
        user_query = db.query(User).filter(User.id == id)
        user_query.delete(synchronize_session=False)
        db.commit()
