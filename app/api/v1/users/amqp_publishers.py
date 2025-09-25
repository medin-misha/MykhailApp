from faststream.rabbit.fastapi import RabbitRouter
import json
from config import settings
from contracts.user import BirthdayModel

router = RabbitRouter(url=settings.rabbit_url)


@router.get(
    "/auth",
    summary="(Служебный) Отправка данных пользователя в очередь авторизации",
    description=(
        "Служебный эндпоинт. Получает `chat_id` и `username` пользователя, формирует сообщение "
        "и отправляет его в очередь RabbitMQ `auth_user`. "
        "Очередь используется исключительно для создания новых пользователей "
        "и не предназначена для внешнего использования."
    ),
    response_description="Подтверждение успешной отправки сообщения в очередь.",
)
async def auth_user_handler_publisher(chat_id: int, username: str) -> dict:
    dict_data: dict = {"chat_id": chat_id, "username": username}
    string = json.dumps(dict_data)
    await router.broker.publish(
        message=string,
        queue="auth_user",
    )
    return {"sended": "True"}

@router.patch(
    "/auth/birthday",
    summary="(Служебный) Установка даты рождения пользователя",
    description=(
        "Служебный эндпоинт. Получает `chat_id` и дату рождения пользователя `birthday`, "
        "после чего формирует сообщение и отправляет его в очередь RabbitMQ `user_birthday`. "
        "Очередь используется для сохранения или обновления даты рождения пользователя "
        "и не предназначена для внешнего использования."
    ),
    response_description="Подтверждение успешной отправки сообщения в очередь.",
)
async def set_user_birthday_publisher(birthday: BirthdayModel) -> dict:
    dict_data = {"chat_id": birthday.chat_id, "birthday": birthday.birthday}
    string = json.dumps(dict_data)
    await router.broker.publish(
        message=string,
        queue="user_birthday"
    )
    return {"sended": "True"}