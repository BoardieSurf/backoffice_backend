import hashlib
import json
from datetime import datetime, timedelta

import jwt
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession

from api.core.config import settings
from api.repos.auth_repo import (  # create_user,
    search_rental_business_user_by_username_and_encrypted_password,
)
from api.schemas.rental_business_schemas import CredentialsSubmitInstance
from api.schemas.schemas import AuthSuccessfulToken, JWTData
from api.utils.enums import UserType


def create_jwt_token(user_id: int, user_type: UserType) -> str:
    expires_date = datetime.now() + timedelta(
        minutes=settings.auth_access_token_expire_minutes
    )

    jwt_data = JWTData(
        user_id=user_id,
        expires_date=expires_date,
        user_type=user_type,
    )

    jtw_token = jwt.encode(
        json.loads(jwt_data.json()),
        settings.auth_secret_key,
        algorithm=settings.auth_algorithm,
    )

    return jtw_token


def decrypt_jwt_token(jwt_token: str) -> JWTData | None:
    try:
        jwt_data = JWTData.parse_obj(
            jwt.decode(
                jwt_token,
                settings.auth_secret_key,
                algorithms=[settings.auth_algorithm],
            )
        )
    except jwt.exceptions.DecodeError:
        return None

    return jwt_data


def encrypt_password(password: str) -> str:
    # as seen in https://docs.python.org/3/library/hashlib.html
    sha_instance = hashlib.sha256()
    sha_instance.update(str.encode(password))
    return sha_instance.hexdigest()


async def submit_backoffice_credentials(
    db: AsyncDBSession, credentials: CredentialsSubmitInstance
) -> AuthSuccessfulToken:
    # encrypt the password
    encrypted_password = encrypt_password(credentials.password)

    # check if the password matches

    rental_business_user_obj = (
        await search_rental_business_user_by_username_and_encrypted_password(
            db, credentials.username, encrypted_password
        )
    )

    # generate a JWT

    assert isinstance(rental_business_user_obj.private_id, int)
    jwt_token = create_jwt_token(
        rental_business_user_obj.private_id, UserType.RENTAL_BUSINESS
    )

    return AuthSuccessfulToken(token=jwt_token)
