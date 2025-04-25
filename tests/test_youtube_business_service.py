"""
Tests for YouTube Router endpoints
Author: sg.kim
Date: 2025-04-24
"""
import pytest

import pytest_asyncio
from fastapi import HTTPException
from app.service.business.youtube import YouTubeBusinessService
from app.model.youtube.response import (
    ChannelItem,
    PlaylistItemsListResponse,
    VideosListResponse,
    CommentThreadsListResponse,
)

# Helper to create a dummy Response-like object
class FakeResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data


@pytest_asyncio.fixture
async def service():
    svc = YouTubeBusinessService()
    yield svc
    await svc.close()

@pytest.mark.asyncio
async def test_get_channel_by_handle_success(monkeypatch, service):
    fake_data = {
        "kind": "youtube#channelListResponse",
        "etag": "etag",
        "items": [
            {"id": "UC123", "snippet": {"title": "Test", "description": "Desc", "publishedAt": "2023-01-01T00:00:00Z", "country": "KR"}, "contentDetails": {"relatedPlaylists": {"uploads": "UU123"}}}
        ],
        "regionCode": "KR",
        "pageInfo": {"totalResults": 1, "resultsPerPage": 1},
        "nextPageToken": None
    }
    async def fake_get(path, params=None):
        return FakeResponse(fake_data)
    monkeypatch.setattr(service.client, 'get', fake_get)

    channel = await service.get_channel_by_handle("@handle")
    assert isinstance(channel, ChannelItem)
    assert channel.id == "UC123"

@pytest.mark.asyncio
async def test_get_channel_by_handle_not_found(monkeypatch, service):
    fake_data = {
        "kind": "youtube#channelListResponse",
        "etag": "etag",
        "items": [],
        "regionCode": "KR",
        "pageInfo": {"totalResults": 0, "resultsPerPage": 0},
        "nextPageToken": None
    }
    async def fake_get(path, params=None):
        return FakeResponse(fake_data)
    monkeypatch.setattr(service.client, 'get', fake_get)

    with pytest.raises(HTTPException) as exc:
        await service.get_channel_by_handle("@bad")
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_get_uploads_playlist_id(monkeypatch, service):
    fake_data = {
        "kind": "youtube#channelListResponse",
        "etag": "etag",
        "items": [
            {
                "id": "UC123",
                "snippet": {
                    "title": "Test Channel",
                    "description": "",
                    "publishedAt": "2023-01-01T00:00:00Z",
                    "country": "KR"
                },
                "contentDetails": {
                    "relatedPlaylists": {
                        "uploads": "UU123"
                    }
                }
            }
        ],
        "regionCode": "KR",
        "pageInfo": {"totalResults": 1, "resultsPerPage": 1},
        "nextPageToken": None
    }
    async def fake_get(path, params=None):
        return FakeResponse(fake_data)
    monkeypatch.setattr(service.client, 'get', fake_get)

    uploads = await service.get_uploads_playlist_id("UC123")
    assert uploads == "UU123"

@pytest.mark.asyncio
async def test_get_playlist_items(monkeypatch, service):
    fake_data = {"kind": "youtube#playlistItemListResponse", "etag": "etag", "items": [], "nextPageToken": None, "prevPageToken": None, "pageInfo": {"totalResults": 0, "resultsPerPage": 0}}
    async def fake_get(path, params=None):
        return FakeResponse(fake_data)
    monkeypatch.setattr(service.client, 'get', fake_get)

    resp = await service.get_playlist_items("PL123", page_token="tok", max_results=10)
    assert isinstance(resp, PlaylistItemsListResponse)
    assert resp.pageInfo["resultsPerPage"] == 0

@pytest.mark.asyncio
async def test_get_video_details(monkeypatch, service):
    fake_data = {"kind": "youtube#videoListResponse", "etag": "etag", "items": [], "nextPageToken": None, "prevPageToken": None, "pageInfo": {"totalResults": 0, "resultsPerPage": 0}}
    async def fake_get(path, params=None):
        return FakeResponse(fake_data)
    monkeypatch.setattr(service.client, 'get', fake_get)

    resp = await service.get_video_details("VID123")
    assert isinstance(resp, VideosListResponse)
    assert resp.pageInfo["totalResults"] == 0

@pytest.mark.asyncio
async def test_get_comment_threads(monkeypatch, service):
    fake_data = {"kind": "youtube#commentThreadListResponse", "etag": "etag", "items": [], "nextPageToken": None, "prevPageToken": None, "pageInfo": {"totalResults": 0, "resultsPerPage": 0}}
    async def fake_get(path, params=None):
        return FakeResponse(fake_data)
    monkeypatch.setattr(service.client, 'get', fake_get)

    resp = await service.get_comment_threads("VID123", page_token="tok", max_results=5)
    assert isinstance(resp, CommentThreadsListResponse)
    assert resp.pageInfo["resultsPerPage"] == 0

@pytest.mark.asyncio
async def test_close():
    svc = YouTubeBusinessService()
    await svc.close()
