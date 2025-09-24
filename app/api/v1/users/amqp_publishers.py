from faststream.rabbit.fastapi import RabbitRouter
from config import settings

router = RabbitRouter(url=settings.rabbit_url)


@router.get(
    "/auth-user",
    summary="Отправка данных пользователя в очередь авторизации",
    description=(
        "Эндпоинт получает `chat_id` и `username` пользователя, формирует сообщение "
        "и отправляет его в очередь RabbitMQ `auth_user`. "
        "Очередь используется исключительно для создания новых пользователей."
    ),
    response_description="Подтверждение успешной отправки сообщения в очередь.",
)
async def auth_user_handler(chat_id: int, username: str):
    string = f'{{"chat_id": {chat_id}, "username": "{username}"}}'
    await router.broker.publish(
        message=string,
        queue="auth_user",
    )
    return {"sended": "True"}