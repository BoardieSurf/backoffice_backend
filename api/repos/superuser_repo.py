from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.models import RentalBusinessRegisterAccountInvite


async def create_rental_business_invite_db_obj(
    db: AsyncDBSession,
    email: str,
    register_token: str,
) -> None:
    new_rental_business_invite_obj = RentalBusinessRegisterAccountInvite(
        email=email, token=register_token
    )
    db.add(new_rental_business_invite_obj)

    await db.commit()

    return None
