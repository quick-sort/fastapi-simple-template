import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.controllers.user import UserController
from app.db.models.user import User, UserRole
import logging

logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_controller_user(db_session:AsyncSession):
    controller = UserController(User, db_session, autocommit=True)
    user2 = await controller.find(username="test")
    if user2:
        await controller.delete(user2[0])
    user = await controller.create(username="test", email="test@example.com", role=UserRole.user, password="test")
    assert user.id is not None
    user2 = await controller.find(username="test")
    assert len(user2) == 1
    assert user2[0].id == user.id
    