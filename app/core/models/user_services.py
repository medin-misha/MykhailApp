from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    BigInteger,
    DateTime,
    String,
    Boolean,
    ForeignKey,
    func,
    CheckConstraint, UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class UserService(Base):
    """
    Связь User - Service позволяет работать с юзером в рамках одного сервиса а не всех сразу
    """

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("User.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    service_id = mapped_column(
        Integer, ForeignKey("Service.id", ondelete="CASCADE"), nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=func.now()
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # отношения
    user: Mapped["User"] = relationship(back_populates="services")
    service: Mapped["Service"] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"<UserService user_id={self.user_id} service_id={self.service_id} active={self.is_active}>"

    __table_args__ = (
        UniqueConstraint("user_id", "service_id", name="uq_user_service_pair"),
    )
