from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

import asyncpg

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from main_api.loggers import db_logger as logger
from main_api import config


class Base(DeclarativeBase):
    pass


sqlalchemy_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
)

engine = create_async_engine(sqlalchemy_uri)


@asynccontextmanager
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSession(engine)
    try:
        yield session
    except Exception as e:
        logger.error(f"DB Session Error: {e}")
        await session.rollback()
        raise
    finally:
        await session.close()


@asynccontextmanager
async def main_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    try:
        connection = await asyncpg.connect(
            user=config.MAIN_DB_DB_USER,
            password=config.MAIN_DB_DB_PASSWORD,
            host=config.MAIN_DB_DB_HOST,
            port=config.MAIN_DB_DB_PORT,
            database=config.MAIN_DB_DB_NAME,
        )
    except Exception:
        logger.exception("Cannot connect to the main_db")
        raise

    try:
        yield connection
    except Exception:
        logger.exception("Error during main_db connection")
        raise
    finally:
        await connection.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db_session() as session:
        yield session


Database = Annotated[AsyncSession, Depends(get_db)]