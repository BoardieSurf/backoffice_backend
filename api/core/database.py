from asyncio import current_task
from typing import AsyncGenerator, Optional

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession as AsyncDBSession
from sqlalchemy.ext.asyncio import async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.core.config import settings
from api.core.loggr import loggr

engine = create_async_engine(
    settings.db_url,
    future=True,
    echo=True,
    json_serializer=jsonable_encoder,
    pool_size=20,
    max_overflow=80,
    pool_timeout=240,
    pool_pre_ping=True,
    connect_args={"command_timeout": 180.0},
)

async_session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncDBSession
)
AsyncScopedSession = async_scoped_session(async_session_factory, scopefunc=current_task)


logger = loggr.get_logger(__name__)


async def get_db() -> AsyncGenerator:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()


async def execute_db_statement(db: AsyncDBSession, statement, current_function: str):
    try:
        existing_data = await db.execute(statement)
        return existing_data

    except SQLAlchemyError as ex:
        logger.error(f"SQLAlchemyError at {current_function} method", ex)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=repr(ex)
        )


def handle_no_data(results: list, message: Optional[str] = None) -> None:
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
