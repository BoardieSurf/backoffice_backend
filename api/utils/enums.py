from enum import Enum


class UserType(Enum):
    CUSTOMER = "customer"
    RENTAL_BUSINESS = "rental_business"
    SUPERUSER = "superuser"
