from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ---------- Базовая модель ----------
class APIKeyBase(BaseModel):
    """
    Базовая модель API-ключа (общие поля, используемые в разных контекстах).
    """

    service_id: int = Field(..., description="ID сервиса, которому принадлежит ключ")
    description: Optional[str] = Field(
        None, max_length=256, description="Описание API-ключа"
    )
    is_active: bool = Field(default=True, description="Активен ли ключ")


# ---------- Модель создания ----------
class APIKeyCreate(APIKeyBase):
    """
    Используется при создании нового API-ключа (например, через панель администратора).
    """

    key: str = Field(..., max_length=128, description="Хэш API-ключа (не сам ключ!)")


# ---------- Модель создания ----------
class APIKeyCreateForm(APIKeyBase):
    """
    Используется как форма при создании нового API-ключа (например, через панель администратора).
    """


# ---------- Модель обновления ----------
class APIKeyUpdate(BaseModel):
    """
    Используется для частичного обновления данных API-ключа.
    """

    description: Optional[str] = Field(None, max_length=256)
    is_active: Optional[bool] = None


# ---------- Модель возврата ----------
class APIKeyReturn(APIKeyBase):
    """
    Используется для возврата данных клиенту (HTTP-ответ, AMQP payload и т.п.).
    """

    id: int = Field(..., description="Идентификатор API-ключа")
    created_at: datetime = Field(..., description="Дата создания ключа")

    # если нужно возвращать связанную сущность
    service_name: Optional[str] = Field(None, description="Название связанного сервиса")

    class Config:
        from_attributes = True  # (Pydantic v2) — аналог orm_mode=True
