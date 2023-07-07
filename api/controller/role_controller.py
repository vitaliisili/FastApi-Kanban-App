from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.models import role_model
from api.schemas import role_schemas

router = APIRouter(tags=['Role'])


@router.get('/api/roles', response_model=List[role_schemas.Role])
def get_users(db: Session = Depends(get_db)):
    roles = db.query(role_model.Role).all()
    return roles
