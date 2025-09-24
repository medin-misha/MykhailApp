__all__ = "user_router", "user_broker"

from fastapi import APIRouter
from .amqp_publishers import router as amqp_publisher_router
from .amqp_consumers import broker as user_broker
from .views import router as http_router

user_router = APIRouter()
user_router.include_router(amqp_publisher_router)
user_router.include_router(http_router)