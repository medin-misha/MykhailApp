from faststream.rabbit import RabbitMessage
from services.amqp_error_handler import AMQPErrorHandler
from core.database import database
from contracts.amqp.user import UserRegistered
from contracts.user import UserCreateForm
from services.API_keys.crud import check_valid_api_key
from services.user.crud import create_new_user

async def register_new_user(msg: RabbitMessage) -> None:
    """
    Регистрация нового пользователя через AMQP
    """
    try:
        message = UserRegistered(**msg.decoded_body)
        async with database.session_maker() as session:
            await check_valid_api_key(
                key=message.meta.api_key, service_id=message.meta.service_id,
                session=session, raise_exception=True
            )
            is_valid_key: bool = await check_valid_api_key(
                key=message.meta.api_key,
                service_id=message.meta.service_id,
                session=session,
            )
            if not is_valid_key:
                return
            form = UserCreateForm(
                **message.data.model_dump(),
                service_id=message.meta.service_id,
            )
            await create_new_user(form=form, session=session)
            await msg.ack()
    except Exception as err:
        await msg.nack(requeue=False)
        AMQPErrorHandler.handle(err=err)
