from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from contracts.admin import AdminCreateForm, AdminReturn
from core.models import Admin
from core.security import hash_password
from services.error_handlers import DBErrorHandler


async def create_admin(form: AdminCreateForm, session: AsyncSession) -> AdminReturn:
    """
    Создаёт нового администратора в базе данных.
    Хэширует пароль, проверяет уникальность, возвращает безопасную модель.
    """
    # Проверка уникальности
    existing = await session.scalar(select(Admin).where(Admin.email == form.email))
    if existing:
        raise HTTPException(
            status_code=400, detail="Администратор с таким email уже существует"
        )

    # Подготовка данных
    data = form.model_dump(exclude_none=True)
    data["hashed_password"] = hash_password(data.pop("password"))

    # Создание и сохранение
    new_admin = Admin(**data)
    session.add(new_admin)

    try:
        await session.commit()
        await session.refresh(new_admin)
    except Exception as err:
        await session.rollback()
        DBErrorHandler.handle(err=err, model=Admin)

    # Возврат в виде Pydantic-схемы
    return AdminReturn.model_validate(new_admin)
