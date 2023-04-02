import json
from sqlalchemy import delete, literal_column, select, update
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import execute_db_statement, handle_no_data
from api.core.loggr import loggr
from api.models import Board
from api.schemas.schemas import CreateSingleBoardInstance, UpdateSingleBoardInstance

logger = loggr.get_logger(__name__)


async def select_all_boards_by_rental_business(
    db: AsyncDBSession, rental_business_id: int
) -> list[Board]:
    statement = select(Board).where(Board.rental_business_user_id == rental_business_id)

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[Board] = existing_data.scalars().all()

    return results


async def select_board_by_rental_business_and_id(
    db: AsyncDBSession, rental_business_id: int, board_id: int
) -> Board:
    statement = (
        select(Board)
        .where(Board.rental_business_user_id == rental_business_id)
        .where(Board.private_id == board_id)
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[Board] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return results[0]


async def delete_board_by_rental_business_and_id(
    db: AsyncDBSession, rental_business_user_id: int, board_id: int
) -> None:
    statement = (
        delete(Board)
        .where(Board.rental_business_user_id == rental_business_user_id)
        .where(Board.private_id == board_id)
        .returning(literal_column("*"))
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[Board] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return None


async def update_board_by_rental_business_and_id(
    db: AsyncDBSession,
    new_board_values: UpdateSingleBoardInstance,
    rental_business_user_id: int,
    board_id: int,
) -> None:
    statement = (
        update(Board)
        .where(Board.rental_business_user_id == rental_business_user_id)
        .where(Board.private_id == board_id)
        .values(json.loads(new_board_values.json()))
        .returning(literal_column("*"))
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[Board] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return None


async def create_board_obj(
    db: AsyncDBSession,
    new_board: CreateSingleBoardInstance,
    rental_business_user_id: int,
) -> list[Board]:
    db_objs: list[Board] = []

    for _ in range(new_board.replicas):
        new_board_obj = Board(
            title=new_board.title,
            category=new_board.category.value,
            description=new_board.description,
            rental_business_user_id=rental_business_user_id,
        )
        db_objs.append(new_board_obj)

        db.add(new_board_obj)

    await db.commit()

    return db_objs
