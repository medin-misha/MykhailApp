from faststream.rabbit.broker import RabbitBroker
from config import settings
from services.user.user_registered import register_new_user
from services.user.user_updated import update_user_by_chat_id

broker = RabbitBroker(url=settings.rabbit_url)


@broker.subscriber("user.registered")
async def register_new_user_handler(data: dict):
    await register_new_user(data=data)

@broker.subscriber("user.updated")
async def update_user_by_chat_id_handler(data: dict):
    await update_user_by_chat_id(data=data)