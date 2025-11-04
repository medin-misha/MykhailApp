from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException, status
from contracts.user import UserCreateForm, UserCreate
from core.models import User, UserService, Service
from services.crud import CRUD
from services.error_handlers import DBErrorHandler


async def get_user_by_chat_id(chat_id: int, session: AsyncSession) -> User:
    stmt = select(User).where(User.chat_id == chat_id)
    result: Result = await session.execute(stmt)
    user: User | None = result.one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user[0]


async def create_new_user(form: UserCreateForm, session: AsyncSession) -> User:
    """
    Создаёт нового пользователя и привязывает его к сервису (UserService).
    Используется транзакция, чтобы избежать несогласованных данных.
    """
    data = form.model_dump(exclude_none=True).copy()
    service: Service = await CRUD.get(
        model=Service, id=form.service_id, session=session
    )
    user_fields = list(UserCreate.model_fields.keys())

    for key in data.copy().keys():
        if not key in user_fields:
            data.pop(key)
        pass
    user_data = UserCreate(**data)
    new_user = User(**user_data.model_dump())

    try:
        session.add(new_user)
        await session.flush()  # Получаем ID без коммита
        session.add(UserService(user_id=new_user.id, service_id=service.id))

        await session.commit()
        await session.refresh(new_user)

    except Exception as err:
        DBErrorHandler.handle(err=err, model=User)
    else:
        return new_user
