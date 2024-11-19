from __future__ import annotations
from typing import Annotated, AsyncGenerator
import logging
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException, Request
from fastapi.security import SecurityScopes
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from app.db.session import ASYNC_SCOPED_SESSION
from app.db.models import User
from app.db.dao import UserDAO
from app.config import settings
from app.utils.security import decode_jwt_token

logger = logging.getLogger(__name__)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = ASYNC_SCOPED_SESSION()
    try:
        yield async_session
    except Exception:
        logger.exception('error in processing request')
        await async_session.rollback()
        raise
    finally:
        await ASYNC_SCOPED_SESSION.remove()

async def get_scoped_user(
    security_scopes: SecurityScopes,
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    for scope in security_scopes.scopes:
        if scope not in user.roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
            )
    return user

async def get_current_user(
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    user = None
    #logger.info(request.scope['auth'].scopes)
    if request.user.is_authenticated:
        dao = UserDAO(db_session)
        user = await dao.get_by_id(request.user.identity)
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Unauthorized'
        )