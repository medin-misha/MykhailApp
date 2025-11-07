from typing import Optional
from .base import BaseMessage
from contracts.user import UserCreate, UserUpdateAMQP

class UserRegistered(BaseMessage):
    """
    Модель формы создания юзера
    """
    data: Optional[UserCreate]

class UserUpdated(BaseMessage):
    """
    Модель формы обновления пользователя
    """
    data: Optional[UserUpdateAMQP]