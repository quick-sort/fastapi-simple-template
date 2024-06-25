from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from app.db.session import ASYNC_SCOPED_SESSION
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db_session():
    async_session = ASYNC_SCOPED_SESSION()
    try:
        yield async_session
    except Exception as e:
        await async_session.rollback()
    finally:
        await ASYNC_SCOPED_SESSION.remove()