from contracts.amqp.subscriptions import CreateSubscription
from services.API_keys.crud import check_valid_api_key
from services.subscription.subscribe_user import subscribe
from faststream.rabbit import RabbitMessage
from core.database import database
from services.amqp_error_handler import AMQPErrorHandler

async def create_subscribe(msg: RabbitMessage):
    try:
        message = CreateSubscription(**msg.decoded_body)
        async with database.session_maker() as session:
            await check_valid_api_key(
                key=message.meta.api_key, service_id=message.meta.service_id,
                session=session, raise_exception=True
            )
            await subscribe(data=message.data, session=session)
            await msg.ack()
    except Exception as err:
        await msg.nack(requeue=False)
        AMQPErrorHandler.handle(err=err)