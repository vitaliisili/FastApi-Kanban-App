from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.exception.exception import EntityAlreadyExistsException, BadRequestException
from api.models.user_model import User
from api.schemas.user_schemas import UserCreate
from api.security.token_schemas import Token
from api.security.jwt_config import authenticate_user, create_access_token
from api.service.user_service import UserService

router = APIRouter(tags=["Authentication"])
user_service = UserService()


@router.post("/api/auth/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user: User = authenticate_user(form_data.username, form_data.password, db)
    token: Token = create_access_token(data={"email": user.email})
    return token


@router.post('/api/auth/register', status_code=status.HTTP_201_CREATED, response_model=Token)
def save_user(user_create: UserCreate, db: Annotated[Session, Depends(get_db)]):
    try:
        user: User = user_service.save(user_create, db)
        token: Token = create_access_token(data={"email": user.email})
        return token

    except BadRequestException as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))

    except EntityAlreadyExistsException as err:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))
