from faststream.rabbit.broker import RabbitBroker
from config import settings
from services.user.user_registered import register_new_user

broker = RabbitBroker(url=settings.rabbit_url)


@broker.subscriber("user.registered")
async def register_new_user_handler(data: dict):
    await register_new_user(data=data)
