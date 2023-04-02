from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.models import Board
from api.repos.board_repo import (
    create_board_obj,
    delete_board_by_rental_business_and_id,
    select_all_boards_by_rental_business,
    select_board_by_rental_business_and_id,
    update_board_by_rental_business_and_id,
)
from api.schemas.schemas import (
    BoardInstance,
    CreateSingleBoardInstance,
    UpdateSingleBoardInstance,
)


def board_db_to_schema_converter(
    board_db_obj: Board,
) -> BoardInstance:
    return BoardInstance(**board_db_obj.__dict__)


async def get_all_boards_of_rental_business(
    db: AsyncDBSession, rental_business_id: int
) -> list[BoardInstance]:
    board_db_objs = await select_all_boards_by_rental_business(db, rental_business_id)
    return [board_db_to_schema_converter(x) for x in board_db_objs]


async def get_board_of_rental_business_by_id(
    db: AsyncDBSession, rental_business_id: int, board_id: int
) -> BoardInstance:
    board_db_obj = await select_board_by_rental_business_and_id(
        db, rental_business_id, board_id
    )
    return board_db_to_schema_converter(board_db_obj)


async def delete_board_of_rental_business_by_id(
    db: AsyncDBSession, rental_business_id: int, board_id: int
) -> None:
    await delete_board_by_rental_business_and_id(db, rental_business_id, board_id)
    return None


async def update_board_of_rental_business_by_id(
    db: AsyncDBSession,
    new_board_values: UpdateSingleBoardInstance,
    rental_business_id: int,
    board_id: int,
) -> None:
    await update_board_by_rental_business_and_id(
        db, new_board_values, rental_business_id, board_id
    )


async def create_board(
    db: AsyncDBSession,
    new_board: CreateSingleBoardInstance,
    rental_business_user_id: int,
) -> list[BoardInstance]:
    board_db_objs = await create_board_obj(db, new_board, rental_business_user_id)

    return [board_db_to_schema_converter(x) for x in board_db_objs]
