from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User
from services.crud import CRUD
from core.database import database
from contracts.amqp.user import UserUpdated
from services.amqp_error_handler import AMQPErrorHandler
from services.user.crud import get_user_by_chat_id
import logging

logger = logging.getLogger(__name__)

async def update_user_by_chat_id(data:dict):
    try:
        message = UserUpdated(**data)
        async with database.session_maker() as session:
            user = await get_user_by_chat_id(chat_id=message.data.chat_id, session=session)
            await CRUD.patch(new_data=message.data, id=user.id, session=session, model=User)
    except Exception as err:
        AMQPErrorHandler.handle(err=err)