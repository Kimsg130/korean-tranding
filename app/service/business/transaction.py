"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
from typing import Dict, List

from sqlmodel import select

from app.database import get_async_database
from app.schema.public import YoutubeVideo, YoutubeComment


class TransactionBusinessService:
    def __init__(self):
        self._session_factory = get_async_database()

    async def insert_youtube_video(self, video_data: Dict) -> None:
        async with self._session_factory() as session:
            # merge 사용: PK(video_id) 가 있으면 UPDATE, 없으면 INSERT
            obj = YoutubeVideo(**video_data)
            merged = await session.merge(obj)
            session.add(merged)
            await session.commit()

    async def insert_youtube_comments_bulk(self, comments_data: List[Dict]) -> None:
        """
        한 비디오에 대한 다수의 댓글을 한 번에 insert 혹은 upsert 합니다.
        - comments_data: List[Dict] 형태로 YoutubeComment 필드들을 제공받습니다.
        """
        async with self._session_factory() as session:
            # objects 리스트에 모델 인스턴스 생성
            objects = [YoutubeComment(**data) for data in comments_data]
            # merge_all 은 없으므로 일괄 merge loop
            for obj in objects:
                await session.merge(obj)
            await session.commit()