import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.user import UserController
from app.db.models.user import User, UserRole
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_controller_user(db_session:AsyncSession):
    controller = UserController(db_session, autocommit=True)
    user2 = await controller.find(username="test")
    if user2:
        await controller.delete(user2[0])
    user = await controller.create_user(username="test", email="test@example.com", role=UserRole.user, password="test")
    assert user.id is not None
    user2 = await controller.find(username="test")
    assert len(user2) == 1
    user2 = user2[0]
    assert user2.id == user.id
    assert not user2.verify_password("wrong_password")
    assert user2.verify_password("test")
    user = await controller.get_by_id(user.id)
    assert user.id == user2.id
    