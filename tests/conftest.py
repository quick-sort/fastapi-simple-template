import asyncio
from typing import Generator, AsyncGenerator
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.config import settings
from app.db.session import ASYNC_SCOPED_SESSION
from app.main import app

@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def db_session(event_loop) -> AsyncGenerator[AsyncSession, None]:
    async with ASYNC_SCOPED_SESSION() as session:
        yield session
    await ASYNC_SCOPED_SESSION.remove()
    