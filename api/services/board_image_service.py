from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.models import BoardImage
from api.repos.board_image_repo import (
    create_board_image_main_on_db,
    create_board_image_on_db,
    get_board_image_main_from_db,
    set_board_image_as_main_on_db,
)
from api.repos.board_repo import (
    get_all_images_of_board_by_id_from_db,
    select_board_by_rental_business_and_id,
)
from api.schemas.schemas import BoardImageInstance
from api.services.board_service import get_board_of_rental_business_by_id
from api.utils.constants import BOARD_IMAGES_LIMIT
from api.utils.file_utils import generate_file_name, upload_file_to_bucket


def board_image_db_to_schema_converter(
    board_image_db_obj: BoardImage, is_main: bool = False
) -> BoardImageInstance:
    board_instance_obj = BoardImageInstance(**board_image_db_obj.__dict__)
    board_instance_obj.is_main = is_main

    return board_instance_obj


async def get_all_images_of_rental_business_own_board_by_id(
    db: AsyncDBSession, rental_business_id: int, board_id: int
) -> list[BoardImageInstance]:
    # this checks if the board belongs to the user or not
    # and it returns a 404 if not
    await select_board_by_rental_business_and_id(db, rental_business_id, board_id)

    return await get_all_images_of_board_by_id(db, board_id)


async def get_all_images_of_board_by_id(
    db: AsyncDBSession, board_id: int
) -> list[BoardImageInstance]:
    board_image_db_objs = await get_all_images_of_board_by_id_from_db(db, board_id)

    if not board_image_db_objs:
        return []

    # get main image

    main_board_image_obj = await get_board_image_main_from_db(db, board_id)

    return [
        board_image_db_to_schema_converter(
            x, is_main=x.private_id == main_board_image_obj.image_id
        )
        for x in board_image_db_objs
    ]


async def upload_board_image(
    db: AsyncDBSession, file: UploadFile, rental_business_id: int, board_id: int
) -> None:
    # this checks if the board belongs to the user or not
    # and it returns a 404 if not
    await select_board_by_rental_business_and_id(db, rental_business_id, board_id)

    current_images_bd_objs = await get_all_images_of_board_by_id(db, board_id)

    if len(current_images_bd_objs) >= BOARD_IMAGES_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You cannot have more than {BOARD_IMAGES_LIMIT} images",
        )

    # upload image

    file_name = generate_file_name(file.filename)

    await upload_file_to_bucket(await file.read(), file_name)

    # create image db obj

    new_board_image_obj = await create_board_image_on_db(db, board_id, file_name)

    # if its the 1st image uploaded, set it as main

    if len(current_images_bd_objs) == 0:
        assert isinstance(new_board_image_obj.private_id, int)
        await create_board_image_main_on_db(
            db, board_id, new_board_image_obj.private_id
        )

    return None


async def set_board_main_image_by_id(
    db: AsyncDBSession, rental_business_id: int, board_id: int, image_id: int
) -> None:
    # check if the board exists
    await get_board_of_rental_business_by_id(db, rental_business_id, board_id)

    # set that image as main
    await set_board_image_as_main_on_db(db, board_id, image_id)

    return None
