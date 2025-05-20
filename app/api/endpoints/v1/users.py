from fastapi import APIRouter, Depends, HTTPException, Response, Security
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.middlewares.auth import get_current_user, get_scoped_user
from app.api.middlewares.db import get_db_session
from app.db.models import User, UserRole
from app.api import schema

router = APIRouter()

@router.get('/')
async def list_users(
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> schema.PagedList[schema.User]:
    users = await User.find(db_session, offset=offset, limit=limit)
    total = await User.count(db_session)
    return schema.PagedList(items=users, total=total, offset=offset, limit=limit)


@router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.Deleted:
    await User.delete_by_id(db_session, user_id)
    return {'id': user_id}