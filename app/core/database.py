from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
)
from asyncio import current_task
from config import settings


class DataBaseHelper:
    def __init__(self, url: str):
        self.engine = create_async_engine(url=url)
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # не сбрасываем все несохранённые данные перед запросом
            # Изменения копяться в памяти до .commit() или .flush()
            autocommit=False,  # Не коммитим запрос сразу. В одной сессии копяться команды и мы
            # выполняем их одной транзакцией
            expire_on_commit=False,  # Актуальность обьекта (User например) остаёться после изменения даты рождения.
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_maker() as sess:
            yield sess
            await sess.close()
