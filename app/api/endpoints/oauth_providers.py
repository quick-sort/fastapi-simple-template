from fastapi import APIRouter, Depends, HTTPException, Response, Security
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole, OauthProvider
from app.db.dao.base import DAO
from .. import schema
from .. import depends

router = APIRouter()

@router.get('/')
async def list_oauth_providers(
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
) -> list[schema.OAuthProvider]:
    dao = DAO(OauthProvider, db_session, autocommit=True)
    objs = await dao.find()
    return objs

@router.post('/')
async def create_oauth_provider(
    params: schema.CreateOAuthProviderParams,
    admin_user: Annotated[User, Security(depends.get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
) -> schema.OAuthProvider:
    dao = DAO(OauthProvider, db_session, autocommit=True)
    obj = await dao.create(**params.model_dump())
    return obj

@router.put('/{provider_id}')
async def update_oauth_provider(
    provider_id: int,
    params: schema.UpdateOAuthProviderParams,
    admin_user: Annotated[User, Security(depends.get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
) -> schema.OAuthProvider:
    dao = DAO(OauthProvider, db_session, autocommit=True)
    data = params.model_dump(exclude_unset=True)
    await dao.update_by_id(provider_id, **data)
    obj = await dao.find_one(provider_id)
    return obj

@router.delete('/{provider_id}')
async def delete_oauth_provider(
    provider_id: int,
    admin_user: Annotated[User, Security(depends.get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(depends.get_db_session)],
) -> schema.Deleted:
    dao = DAO(OauthProvider, db_session, autocommit=True)
    await dao.delete_id(provider_id)
    return {'id': provider_id}