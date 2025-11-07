from contracts.amqp.payment import ReceivedPayment
from core.database import database
from services.user.crud import get_user_by_chat_id
from contracts.payments import PaymentCreate
from services.amqp_error_handler import AMQPErrorHandler
from services.crud import CRUD
from core.models import Payment

async def create_payment(data: dict):
    try:
        message = ReceivedPayment(**data)
        async with database.session_maker() as session:
            user = await get_user_by_chat_id(chat_id=message.data.chat_id, session=session)
            payment_data = PaymentCreate(**message.data.model_dump(exclude={"chat_id"}), user_id=user.id)
            await CRUD.create(data=payment_data, model=Payment, session=session)
    except Exception as err:
        AMQPErrorHandler.handle(err=err)