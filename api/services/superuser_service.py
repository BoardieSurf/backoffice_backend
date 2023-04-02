import uuid

from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.repos.superuser_repo import create_rental_business_invite_db_obj
from api.schemas.superuser import RentalBusinessUserInviteCreationInstance


async def create_rental_business_invite(
    db: AsyncDBSession, body: RentalBusinessUserInviteCreationInstance
) -> None:
    # generate token
    register_token = str(uuid.uuid4())

    # save token associated with email
    await create_rental_business_invite_db_obj(db, body.email, register_token)

    # send email with token
    print("IMPLEMENT THIS!!!!!!")
    print("register token: ", register_token)

    return None
