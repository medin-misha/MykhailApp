from typing import Optional

from .base import BaseMessage
from contracts.subscriptions import SubscribeUserCreateForm

class CreateSubscription(BaseMessage):
    """
    Класс создания подписки пользователя
    """
    data: Optional[SubscribeUserCreateForm]