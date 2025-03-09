import logging
from sqlalchemy import Select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import OauthProvider, ProviderType
from authlib.integrations.starlette_client import OAuth
from .base import DAO
from typing import Optional, ClassVar
import asyncio

logger = logging.getLogger(__name__)

class OauthProviderDAO(DAO[OauthProvider]):
    _registry: ClassVar[Optional[OAuth]] = None
    _registry_lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    def __init__(self, session:AsyncSession):
        super().__init__(OauthProvider, session)

    async def get_registry(self) -> OAuth:
        if not OauthProviderDAO._registry:
            async with OauthProviderDAO._registry_lock:
                authlib_registry = OAuth()
                providers = await self.find()
                for provider in providers:
                    if provider.provider_type == ProviderType.oauth1:
                        authlib_registry.register(
                            name=provider.name,
                            client_id=provider.client_id,
                            client_secret=provider.client_secret,
                            request_token_url=provider.request_token_url,
                            request_token_params=provider.request_token_params,
                            client_kwargs=provider.client_kwargs,
                        )
                    elif provider.provider_type == ProviderType.oauth2:
                        authlib_registry.register(
                            name=provider.name,
                            client_id=provider.client_id,
                            client_secret=provider.client_secret,
                            access_token_url=provider.access_token_url,
                            access_token_params=provider.access_token_params,
                            authorize_url=provider.authorize_url,
                            authorize_params=provider.authorize_params,
                            refresh_token_url=provider.refresh_token_url,
                            refresh_token_params=provider.refresh_token_params,
                            client_kwargs=provider.client_kwargs,
                        )
                    elif provider.provider_type == ProviderType.oidc:
                        authlib_registry.register(
                            name=provider.name,
                            client_id=provider.client_id,
                            client_secret=provider.client_secret,
                            server_metadata_url=provider.server_metadata_url,
                            client_kwargs=provider.client_kwargs,
                        )
                OauthProviderDAO._registry = authlib_registry
        return OauthProviderDAO._registry