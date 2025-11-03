from __future__ import annotations

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import BigInteger, Date, DateTime, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

from .base import Base

class LanguageEnum(str, enum.Enum):
    """
    Язык пользователь (в дальнейшем язык интерфейса)
    """
    EN = "en"
    RU = "ru"

class User(Base):
    """
    Пользователь, ключевая сущность для аутентификации по Telegram chat_id
    """
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(64),  nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    birthday_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    source: Mapped[Optional[str]] = mapped_column(String(100))
    language: Mapped[str] = mapped_column(
        nullable=True,
        default=LanguageEnum.RU,
        doc="Язык интерфейса пользователя"
    )
    # отношения
    subscriptions: Mapped[list["UserSubscription"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    payments: Mapped[list["Payment"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User chat_id={self.chat_id} username={self.username!r}>"