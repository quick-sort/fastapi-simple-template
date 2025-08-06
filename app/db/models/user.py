from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Enum, Select, String, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from starlette.authentication import BaseUser

from app.utils.security import hash_password, verify_password

from .api_key import APIKey
from .base import Base

if TYPE_CHECKING:
    from .external_user import ExternalUser


class UserRole(enum.StrEnum):
    admin = "admin"
    user = "user"


class UserState(enum.IntEnum):
    active = 0
    deactive = 1


class User(Base, BaseUser):
    username: Mapped[str] = mapped_column(String, unique=True)
    roles: Mapped[list[UserRole]] = mapped_column(
        ARRAY(Enum(UserRole)), default=[UserRole.user]
    )
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[UserState] = mapped_column(Enum(UserState), default=UserState.active)
    api_keys: Mapped[list[APIKey]] = relationship(back_populates="user")
    external_users: Mapped[list[ExternalUser]] = relationship(back_populates="user")

    @classmethod
    async def create(
        cls,
        async_session: AsyncSession,
        username: str,
        email: str,
        password: str,
        roles: list[UserRole] = [UserRole.user],
    ) -> User:
        return await super().create(
            async_session=async_session,
            username=username,
            email=email,
            password=hash_password(password),
            roles=roles,
        )

    @classmethod
    async def get_user_by_apikey(cls, async_session: AsyncSession, apikey: str) -> User:
        stmt = Select(User).where(User.api_keys.any(APIKey.api_key == apikey))
        objs = await async_session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]

    @classmethod
    async def get_user_by_external_token(
        cls, async_session: AsyncSession, token: str
    ) -> User:
        stmt = Select(User).where(
            User.external_users.any(
                and_(
                    ExternalUser.expires_at > func.now(),
                    ExternalUser.access_token == token,
                )
            )
        )
        objs = await async_session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]

    def verify_password(self, password: str) -> bool:
        return verify_password(self.password, password)

    def update_password(self, password: str) -> None:
        self.password = hash_password(password)

    @property
    def identity(self) -> int:
        return self.id

    @property
    def is_authenticated(self) -> bool:
        return self.id is not None
