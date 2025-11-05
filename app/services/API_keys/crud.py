from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from fastapi import HTTPException
import secrets
from contracts.api_keys import APIKeyCreate, APIKeyCreateForm
from core.models import APIKey
from core.security import hash_password, HASHER
from services.error_handlers import DBErrorHandler


async def create_key(form: APIKeyCreateForm, session: AsyncSession) -> str:
    """
    Создаёт нового апи-ключа в базе данных.
    Создаёт и хеширует ключ
    """

    key = secrets.token_urlsafe(32)
    key_hash = hash_password(plain_password=key)
    data = form.model_dump()
    data["key"] = key_hash
    created_data = APIKeyCreate(**data)
    session.add(APIKey(**created_data.model_dump()))
    try:
        await session.commit()
    except Exception as err:
        DBErrorHandler.handle(err=err, model=APIKey)
        await session.rollback()

    return key


async def check_valid_api_key(key: str, session: AsyncSession) -> bool:
    """
    Проверяет, существует ли данный API-ключ в базе.
    Ключи хранятся в виде хэшей (argon2), поэтому прямое сравнение невозможно.
    """
    # TODO добавить where с service_id так быстрее
    # Получаем все ключи (или оптимизируем выборку позже)
    stmt = select(APIKey)
    try:
        result: Result = await session.execute(stmt)
        keys = result.scalars().all()
    except Exception as err:
        DBErrorHandler.handle(err=err, model=APIKey)
        await session.rollback()
    # Проверяем каждый хэш
    for db_key in keys:
        try:
            if HASHER.verify(db_key.key, key):
                return True
        except Exception:
            continue

    return False
