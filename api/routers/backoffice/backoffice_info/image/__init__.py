from fastapi import APIRouter, Depends, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.schemas.rental_business_schemas import (
    AllBackofficeUserInfoImageResponse,
    BackofficeUserInfoImageUploadResponse,
    SetBackofficeUserInfoImageAsMainResponse,
)
from api.schemas.schemas import JWTData
from api.services.rental_business_service import (
    get_all_rental_business_info_images,
    set_main_rental_business_info_image_by_id,
    upload_rental_business_info_image,
)
from api.utils.api_utils import ensure_file_is_image

# from api.utils.api_utils import ensure_file_is_image

router = APIRouter()


@router.get(
    "/",
    response_model=AllBackofficeUserInfoImageResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Get all your Rental Business Info images",
)
async def get_images_of_own_rental_business_endpoint(
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data

    rental_business_info_images = await get_all_rental_business_info_images(
        db, jwt_data.user_id
    )

    return AllBackofficeUserInfoImageResponse(data=rental_business_info_images)


@router.get(
    "/{image_id}/set_as_main",
    response_model=SetBackofficeUserInfoImageAsMainResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Set Image as main image of Rental Business Info",
)
async def set_image_as_main_rental_business_info_endpoint(
    image_id: int,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data

    await set_main_rental_business_info_image_by_id(db, jwt_data.user_id, image_id)

    return SetBackofficeUserInfoImageAsMainResponse()


@router.post(
    "/",
    response_model=BackofficeUserInfoImageUploadResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Upload your rental business info image",
)
async def upload_image_file_of_rental_business_endpoint(
    request: Request,
    file: UploadFile,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data

    ensure_file_is_image(file)

    await upload_rental_business_info_image(db, file, jwt_data.user_id)

    return BackofficeUserInfoImageUploadResponse()
