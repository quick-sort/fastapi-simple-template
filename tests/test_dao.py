import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.dao.user import UserDAO
from app.db.models.user import User, UserRole
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_dao_user(db_session:AsyncSession):
    dao = UserDAO(db_session, autocommit=True)
    user2 = await dao.find(username="test")
    if user2:
        await dao.delete(user2[0])
    user = await dao.create_user(username="test", email="test@example.com", roles=[UserRole.user], password="test")
    assert user.id is not None
    user2 = await dao.find(username="test")
    assert len(user2) == 1
    user2 = user2[0]
    assert user2.id == user.id
    assert not user2.verify_password("wrong_password")
    assert user2.verify_password("test")
    user = await dao.get_by_id(user.id)
    assert user.id == user2.id
    await dao.delete_id(user.id)
    user2 = await dao.find(username="test")
    assert not user2
    