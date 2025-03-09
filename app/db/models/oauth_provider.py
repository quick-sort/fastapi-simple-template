from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, JSON, ForeignKey, func, Text, UniqueConstraint, Boolean, ARRAY, Enum, Integer
from .base import Base

if TYPE_CHECKING:
    from .external_user import ExternalUser

class ProviderType(enum.StrEnum):
    oauth1 = 'oauth1'
    oauth2 = 'oauth2'
    oidc = 'oidc'

class OauthProvider(Base):
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