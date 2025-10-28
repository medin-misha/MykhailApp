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


class SubscribeUserBase(BaseModel):
    """
    Базовая модель подписки пользователя.
    Используется как основа для создания и возврата данных.
    """

    subscription_id: int = Field(
        ..., description="Идентификатор подписки (Subscription.id)"
    )
    user_id: int = Field(..., description="Идентификатор пользователя (User.id)")
    source: str = Field(
        ..., description="Источник подписки, например 'tribute', 'telegram_stars'"
    )


class SubscribeUserCreate(SubscribeUserBase):
    """
    Входные данные при создании подписки пользователя.
    Используется в HTTP-запросе или AMQP-событии.
    """

    pass


class SubscribeUserReturn(SubscribeUserBase):
    """
    Возврат клиенту (HTTP-ответ, AMQP-payload).
    """

    id: int = Field(
        ..., description="ID записи подписки пользователя (UserSubscription.id)"
    )
    started_at: datetime = Field(..., description="Дата начала действия подписки")
    expires_at: datetime = Field(..., description="Дата окончания действия подписки")
    active: bool = Field(..., description="Флаг активности подписки")
