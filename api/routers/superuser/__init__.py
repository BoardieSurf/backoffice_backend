from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.schemas.superuser import (
    RentalBusinessInviteCreationResponse,
    RentalBusinessUserInviteCreationInstance,
)
from api.services.superuser_service import create_rental_business_invite

router = APIRouter()


@router.post(
    "/create_rental_business_register_invite",
    response_model=RentalBusinessInviteCreationResponse,
    response_model_exclude_none=True,
    summary="Send an invite to an email to create a Rental Business User Account",
)
async def superuser_invite_rental_business_endpoint(
    body: RentalBusinessUserInviteCreationInstance, db: AsyncDBSession = Depends(get_db)
):
    await create_rental_business_invite(db, body)

    return RentalBusinessInviteCreationResponse()
