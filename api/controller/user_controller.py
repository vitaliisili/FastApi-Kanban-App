from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.exception.exception import BadRequestException, EntityNotFoundException, EntityAlreadyExistsException
from api.schemas.user_schemas import UserCreate, User
from api.service.user_service import UserService

router = APIRouter(tags=['Users'])
user_service = UserService()


@router.post('/api/users', status_code=status.HTTP_201_CREATED, response_model=User)
def save_user(user_create: UserCreate, db: Session = Depends(get_db)):
    try:
        return user_service.save(user_create, db)

    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))

    except BadRequestException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    except EntityAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.get('/api/users', status_code=status.HTTP_200_OK, response_model=List[User])
def get_all(db: Session = Depends(get_db)):
    return user_service.get_all(db)
