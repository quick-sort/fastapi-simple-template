from typing import Optional, TYPE_CHECKING
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, String, DateTime, ForeignKey, func, Text, UniqueConstraint, Column, Table, Boolean, ARRAY
from app.utils.security import verify_password
from .base import Base

class UserRole(enum.StrEnum):
    admin = 'admin'
    user = 'user'

class User(Base):
    username:Mapped[str] = mapped_column(String, unique=True)
    roles: Mapped[list[UserRole]] = mapped_column(ARRAY(Enum(UserRole)), default=[UserRole.user])
    email:Mapped[str] = mapped_column(String, unique=True)
    password:Mapped[str] = mapped_column(String, nullable=False)

    def verify_password(self, password:str) -> bool:
        return verify_password(self.password, password)