from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import CRUD
from core.models import Service
from contracts.services import ServiceCreate, ServiceUpdate, ServiceReturn
from core.database import database

router = APIRouter(
    prefix="/services",
    tags=["Services (dev)"],
    include_in_schema=True,  # можно скрыть при деплое
)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post(
    "/",
    response_model=ServiceReturn,
    status_code=status.HTTP_201_CREATED,
    summary="Создать сервис (dev)",
    response_model_exclude_none=True,
)
async def create_service_view(
    data: ServiceCreate,
    session: SessionDep,
) -> ServiceReturn:
    """
    ⚙️ **Dev-only endpoint**

    Создаёт новый сервис в базе данных.
    Используется при добавлении внутренних или внешних систем, взаимодействующих с Auth.
    """
    return await CRUD.create(data=data, model=Service, session=session)


@router.get(
    "/",
    response_model=list[ServiceReturn],
    summary="Получить список всех сервисов (dev)",
    response_model_exclude_none=True,
)
async def get_services_list_view(session: SessionDep) -> list[ServiceReturn]:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает список всех зарегистрированных сервисов.
    Удобно для мониторинга и отладки интеграций.
    """
    return await CRUD.get(model=Service, session=session)


@router.get(
    "/{id:int}",
    response_model=ServiceReturn,
    summary="Получить сервис по ID (dev)",
    response_model_exclude_none=True,
)
async def get_service_by_id_view(
    id: Annotated[int, Path(description="Идентификатор сервиса")],
    session: SessionDep,
) -> ServiceReturn:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает данные сервиса по указанному ID.
    Применяется при ручной проверке конкретной записи.
    """
    return await CRUD.get(model=Service, session=session, id=id)


@router.patch(
    "/{id:int}",
    response_model=ServiceReturn,
    summary="Изменить данные сервиса (dev)",
    response_model_exclude_none=True,
)
async def patch_service_view(
    id: Annotated[int, Path(description="Идентификатор сервиса")],
    new_data: ServiceUpdate,
    session: SessionDep,
) -> ServiceReturn:
    """
    ⚙️ **Dev-only endpoint**

    Частично обновляет данные сервиса — например, описание или владельца.
    Может использоваться при изменении структуры интеграций.
    """
    return await CRUD.patch(new_data=new_data, model=Service, session=session, id=id)


@router.delete(
    "/{id:int}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Удалить сервис (dev)",
)
async def delete_service_view(
    id: Annotated[int, Path(description="Идентификатор сервиса")],
    session: SessionDep,
) -> str:
    """
    ⚙️ **Dev-only endpoint**

    Удаляет сервис по его ID.
    Применяется при тестировании или удалении устаревших интеграций.
    """
    return await CRUD.delete(id=id, session=session, model=Service)
