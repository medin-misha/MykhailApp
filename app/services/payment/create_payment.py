from faststream.rabbit import RabbitMessage
from contracts.amqp.payment import ReceivedPayment
from core.database import database
from services.API_keys.crud import check_valid_api_key
from services.user.crud import get_user_by_chat_id
from contracts.payments import PaymentCreate
from services.amqp_error_handler import AMQPErrorHandler
from services.crud import CRUD
from core.models import Payment

async def create_payment(msg: RabbitMessage):
    try:
        message = ReceivedPayment(**msg.decoded_body)
        async with database.session_maker() as session:
            await check_valid_api_key(
                key=message.meta.api_key, service_id=message.meta.service_id,
                session=session, raise_exception=True
            )
            user = await get_user_by_chat_id(chat_id=message.data.chat_id, session=session)
            payment_data = PaymentCreate(**message.data.model_dump(exclude={"chat_id"}), user_id=user.id)
            await CRUD.create(data=payment_data, model=Payment, session=session)
            await msg.ack()
    except Exception as err:
        await msg.nack(requeue=False)
        AMQPErrorHandler.handle(err=err)