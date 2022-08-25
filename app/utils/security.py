from fastapi import Depends, HTTPException, APIRouter, Request, Response, Form
from typing import Optional
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime, timedelta
from jose import jwt, JWTError
from routers import auth
from utils.schemas import LoginForm

SECRET_KEY = '3K75JD2JKDS99U342YINQ0'

ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return bcrypt_context.hash(password)


def verify_password(password, hashed_password):
    return bcrypt_context.verify(password, hashed_password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user

# [create an encoded JWT]


def create_access_token(username: str, user_id: int,
                        expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# [decode JWT]


async def get_current_user(request: Request):
    try:
        token = request.cookies.get('access_token')
        if token is None:
            return None

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if username is None or user_id is None:
            auth.logout(request)

        return {'username': username, 'id': user_id}

    except JWTError:
        raise HTTPException(status_code=404, detail="Not found")