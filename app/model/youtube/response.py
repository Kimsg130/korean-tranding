"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
from typing import List, Optional
from pydantic import BaseModel, Field

# 1. channels.list response
class ChannelContentDetailsRelatedPlaylists(BaseModel):
    uploads: str

class ChannelContentDetails(BaseModel):
    relatedPlaylists: ChannelContentDetailsRelatedPlaylists

class ChannelSnippet(BaseModel):
    title: str
    description: Optional[str] = None
    publishedAt: Optional[str] = None
    country: Optional[str] = None

class ChannelItem(BaseModel):
    id: str
    snippet: Optional[ChannelSnippet] = None
    contentDetails: Optional[ChannelContentDetails] = None

class ChannelsListResponse(BaseModel):
    kind: str
    etag: str
    items: List[ChannelItem]
    regionCode: Optional[str] = None
    pageInfo: Optional[dict] = None
    nextPageToken: Optional[str] = None


# 2. playlistItems.list response
class PlaylistItemContentDetails(BaseModel):
    videoId: str
    videoPublishedAt: Optional[str] = None

class PlaylistItemSnippet(BaseModel):
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: dict
    channelTitle: str
    playlistId: str
    position: int

class PlaylistItem(BaseModel):
    kind: str
    etag: str
    id: Optional[str] = None
    snippet: PlaylistItemSnippet
    contentDetails: PlaylistItemContentDetails

class PlaylistItemsListResponse(BaseModel):
    kind: str
    etag: str
    items: List[PlaylistItem]
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    pageInfo: dict


# 3. videos.list response
class VideoStatistics(BaseModel):
    viewCount: Optional[str] = None
    likeCount: Optional[str] = None
    favoriteCount: Optional[str] = None
    commentCount: Optional[str] = None

class VideoStatus(BaseModel):
    uploadStatus: Optional[str] = None
    privacyStatus: Optional[str] = None
    license: Optional[str] = None

class VideoContentDetails(BaseModel):
    duration: Optional[str] = None
    dimension: Optional[str] = None
    definition: Optional[str] = None
    caption: Optional[str] = None

class VideoSnippet(BaseModel):
    publishedAt: str
    channelId: str
    title: str
    description: str
    thumbnails: dict
    channelTitle: str
    tags: Optional[List[str]] = None
    categoryId: Optional[str] = None
    liveBroadcastContent: Optional[str] = None
    defaultLanguage: Optional[str] = None

class VideoItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: VideoSnippet
    contentDetails: Optional[VideoContentDetails] = None
    statistics: Optional[VideoStatistics] = None
    status: Optional[VideoStatus] = None

class VideosListResponse(BaseModel):
    kind: str
    etag: str
    items: List[VideoItem]
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    pageInfo: dict


# 4. commentThreads.list response
class TopLevelCommentSnippet(BaseModel):
    authorDisplayName: str
    authorProfileImageUrl: str
    authorChannelId: dict
    textDisplay: str
    parentId: Optional[str] = None
    viewerRating: Optional[str] = None
    likeCount: Optional[int] = None
    publishedAt: str
    updatedAt: str

class TopLevelComment(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: TopLevelCommentSnippet

class CommentThreadSnippet(BaseModel):
    videoId: str
    topLevelComment: TopLevelComment
    canReply: bool
    totalReplyCount: int
    isPublic: bool

class CommentReply(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: TopLevelCommentSnippet

class CommentReplies(BaseModel):
    comments: List[CommentReply]

class CommentThreadItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: CommentThreadSnippet
    replies: Optional[CommentReplies] = None

class CommentThreadsListResponse(BaseModel):
    kind: Optional[str] = None
    etag: Optional[str] = None
    items: Optional[List[CommentThreadItem]] = None
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None
    pageInfo: Optional[dict] = None
