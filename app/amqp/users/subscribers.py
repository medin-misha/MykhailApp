from faststream.rabbit.broker import RabbitBroker
from config import settings
from services.user.user_registered import register_new_user
from services.user.user_updated import update_user_by_chat_id
from faststream.rabbit import RabbitMessage
from ..queues import USER_REGISTERED, USER_UPDATED

broker = RabbitBroker(url=settings.rabbit_url)


@broker.subscriber(USER_REGISTERED, no_ack=True)
async def register_new_user_handler(message: RabbitMessage):
    await register_new_user(msg=message)

@broker.subscriber(USER_UPDATED, no_ack=True)
async def update_user_by_chat_id_handler(message: RabbitMessage):
    await update_user_by_chat_id(msg=message)