from __future__ import annotations
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, BigInteger, String, Numeric, DateTime, Boolean, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Payment(Base):
    """
    Платёжная запись. Минимальная версия, строго соответствующая таблице.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    user_id: Mapped[Optional[int]] = mapped_column(
        BigInteger, ForeignKey("User.id", ondelete="SET NULL"), nullable=True, index=True
    )
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(8), nullable=False, default="USD")
    provider: Mapped[str] = mapped_column(String(64), nullable=False)
    provider_payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    succeeded: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    # Связь с User для удобства ORM
    user: Mapped[Optional["User"]] = relationship(back_populates="payments")

    def __repr__(self) -> str:
        return f"<Payment id={self.id} provider={self.provider} succeeded={self.succeeded}>"
