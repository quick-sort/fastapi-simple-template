from fastapi import APIRouter, Depends, HTTPException, Response, Security
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.middlewares.auth import get_current_user, get_scoped_user
from app.api.middlewares.db import get_db_session
from app.db.models import User, UserRole
from app.db.dao.user import UserDAO
from app.api import schema

router = APIRouter()

@router.get('/')
async def list_users(
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[schema.User]:
    dao = UserDAO(db_session)
    users = await dao.find()
    return users


@router.delete('/{user_id}')
async def delete_user(
    user_id: int,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.Deleted:
    dao = UserDAO(db_session)
    await dao.delete_id(user_id)
    return {'id': user_id}