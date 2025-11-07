from faststream.rabbit.broker import RabbitBroker
from faststream.rabbit import RabbitMessage
from config import settings
from services.subscription.create_subscribe import create_subscribe
from ..queues import SUBSCRIPTON_CREATED

broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber(SUBSCRIPTON_CREATED, no_ack=True)
async def create_subscribe_handler(message: RabbitMessage):
    await create_subscribe(msg=message)