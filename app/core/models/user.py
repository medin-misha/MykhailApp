from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Date, BigInteger, DateTime, String, func
from typing import Optional
from datetime import date, datetime
from .base import Base

class User(Base):

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    username: Mapped[Optional[str]] = mapped_column(String(64), unique=False, nullable=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)

    birthday_date: Mapped[date] = mapped_column(Date, nullable=True)

    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username} chat_id={self.chat_id}>"
