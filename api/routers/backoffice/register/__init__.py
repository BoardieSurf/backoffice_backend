from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.schemas.rental_business_schemas import (
    RegisterAccountResponse,
    RegisterRentalBusinessUserAccountInstance,
)
from api.services.rental_business_service import register_rental_business_user_account

router = APIRouter()


@router.post(
    "/",
    response_model=RegisterAccountResponse,
    response_model_exclude_none=True,
    summary="Create a Rental Business User account (if you have a register token).",
)
async def register_rental_business_user_account_endpoint(
    body: RegisterRentalBusinessUserAccountInstance,
    db: AsyncDBSession = Depends(get_db),
):
    await register_rental_business_user_account(db, body)

    return RegisterAccountResponse()
