from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import CRUD
from core.models import Subscription
from contracts.subscriptions import (
    SubscriptionCreate,
    SubscriptionReturn,
    SubscriptionUpdate,
)
from core.database import database

router = APIRouter(
    prefix="/subscriptions",
    tags=["Subscriptions (dev)"],
    include_in_schema=True,  # можно скрыть в Swagger при деплое
)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post(
    "/",
    response_model=SubscriptionReturn,
    status_code=status.HTTP_201_CREATED,
    summary="Создать подписку (dev)",
    response_model_exclude_none=True,
)
async def create_subscription_view(
    data: SubscriptionCreate,
    session: SessionDep,
) -> SubscriptionReturn:
    """
    ⚙️ **Dev-only endpoint**

    Создаёт новую подписку в базе данных.
    Используется для ручного добавления тарифов (например, `pro_month`, `free`).
    """
    subscription = await CRUD.create(data=data, model=Subscription, session=session)
    return subscription


@router.get(
    "/",
    response_model=list[SubscriptionReturn],
    summary="Получить список всех подписок (dev)",
    response_model_exclude_none=True,
)
async def get_subscriptions_list_view(session: SessionDep) -> list[SubscriptionReturn]:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает список всех подписок из базы.
    Применяется для проверки содержимого и отладки тарифов.
    """
    return await CRUD.get(model=Subscription, session=session)


@router.get(
    "/{id:int}",
    response_model=SubscriptionReturn,
    summary="Получить подписку по ID (dev)",
    response_model_exclude_none=True,
)
async def get_subscription_by_id_view(
    id: Annotated[int, Path(description="Идентификатор подписки")],
    session: SessionDep,
) -> SubscriptionReturn:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает одну подписку по её ID.
    """
    return await CRUD.get(model=Subscription, session=session, id=id)


@router.patch(
    "/{id:int}",
    response_model=SubscriptionReturn,
    summary="Изменить данные подписки (dev)",
    response_model_exclude_none=True,
)
async def patch_subscription_view(
    id: Annotated[int, Path(description="Идентификатор подписки")],
    new_data: SubscriptionUpdate,
    session: SessionDep,
) -> SubscriptionReturn:
    """
    ⚙️ **Dev-only endpoint**

    Частично обновляет данные подписки — например, описание, цену или срок действия.
    """
    return await CRUD.patch(
        new_data=new_data, model=Subscription, session=session, id=id
    )


@router.delete(
    "/{id:int}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Удалить подписку (dev)",
)
async def delete_subscription_view(
    id: Annotated[int, Path(description="Идентификатор подписки")],
    session: SessionDep,
) -> str:
    """
    ⚙️ **Dev-only endpoint**

    Удаляет подписку по её ID.
    Удобно при тестировании миграций и CRUD-операций.
    """
    return await CRUD.delete(id=id, session=session, model=Subscription)


@router.post("/subscribe")
async def subscribe_user_view()