from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException, status
from contracts.user import UserReturn
from core.models import User
from core.security import hash_password


async def get_user_by_chat_id(
    chat_id: int, session: AsyncSession
) -> User:
    stmt = select(User).where(User.chat_id == chat_id)
    result: Result = await session.execute(stmt)
    user: User | None = result.one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user[0]
