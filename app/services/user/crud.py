from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.util import await_only

from core.models import User
from contracts.user import CreateUser, ReturnUser, ChatId


class UserCrud:
    """
    Класс для CRUD операций с пользователем
    async def create : функция для создания пользователя. Принимиает в себя CreateUser, возвращает ReturnUser (новый пользователь)
        или строку 'This user os already exists' если юзер уже существует
    """
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
        stmt = select(User).where(User.chat_id == chat_id)
        user: Result[User] = await session.execute(stmt)
        user: User | None = user.scalars().one_or_none()
        if user:
            return user
        return await UserCrud.create(data=data, session=session)