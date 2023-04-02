from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import status
from pydantic import BaseModel, Field

from api.utils.enums import UserType


class BaseResponseDataSchema(BaseModel):
    code: int
    message: str | None
    data: Any


class ErrorDataSchema(BaseModel):
    error_message: str = "Internal Server Error"


class ErrorResponseSchema(BaseResponseDataSchema):
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    details: ErrorDataSchema | None


#################

# Specific data #

#################


class RentalBusinessType(Enum):
    SCHOOL = "school"
    SHOP = "shop"


class BoardCategory(Enum):
    LONGBOARD = "longboard"
    SHORTBOARD = "shortboard"
    MIDLENGTH = "midlength"
    GUN = "gun"
    FISH = "fish"
    FOAMBOARD = "foamboard"


class JWTData(BaseModel):
    user_id: int
    user_type: UserType
    expires_date: datetime


class AuthSuccessfulToken(BaseModel):
    token: str


class SingleBoardInstance(BaseModel):
    title: str
    description: str
    category: BoardCategory


class CreateSingleBoardInstance(SingleBoardInstance):
    replicas: int = Field(default=1, ge=1)


class UpdateSingleBoardInstance(SingleBoardInstance):
    pass


class BoardInstance(BaseModel):
    private_id: int
    rental_business_user_id: int
    title: str
    category: BoardCategory
    description: str
    # main_image_url: str
    # images_urls: list[str]


class BoundingBoxVelocityMeasurementInstance(BaseModel):
    velocity_measured: float
    created_at: datetime
    private_id: int


# Response Schemas


class BoardsResponse(BaseResponseDataSchema):
    data: list[BoardInstance]
    code = 200


class SingleBoardResponse(BaseResponseDataSchema):
    data: BoardInstance
    code = 200


class CreateBoardResponse(BaseResponseDataSchema):
    data: list[BoardInstance]
    code = 200


class UpdateBoardResponse(BaseResponseDataSchema):
    code = 200


class DeleteBoardResponse(BaseResponseDataSchema):
    code = 200


class ManyBoundingBoxVelocityMeasurementsResponse(BaseResponseDataSchema):
    data: list[BoundingBoxVelocityMeasurementInstance]
    code = 200


class SingleBoundingBoxVelocityMeasurementResponse(BaseResponseDataSchema):
    data: BoundingBoxVelocityMeasurementInstance
    code = 200
