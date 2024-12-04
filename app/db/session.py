import asyncio
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncSession, 
    async_scoped_session, 
    async_sessionmaker,
)
from sqlalchemy.pool import NullPool
from app.config import settings

ASYNC_ENGINE = create_async_engine(
    str(settings.SQLALCHEMY_URI), 
    #echo=True,
    poolclass=NullPool,
)

ASYNC_ENGINE_FACTORY = async_sessionmaker(
    ASYNC_ENGINE,
    expire_on_commit=False,
)

ASYNC_DB_SESSION:AsyncSession = async_scoped_session(
    ASYNC_ENGINE_FACTORY,
    scopefunc=asyncio.current_task,
)