from __future__ import annotations

from datetime import datetime
from typing import Optional
from enum import Enum

from sqlalchemy import BigInteger, String, Boolean, DateTime, func, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class AdminRole(str, Enum):
    superadmin = "superadmin"
    manager = "manager"
    moderator = "moderator"


class Admin(Base):
    """
    Админ для панельки/операций (не пользователь бота).
    """
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[AdminRole] = mapped_column(SAEnum(AdminRole, name="admin_role"), nullable=False, default=AdminRole.manager)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<Admin {self.username} ({self.role})>"