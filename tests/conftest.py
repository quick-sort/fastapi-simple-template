import asyncio
from typing import Generator, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from app.main import app
from app.db.session import ASYNC_DB_SESSION


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with ASYNC_DB_SESSION() as session:
        yield session
    await ASYNC_DB_SESSION.remove()