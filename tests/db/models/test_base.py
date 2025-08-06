import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User, UserRole


@pytest.mark.asyncio
async def test_base_functions(
    db_session: AsyncSession,
    mock_user: User,
):
    assert await User.count(db_session) == 2

    assert await User.find_one(db_session, username=mock_user.username) is not None
    f1 = await User.find(db_session, offset=0, limit=1)
    result = await User.find(db_session)
    assert len(result) == 2
    mock_user = result[0]
    assert f1[0] in result
    result.remove(f1[0])
    assert len(result) == 1

    f2 = await User.find(db_session, offset=1, limit=1)
    assert f2[0] in result

    f3 = await User.find(db_session, offset=2, limit=1)
    assert not f3

    await User.update_by_id(db_session, mock_user.id, username="test")
    await db_session.commit()
    result_user = await db_session.get(User, mock_user.id)
    assert result_user.username == "test"
    obj = await User.create(
        db_session,
        username="Async Collector",
        email="async_collector@example.com",
        roles=[UserRole.user],
        password="test",
    )
    assert obj.id is not None
    await db_session.commit()
    await User.delete_by_id(db_session, obj.id)
    await db_session.commit()
    user = await db_session.get(User, obj.id)
    assert user is None
