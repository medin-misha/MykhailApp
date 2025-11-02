__all__ = "main_router"

from fastapi import APIRouter
from .v1.users.views import router as user_router
from .v1.subscriptions.views import router as subscription_router
from .v1.admin.views import router as admin_router
from .v1.services.views import router as services_router
from .v1.api_keys.views import router as api_key_router

main_router = APIRouter(prefix="/api/v1")

main_router.include_router(user_router)
main_router.include_router(subscription_router)
main_router.include_router(admin_router)
main_router.include_router(services_router)
main_router.include_router(api_key_router)