from faststream.rabbit.broker import RabbitBroker
from config import settings
from services.subscription.create_subscribe import create_subscribe


broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber("subscription.created")
async def create_subscribe_handler(data: dict):
    await create_subscribe(data=data)