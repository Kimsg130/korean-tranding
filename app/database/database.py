"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
import logging
from functools import lru_cache

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from sqlmodel import SQLModel

from app.config import DatabaseSettings
from app.schema.public import metadata

database_settings = DatabaseSettings()


_async_engine = create_async_engine(
    database_settings.get_connect_url(),
    echo=True,
    future=True,
)

@lru_cache()
def get_async_database() -> async_sessionmaker[AsyncSession]:

    AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=_async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    return AsyncSessionLocal


async def dispose_async_database() -> bool:
    if _async_engine:
        await _async_engine.dispose()
    return True



async def start_async_database():

    logger = logging.getLogger()

    # test connect
    AsyncSessionLocal = get_async_database()

    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(text("select 1"))
    except TimeoutError as te:
        logger.error("db connection timeout...")
        raise te
    except Exception as e:
        logger.error(f"db connection test failed: {e}")
        raise e

    # create all
    if _async_engine:
        async with _async_engine.begin() as conn:
            # await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)