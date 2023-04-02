from fastapi import APIRouter, Depends

from api.routers.backoffice.backoffice_board import router as backoffice_board_router
from api.routers.backoffice.backoffice_info import (
    router as rental_business_user_info_router,
)
from api.routers.backoffice.login import router as login_router
from api.routers.backoffice.register import router as register_router
from api.utils.api_validators import check_if_is_rental_business_user, verify_token

LOGIN_ROUTER_PREFIX = "/login"
REGISTER_ROUTER_PREFIX = "/register"
BACKOFFICE_BOARD_ROUTER_PREFIX = "/board"
BACKOFFICE_USER_INFO_ROUTER_PREFIX = "/info"

router = APIRouter()

router.include_router(
    login_router,
    prefix=LOGIN_ROUTER_PREFIX,
)
router.include_router(
    register_router,
    prefix=REGISTER_ROUTER_PREFIX,
)

router.include_router(
    rental_business_user_info_router,
    prefix=BACKOFFICE_USER_INFO_ROUTER_PREFIX,
    dependencies=[Depends(verify_token), Depends(check_if_is_rental_business_user)],
)

router.include_router(
    backoffice_board_router,
    prefix=BACKOFFICE_BOARD_ROUTER_PREFIX,
    dependencies=[Depends(verify_token), Depends(check_if_is_rental_business_user)],
)
