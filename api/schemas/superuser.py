from pydantic import BaseModel, EmailStr

from api.schemas.schemas import BaseResponseDataSchema


class RentalBusinessUserInviteCreationInstance(BaseModel):
    email: EmailStr


# responses


class RentalBusinessInviteCreationResponse(BaseResponseDataSchema):
    code = 200
