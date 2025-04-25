from typing import Any, AsyncGenerator

from app.database import get_async_database, dispose_async_database
from app.service.business.youtube import YouTubeBusinessService
from app.service.end_point.youtube import YouTubeEndPointService

async def get_youtube_business_service() -> AsyncGenerator[YouTubeBusinessService, Any]:
    """
    Dependency injector for YouTubeBusinessService
    """
    service = YouTubeBusinessService()
    try:
        yield service
    finally:
        await service.close()

async def get_youtube_endpoint_service() -> AsyncGenerator[YouTubeEndPointService, Any]:
    """
    Dependency injector for YouTubeEndPointService
    """
    service = YouTubeEndPointService()
    try:
        yield service
    finally:
        await service.close()


async def get_async_session():
    AsyncSessionLocal = get_async_database()
    async with AsyncSessionLocal() as session:
        yield session
