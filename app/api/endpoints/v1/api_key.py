import logging
from fastapi import APIRouter, Depends, HTTPException, Response, Security
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.middlewares.auth import get_current_user, get_scoped_user
from app.api.middlewares.db import get_db_session
from app.db.models import User, UserRole, APIKey
from app.api import schema

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get('/my')
async def list_my_api_key(
    user: Annotated[User, Depends(get_current_user)],
) -> list[schema.APIKey]:
    objs = await user.awaitable_attrs.api_keys
    return objs

@router.post('/my')
async def create_my_api_key(
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    name: Optional[str] = None,
) -> schema.APIKey:
    obj = await APIKey.create_api_key(async_session=db_session, user_id=user.id, name=name)
    return obj

@router.delete('/my/{key_id}')
async def delete_my_api_key(
    key_id:int,
    user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.Deleted:
    obj = await db_session.get(APIKey, key_id)
    if obj and obj.user_id == user.id:
        await db_session.delete(obj)
    return {'id': key_id}

@router.post('/')
async def create_api_key(
    params: schema.CreateAPIKeyParams,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.APIKey:
    obj = await APIKey.create_api_key(async_session=db_session, user_id=params.user_id, name=params.name)
    return obj

@router.get('/')
async def list_api_key(
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    user_id: Optional[int] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
) -> schema.PagedList[schema.APIKey]:
    if user_id:
        objs = await APIKey.find(async_session=db_session, user_id=user_id)
        total = len(objs)
        offset = 0
        limit = len(objs)
    else:
        objs = await APIKey.find(async_session=db_session, offset=offset, limit=limit)
        total = await APIKey.count(async_session=db_session)
    return schema.PagedList(items=objs, total=total, offset=offset, limit=limit)

@router.delete('/{key_id}')
async def delete_api_key(
    key_id: int,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.Deleted:
    await APIKey.delete_by_id(async_session=db_session, id=key_id)
    return {'id': key_id}