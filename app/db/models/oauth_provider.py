from __future__ import annotations
from typing import Optional, TYPE_CHECKING, ClassVar
import enum
import asyncio
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey, func, Text, UniqueConstraint, Boolean, ARRAY, Enum, Integer
from sqlalchemy.ext.asyncio import AsyncSession
from .base import Base
from .external_user import ExternalUser

if TYPE_CHECKING:
    from .external_user import ExternalUser

class ProviderType(enum.StrEnum):
    oauth1 = 'oauth1'
    oauth2 = 'oauth2'
    oidc = 'oidc'

class OauthProvider(Base):
    _auth_registry: ClassVar[Optional[OAuth]] = None
    _auth_registry_lock: ClassVar[asyncio.Lock] = asyncio.Lock()

    name: Mapped[str] = mapped_column(String, default='oauth', unique=True)
    provider_type: Mapped[ProviderType] = mapped_column(Enum(ProviderType), default=ProviderType.oauth2)
    client_id: Mapped[str] = mapped_column(String)
    client_secret: Mapped[str] = mapped_column(String)
    server_metadata_url: Mapped[Optional[str]] = mapped_column(String)
    api_base_url: Mapped[Optional[str]] = mapped_column(String)
    authorize_url: Mapped[Optional[str]] = mapped_column(String)
    authorize_params: Mapped[dict] = mapped_column(JSON, default={})
    userinfo_url: Mapped[Optional[str]] = mapped_column(String)
    request_token_url: Mapped[Optional[str]] = mapped_column(String)
    request_token_params: Mapped[dict] = mapped_column(JSON, default={})
    access_token_url: Mapped[Optional[str]] = mapped_column(String)
    access_token_params: Mapped[dict] = mapped_column(JSON, default={})
    refresh_token_url: Mapped[Optional[str]] = mapped_column(String)
    refresh_token_params: Mapped[dict] = mapped_column(JSON, default={})
    redirect_uri: Mapped[str] = mapped_column(String)
    client_kwargs: Mapped[dict] = mapped_column(JSON, default={})
    external_users: Mapped[list[ExternalUser]] = relationship(back_populates='oauth_provider')

    @classmethod
    async def get_auth_registry(cls, async_session:AsyncSession) -> OAuth:
        if cls._auth_registry:
            return cls._auth_registry
        async with cls._auth_registry_lock:
            if cls._auth_registry:
                return cls._auth_registry
            authlib_registry = OAuth()
            providers:list[OauthProvider] = await cls.find(async_session)
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
            cls._auth_registry = authlib_registry
        return cls._auth_registry