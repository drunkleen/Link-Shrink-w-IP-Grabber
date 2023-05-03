from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import database, models
from app.config import settings
from app.schemas import userschema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = f'{settings.secret_key}'
ALGORITHM = f'{settings.algorithm}'
EXPIRATION_TIME_IN_MINUTES = settings.access_token_minutes


def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME_IN_MINUTES)
    to_encode = data.copy()
    to_encode.update({'exp': expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')
        if id is None:
            raise credentials_exception
        token_data = userschema.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), datab: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="credentials not validated ",
        headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = datab.query(models.User).filter(models.User.id == token.id).first()

    return user
