from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from contracts.subscriptions import SubscribeUserReturn


# ---------- Базовая модель ----------
class UserBase(BaseModel):
    chat_id: int = Field(..., description="Telegram chat_id пользователя")
    username: Optional[str] = Field(None, max_length=64, description="Имя пользователя в Telegram")
    phone: Optional[str] = Field(None, max_length=15, description="Номер телефона пользователя")
    email: Optional[EmailStr] = Field(None, description="Электронная почта пользователя")
    birthday_date: Optional[date] = Field(None, description="Дата рождения пользователя")
    is_active: bool = Field(default=True, description="Активен ли пользователь")
    source: Optional[str] = Field(None, description="Место откуда пришел пользователь")
    language: Optional[str] = Field(None, description="Язык на котором разговаривает пользователь")

# ---------- Модель создания ----------
class UserCreate(UserBase):
    """
    Используется при создании пользователя (например, при первом логине через Telegram)
    """
    pass


# ---------- Модель обновления ----------
class UserUpdate(BaseModel):
    """
    Используется для обновления данных пользователя
    """
    username: Optional[str] = Field(None, max_length=64)
    phone: Optional[str] = Field(None, max_length=15)
    email: Optional[EmailStr] = None
    birthday_date: Optional[date] = None
    is_active: Optional[bool] = None
    last_login_at: Optional[datetime] = None


# ---------- Модель возврата ----------
class UserReturn(UserBase):
    """
    Используется для возврата данных пользователю (в ответах API)
    """
    id: int
    registered_at: datetime
    last_login_at: Optional[datetime] = None

    # если нужно показать связанные сущности (например, списки платежей и подписок)
    subscriptions: Optional[List[SubscribeUserReturn]] = Field(default_factory=list, description="ID подписок пользователя")
    payments: Optional[List[int]] = Field(default_factory=list, description="ID платежей пользователя")

    class Config:
        from_attributes = True  # (Pydantic v2) аналог orm_mode=True
