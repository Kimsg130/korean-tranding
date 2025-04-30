"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
import traceback

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_youtube_endpoint_service
from app.service.end_point.youtube import YouTubeEndPointService

router = APIRouter(
    prefix="/youtube/end-point",
    tags=["youtube", "end-point"],
    dependencies=[Depends(get_youtube_endpoint_service)],
    responses={404: {"description": "Not found"}},
)

@router.get("/{handle}/videos/{page_limit}", status_code=status.HTTP_200_OK)
async def get_videos_with_comments(
    handle: str,
    page_limit: int,
    service: YouTubeEndPointService = Depends(get_youtube_endpoint_service),
) -> JSONResponse:
    """
    Fetch all videos and top 100 comments for the given channel handle.
    """
    try:
        data = await service.fetch_all_videos_with_comments(handle, page_limit)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"handle": handle, "results": data},
        )
    except HTTPException as exc:
        raise exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/process_korean_wave/{page_size}", summary="Process Korean Wave status for stored videos")
async def process_korean_wave_endpoint(page_size: int = 50):
    """
    Endpoint to trigger batch processing of videos:
    - Fetch videos in pages
    - Analyze with NLP
    - Update DB with Korean Wave status

    Optional query param:
    - page_size: number of videos per page (default: 50)
    """
    service = YouTubeEndPointService()
    try:
        result = await service.process_korean_wave_status(page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()

    return result


@router.get("/process_sentiment_comment/{page_size}", summary="Process Sentiment analysis comment")
async def process_sentiment_comment(page_size: int = 50):
    """
    Endpoint to trigger batch processing of videos:
    - Fetch videos in pages
    - Analyze with NLP
    - Update DB with Korean Wave status

    Optional query param:
    - page_size: number of videos per page (default: 50)
    """
    service = YouTubeEndPointService()
    try:
        result = await service.process_sentiment_for_comment(page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await service.close()

    return result