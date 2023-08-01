from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.exception.exception import BadRequestException, EntityNotFoundException, EntityAlreadyExistsException
from api.models.user_model import User
from api.schemas.user_schemas import UserCreate, UserOut, UserUpdate
from api.security.jwt_config import get_principal
from api.service.user_service import UserService

router = APIRouter(tags=['Users'])
user_service = UserService()


@router.get('/api/users', status_code=status.HTTP_200_OK, response_model=List[UserOut])
def get_all(db: Session = Depends(get_db), principal: User = Depends(get_principal)):
    return user_service.get_all(db)


@router.get('/api/users/{id}', status_code=status.HTTP_200_OK, response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db), principal: User = Depends(get_principal)):
    try:
        return user_service.get_user_by_id(id, db)
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.put("/api/users", status_code=status.HTTP_200_OK, response_model=UserOut)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db), principal: User = Depends(get_principal)):
    try:
        return user_service.update_user(user_update, db)
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except EntityAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))


@router.delete("/api/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), principal: User = Depends(get_principal)):
    try:
        user_service.delete_user(id, db)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except EntityNotFoundException as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
