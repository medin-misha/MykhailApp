from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# ---------- Базовая модель ----------
class ServiceBase(BaseModel):
    """
    Базовая модель сервиса (общие поля, используемые в разных контекстах).
    """
    name: str = Field(..., max_length=128, description="Название сервиса (например: 'mykhailbot', 'publisher')")
    description: Optional[str] = Field(None, description="Описание сервиса")
    owner_id: Optional[int] = Field(None, description="ID администратора, владеющего сервисом")


# ---------- Модель создания ----------
class ServiceCreate(ServiceBase):
    """
    Используется при создании нового сервиса (через панель управления или API).
    """
    pass


# ---------- Модель обновления ----------
class ServiceUpdate(BaseModel):
    """
    Используется для частичного обновления данных сервиса.
    """
    name: Optional[str] = Field(None, max_length=128)
    description: Optional[str] = None
    owner_id: Optional[int] = None


# ---------- Модель возврата ----------
class ServiceReturn(ServiceBase):
    """
    Используется для возврата данных клиенту (HTTP-ответ или AMQP payload).
    """
    id: int = Field(..., description="Идентификатор сервиса")
    api_keys: Optional[List[int]] = Field(default_factory=list, description="ID связанных API-ключей")
    created_at: Optional[datetime] = Field(None, description="Дата создания записи")
    updated_at: Optional[datetime] = Field(None, description="Дата последнего обновления")

    class Config:
        from_attributes = True  # (Pydantic v2) — аналог orm_mode=True
