from typing import Optional
from .base import BaseMessage
from contracts.user import UserCreate

class UserRegistered(BaseMessage):
    """
    Модель формы создания юзера
    """
    data: Optional[UserCreate]