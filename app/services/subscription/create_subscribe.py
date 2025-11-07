from contracts.amqp.subscriptions import CreateSubscription
from services.subscription.subscribe_user import subscribe
from core.database import database
from services.amqp_error_handler import AMQPErrorHandler

async def create_subscribe(data: dict):
    try:
        message = CreateSubscription(**data)
        async with database.session_maker() as session:
            await subscribe(data=message.data, session=session)
    except Exception as err:
        AMQPErrorHandler.handle(err=err)