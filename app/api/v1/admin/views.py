from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import CRUD, create_admin
from core.models import Admin
from contracts.admin import AdminReturn, AdminUpdate, AdminCreateForm
from core.database import database

router = APIRouter(
    prefix="/admins",
    tags=["Admins (dev)"],
    include_in_schema=True,  # можно скрыть из Swagger при деплое
)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post(
    "/",
    response_model=AdminReturn,
    status_code=status.HTTP_201_CREATED,
    summary="Создать администратора (dev)",
    response_model_exclude_none=True,
)
async def create_admin_view(
    data: AdminCreateForm,
    session: SessionDep,
) -> AdminReturn:
    """
    ⚙️ **Dev-only endpoint**

    Создаёт нового администратора в базе данных.
    Используется при первичной настройке панели управления.
    """
    admin = await create_admin(form=data, session=session)
    return admin


@router.get(
    "/",
    response_model=list[AdminReturn],
    summary="Получить список всех администраторов (dev)",
    response_model_exclude_none=True,
)
async def get_admins_list_view(session: SessionDep) -> list[AdminReturn]:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает список всех администраторов из базы данных.
    Удобно для просмотра зарегистрированных аккаунтов панели управления.
    """
    return await CRUD.get(model=Admin, session=session)


@router.get(
    "/{id:int}",
    response_model=AdminReturn,
    summary="Получить администратора по ID (dev)",
    response_model_exclude_none=True,
)
async def get_admin_by_id_view(
    id: Annotated[int, Path(description="Идентификатор администратора")],
    session: SessionDep,
) -> AdminReturn:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает данные администратора по указанному ID.
    Применяется при ручной проверке записи.
    """
    return await CRUD.get(model=Admin, session=session, id=id)


@router.patch(
    "/{id:int}",
    response_model=AdminReturn,
    summary="Изменить данные администратора (dev)",
    response_model_exclude_none=True,
)
async def patch_admin_view(
    id: Annotated[int, Path(description="Идентификатор администратора")],
    new_data: AdminUpdate,
    session: SessionDep,
) -> AdminReturn:
    """
    ⚙️ **Dev-only endpoint**

    Частично обновляет данные администратора — например, email, роль или статус.
    Может использоваться при изменении прав доступа.
    """
    return await CRUD.patch(new_data=new_data, model=Admin, session=session, id=id)


@router.delete(
    "/{id:int}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Удалить администратора (dev)",
)
async def delete_admin_view(
    id: Annotated[int, Path(description="Идентификатор администратора")],
    session: SessionDep,
) -> str:
    """
    ⚙️ **Dev-only endpoint**

    Удаляет администратора по его ID.
    Применяется при тестировании или чистке базы данных.
    """
    return await CRUD.delete(id=id, session=session, model=Admin)
