from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException, status
from core.models import Subscription, UserSubscription, User
from contracts.subscriptions import (
    SubscribeUserCreate,
    SubscribeUserReturn,
    SubscribeUserCreateForm,
)
from services import CRUD
from services.user.crud import get_user_by_chat_id


async def subscribe(
    data: SubscribeUserCreateForm,
    session: AsyncSession,
) -> SubscribeUserReturn:
    """
    💡 Создаёт запись подписки пользователя на конкретный тариф.

    Логика:
    1. Проверяет существование пользователя (по chat_id) и подписки (по id).
    2. Вычисляет дату окончания подписки, если у тарифа задан срок (term_days > 0).
    3. Создаёт новую запись `UserSubscription`, активируя её.
    4. Возвращает данные о подписке в формате Pydantic-схемы `SubscribeUserReturn`.

    Исключения:
    - 404 Not Found — если пользователь или подписка не найдены (обрабатывается вспомогательными функциями).
    - 400 Bad Request — если пользователь уже имеет активную подписку на тот же тариф.
    """

    # 1. Получаем пользователя и подписку (функции сами бросят 404, если не найдут)
    user: User = await get_user_by_chat_id(chat_id=data.chat_id, session=session)
    subscription: Subscription = await CRUD.get(
        model=Subscription, id=data.subscription_id, session=session
    )

    # 2. Проверяем — нет ли уже активной подписки на этот тариф
    existing_sub = await session.scalar(
        select(UserSubscription)
        .where(UserSubscription.user_id == user.id)
        .where(UserSubscription.subscription_id == subscription.id)
        .where(UserSubscription.active.is_(True))
    )
    if existing_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has an active subscription to this plan.",
        )

    # 3. Вычисляем дату истечения, если есть срок
    expires_at = (
        datetime.now(tz=timezone.utc) + timedelta(days=subscription.term_days)
        if subscription.term_days > 0
        else None
    )

    # 4. Создаём объект для ORM
    created_form = SubscribeUserCreate(
        user_id=user.id,
        subscription_id=subscription.id,
        expires_at=expires_at,
        source=data.source,
        active=True,
    )
    user_subscription = UserSubscription(**created_form.model_dump())

    # 5. Сохраняем и возвращаем
    session.add(user_subscription)
    await session.commit()
    await session.refresh(user_subscription)

    return SubscribeUserReturn.model_validate(user_subscription)


async def check_user_subscribe(
    chat_id: int,
    subscription_id: int,
    session: AsyncSession,
) -> bool:
    """
    💡 Проверяет, есть ли у пользователя активная подписка на указанный тариф.

    Возвращает:
        True — если активная подписка найдена
        False — если активной подписки нет
    """
    user = await get_user_by_chat_id(chat_id=chat_id, session=session)
    subscription = await CRUD.get(
        model=Subscription, id=subscription_id, session=session
    )

    stmt = (
        select(UserSubscription)
        .where(UserSubscription.user_id == user.id)
        .where(UserSubscription.subscription_id == subscription.id)
        .where(UserSubscription.active.is_(True))
    )

    result: Result = await session.execute(stmt)
    existing_sub = result.scalar_one_or_none()
    return existing_sub is not None
