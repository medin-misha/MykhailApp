from typing import Optional
from .base import BaseMessage
from contracts.payments import PaymentCreateAMQP

class ReceivedPayment(BaseMessage):
    """
    Модель получения платежа
    """
    data: Optional[PaymentCreateAMQP]