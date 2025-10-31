from fastapi import HTTPException, status
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, Result
from pydantic import BaseModel

from typing import TypeVar, Type, Union

# универсальные дженерики
ModelT = TypeVar("ModelT", bound=DeclarativeBase)
SchemaT = TypeVar("SchemaT", bound=BaseModel)


class CRUD:
    @staticmethod
    async def create(
        data: SchemaT, model: Type[ModelT], session: AsyncSession
    ) -> ModelT:
        instance = model(**data.model_dump())
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

