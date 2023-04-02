from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.database import get_db
from api.schemas.rental_business_schemas import (
    CredentialsSubmitInstance,
    CredentialsSubmitResponse,
)
from api.services.auth_service import submit_backoffice_credentials

router = APIRouter()


@router.post(
    "/",
    response_model=CredentialsSubmitResponse,
    response_model_exclude_none=True,
    summary="Log in / authenticate. Get a JWT as result.",
)
async def backoffice_credentials_submit_endpoint(
    body: CredentialsSubmitInstance, db: AsyncDBSession = Depends(get_db)
):
    auth_successful_token = await submit_backoffice_credentials(db, body)

    return CredentialsSubmitResponse(data=auth_successful_token)
