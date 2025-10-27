from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, BigInteger, DateTime, String, Boolean, ForeignKey, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserSubscription(Base):
    """
    Факт подписки пользователя на тариф (история). Одновременно может быть несколько
    подписок (например, бесплатная + платная), но активность регулируем бизнес-логикой.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    subscription_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("subscriptions.id", ondelete="SET NULL"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    source: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)  # 'tribute', 'telegram_stars', ...

    # отношения
    user: Mapped["User"] = relationship(back_populates="subscriptions")
    subscription: Mapped["Subscription"] = relationship(back_populates="user_subscriptions")

    __table_args__ = (
        # Простая санитарная проверка: дата окончания, если задана, не может быть раньше старта
        CheckConstraint("(expires_at IS NULL) OR (expires_at >= started_at)", name="chk_subscription_time_valid"),
    )

    def __repr__(self) -> str:
        return f"<UserSubscription user_id={self.user_id} sub_id={self.subscription_id} active={self.active}>"
