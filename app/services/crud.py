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

    @staticmethod
    async def get(
        model: Type[ModelT],
        session: AsyncSession,
        id: int | None = None,
    ) -> Union[ModelT, list[ModelT]]:
        stmt = select(model)
        if id:
            stmt = stmt.where(model.id == id)

        result: Result = await session.execute(stmt)
        data = result.scalars().all()

        if id:
            if not data:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            return data[0]

        return data

    @staticmethod
    async def patch(
        new_data: SchemaT, model: Type[ModelT], session: AsyncSession, id: int
    ):
        stmt = select(model).where(model.id == id)
        result: Result = await session.execute(stmt)
        instance = result.scalars().first()

        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        # exclude_unset говорит что можно брать только те поля которые не None
        update_data = new_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(instance, field, value)

        session.add(instance)
        await session.commit()
        await session.refresh(instance)

        return instance

    @staticmethod
    async def delete(
        model: Type[ModelT],
        session: AsyncSession,
        id: int | None = None,
    ) -> str:
        stmt = select(model).where(model.id == id)
        instances: Result = await session.execute(stmt)
        instance: ModelT = instances.scalars().first()
        if not instance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        await session.delete(instance)
        await session.commit()
        return "ok"
