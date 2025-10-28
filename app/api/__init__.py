__all__ = "main_router", "user_broker"

from fastapi import APIRouter
from .v1.users.views import router as user_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(user_router)
