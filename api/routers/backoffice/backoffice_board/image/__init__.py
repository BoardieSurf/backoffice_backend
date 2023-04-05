from fastapi import APIRouter, Depends, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.schemas.schemas import (
    BackofficeUserBoardImagesResponse,
    BackofficeUserBoardImageUploadResponse,
    JWTData,
    SetBoardImageAsMainResponse,
)
from api.services.board_image_service import (
    get_all_images_of_rental_business_own_board_by_id,
    set_board_main_image_by_id,
    upload_board_image,
)
from api.utils.api_utils import ensure_file_is_image

router = APIRouter()


@router.get(
    "/",
    response_model=BackofficeUserBoardImagesResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Get all images of your own Board",
)
async def get_images_of_own_board_endpoint(
    board_id: int,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data

    rental_business_board_images = (
        await get_all_images_of_rental_business_own_board_by_id(
            db, jwt_data.user_id, board_id
        )
    )

    return BackofficeUserBoardImagesResponse(data=rental_business_board_images)


@router.post(
    "/",
    response_model=BackofficeUserBoardImageUploadResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Upload an image of your rental business board",
)
async def upload_image_file_of_own_board_endpoint(
    board_id: int,
    request: Request,
    file: UploadFile,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data

    ensure_file_is_image(file)

    await upload_board_image(db, file, jwt_data.user_id, board_id)

    return BackofficeUserBoardImageUploadResponse()


@router.get(
    "/{image_id}/set_as_main",
    response_model=SetBoardImageAsMainResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Set Image as main image of Rental Business Info",
)
async def set_image_as_main_rental_business_info_endpoint(
    board_id: int,
    image_id: int,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data

    await set_board_main_image_by_id(db, jwt_data.user_id, board_id, image_id)

    return SetBoardImageAsMainResponse()
