from pydantic import BaseModel, Field
from datetime import datetime, timezone


class BaseMeta(BaseModel):
    """
    Метаданные сообщения, описывающие контекст его отправки.
    """

    send_at: datetime = Field(
        # Время генерации сообщения (UTC, ISO 8601)
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        description="Время отправления сообщения",
    )
    service_id: int = Field(..., description="Айди сервиса из которого обращаются")
    api_key: str = Field(
        ...,
        description="Ключ API сервиса, от имени которого отправлено сообщение",
    )


class BaseMessage(BaseModel):
    """
    Базовая структура RMQ-сообщения.
    Содержит тип события, версию контракта, метаданные и полезную нагрузку.
    """

    event: str = Field(..., description="Название события сообщения, например 'user.registered'")
    version: str = Field(
        default="1.0",
        description="Версия контракта сообщения",
    )
    meta: BaseMeta = Field(..., description="Метаданные (время, источник, ключ и т.п.)")
    data: dict = Field(
        None,
        description="Основные данные сообщения (payload, контент события)",
    )
