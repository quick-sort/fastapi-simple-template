from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, DateTime, ForeignKey, func, Text, UniqueConstraint, Column, Table, Boolean
from .base import Base

class User(Base):
    username:Mapped[str] = mapped_column(String, unique=True)
    email:Mapped[str] = mapped_column(String, unique=True)
    email_verified:Mapped[bool] = mapped_column(Boolean)
    password:Mapped[str] = mapped_column(String, nullable=False)