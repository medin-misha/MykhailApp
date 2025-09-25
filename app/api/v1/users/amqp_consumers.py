from faststream.rabbit.broker import RabbitBroker
from pydantic import ValidationError
from config import settings
from core.database import database
from contracts.user import ReturnUser, CreateUser
from services.user import UserCrud
from .utils import str_in_dict_or_error_log

broker = RabbitBroker(url=settings.rabbit_url)

@broker.subscriber(
    "auth_user",
    description=(
        "Хендлер подписан на очередь `auth_user`. "
        "Принимает данные пользователя в формате JSON (строка), "
        "конвертирует их в dict и валидирует через модель `CreateUser`. "
        "Далее создаёт нового пользователя или возвращает существующего "
        "с помощью `UserCrud.get_or_create`."
    ),
)
async def order_queue_handler(data: str): # data: CreateUser
    try:
        payload = str_in_dict_or_error_log(data=data)
        user = CreateUser(**payload)
    except ValidationError as e:
        print(f"Ошибка валидации данных: {e}")
        return
    async with database.session_maker() as session:
        await UserCrud.get_or_create(data=user, session=session)
