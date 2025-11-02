from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, condecimal, conint


class SubscriptionBase(BaseModel):
    """
    Общие поля для всех операций (чтобы не дублировать типы).
    """

    name: str = Field(
        ..., max_length=128, description="Уникальное имя тарифа, например 'pro_month'"
    )
    description: Optional[str] = Field(None, description="Описание тарифа / плана")
    term_days: int = Field(
        ..., ge=0, description="Срок подписки в днях (0 = бессрочно)"
    )
    price: condecimal(max_digits=10, decimal_places=2) = Field(
        0, description="Цена тарифа"
    )
    sale_percent: conint(ge=0, le=100) = Field(0, description="Скидка, %")
    is_trial_available: bool = Field(
        False, description="Есть ли бесплатный пробный период"
    )


# --- схемы запросов / ответов ---


class SubscriptionCreate(SubscriptionBase):
    """
    Используется при создании нового тарифа.
    """

    pass


class SubscriptionUpdate(BaseModel):
    """
    Частичное обновление полей тарифа.
    Все поля опциональные — патч.
    """

    name: Optional[str] = Field(None, max_length=128)
    description: Optional[str] = None
    term_days: Optional[int] = Field(None, ge=0)
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    sale_percent: Optional[conint(ge=0, le=100)] = None
    is_trial_available: Optional[bool] = None


class SubscriptionReturn(SubscriptionBase):
    """
    Возврат клиенту (HTTP-ответ, AMQP-payload).
    """

    id: int = Field(..., description="Идентификатор тарифа")

    model_config = {
        "from_attributes": True  # позволяет создавать схему из ORM-объекта
    }


# SubscribeUserCreate, SubscribeUserReturn, SubscribeUserCreateForm

class SubscribeUserBase(BaseModel):
    """
    Базовая модель оформления подписки
    """
    subscription_id: int = Field(..., description="Subscription.id подписки")
    source: Optional[str] = Field(None, description="Откуда подписался человек")

class SubscribeUserCreateForm(SubscribeUserBase):
    """
    Форма оформления подписки на пользователя
    """
    chat_id: int = Field(..., description="User.id пользователя")
    subscription_id: int = Field(..., description="Subscription.id подписки")
    source: Optional[str] = Field(None, description="Откуда подписался человек")

class SubscribeUserCreate(SubscribeUserBase):
    """
    Модель оформления подписки. Идентична модели
    """
    user_id: int = Field(..., description="User.id пользователя")
    expires_at: Optional[datetime] = Field(None, description="Дата и время когда подписка исчезает")
    active: Optional[bool]

class SubscribeUserReturn(BaseModel):
    """
    Модель возвращения оформленной подписки
    """
    id: int = Field(..., description="Айди подписки ")
    user_id: int = Field(..., description="User.id пользователя")
    expires_at: Optional[datetime] = Field(None, description="Дата и время когда подписка исчезает")
    active: Optional[bool]

    model_config = {
        "from_attributes": True  # позволяет создавать схему из ORM-объекта
    }