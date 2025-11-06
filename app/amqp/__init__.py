__all__ = "main_broker"

from faststream.rabbit.broker import RabbitBroker
from config import settings
from .users.subscribers import broker as user_broker

main_broker = RabbitBroker(url=settings.rabbit_url)
main_broker.include_router(user_broker)
