from pydantic import BaseModel, Field

from api.schemas.schemas import (
    AuthSuccessfulToken,
    BaseResponseDataSchema,
    RentalBusinessType,
)


class BaseRentalBusinessUserInfoInstance(BaseModel):
    phone: str = Field(min_length=5)
    address: str = Field(min_length=5)
    business_title: str = Field(min_length=5)
    business_description: str = Field(min_length=5)
    business_type: RentalBusinessType


class UpdateRentalBusinessUserInfoInstance(BaseRentalBusinessUserInfoInstance):
    pass


class RentalBusinessUserInfoInstance(BaseRentalBusinessUserInfoInstance):
    private_id: int
    rental_business_user_id: int
    email: str


class RentalBusinessUserInfoImageInstance(BaseModel):
    private_id: int
    filename: str
    is_main: bool = False


# auth


class CredentialsSubmitInstance(BaseModel):
    username: str = Field(min_length=4)
    password: str = Field(min_length=7)


class RegisterRentalBusinessUserAccountInstance(
    CredentialsSubmitInstance, BaseRentalBusinessUserInfoInstance
):
    register_token: str


# Responses


class SetBackofficeUserInfoImageAsMainResponse(BaseResponseDataSchema):
    code = 200


class AllBackofficeUserInfoImageResponse(BaseResponseDataSchema):
    data: list[RentalBusinessUserInfoImageInstance]
    code = 200


class BackofficeUserInfoImageUploadResponse(BaseResponseDataSchema):
    code = 200


class BackofficeUserInfoResponse(BaseResponseDataSchema):
    data: RentalBusinessUserInfoInstance
    code = 200


class UpdateBackofficeUserInfoResponse(BaseResponseDataSchema):
    code = 200


class CredentialsSubmitResponse(BaseResponseDataSchema):
    data: AuthSuccessfulToken
    code = 200


class RegisterAccountResponse(BaseResponseDataSchema):
    code = 200
