"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
import logging
from typing import Optional, List, Dict

from app.model.youtube.response import ChannelItem
from app.service.business.nlp import NlpBusinessService
from app.service.business.search import SearchBusinessService
from app.service.business.transaction import TransactionBusinessService
from app.service.business.youtube import YouTubeBusinessService
from app.utils.text import TextUtils


class YouTubeEndPointService:
    """
    Service layer for fetching Videos and Comments for a given YouTube channel handle.
    """
    def __init__(
        self,
        business_service: Optional[YouTubeBusinessService] = None,
        tx_service: Optional[TransactionBusinessService] = None,
        search_service: Optional[SearchBusinessService] = None,
        nlp_service: Optional[NlpBusinessService] = None,
    ):
        self.business = business_service or YouTubeBusinessService()
        self.tx = tx_service or TransactionBusinessService()
        self.search = search_service or SearchBusinessService()
        self.nlp = nlp_service or NlpBusinessService()

    async def fetch_all_videos_with_comments(
        self, handle: str, video_page_limit: int = 5
    ) -> Dict[str, str]:
        # 1) 채널 → 업로드 플레이리스트
        channel: ChannelItem = await self.business.get_channel_by_handle(handle)
        playlist_id = await self.business.get_uploads_playlist_id(channel.id)

        # 2) 비디오 ID 수집
        all_video_ids, next_token, pages = [], None, 0
        while pages < video_page_limit:
            resp = await self.business.get_playlist_items(
                playlist_id=playlist_id,
                page_token=next_token,
                max_results=50,
            )
            pages += 1
            all_video_ids += [item.contentDetails.videoId for item in resp.items]
            next_token = resp.nextPageToken
            if not next_token:
                break

        # 3) 비디오별 메타·댓글 fetch & 저장
        for vid in all_video_ids:
            # 3.1) 영상 메타
            vresp = await self.business.get_video_details(vid)
            item = vresp.items[0] if vresp.items else None
            if not item:
                continue

            vid_data = {
                "video_id": item.id,
                "published_at": TextUtils.parse_ts(item.snippet.publishedAt),
                "channel_id": item.snippet.channelId,
                "title": TextUtils.escape_control_chars(item.snippet.title),
                "description": TextUtils.escape_control_chars(item.snippet.description),
                "channel_title": item.snippet.channelTitle,
                "live_broadcast_content": item.snippet.liveBroadcastContent,
                "default_language": item.snippet.defaultLanguage,
                "view_count": item.statistics.viewCount if item.statistics else None,
                "like_count": item.statistics.likeCount if item.statistics else None,
                "comment_count": item.statistics.commentCount if item.statistics else None,
            }
            await self.tx.insert_youtube_video(vid_data)

            # 3.2) 댓글 + 답글 수집
            crep = await self.business.get_comment_threads(video_id=vid, max_results=100)
            batch: List[Dict] = []

            for thread in crep.items or []:
                top = thread.snippet.topLevelComment.snippet
                batch.append({
                    "comment_id": thread.id,
                    "video_id": thread.snippet.videoId,
                    "parent_comment_id": None,
                    "etag": thread.etag,
                    "author_display_name": top.authorDisplayName,
                    "author_channel_id": top.authorChannelId.get("value"),
                    "text_display": TextUtils.escape_control_chars(top.textDisplay),
                    "published_at": TextUtils.parse_ts(top.publishedAt),
                    "updated_at": TextUtils.parse_ts(top.updatedAt),
                    "viewer_rating": getattr(top, "viewerRating", None),
                    "like_count": getattr(top, "likeCount", None),
                })

                # 답글이 있으면 batch에 추가
                if thread.replies and thread.replies.comments:
                    for reply in thread.replies.comments:
                        r = reply.snippet
                        batch.append({
                            "comment_id": reply.id,
                            "video_id": thread.snippet.videoId,
                            "parent_comment_id": thread.id,
                            "etag": reply.etag,
                            "author_display_name": r.authorDisplayName,
                            "author_channel_id": r.authorChannelId.get("value"),
                            "text_display": TextUtils.escape_control_chars(r.textDisplay),
                            "published_at": TextUtils.parse_ts(r.publishedAt),
                            "updated_at": TextUtils.parse_ts(r.updatedAt),
                            "viewer_rating": getattr(r, "viewerRating", None),
                            "like_count": getattr(r, "likeCount", None),
                        })

            # 3.3) 한 번에 bulk insert/upsert
            if batch:
                await self.tx.insert_youtube_comments_bulk(batch)

        return {"detail": "추출이 완료되었습니다"}

    async def process_korean_wave_status(
            self, page_size: int = 50
    ) -> Dict[str, str]:
        """
        1) SearchBusinessService로 페이징 단위 videos 조회
        2) NlpBusinessService로 한류 여부 판정
        3) TransactionBusinessService로 결과 업데이트
        """


        print(f"page_size >> {page_size}")

        previous_id: Optional[str] = None
        while True:
            videos, last_id = await self.search.get_videos(previous_id, page_size)
            print(f"SELECT COUNT>> {len(videos)}")
            if not videos:
                break
            # NLP 처리
            results = await self.nlp.identify_korean_wave_for_video(videos)
            print(f"PROCESS COUNT>> {len(results)}")
            # DB 업데이트
            await self.tx.update_korean_wave_status(results)
            previous_id = last_id
            if previous_id is None:
                break

        return {"detail": "한류 여부 처리 완료"}


    async def process_sentiment_for_comment(
            self, page_size: int = 50
    ) -> Dict[str, str]:

        print(f"page_size >> {page_size}")

        previous_id: Optional[str] = None
        while True:
            comments, last_id = await self.search.get_comments_for_video(previous_id, page_size)
            print(f"SELECT COUNT>> {len(comments)}")
            if not comments:
                break
            # NLP 처리
            results = await self.nlp.identify_sentiment_for_comments(comments)
            print(f"PROCESS COUNT>> {len(results)}")
            # DB 업데이트
            await self.tx.update_sentiment_for_comments(results)
            previous_id = last_id
            if previous_id is None:
                break

        return {"detail": "감성 분석 및 키워드 추출 완료"}

    async def close(self):
        await self.business.close()