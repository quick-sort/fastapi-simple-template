import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_auth(client:TestClient, db_session: AsyncSession):
    pass