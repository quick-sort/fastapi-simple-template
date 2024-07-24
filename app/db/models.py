import enum
from typing import Optional
import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, DateTime, ForeignKey, func, Text, UniqueConstraint, Column, Table, Boolean
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import JSON
import re
TABLE_NAME_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')

class Base(AsyncAttrs, DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        # Replace 'Base' with the name of your base class
        return TABLE_NAME_PATTERN.sub('_', cls.__name__).lower() + 's'
    
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at:Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
    updated_at:Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_

class IntEnumType(enum.IntEnum):
    done = 0

class StrEnumType(enum.StrEnum):
    done = 'done'

class User(Base):
    username:Mapped[str] = mapped_column(String, unique=True)
    email:Mapped[str] = mapped_column(String, unique=True)
    email_verified:Mapped[bool] = mapped_column(Boolean)
    password:Mapped[str] = mapped_column(String, nullable=False)
