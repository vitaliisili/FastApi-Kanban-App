from typing import List, Type
from sqlalchemy.orm import Session
from api.models.user_model import User


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
