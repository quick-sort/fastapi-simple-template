import secrets
import string
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from app.config import settings


def generate_api_key(length: int = None):
    if not isinstance(length, int) or length < settings.API_KEY_LEN:
        length = settings.API_KEY_LEN
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for i in range(length))


HASH = PasswordHash.recommended()


def verify_password(hashed_password: str, password: str) -> bool:
    try:
        if not hashed_password or not password:
            return False
        return HASH.verify(password, hashed_password)
    except:
        return False


def hash_password(password: str) -> str:
    if not password:
        return None
    return HASH.hash(password)


def generate_jwt_token(data: dict, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        )
    to_encode = data.copy()
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.InvalidTokenError:
        pass
