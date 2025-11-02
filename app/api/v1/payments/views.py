from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import CRUD
from core.models import Payment
from contracts.payments import PaymentCreate, PaymentUpdate, PaymentReturn
from core.database import database

router = APIRouter(
    prefix="/payments",
    tags=["Payments (dev)"],
    include_in_schema=True,  # можно скрыть при деплое
)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post(
    "/",
    response_model=PaymentReturn,
    status_code=status.HTTP_201_CREATED,
    summary="Создать платёж (dev)",
    response_model_exclude_none=True,
)
async def create_payment_view(
    data: PaymentCreate,
    session: SessionDep,
) -> PaymentReturn:
    """
    ⚙️ **Dev-only endpoint**

    Создаёт новый платёж в базе данных.
    Используется для ручного добавления тестовых или служебных транзакций
    между пользователями, сервисами или заказами.
    """
    return await CRUD.create(data=data, model=Payment, session=session)


@router.get(
    "/",
    response_model=list[PaymentReturn],
    summary="Получить список всех платежей (dev)",
    response_model_exclude_none=True,
)
async def get_payments_list_view(session: SessionDep) -> list[PaymentReturn]:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает список всех зарегистрированных платежей.
    Полезно для тестирования финансовых транзакций и их связей с заказами.
    """
    return await CRUD.get(model=Payment, session=session)


@router.get(
    "/{id:int}",
    response_model=PaymentReturn,
    summary="Получить платёж по ID (dev)",
    response_model_exclude_none=True,
)
async def get_payment_by_id_view(
    id: Annotated[int, Path(description="Идентификатор платежа")],
    session: SessionDep,
) -> PaymentReturn:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает данные платежа по его ID.
    Применяется при ручной проверке статуса или структуры транзакции.
    """
    return await CRUD.get(model=Payment, session=session, id=id)


@router.patch(
    "/{id:int}",
    response_model=PaymentReturn,
    summary="Изменить данные платежа (dev)",
    response_model_exclude_none=True,
)
async def patch_payment_view(
    id: Annotated[int, Path(description="Идентификатор платежа")],
    new_data: PaymentUpdate,
    session: SessionDep,
) -> PaymentReturn:
    """
    ⚙️ **Dev-only endpoint**

    Частично обновляет данные платежа —
    например, статус, описание, или идентификаторы связанных сущностей.
    Удобно для ручной корректировки во время тестирования.
    """
    return await CRUD.patch(new_data=new_data, model=Payment, session=session, id=id)


@router.delete(
    "/{id:int}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Удалить платёж (dev)",
)
async def delete_payment_view(
    id: Annotated[int, Path(description="Идентификатор платежа")],
    session: SessionDep,
) -> str:
    """
    ⚙️ **Dev-only endpoint**

    Удаляет платёж по его ID.
    Применяется при тестировании или очистке базы от старых записей.
    """
    return await CRUD.delete(id=id, session=session, model=Payment)
