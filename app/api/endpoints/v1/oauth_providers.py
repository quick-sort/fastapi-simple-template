from typing import Optional, Annotated
import logging
from fastapi import APIRouter, Depends, HTTPException, Response, Security, Path
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole, OauthProvider
from app.db.dao.base import DAO
from app.api.middlewares.db import get_db_session
from app.api.middlewares.auth import get_scoped_user
from app.api import schema

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get('/')
async def list_oauth_providers(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[schema.OAuthProvider]:
    dao = DAO(OauthProvider, db_session)
    objs = await dao.find()
    return objs

@router.get('/{provider_id}')
async def get_oauth_provider(
    provider_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.OAuthProvider:
    dao = DAO(OauthProvider, db_session)
    obj = await dao.get_by_id(provider_id)
    return obj

@router.post('/')
async def create_oauth_provider(
    params: schema.CreateOAuthProviderParams,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.OAuthProvider:
    dao = DAO(OauthProvider, db_session)
    obj = await dao.create(**params.model_dump())
    return obj

@router.put('/{provider_id}')
async def update_oauth_provider(
    provider_id: int,
    params: schema.UpdateOAuthProviderParams,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.OAuthProvider:
    dao = DAO(OauthProvider, db_session)
    data = params.model_dump(exclude_unset=True)
    await dao.update_by_id(provider_id, **data)
    obj = await dao.get_by_id(provider_id)
    return obj

@router.delete('/{provider_id}')
async def delete_oauth_provider(
    provider_id: int,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.Deleted:
    dao = DAO(OauthProvider, db_session)
    await dao.delete_id(provider_id)
    return {'id': provider_id}