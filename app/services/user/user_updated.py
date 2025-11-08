from faststream.rabbit import RabbitMessage
from core.models import User
from services.crud import CRUD
from core.database import database
from contracts.amqp.user import UserUpdated
from services.amqp_error_handler import AMQPErrorHandler
from services.user.crud import get_user_by_chat_id
from services.API_keys.crud import check_valid_api_key

async def update_user_by_chat_id(msg: RabbitMessage):
    try:
        message = UserUpdated(**msg.decoded_body)
        async with database.session_maker() as session:
            await check_valid_api_key(
                key=message.meta.api_key, service_id=message.meta.service_id,
                session=session, raise_exception=True
            )
            user = await get_user_by_chat_id(chat_id=message.data.chat_id, session=session)
            await CRUD.patch(new_data=message.data, id=user.id, session=session, model=User)
            await msg.ack()
    except Exception as err:
        await msg.nack(requeue=False)
        AMQPErrorHandler.handle(err=err)