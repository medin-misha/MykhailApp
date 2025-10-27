from __future__ import annotations

from typing import Optional

from sqlalchemy import Integer, String, Text, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Subscription(Base):
    """
    Описание тарифа/плана. Примеры: 'free', 'pro_month', 'pro_year'.
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    term_days: Mapped[int] = mapped_column(Integer, nullable=False)  # 0 = бессрочно
                                        # Numeric без float погрешностей.
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    sale_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_trial_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # отношения
    user_subscriptions: Mapped[list["UserSubscription"]] = relationship(
        back_populates="subscription", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Subscription {self.name} {self.term_days}d {self.price}>"