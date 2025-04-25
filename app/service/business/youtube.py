"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
import os
from typing import Optional, List
import httpx

from fastapi import HTTPException

from app.config import Settings
from app.model.youtube.response import (
    ChannelsListResponse,
    PlaylistItemsListResponse,
    VideosListResponse,
    CommentThreadsListResponse,
    ChannelItem,
)

settings: Settings = Settings()

class YouTubeBusinessService:
    def __init__(self):
        # 1. Try to use provided settings
        if settings:
            self.api_key = settings.youtube_api_key
            self.base_url = settings.youtube_api_base_url
        # 2. Fall back to direct environment variables
        else:
            self.api_key = os.environ.get("YOUTUBE_API_KEY")
            self.base_url = os.environ.get("YOUTUBE_API_BASE_URL")
            
        # Validate required settings
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable is not set")
        if not self.base_url:
            raise ValueError("YOUTUBE_API_BASE_URL environment variable is not set")
            
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def get_channel_by_handle(self, handle: str) -> ChannelItem:
        """
        Retrieve a channel by its handle (e.g., @BandJannabi).
        Returns the first ChannelItem.
        """
        params = {
            "part": "id,snippet,contentDetails",
            "forHandle": handle,
            "key": self.api_key,
        }
        resp = await self.client.get("/channels", params=params)
        data = resp.json()
        parsed = ChannelsListResponse.model_validate(data)
        if not parsed.items:
            raise HTTPException(status_code=404, detail="Channel not found")
        return parsed.items[0]

    async def get_uploads_playlist_id(self, channel_id: str) -> str:
        """
        Given a channel ID, return the uploads playlist ID.
        """
        params = {
            "part": "contentDetails",
            "id": channel_id,
            "key": self.api_key,
        }
        resp = await self.client.get("/channels", params=params)
        data = resp.json()
        parsed = ChannelsListResponse.model_validate(data)
        if not parsed.items:
            raise HTTPException(status_code=404, detail="Channel not found")
        return parsed.items[0].contentDetails.relatedPlaylists.uploads

    async def get_playlist_items(
        self,
        playlist_id: str,
        page_token: Optional[str] = None,
        max_results: int = 50,
    ) -> PlaylistItemsListResponse:
        """
        Fetch a page of playlist items from the given playlist ID.
        """
        params = {
            "part": "snippet,contentDetails",
            "playlistId": playlist_id,
            "maxResults": max_results,
            "key": self.api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = await self.client.get("/playlistItems", params=params)
        data = resp.json()
        return PlaylistItemsListResponse.model_validate(data)

    async def get_video_details(self, video_id: str) -> VideosListResponse:
        """
        Retrieve metadata for a single video.
        """
        params = {
            "part": "snippet,contentDetails,statistics,status",
            "id": video_id,
            "key": self.api_key,
        }
        resp = await self.client.get("/videos", params=params)
        data = resp.json()
        return VideosListResponse.model_validate(data)

    async def get_comment_threads(
        self,
        video_id: str,
        page_token: Optional[str] = None,
        max_results: int = 100,
    ) -> CommentThreadsListResponse:
        """
        Fetch a page of top-level comment threads for a video.
        """
        params = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": max_results,
            "textFormat": "plainText",
            "order": "time",
            "key": self.api_key,
        }
        if page_token:
            params["pageToken"] = page_token

        resp = await self.client.get("/commentThreads", params=params)
        data = resp.json()
        return CommentThreadsListResponse.model_validate(data)

    async def close(self):
        await self.client.aclose()
