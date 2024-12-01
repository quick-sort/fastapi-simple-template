from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, func, Text, UniqueConstraint, Boolean, ARRAY, Enum
from .base import Base

if TYPE_CHECKING:
    from .external_user import ExternalUser

class OauthProvider(Base):
    name: Mapped[str] = mapped_column(String, default='oauth provider')
    provider_type: Mapped[str] = mapped_column(String, default='oauth2')
    client_id: Mapped[str] = mapped_column(String)
    client_secret: Mapped[str] = mapped_column(String)
    login_url: Mapped[str] = mapped_column(String)
    verify_url: Mapped[str] = mapped_column(String)
    access_token_url: Mapped[str] = mapped_column(String)
    refresh_token_url: Mapped[str] = mapped_column(String)
    callback_url: Mapped[str] = mapped_column(String)
    scope: Mapped[list[str]] = mapped_column(ARRAY(String))
    external_users: Mapped[list[ExternalUser]] = relationship(back_populates='oauth_provider')