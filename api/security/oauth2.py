from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api.db.database_config import get_db
from api.models.user_model import User
from api.security.token_schemas import TokenData, Token
from api.service.user_service import UserService
from jose import JWTError, jwt
from api.security.password import HashPassword
from api.config.env_config import settings as env

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

SECRET_KEY: str = env.token_secret_key
ALGORITHM: str = env.token_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.token_expire_minutes

user_service = UserService()
hash_password = HashPassword()


def create_access_token(data: dict) -> Token:
    to_encode: dict = data.copy()
    expire: datetime = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=token)


def verify_access_token(token: str, credentials_exception: HTTPException) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get('email')
        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    return token_data


def authenticate_user(email: str, plain_password: str, db: Session) -> User:
    user: User = db.query(User).filter_by(email=email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not hash_password.verify_password(plain_password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    return user


def get_principal(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception: HTTPException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                         detail="Could not validate credentials",
                                                         headers={"WWW-Authenticate": "Bearer"})
    token: TokenData = verify_access_token(token, credentials_exception)
    principal: User = db.query(User).filter_by(email=token.email).first()
    return principal
