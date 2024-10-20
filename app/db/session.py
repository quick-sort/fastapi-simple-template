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

ASYNC_SCOPED_SESSION:AsyncSession = async_scoped_session(
    ASYNC_ENGINE_FACTORY,
    scopefunc=asyncio.current_task,
)

class DBSession:
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        self.session = ASYNC_SCOPED_SESSION()
        return self.session

    async def __aexit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
        

