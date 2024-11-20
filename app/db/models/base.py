import enum
from typing import Optional
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, DateTime, ForeignKey, func, Text, UniqueConstraint, Column, Table, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import JSON
import re
TABLE_NAME_PATTERN = re.compile(r'(?<!^)(?=[A-Z][a-z])')

class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        # Replace 'Base' with the name of your base class
        return TABLE_NAME_PATTERN.sub('_', cls.__name__).lower() + 's'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)