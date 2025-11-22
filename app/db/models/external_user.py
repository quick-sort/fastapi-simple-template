from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Select, String, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .oauth_provider import OauthProvider
    from .user import User, UserRole


class ExternalUser(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped[User] = relationship(back_populates="external_users")
    oauth_provider_id: Mapped[int] = mapped_column(
        ForeignKey("oauth_providers.id", ondelete="CASCADE")
    )
    oauth_provider: Mapped[OauthProvider] = relationship(
        back_populates="external_users"
    )
    external_id: Mapped[str] = mapped_column(String, index=True)
    id_token: Mapped[Optional[str]] = mapped_column(Text)
    access_token: Mapped[str] = mapped_column(Text)
    refresh_token: Mapped[str] = mapped_column(Text)
    userinfo: Mapped[dict] = mapped_column(JSON, default={})
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime)

    @classmethod
    async def create_external_user(
        cls,
        async_session: AsyncSession,
        provider: OauthProvider,
        access_token: str,
        refresh_token: str,
        expires_at: int,
        userinfo: dict,
        id_token: str = None,
    ) -> ExternalUser:
        external_id = userinfo.get("sub")
        if not external_id:
            return
        if isinstance(expires_at, int):
            expires_at = datetime.datetime.fromtimestamp(expires_at)
        stmt = Select(ExternalUser).where(
            ExternalUser.oauth_provider_id == provider.id,
            ExternalUser.external_id == external_id,
        )
        external_user: ExternalUser | None = await async_session.scalar(stmt)
        if external_user:
            external_user.id_token = id_token
            external_user.access_token = access_token
            external_user.refresh_token = refresh_token
            external_user.expires_at = expires_at
            external_user.userinfo = userinfo
            return external_user

        async with async_session.begin_nested() as nested_transaction:
            user = User(
                username=userinfo.get(provider.username_field),
                roles=[UserRole.user],
            )
            external_user = ExternalUser(
                user=user,
                oauth_provider_id=provider.id,
                external_id=external_id,
                id_token=id_token,
                access_token=access_token,
                refresh_token=refresh_token,
                userinfo=userinfo,
                expires_at=expires_at,
            )
            async_session.add_all([user, external_user])
            await nested_transaction.commit()
            return external_user
