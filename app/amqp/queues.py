from faststream.rabbit import RabbitBroker, RabbitQueue, RabbitExchange, ExchangeType
from faststream.rabbit import RabbitMessage
from config import settings

broker = RabbitBroker(url=settings.rabbit_url)

# --------- DLX и DLQ ----------
DLX = RabbitExchange(
    "dlx.global",
    type=ExchangeType.DIRECT,
    durable=True
)

DLQ = RabbitQueue(
    "dead.letters",
    durable=True,
    routing_key="dead"
)

DL_ARGS = {
    "x-dead-letter-exchange": "dlx.global",
    "x-dead-letter-routing-key": "dead"
}

# --------- Рабочие очереди ----------
USER_REGISTERED = RabbitQueue("user.registered", durable=True, arguments=DL_ARGS)
USER_UPDATED = RabbitQueue("user.updated", durable=True, arguments=DL_ARGS)
SUBSCRIPTON_CREATED = RabbitQueue("subscription.created", durable=True, arguments=DL_ARGS)
PAYMENT_RECEIVED = RabbitQueue("payment.received", durable=True, arguments=DL_ARGS)

# --------- DLQ-обработчик ----------
@broker.subscriber(
    DLQ,
    exchange=DLX,
    no_ack=True           # DLQ никогда не обрабатываем повторно
)
async def dlq_observer(message: RabbitMessage):
    # тут удобно логировать/сохранять в БД/отправлять алерты
    print("Message moved to DLQ:", message.body)
    await message.ack()
