from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field


# ---------- Базовая модель ----------
class PaymentBase(BaseModel):
    """
    Базовая модель платежа (общие поля, используемые в разных контекстах).
    """
    user_id: Optional[int] = Field(None, description="ID пользователя, совершившего платёж")
    amount: float = Field(..., gt=0, description="Сумма платежа")
    currency: str = Field(..., max_length=8, description="Валюта платежа (например, 'USD', 'EUR', 'UAH')")
    provider: str = Field(..., max_length=64, description="Платёжный провайдер (например, 'stripe', 'telegram', 'paypal')")
    provider_payload: Optional[dict[str, Any]] = Field(None, description="JSON-данные, полученные от платёжного провайдера")
    succeeded: bool = Field(default=False, description="Флаг успешности платежа")


# ---------- Модель создания ----------
class PaymentCreate(PaymentBase):
    """
    Используется при создании новой записи о платеже (в момент получения уведомления от провайдера).
    """
    pass


# ---------- Модель обновления ----------
class PaymentUpdate(BaseModel):
    """
    Используется для обновления состояния платежа (например, после подтверждения).
    """
    succeeded: Optional[bool] = Field(None, description="Статус успешности платежа")
    provider_payload: Optional[dict[str, Any]] = Field(None, description="Обновлённые данные от провайдера")


# ---------- Модель возврата ----------
class PaymentReturn(PaymentBase):
    """
    Используется для возврата данных клиенту (HTTP-ответ, AMQP payload и т.п.).
    """
    id: int = Field(..., description="Идентификатор платежа")
    created_at: datetime = Field(..., description="Дата создания записи о платеже")

    # Дополнительно (если нужно показывать информацию о пользователе)
    user_name: Optional[str] = Field(None, description="Имя пользователя, совершившего платёж")

    class Config:
        from_attributes = True  # (Pydantic v2) — аналог orm_mode=True
