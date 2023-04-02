from sqlalchemy import literal_column, select, update
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession
import json
from api.core.database import execute_db_statement, handle_no_data
from api.models import (
    RentalBusinessRegisterAccountInvite,
    RentalBusinessUser,
    RentalBusinessUserInfo,
    RentalBusinessUserInfoImage,
    RentalBusinessUserInfoImageMain,
)
from api.schemas.rental_business_schemas import (
    RegisterRentalBusinessUserAccountInstance,
    UpdateRentalBusinessUserInfoInstance,
)


async def select_info_of_rental_business_by_id(
    db: AsyncDBSession, rental_business_user_id: int
) -> RentalBusinessUserInfo:
    statement = select(RentalBusinessUserInfo).where(
        RentalBusinessUserInfo.rental_business_user_id == rental_business_user_id
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfo] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return results[0]


async def update_info_of_rental_business_by_id(
    db: AsyncDBSession,
    new_rental_business_info_values: UpdateRentalBusinessUserInfoInstance,
    rental_business_user_id: int,
) -> None:
    statement = (
        update(RentalBusinessUserInfo)
        .where(
            RentalBusinessUserInfo.rental_business_user_id == rental_business_user_id
        )
        .values(json.loads(new_rental_business_info_values.json()))
        .returning(literal_column("*"))
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfo] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return None


async def get_register_invite(
    db: AsyncDBSession,
    register_token: str,
) -> RentalBusinessRegisterAccountInvite:
    statement = (
        select(RentalBusinessRegisterAccountInvite)
        .where(RentalBusinessRegisterAccountInvite.token == register_token)
        .where(RentalBusinessRegisterAccountInvite.used_by == None)
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessRegisterAccountInvite] = existing_data.scalars().all()

    handle_no_data(results, message="Invalid Register Token")
    assert len(results) == 1

    return results[0]


async def update_register_invite_with_user_id(
    db: AsyncDBSession, register_token: str, rental_business_user_id: int
) -> None:
    statement = (
        update(RentalBusinessRegisterAccountInvite)
        .where(RentalBusinessRegisterAccountInvite.token == register_token)
        .where(RentalBusinessRegisterAccountInvite.used_by == None)
        .values(
            {RentalBusinessRegisterAccountInvite.used_by.key: rental_business_user_id},
        )
        .returning(literal_column("*"))
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfo] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return None


async def create_rental_business_user(
    db: AsyncDBSession,
    register_rental_business_user_info_instance: RegisterRentalBusinessUserAccountInstance,
    password_encrypted: str,
) -> int:
    new_rental_business_user_obj = RentalBusinessUser(
        username=register_rental_business_user_info_instance.username,
        password_encrypted=password_encrypted,
    )
    db.add(new_rental_business_user_obj)

    await db.commit()

    assert isinstance(new_rental_business_user_obj.private_id, int)

    return new_rental_business_user_obj.private_id


async def create_rental_business_user_info(
    db: AsyncDBSession,
    rental_business_user_id: int,
    register_rental_business_user_info_instance: RegisterRentalBusinessUserAccountInstance,
    email: str,
) -> None:
    new_rental_business_user_info_obj = RentalBusinessUserInfo(
        rental_business_user_id=rental_business_user_id,
        email=email,
        phone=register_rental_business_user_info_instance.phone,
        address=register_rental_business_user_info_instance.address,
        business_title=register_rental_business_user_info_instance.business_title,
        business_description=register_rental_business_user_info_instance.business_description,
        business_type=register_rental_business_user_info_instance.business_type.value,
    )
    db.add(new_rental_business_user_info_obj)

    await db.commit()

    return None


async def get_rental_business_info_image_by_id_from_db(
    db: AsyncDBSession, rental_business_user_id: int, image_id: int
) -> RentalBusinessUserInfoImage:
    statement = (
        select(RentalBusinessUserInfoImage)
        .where(
            RentalBusinessUserInfoImage.rental_business_user_id
            == rental_business_user_id
        )
        .where(RentalBusinessUserInfoImage.private_id == image_id)
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfoImage] = existing_data.scalars().all()

    handle_no_data(results, f"Image with ID {image_id} not found.")

    assert len(results) == 1

    return results[0]


async def get_rental_business_info_images_from_db(
    db: AsyncDBSession,
    rental_business_user_id: int,
) -> list[RentalBusinessUserInfoImage]:
    statement = select(RentalBusinessUserInfoImage).where(
        RentalBusinessUserInfoImage.rental_business_user_id == rental_business_user_id
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfoImage] = existing_data.scalars().all()

    return results


async def create_rental_business_info_image_on_db(
    db: AsyncDBSession, rental_business_user_id: int, filename: str
) -> RentalBusinessUserInfoImage:
    new_rental_business_user_info_image_obj = RentalBusinessUserInfoImage(
        rental_business_user_id=rental_business_user_id, filename=filename
    )
    db.add(new_rental_business_user_info_image_obj)

    await db.commit()

    return new_rental_business_user_info_image_obj


async def get_rental_business_info_image_main_from_db(
    db: AsyncDBSession,
    rental_business_user_id: int,
) -> RentalBusinessUserInfoImageMain:
    statement = select(RentalBusinessUserInfoImageMain).where(
        RentalBusinessUserInfoImageMain.rental_business_user_id
        == rental_business_user_id
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfoImage] = existing_data.scalars().all()

    assert len(results) == 1

    return results[0]


async def create_rental_business_info_image_main_on_db(
    db: AsyncDBSession,
    rental_business_user_id: int,
    image_id: int,
) -> RentalBusinessUserInfoImageMain:
    rental_business_user_info_image_main_obj = RentalBusinessUserInfoImageMain(
        rental_business_user_id=rental_business_user_id, image_id=image_id
    )
    db.add(rental_business_user_info_image_main_obj)

    await db.commit()

    return rental_business_user_info_image_main_obj


async def set_rental_business_info_image_as_main_on_db(
    db: AsyncDBSession,
    rental_business_user_id: int,
    image_id: int,
) -> None:
    statement = (
        update(RentalBusinessUserInfoImageMain)
        .where(
            RentalBusinessUserInfoImageMain.rental_business_user_id
            == rental_business_user_id
        )
        .values(image_id=image_id)
        .returning(literal_column("*"))
    )

    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUserInfo] = existing_data.scalars().all()

    handle_no_data(results)
    assert len(results) == 1

    return None
