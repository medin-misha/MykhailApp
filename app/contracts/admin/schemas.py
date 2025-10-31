from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ---------- Enum ----------
class AdminRole(str, Enum):
    superadmin = "superadmin"
    manager = "manager"
    moderator = "moderator"


# ---------- Базовая модель ----------
class AdminBase(BaseModel):
    """
    Базовая модель администратора (используется для общих полей).
    """
    username: str = Field(..., max_length=64, description="Имя администратора")
    email: EmailStr = Field(..., description="Электронная почта администратора")
    role: AdminRole = Field(default=AdminRole.manager, description="Роль администратора")
    is_active: bool = Field(default=True, description="Активен ли администратор")


# ---------- Модель формы (ввод от пользователя) ----------
class AdminCreateForm(AdminBase):
    """
    Используется при создании администратора из формы или запроса API.
    Содержит пароль в открытом виде.
    """
    password: str = Field(..., min_length=6, description="Пароль администратора")


# ---------- Модель создания (в БД) ----------
class AdminCreate(AdminBase):
    """
    Используется при сохранении администратора в БД.
    Содержит уже хэшированный пароль.
    """
    hashed_password: str = Field(..., description="Хэшированный пароль администратора")



# ---------- Модель обновления ----------
class AdminUpdate(BaseModel):
    """
    Используется для обновления данных администратора.
    """
    username: Optional[str] = Field(None, max_length=64, description="Имя администратора")
    email: Optional[EmailStr] = Field(None, description="Электронная почта администратора")
    password: Optional[str] = Field(None, min_length=6, description="Пароль администратора")
    role: Optional[AdminRole] = Field(None, description="Роль администратора")
    is_active: Optional[bool] = Field(None, description="Активен ли администратор")
    last_login_at: Optional[datetime] = Field(None, description="Дата последнего входа администратора")


# ---------- Модель возврата ----------
class AdminReturn(AdminBase):
    """
    Используется для возврата данных администратора (в ответах API).
    """
    id: int = Field(..., description="Идентификатор администратора")
    created_at: datetime = Field(..., description="Дата создания администратора")
    last_login_at: Optional[datetime] = Field(None, description="Дата последнего входа администратора")

    class Config:
        from_attributes = True  # Pydantic v2 аналог orm_mode=True
