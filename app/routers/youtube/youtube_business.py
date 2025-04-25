"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
from fastapi import APIRouter
from fastapi.params import Depends, Query

from app.dependencies import get_youtube_business_service
from app.model.youtube.response import (
    ChannelItem,
    PlaylistItemsListResponse,
    VideosListResponse,
    CommentThreadsListResponse,
)
from app.service.business.youtube import YouTubeBusinessService



router = APIRouter(
    prefix="/youtube/business",
    tags=["youtube", "business"],
    dependencies=[Depends(get_youtube_business_service)],
    responses={404: {"description": "Not found"}},
)



@router.get(
    "/channels/{handle}",
    response_model=ChannelItem,
    summary="Get Channel by Handle",
)
async def get_channel(
    handle: str,
    service: YouTubeBusinessService = Depends(get_youtube_business_service),
) -> ChannelItem:
    """Retrieve channel information using its handle (e.g., @BandJannabi)."""
    return await service.get_channel_by_handle(handle)

@router.get(
    "/channels/{channel_id}/uploads_playlist",
    response_model=str,
    summary="Get Uploads Playlist ID",
)
async def get_uploads_playlist(
    channel_id: str,
    service: YouTubeBusinessService = Depends(get_youtube_business_service),
) -> str:
    """Return the uploads playlist ID for a given channel ID."""
    return await service.get_uploads_playlist_id(channel_id)

@router.get(
    "/playlists/{playlist_id}/items",
    response_model=PlaylistItemsListResponse,
    summary="List Playlist Items",
)
async def list_playlist_items(
    playlist_id: str,
    page_token: str = Query(None, description="Page token for pagination"),
    max_results: int = Query(50, ge=1, le=50, description="Max results per page"),
    service: YouTubeBusinessService = Depends(get_youtube_business_service),
) -> PlaylistItemsListResponse:
    """Fetch a page of items from the uploads or any playlist."""
    return await service.get_playlist_items(playlist_id, page_token, max_results)

@router.get(
    "/videos/{video_id}",
    response_model=VideosListResponse,
    summary="Get Video Details",
)
async def get_video_details(
    video_id: str,
    service: YouTubeBusinessService = Depends(get_youtube_business_service),
) -> VideosListResponse:
    """Retrieve metadata for a given video ID."""
    return await service.get_video_details(video_id)

@router.get(
    "/videos/{video_id}/comments",
    response_model=CommentThreadsListResponse,
    summary="List Top-Level Comment Threads",
)
async def list_comments(
    video_id: str,
    page_token: str = Query(None, description="Page token for pagination"),
    max_results: int = Query(100, ge=1, le=100, description="Max results per page"),
    service: YouTubeBusinessService = Depends(get_youtube_business_service),
) -> CommentThreadsListResponse:
    """Fetch top-level comment threads for a given video ID."""
    return await service.get_comment_threads(video_id, page_token, max_results)

# Root endpoint health check
@router.get("/", summary="Health Check")
def root():
    return {"status": "ok"}
