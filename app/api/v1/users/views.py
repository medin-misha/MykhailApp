from fastapi import APIRouter, Depends, HTTPException, status

from contracts.user import ReturnUser
from core.database import database
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from services.user import UserCrud

router = APIRouter(tags=["http user"], prefix="/users")


@router.get("/{chat_id:int}")
async def get_user_birthday_handler(
    chat_id: int, session: AsyncSession = Depends(database.get_session)
) -> ReturnUser:
    user: User | None = await UserCrud.get_user_by_chat_id(chat_id=chat_id, session=session)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")