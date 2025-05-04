from __future__ import annotations
from typing import Optional, TYPE_CHECKING
import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, func, Text, UniqueConstraint, Column, Table, Boolean, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.security import generate_api_key
from app.config import settings
from .base import Base

if TYPE_CHECKING:
    from .user import User

class APIKey(Base):
    name: Mapped[str] = mapped_column(String, default='api_key')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete='CASCADE'))
    user: Mapped[User] = relationship(back_populates="api_keys")
    api_key: Mapped[str] = mapped_column(String, index=True)
    lastest_access: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())

    @classmethod
    async def create_api_key(cls, async_session:AsyncSession, user_id:int, name:str) -> APIKey:
        api_key = generate_api_key(settings.API_KEY_LEN)
        obj = await cls.create(async_session, user_id=user_id, name=name, api_key=api_key)
        return obj