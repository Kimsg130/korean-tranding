"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
from typing import List, Dict, Optional, Tuple

from sqlalchemy import Null
from sqlalchemy.sql.operators import is_
from sqlmodel import select, and_, col

from app.database import get_async_database
from app.schema.public import YoutubeComment, YoutubeVideo


class SearchBusinessService:
    def __init__(self):
        self._session_factory = get_async_database()

    async def get_videos(self, previous_id: Optional[str], page_size: int) -> Tuple[List[YoutubeVideo], Optional[str]]:

        conditions = [col(YoutubeVideo.korean_wave_yn).is_(None)]

        if previous_id:
            conditions.append(YoutubeVideo.video_id > previous_id)

        async with self._session_factory() as session:
            async with session.begin():
                # 1) 해당 비디오 페이징 조회
                stmt = (
                    select(YoutubeVideo)
                    .where(
                        and_(*conditions)
                    )
                    .order_by(YoutubeVideo.video_id)
                    .limit(page_size)
                )
                result = await session.execute(stmt)
                videos: List[YoutubeVideo] = result.scalars().all()

        # 마지막 video_id 계산
        last_id: Optional[str]
        if videos:
            last_id = videos[-1].video_id
        else:
            last_id = None

        return videos, last_id


    async def get_comments_for_video(self, previous_id: Optional[str], page_size: int) -> Tuple[List[YoutubeComment], Optional[str]]:
        """
        video_id에 속한 댓글(최상위 + 답글)을 조회 후 반환
        """

        async with self._session_factory() as session:
            async with session.begin():
                # 1) 해당 비디오의 모든 댓글 조회
                stmt = (
                    select(YoutubeComment)
                    .join(YoutubeComment.video)  # join to YoutubeVideo
                    .where(
                        and_(
                            YoutubeVideo.korean_wave_yn == 'Y',
                            YoutubeComment.extract_yn == 'N',
                            *(
                                [YoutubeComment.comment_id > previous_id]
                                if previous_id is not None else []
                            )
                        )
                    )
                    .order_by(YoutubeComment.comment_id)
                    .limit(page_size)
                )
                result = await session.execute(stmt)
                all_comments: List[YoutubeComment] = result.scalars().all()

        # 마지막 video_id 계산
        last_id: Optional[str]
        if all_comments:
            last_id = all_comments[-1].comment_id
        else:
            last_id = None

        return all_comments, last_id
