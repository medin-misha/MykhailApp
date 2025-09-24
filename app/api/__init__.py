__all__ = "main_router", "user_broker"

from fastapi import APIRouter
from .v1.users import user_router, user_broker
main_router = APIRouter()

main_router.include_router(user_router)