from contextvars import ContextVar, Token
import uuid
import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncSession, 
    async_scoped_session, 
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from app.config import settings

db_session_id = ContextVar('db_session')

def set_db_session_id() -> Token:
    return db_session_id.set(str(uuid.uuid4()))

def reset_db_session_id(token: Token) -> None:
    db_session_id.reset(token)

def scopefunction() -> any:
    session_id = db_session_id.get(None)
    if not session_id:
        return asyncio.current_task()
    else:
        return session_id

ASYNC_DB_SESSION:AsyncSession = async_scoped_session(
    async_sessionmaker(
        create_async_engine(
            str(settings.SQLALCHEMY_URI), 
            #echo=True,
            poolclass=NullPool,
        ),
        expire_on_commit=False,
    ),
    scopefunc=scopefunction,
)
__all__ = [
    'ASYNC_DB_SESSION',
    'set_db_session_id',
    'reset_db_session_id'
]