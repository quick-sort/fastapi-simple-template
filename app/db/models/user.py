from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import enum
from starlette.authentication import BaseUser
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, ARRAY
from app.utils.security import verify_password, hash_password
from .base import Base

if TYPE_CHECKING:
    from .api_key import APIKey
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