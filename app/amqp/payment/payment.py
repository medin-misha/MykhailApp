from faststream.rabbit.broker import RabbitBroker
from config import settings
from services.payment.create_payment import create_payment


broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber("payment.received")
async def create_subscribe_handler(data: dict):
    await create_payment(data=data)