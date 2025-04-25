"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import start_async_database, dispose_async_database


@asynccontextmanager
async def lifespan(app: FastAPI):

    # start
    await start(app)

    yield

    # close
    await close(app)


async def start(app: FastAPI):

    # start database
    await start_async_database()
    pass

async def close(app: FastAPI):

    # dispose database
    await dispose_async_database()
    pass