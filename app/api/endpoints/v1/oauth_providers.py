import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import schema
from app.api.middlewares.auth import get_scoped_user
from app.api.middlewares.db import get_db_session
from app.db.models import OauthProvider, User, UserRole

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def list_oauth_providers(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
) -> list[schema.OAuthProvider]:
    objs: list[OauthProvider] = await OauthProvider.find(async_session=db_session)
    return objs


@router.get("/{provider_id}")
async def get_oauth_provider(
    provider_id: int,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.OAuthProvider:
    obj: OauthProvider | None = await db_session.get(OauthProvider, provider_id)
    if not obj:
        raise HTTPException(status_code=404, detail="OAuth provider not found")
    return obj


@router.post("/")
async def create_oauth_provider(
    params: schema.CreateOAuthProviderParams,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.OAuthProvider:
    obj: OauthProvider = await OauthProvider.create(
        async_session=db_session, **params.model_dump()
    )
    return obj


@router.patch("/{provider_id}")
async def update_oauth_provider(
    provider_id: int,
    params: schema.UpdateOAuthProviderParams,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.OAuthProvider:
    obj: OauthProvider | None = await db_session.get(OauthProvider, provider_id)
    if not obj:
        raise HTTPException(status_code=404, detail="OAuth provider not found")
    data = params.model_dump(exclude_unset=True)
    await OauthProvider.update_by_id(async_session=db_session, id=provider_id, **data)
    obj: OauthProvider | None = await db_session.get(OauthProvider, provider_id)
    return obj


@router.delete("/{provider_id}")
async def delete_oauth_provider(
    provider_id: int,
    admin_user: Annotated[User, Security(get_scoped_user, scopes=[UserRole.admin])],
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> schema.Deleted:
    await OauthProvider.delete_by_id(async_session=db_session, id=provider_id)
    return {"id": provider_id}
