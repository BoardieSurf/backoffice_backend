from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.routers.backoffice.backoffice_board.image import (
    router as backoffice_board_image_router,
)
from api.schemas.schemas import (
    BoardsResponse,
    CreateBoardResponse,
    CreateSingleBoardInstance,
    DeleteBoardResponse,
    JWTData,
    SingleBoardResponse,
    UpdateBoardResponse,
    UpdateSingleBoardInstance,
)
from api.services.board_service import (
    create_board,
    delete_board_of_rental_business_by_id,
    get_all_boards_of_rental_business,
    get_board_of_rental_business_by_id,
    update_board_of_rental_business_by_id,
)

BACKOFFICE_USER_INFO_IMAGE_ROUTER_PREFIX = "/{board_id}/image"

router = APIRouter()

router.include_router(
    backoffice_board_image_router,
    prefix=BACKOFFICE_USER_INFO_IMAGE_ROUTER_PREFIX,
)


@router.get(
    "/",
    response_model=BoardsResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Get all Boards of your own Rental Business",
)
async def get_all_boards_of_own_rental_business_endpoint(
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    boards = await get_all_boards_of_rental_business(db, jwt_data.user_id)

    return BoardsResponse(data=boards)


@router.get(
    "/{board_id}",
    response_model=SingleBoardResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Get a Board of your own Rental Business by the ID",
)
async def get_board_of_own_rental_business_by_id_endpoint(
    board_id: int,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    boards = await get_board_of_rental_business_by_id(db, jwt_data.user_id, board_id)

    return SingleBoardResponse(data=boards)


@router.delete(
    "/{board_id}",
    response_model=DeleteBoardResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Delete a Board of your own Rental Business by the ID",
)
async def delete_board_of_own_rental_business_by_id_endpoint(
    board_id: int,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    await delete_board_of_rental_business_by_id(db, jwt_data.user_id, board_id)

    return DeleteBoardResponse()


@router.put(
    "/{board_id}",
    response_model=UpdateSingleBoardInstance,
    response_model_exclude_none=True,
    tags=[],
    summary="Update a Board of your own Rental Business by the ID",
)
async def update_board_of_own_rental_business_by_id_endpoint(
    board_id: int,
    body: UpdateSingleBoardInstance,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    await update_board_of_rental_business_by_id(db, body, jwt_data.user_id, board_id)

    return UpdateBoardResponse()


@router.post(
    "/",
    response_model=CreateBoardResponse,
    response_model_exclude_none=True,
    tags=[],
    summary="Create Board",
)
async def create_board_endpoint(
    body: CreateSingleBoardInstance,
    request: Request,
    db: AsyncDBSession = Depends(get_db),
):
    jwt_data: JWTData = request.state.jwt_data
    boards = await create_board(db, body, jwt_data.user_id)

    return CreateBoardResponse(data=boards)
