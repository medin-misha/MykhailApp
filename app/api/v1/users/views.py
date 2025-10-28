from typing import Annotated

from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from services import CRUD
from core.models import User
from contracts.user import UserReturn, UserCreate, UserUpdate
from core.database import database

router = APIRouter(
    prefix="/users",
    tags=["Users (dev)"],
    include_in_schema=True,  # можно скрыть из Swagger, если нужно => False
)

SessionDep = Annotated[AsyncSession, Depends(database.get_session)]


@router.post(
    "/",
    response_model=UserReturn,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя (dev)",
    response_model_exclude_none=True,
)
async def create_user_view(
    data: UserCreate,
    session: SessionDep,
) -> UserReturn:
    """
    ⚙️ **Dev-only endpoint**

    Создаёт пользователя в базе данных.
    Используется при разработке или для ручных тестов.
    """
    user = await CRUD.create(data=data, model=User, session=session)
    return user


@router.get(
    "/",
    response_model=list[UserReturn],
    summary="Получить список всех пользователей (dev)",
    response_model_exclude_none=True,
)
async def get_users_list_view(session: SessionDep) -> list[UserReturn]:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает список всех пользователей в базе.
    Только для отладки и внутренних тестов.
    """
    return await CRUD.get(model=User, session=session)


@router.get(
    "/{id:int}",
    response_model=UserReturn,
    summary="Получить пользователя по ID (dev)",
    response_model_exclude_none=True,
)
async def get_user_by_id_view(
    id: Annotated[int, Path(description="Идентификатор пользователя")],
    session: SessionDep,
) -> UserReturn:
    """
    ⚙️ **Dev-only endpoint**

    Возвращает пользователя по его ID.
    Используется для отладки и проверки CRUD-операций.
    """
    return await CRUD.get(model=User, session=session, id=id)


@router.patch(
    "/{id:int}",
    response_model=UserReturn,
    summary="Изменить данные пользователя (dev)",
    response_model_exclude_none=True,
)
async def patch_user_view(
    id: Annotated[int, Path(description="Идентификатор пользователя")],
    new_data: UserUpdate,
    session: SessionDep,
) -> UserReturn:
    """
    ⚙️ **Dev-only endpoint**

    Частично обновляет данные пользователя.
    Применяется для тестирования PATCH-операций.
    """
    return await CRUD.patch(new_data=new_data, model=User, session=session, id=id)


@router.delete(
    "/{id:int}",
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="Удалить пользователя (dev)",
)
async def delete_user_view(
    id: Annotated[int, Path(description="Идентификатор пользователя")],
    session: SessionDep,
) -> str:
    """
    ⚙️ **Dev-only endpoint**

    Удаляет пользователя по ID.
    Используется при тестировании CRUD и миграций.
    """
    return await CRUD.delete(id=id, session=session, model=User)
