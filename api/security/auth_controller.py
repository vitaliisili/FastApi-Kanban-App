from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.models.user_model import User
from api.security.token_schemas import Token
from api.security.oauth2 import authenticate_user, create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/api/auth/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User = authenticate_user(user_credentials.username, user_credentials.password, db)
    token: Token = create_access_token(data={"email": user.email})
    return token
