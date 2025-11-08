import logging
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from services.exceptions import APIKeyException


logger = logging.getLogger("amqp")


class AMQPErrorHandler:
    """
    💡 Универсальный обработчик ошибок AMQP.
    Преобразует исключения в безопасные логи и нормализованные объекты ошибки.
    """

    @staticmethod
    def handle(err: Exception) -> None:
        """
        Централизованный обработчик исключений:
        - валидационные ошибки Pydantic
        - бизнесовые ошибки HTTPException
        - SQLAlchemy исключения
        - системные Runtime ошибки
        """
        # ✅ Ошибки валидации контракта
        if isinstance(err, ValidationError):
            logger.warning(f"AMQP ValidationError: {err}")
            return

        # ✅ HTTP ошибки (например 404, 409, 401)
        if isinstance(err, (HTTPException, APIKeyException)):
            logger.warning(
                f"AMQP HTTPException: {err.detail} (status_code={err.status_code})"
            )
            return

        # ✅ Ошибки базы данных
        if isinstance(err, SQLAlchemyError):
            logger.error(f"Database error: {err}", exc_info=True)
            return

        # ✅ Любые runtime ошибки
        logger.critical(f"Unexpected error: {err}", exc_info=True)
