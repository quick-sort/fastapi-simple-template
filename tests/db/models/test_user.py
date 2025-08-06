import logging

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserRole

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_sub_transaction(db_session: AsyncSession):
    user = await User.create(
        async_session=db_session,
        username="test1",
        email="test1@example.com",
        roles=[UserRole.user],
        password="test",
    )
    assert user.id is not None
    await db_session.rollback()
    user2 = await User.find_one(async_session=db_session, username="test1")
    assert user2 is None


@pytest.mark.asyncio
async def test_crud_user(db_session: AsyncSession):
    user = await User.create(
        async_session=db_session,
        username="test2",
        email="test2@example.com",
        roles=[UserRole.user],
        password="test",
    )
    assert user.id is not None
    await db_session.commit()
    user2 = await User.find(async_session=db_session, username="test2")
    assert len(user2) == 1
    user2 = user2[0]
    assert user2.id == user.id
    assert not user2.verify_password("wrong_password")
    assert user2.verify_password("test")
    user = await db_session.get(User, user.id)
    assert user.id == user2.id
    await User.delete_by_id(db_session, user.id)
    await db_session.commit()
    user2 = await User.find_one(async_session=db_session, username="test2")
    assert not user2
