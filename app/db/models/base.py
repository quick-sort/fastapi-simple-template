from __future__ import annotations

import datetime
import re

from sqlalchemy import DateTime, Delete, Select, Update, func, text
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_object_session
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

TABLE_NAME_PATTERN = re.compile(r"(?<!^)(?=[A-Z][a-z])")


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        # Replace 'Base' with the name of your base class
        return TABLE_NAME_PATTERN.sub("_", cls.__name__).lower() + "s"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    @classmethod
    async def count(cls, async_session: AsyncSession, **kwargs) -> int:
        result = await async_session.scalar(
            Select(func.count(cls.id)).filter_by(**kwargs)
        )
        return result

    @classmethod
    async def clean_all(cls, async_session: AsyncSession) -> None:
        await async_session.execute(
            text(f"TRUNCATE TABLE {cls.__tablename__} RESTART IDENTITY CASCADE")
        )

    @classmethod
    async def create(cls, async_session: AsyncSession, **kwargs) -> Base:
        async with async_session.begin_nested() as nested_transaction:
            obj = cls(**kwargs)
            async_session.add(obj)
            await nested_transaction.commit()
            return obj

    @classmethod
    async def find(
        cls,
        async_session: AsyncSession,
        offset: int = None,
        limit: int = None,
        **kwargs,
    ) -> list[Base]:
        query = Select(cls).filter_by(**kwargs)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        result = await async_session.scalars(query)
        return result.all()

    @classmethod
    async def find_one(cls, async_session: AsyncSession, **kwargs) -> Base | None:
        result: list[Base] = await cls.find(async_session, **kwargs)
        if len(result) > 0:
            return result[0]

    @classmethod
    async def update_by_id(cls, async_session: AsyncSession, id: int, **kwargs) -> None:
        stmt = Update(cls).values(**kwargs).where(cls.id == id)
        await async_session.execute(stmt)

    @classmethod
    async def delete_by_id(cls, async_session: AsyncSession, id: int) -> None:
        stmt = Delete(cls).where(cls.id == id)
        await async_session.execute(stmt)

    @property
    def async_db_session(self) -> AsyncSession:
        return async_object_session(self)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
