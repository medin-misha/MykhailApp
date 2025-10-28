__all__ = "main_router"

from fastapi import APIRouter
from .v1.users.views import router as user_router
from .v1.subscriptions.views import router as subscription_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(user_router)
main_router.include_router(subscription_router)
