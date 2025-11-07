from faststream.rabbit.broker import RabbitBroker
from faststream.rabbit import RabbitMessage
from config import settings
from services.payment.create_payment import create_payment
from amqp.queues import PAYMENT_RECEIVED

broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber(PAYMENT_RECEIVED, no_ack=True)
async def create_subscribe_handler(message: RabbitMessage):
    await create_payment(msg=message)