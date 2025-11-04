from __future__ import annotations

from typing import Optional

from sqlalchemy import Integer, String, Text, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Service(Base):
    """
    Внешние/внутренние сервисы, которые обращаются к Auth (боты, мини-аппы, бэк-воркеры).
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False
    )  # 'mykhailbot', 'publisher', ...
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("Admin.id", ondelete="SET NULL"), nullable=True
    )

    # отношения
    api_keys: Mapped[list["APIKey"]] = relationship(
        back_populates="service", cascade="all, delete-orphan", lazy="selectin"
    )
    user_subscriptions: Mapped[list["UserService"]] = relationship(
        back_populates="service", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Service {self.name}>"
