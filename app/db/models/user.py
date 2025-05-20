from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import enum
from starlette.authentication import BaseUser
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import Enum, String, ARRAY, Select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.utils.security import verify_password, hash_password
from .base import Base
from .api_key import APIKey
if TYPE_CHECKING:
    from .external_user import ExternalUser

class UserRole(enum.StrEnum):
    admin = 'admin'
    user = 'user'

class UserState(enum.IntEnum):
    active = 0
    deactive = 1

class User(Base, BaseUser):
    username:Mapped[str] = mapped_column(String, unique=True)
    roles: Mapped[list[UserRole]] = mapped_column(ARRAY(Enum(UserRole)), default=[UserRole.user])
    email:Mapped[str] = mapped_column(String, unique=True)
    password:Mapped[str] = mapped_column(String, nullable=False)
    state:Mapped[UserState] = mapped_column(Enum(UserState), default=UserState.active)
    api_keys:Mapped[list[APIKey]] = relationship(back_populates='user')
    external_users:Mapped[list[ExternalUser]] = relationship(back_populates='user')

    @classmethod
    def init_user(cls, session: Session):
        session.add(User(username=settings.DEFAULT_ADMIN_USERNAME, email=settings.DEFAULT_ADMIN_EMAIL, password=hash_password(settings.DEFAULT_ADMIN_PASSWORD), roles=[UserRole.admin]))

    @classmethod
    async def create(cls, async_session:AsyncSession, username:str, email:str, password:str, roles: list[UserRole] = [UserRole.user]) -> User:
        return await super().create(async_session=async_session, username=username, email=email, password=hash_password(password), roles=roles)
    
    @classmethod
    async def get_user_by_apikey(cls, async_session:AsyncSession, apikey:str) -> User:
        stmt = Select(User).where(User.api_keys.any(APIKey.api_key == apikey))
        objs = await async_session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]
    
    @classmethod
    async def get_user_by_external_token(cls, async_session:AsyncSession, token:str) -> User:
        stmt = Select(User).where(User.external_users.any(and_(ExternalUser.expires_at > func.now(), ExternalUser.access_token == token)))
        objs = await async_session.scalars(stmt)
        objs = objs.all()
        if len(objs):
            return objs[0]

    def verify_password(self, password:str) -> bool:
        return verify_password(self.password, password)

    def update_password(self, password:str) -> None:
        self.password = hash_password(password)

    @property
    def identity(self) -> int:
        return self.id
    
    @property
    def is_authenticated(self) -> bool:
        return self.id is not None