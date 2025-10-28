from __future__ import annotations

from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class APIKey(Base):
    """
    Таблица API-ключей для сервисов.
    Храним ХЕШ ключа (а не сам ключ) в поле key.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    service_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("Service.id", ondelete="CASCADE"),
        nullable=False
    )
    key: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(256), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    # отношения
    service: Mapped["Service"] = relationship(back_populates="api_keys")
    def __repr__(self) -> str:
        return f"<APIKey id={self.id} service_id={self.service_id} active={self.is_active}>"
