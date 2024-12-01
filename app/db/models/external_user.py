from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, func, Text, UniqueConstraint, Column, Table, Boolean, ARRAY, JSON
from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .oauth_provider import OauthProvider

class ExternalUser(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    user: Mapped[User] = relationship(back_populates="external_users")
    oauth_provider_id: Mapped[int] = mapped_column(ForeignKey("oauth_providers.id", ondelete='CASCADE'))
    oauth_provider: Mapped[OauthProvider] = relationship(back_populates="external_users")
    external_id: Mapped[str] = mapped_column(String)
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str] = mapped_column(String)
    userinfo: Mapped[dict] = mapped_column(JSON)
    token_expired_at: Mapped[datetime.datetime] = mapped_column(DateTime)