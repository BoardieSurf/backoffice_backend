from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.schemas.rental_business_schemas import (
    BackofficeUserInfoResponse,
    UpdateBackofficeUserInfoResponse,
    UpdateRentalBusinessUserInfoInstance,
)
from api.schemas.schemas import JWTData
from api.services.rental_business_service import (
    get_info_of_own_rental_business,
    update_info_of_own_rental_business,
)
from api.routers.backoffice.backoffice_info.image import (
    router as backoffice_info_image_router,
)

BACKOFFICE_USER_INFO_IMAGE_ROUTER_PREFIX = "/image"

router = APIRouter()

router.include_router(
    backoffice_info_image_router,
    prefix=BACKOFFICE_USER_INFO_IMAGE_ROUTER_PREFIX,
)


@router.get(
    "/",
    response_model=BackofficeUserInfoResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Get your own info",
)
async def get_own_rental_info_business_endpoint(
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    rental_business_user_info = await get_info_of_own_rental_business(
        db, jwt_data.user_id
    )

    return BackofficeUserInfoResponse(data=rental_business_user_info)


@router.put(
    "/",
    response_model=UpdateBackofficeUserInfoResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Update your own info",
)
async def update_own_rental_info_business_endpoint(
    body: UpdateRentalBusinessUserInfoInstance,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    await update_info_of_own_rental_business(db, body, jwt_data.user_id)

    return UpdateBackofficeUserInfoResponse()
