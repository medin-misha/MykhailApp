from faststream.rabbit.broker import RabbitBroker
from pydantic import ValidationError
from config import settings
from core.database import database
from contracts.user import ReturnUser, CreateUser, BirthdayModel
from services.user import UserCrud
from .utils import str_in_dict_or_error_log, str_in_date

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
async def order_queue_handler(data: str):  # data: CreateUser
    try:
        payload = str_in_dict_or_error_log(data=data)
        user = CreateUser(**payload)
    except ValidationError as e:
        print(f"Ошибка валидации данных: {e}")
        return
    async with database.session_maker() as session:
        await UserCrud.get_or_create(data=user, session=session)


@broker.subscriber(
    "user_birthday",
    description=(
        "Хендлер подписан на очередь `auth_birthday`. "
        "Принимает данные пользователя в формате JSON (строка), "
        "конвертирует их в dict и валидирует через модель `BirthdayModel`. "
        "После успешной валидации обновляет дату рождения пользователя "
        "в базе данных с помощью метода `UserCrud.update`."
    ),
)
async def set_user_birthday_handler(data: str):  # data: BrithdayModel
    try:
        payload = str_in_dict_or_error_log(data=data)
        birthday_data = BirthdayModel(**payload)
    except ValidationError as e:
        print(f"Ошибка валидации данных: {e}")
        return
    async with database.session_maker() as session:
        await UserCrud.update(
            chat_id=birthday_data.chat_id,
            field="birthday_date",
            session=session,
            new_value=str_in_date(birthday_data.birthday),
        )
