from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.models import RentalBusinessUserInfo
from api.repos.rental_business_repo import (
    create_rental_business_info_image_main_on_db,
    create_rental_business_info_image_on_db,
    create_rental_business_user,
    create_rental_business_user_info,
    get_register_invite,
    get_rental_business_info_image_by_id_from_db,
    get_rental_business_info_image_main_from_db,
    get_rental_business_info_images_from_db,
    select_info_of_rental_business_by_id,
    set_rental_business_info_image_as_main_on_db,
    update_info_of_rental_business_by_id,
    update_register_invite_with_user_id,
)
from api.schemas.rental_business_schemas import (
    RegisterRentalBusinessUserAccountInstance,
    RentalBusinessUserInfoImageInstance,
    RentalBusinessUserInfoInstance,
    UpdateRentalBusinessUserInfoInstance,
)
from api.services.auth_service import encrypt_password
from api.utils.constants import RENTAL_BUSINESS_INFO_IMAGES_LIMIT
from api.utils.file_utils import generate_file_name, upload_file_to_bucket


def rental_business_info_db_to_schema_converter(
    rental_business_db_obj: RentalBusinessUserInfo,
) -> RentalBusinessUserInfoInstance:
    return RentalBusinessUserInfoInstance(**rental_business_db_obj.__dict__)


async def get_info_of_own_rental_business(
    db: AsyncDBSession, rental_business_id: int
) -> RentalBusinessUserInfoInstance:
    rental_business_info_db_obj = await select_info_of_rental_business_by_id(
        db, rental_business_id
    )
    return rental_business_info_db_to_schema_converter(rental_business_info_db_obj)


async def update_info_of_own_rental_business(
    db: AsyncDBSession,
    update_rental_business_user_info_instance: UpdateRentalBusinessUserInfoInstance,
    rental_business_id: int,
) -> None:
    await update_info_of_rental_business_by_id(
        db, update_rental_business_user_info_instance, rental_business_id
    )
    return None


async def register_rental_business_user_account(
    db: AsyncDBSession,
    register_rental_business_user_info_instance: RegisterRentalBusinessUserAccountInstance,
) -> None:
    # check if the register token is valid and get the associated email address

    register_invite_db_obj = await get_register_invite(
        db, register_rental_business_user_info_instance.register_token
    )

    email = register_invite_db_obj.email
    assert isinstance(email, str)

    # encrypt the password so it can be saved

    password_encrypted = encrypt_password(
        register_rental_business_user_info_instance.password
    )

    # now, create the rental business user

    rental_business_user_id = await create_rental_business_user(
        db, register_rental_business_user_info_instance, password_encrypted
    )

    # set the rental invite used_by to the new user_id

    await update_register_invite_with_user_id(
        db,
        register_rental_business_user_info_instance.register_token,
        rental_business_user_id,
    )

    # create rental business user info (just email)

    await create_rental_business_user_info(
        db, rental_business_user_id, register_rental_business_user_info_instance, email
    )

    return None


async def set_main_rental_business_info_image_by_id(
    db: AsyncDBSession, rental_business_id: int, image_id: int
) -> None:
    # check if the image exists
    await get_rental_business_info_image_by_id_from_db(db, rental_business_id, image_id)

    # set that image as main
    await set_rental_business_info_image_as_main_on_db(db, rental_business_id, image_id)

    return None


async def get_all_rental_business_info_images(
    db: AsyncDBSession, rental_business_id: int
) -> list[RentalBusinessUserInfoImageInstance]:
    image_db_objs = await get_rental_business_info_images_from_db(
        db, rental_business_id
    )
    if not image_db_objs:
        return []

    main_image_db_obj = await get_rental_business_info_image_main_from_db(
        db, rental_business_id
    )

    return [
        RentalBusinessUserInfoImageInstance(
            private_id=x.private_id,
            filename=x.filename,
            is_main=x.private_id == main_image_db_obj.image_id,
        )
        for x in image_db_objs
    ]


async def upload_rental_business_info_image(
    db: AsyncDBSession, file: UploadFile, rental_business_id: int
) -> None:
    current_images_bd_objs = await get_rental_business_info_images_from_db(
        db, rental_business_id
    )

    if len(current_images_bd_objs) >= RENTAL_BUSINESS_INFO_IMAGES_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You cannot have more than {RENTAL_BUSINESS_INFO_IMAGES_LIMIT} images",
        )

    # upload image

    file_name = generate_file_name(file.filename)

    await upload_file_to_bucket(await file.read(), file_name)

    # create image db obj

    new_rental_business_user_info_image_obj = (
        await create_rental_business_info_image_on_db(db, rental_business_id, file_name)
    )

    # if its the 1st image uploaded, set it as main

    if len(current_images_bd_objs) == 0:
        assert isinstance(new_rental_business_user_info_image_obj.private_id, int)
        await create_rental_business_info_image_main_on_db(
            db, rental_business_id, new_rental_business_user_info_image_obj.private_id
        )

    return None
