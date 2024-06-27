from typing import Annotated, AsyncGenerator
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from app.db.session import ASYNC_SCOPED_SESSION
from app.db.models import User
from app.config import settings
from app.utils.security import decode_jwt_token

get_oauth_token = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(get_oauth_token)]
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_jwt_token(token)
    if not payload or payload.get('user_id'):
        raise credentials_exception
    user_id = payload.get('user_id')
    

    ## TODO: get user from db_session by user_id
    user = {}
    if not user:
        raise credentials_exception
    return user

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = ASYNC_SCOPED_SESSION()
    try:
        yield async_session
    except Exception as e:
        await async_session.rollback()
    finally:
        await ASYNC_SCOPED_SESSION.remove()