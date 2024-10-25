from typing import Annotated, AsyncGenerator
import logging
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, status, HTTPException, Request
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

async def get_current_user(
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    user = None
    if request.user.is_authenticated:
        dao = UserDAO(db_session)
        user = await dao.get_by_id(request.user.identity)
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user