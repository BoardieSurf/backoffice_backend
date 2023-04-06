from sqlalchemy import literal_column, select, update
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import execute_db_statement, handle_no_data
from api.models import BoardImage, BoardImageMain


async def create_board_image_on_db(
    db: AsyncDBSession, board_id: int, filename: str
) -> BoardImage:
    new_board_image_obj = BoardImage(board_id=board_id, filename=filename)
    db.add(new_board_image_obj)

    await db.commit()

    return new_board_image_obj


async def create_board_image_main_on_db(
    db: AsyncDBSession,
    board_id: int,
    image_id: int,
) -> BoardImageMain:
    board_image_main_obj = BoardImageMain(board_id=board_id, image_id=image_id)
    db.add(board_image_main_obj)

    await db.commit()

    return board_image_main_obj


async def set_board_image_as_main_on_db(
    db: AsyncDBSession,
    board_id: int,
    image_id: int,
) -> None:
    statement = (
        update(BoardImageMain)
        .where(BoardImageMain.board_id == board_id)
        .values(image_id=image_id)
        .returning(literal_column("*"))
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[BoardImageMain] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return None


async def get_board_image_main_from_db(
    db: AsyncDBSession,
    board_id: int,
) -> BoardImageMain:
    statement = select(BoardImageMain).where(BoardImageMain.board_id == board_id)

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[BoardImageMain] = existing_data.scalars().all()

    assert len(results) == 1

    return results[0]
