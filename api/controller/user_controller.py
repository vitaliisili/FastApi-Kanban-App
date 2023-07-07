from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.models import user_model
from api.schemas import user_schemas

router = APIRouter(tags=['User'])


@router.get('/api/users', response_model=List[user_schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(user_model.User).all()
    return users
