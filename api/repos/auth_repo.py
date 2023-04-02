from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession
from sqlalchemy.future import select

from api.core.database import execute_db_statement
from api.core.loggr import loggr
from api.models import RentalBusinessUser

logger = loggr.get_logger(__name__)


# async def create_user(
#     db: AsyncDBSession, username: str, password_encrypted: str, permission_level: int
# ) -> None:
#     user_db_obj = User(
#         username=username,
#         password_encrypted=password_encrypted,
#         permission_level=permission_level,
#     )
#     try:
#         db.add(user_db_obj)
#         await db.commit()
#         await db.refresh(user_db_obj)
#     except SQLAlchemyError as ex:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex)
#         )


async def search_rental_business_user_by_username_and_encrypted_password(
    db: AsyncDBSession, username: str, password_encrypted: str
) -> RentalBusinessUser:
    statement = (
        select(RentalBusinessUser)
        .where(RentalBusinessUser.username == username)
        .where(RentalBusinessUser.password_encrypted == password_encrypted)
    )
    existing_data = await execute_db_statement(db, statement, __name__)
    results: list[RentalBusinessUser] = existing_data.scalars().all()
    if not results:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )
        # 401 as explained in https://stackoverflow.com/questions/32752578
    assert len(results) == 1
    return results[0]
