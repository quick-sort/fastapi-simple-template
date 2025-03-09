from typing import Annotated, Optional
from datetime import timedelta
from fastapi import APIRouter, Depends, Path, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.middlewares.db import get_db_session
from app.db.dao import DAO, ExternalUserDAO, OauthProviderDAO
from app.config import settings
from app.utils.security import generate_jwt_token

import logging
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get('/login/{provider_name}')
async def authorize(
    provider_name: Annotated[str, Path(pattern=r'^[A-Za-z0-9_\-]+$')],
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    redirect_uri: Optional[str] = None,
) -> RedirectResponse:
    dao = OauthProviderDAO(db_session)
    provider = await dao.find_one(name=provider_name)
    if not provider:
        raise HTTPException(status_code=400, detail="Invalid Authentication")
    
    authlib_registry = await dao.get_registry()
    oauth_client = authlib_registry.create_client(provider_name)
    request.session['redirect_uri'] = redirect_uri
    return await oauth_client.authorize_redirect(request, provider.redirect_uri)

@router.get('/callback/{provider_name}')
async def oauth_callback(
    provider_name: Annotated[str, Path(pattern=r'^[A-Za-z0-9_\-]+$')],
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> RedirectResponse:
    dao = OauthProviderDAO(db_session)
    provider = await dao.find_one(name=provider_name)
    if not provider:
        raise HTTPException(status_code=400, detail="Invalid Authentication")
    authlib_registry = await dao.get_registry()
    oauth_client = authlib_registry.create_client(provider_name)
    token = await oauth_client.authorize_access_token(request)
    logger.info(token)
    external_dao = ExternalUserDAO(db_session)
    external_user = await external_dao.create_external_user(provider=provider, access_token=token.get('access_token'), refresh_token=token.get('refresh_token'), expires_at=token.get('expires_at'), id_token=token.get('id_token'), userinfo=token.get('userinfo'))
    user = await external_user.awaitable_attrs.user
    expires = timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    jwt_token = generate_jwt_token({'user_id': user.id}, expires_delta=expires)
    request.session['token'] = jwt_token
    redirect_uri = request.session.pop('redirect_uri', '/')
    return RedirectResponse(redirect_uri)