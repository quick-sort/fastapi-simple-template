import logging
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Base, User, UserRole
from app.db.session import ASYNC_DB_SESSION, ASYNC_ENGINE
from app.utils.security import hash_password

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mock_admin():
    admin = "admin"
    return User(
        username=admin,
        email="admin@admin.com",
        password=hash_password(admin),
        roles=[UserRole.admin],
    )


@pytest.fixture(scope="session")
def mock_user():
    user = "user"
    return User(
        username=user,
        email="user@example.com",
        password=hash_password(user),
        roles=[UserRole.user],
    )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_all_tables(mock_admin, mock_user):
    async with ASYNC_ENGINE.begin() as conn:
        logger.info("Recreating all tables")
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        async with ASYNC_DB_SESSION() as session:
            session.add(mock_admin)
            session.add(mock_user)
            logger.info("Creating admin and default user")
            await session.commit()


@pytest_asyncio.fixture(scope="function")
async def db_session(create_all_tables) -> AsyncGenerator[AsyncSession, None]:
    async with ASYNC_DB_SESSION() as session:
        yield session
