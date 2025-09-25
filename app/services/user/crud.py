from sqlalchemy import select, Result, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Any

from core.models import User
from contracts.user import CreateUser, ReturnUser, ChatId


class UserCrud:
    """
    Класс для CRUD операций с пользователем
    async def create : функция для создания пользователя. Принимиает в себя CreateUser, возвращает ReturnUser (новый пользователь)
        или строку 'This user os already exists' если юзер уже существует
    """

    @staticmethod
    async def get_user_by_chat_id(chat_id: int, session: AsyncSession) -> User | None:
        stmt = select(User).where(User.chat_id == chat_id)
        user: Result[User] = await session.execute(stmt)
        user: User | None = user.scalars().one_or_none()
        return user or None

    @staticmethod
    async def create(data: CreateUser, session: AsyncSession) -> ReturnUser | str:
        new_user = User(**data.model_dump())
        session.add(new_user)
        try:
            await session.commit()
        except IntegrityError as error:
            return "This user is already exists."
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def get_or_create(data: CreateUser, session: AsyncSession) -> ReturnUser:
        chat_id: ChatId = data.chat_id
        user = await UserCrud.get_user_by_chat_id(chat_id=chat_id, session=session)
        if user:
            return user
        return await UserCrud.create(data=data, session=session)

    @staticmethod
    async def update(
        chat_id: int, field: str, session: AsyncSession, new_value: Any
    ) -> ReturnUser:
        essence = await UserCrud.get_user_by_chat_id(chat_id=chat_id, session=session)
        print(essence.birthday_date)
        setattr(essence, field, new_value)
        await session.commit()
        await session.refresh(essence)
        print(essence.birthday_date)
        return essence
