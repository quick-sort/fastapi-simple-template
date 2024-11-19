from typing import Any
from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext
from app.config import settings

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return PWD_CONTEXT.verify(password, hashed_password)
    except:
        return False

def hash_password(password:str) -> str:
    return PWD_CONTEXT.hash(password)

def generate_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode['exp'] = expire
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_jwt_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        pass