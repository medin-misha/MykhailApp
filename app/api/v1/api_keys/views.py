from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import CRUD
from core.models import APIKey
from contracts.api_keys import APIKeyReturn, APIKeyUpdate, APIKeyCreate
from core.database import database

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys (dev)"],
    include_in_schema=True,  # можно скрыть при деплое
)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post(
    "/",
    response_model=APIKeyReturn,
    status_code=status.HTTP_201_CREATED,
    summary="Создать API-ключ (dev)",
    response_model_exclude_none=True,
)
async def create_api_key_view(
    data: APIKeyCreate,
    session: SessionDep,
) -> APIKeyReturn:
    """
    ⚙️ **Dev-only endpoint**

    Создаёт новый API-ключ в базе данных.
    Используется при добавлении новых сервисов или модулей,
    которые будут обращаться к Auth через защищённый доступ.
    """
    return await CRUD.create(data=data, model=APIKey, session=session)


@router.get(
    "/",
    response_model=list[APIKeyReturn],
    summary="Получить список всех API-ключей (dev)",
    response_model_exclude_none=True,
)
async def get_api_keys_list_view(session: SessionDep) -> list[APIKeyReturn]:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает список всех существующих API-ключей.
    Удобно для ручной проверки активных ключей и их связей с сервисами.
    """
    return await CRUD.get(model=APIKey, session=session)


@router.get(
    "/{id:int}",
    response_model=APIKeyReturn,
    summary="Получить API-ключ по ID (dev)",
    response_model_exclude_none=True,
)
async def get_api_key_by_id_view(
    id: Annotated[int, Path(description="Идентификатор API-ключа")],
    session: SessionDep,
) -> APIKeyReturn:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает данные API-ключа по указанному ID.
    Применяется при отладке или ручной проверке привязки ключей.
    """
    return await CRUD.get(model=APIKey, session=session, id=id)


@router.patch(
    "/{id:int}",
    response_model=APIKeyReturn,
    summary="Изменить данные API-ключа (dev)",
    response_model_exclude_none=True,
)
async def patch_api_key_view(
    id: Annotated[int, Path(description="Идентификатор API-ключа")],
    new_data: APIKeyUpdate,
    session: SessionDep,
) -> APIKeyReturn:
    """
    ⚙️ **Dev-only endpoint**

    Частично обновляет данные API-ключа —
    например, описание, срок действия или статус активности.
    Используется при управлении правами доступа.
    """
    return await CRUD.patch(new_data=new_data, model=APIKey, session=session, id=id)


@router.delete(
    "/{id:int}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Удалить API-ключ (dev)",
)
async def delete_api_key_view(
    id: Annotated[int, Path(description="Идентификатор API-ключа")],
    session: SessionDep,
) -> str:
    """
    ⚙️ **Dev-only endpoint**

    Удаляет API-ключ по его ID.
    Применяется при тестировании или отзыве неиспользуемых ключей.
    """
    return await CRUD.delete(id=id, session=session, model=APIKey)
