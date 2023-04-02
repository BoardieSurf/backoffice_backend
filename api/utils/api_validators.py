from datetime import datetime

from fastapi import HTTPException, Request, Security, status
from fastapi.security.api_key import APIKeyHeader

from api.schemas.schemas import JWTData
from api.services.auth_service import decrypt_jwt_token
from api.utils.enums import UserType

auth_jwt_header = APIKeyHeader(name="access_token", scheme_name="auth_token")


async def verify_token(auth_token: str = Security(auth_jwt_header)):
    # temp_jwt = create_jwt_token(
    #     user_id=0,
    #     user_type=UserType.RENTAL_BUSINESS,
    # )
    # print("JWT: ", temp_jwt)

    jwt_data = decrypt_jwt_token(auth_token)

    if jwt_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad token",
        )

    if datetime.now() > jwt_data.expires_date:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your token has expired",
        )


async def check_if_is_rental_business_user(
    request: Request,
    auth_token: str = Security(auth_jwt_header),
) -> JWTData:
    jwt_data = decrypt_jwt_token(auth_token)
    assert jwt_data
    if jwt_data.user_type != UserType.RENTAL_BUSINESS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowed for this user type",
        )

    request.state.jwt_data = jwt_data
    return jwt_data
