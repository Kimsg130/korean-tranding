"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
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
