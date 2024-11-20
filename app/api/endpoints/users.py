from fastapi import APIRouter, Depends, HTTPException, Response, Security
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole
from app.db.dao.user import UserDAO
from .. import schema
from .. import depends

router = APIRouter()

@router.get('/')
async def list_users(
    admin_user: Annotated[User, Security(depends.get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
) -> list[schema.User]:
    dao = UserDAO(db_session, autocommit=True)
    users = await dao.find()
    return users

@router.get('/me')
async def get_my_user(
    user: Annotated[User, Depends(depends.get_current_user)],
) -> schema.User:
    return user