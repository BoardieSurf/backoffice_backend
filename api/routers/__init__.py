from fastapi import APIRouter

from api.routers.backoffice import router as backoffice_router
from api.routers.superuser import router as superuser_router

router = APIRouter()

BACKOFFICE_ROUTER_PREFIX = "/backoffice"
SUPERUSER_ROUTER_PREFIX = "/superuser"

router.include_router(
    backoffice_router,
    prefix=BACKOFFICE_ROUTER_PREFIX,
)

router.include_router(
    superuser_router,
    prefix=SUPERUSER_ROUTER_PREFIX,
    tags=["superuser"],
)
