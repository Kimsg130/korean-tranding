"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
from typing import Dict, List

from sqlalchemy import update
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

    async def update_korean_wave_status(self, videos_data: List[Dict]) -> None:
        """
        비디오의 한류 상태를 bulk 업데이트합니다.
        - videos_data: List[Dict] 형태로 각 Dict는 video_id, korean_wave_yn, reason 필드를 포함합니다.
          예: [{'video_id': 'abcde', 'korean_wave_yn': 'Y', 'reason': '한류 콘텐츠입니다'}]
        - reason 필드는 YoutubeVideo 테이블의 identify_reason 필드로 매핑됩니다.
        """
        if not videos_data:
            return
            
        async with self._session_factory() as session:
            # 일괄 업데이트를 위한 효율적인 방법
            # 데이터 처리
            for video_data in videos_data:
                if 'video_id' not in video_data:
                    continue
                
                update_values = {}
                if 'korean_wave_yn' in video_data:
                    update_values['korean_wave_yn'] = video_data['korean_wave_yn']
                if 'reason' in video_data:
                    update_values['identify_reason'] = video_data['reason']

                if update_values:
                    # 각 비디오에 대해 개별적인 업데이트 실행 (BULK 처리)
                    stmt = update(YoutubeVideo).where(
                        YoutubeVideo.video_id == video_data['video_id']
                    ).values(**update_values)
                    
                    await session.execute(stmt)
            
            # 한 번의 커밋으로 모든 변경사항 저장
            await session.commit()

    async def update_sentiment_for_comments(self, comment_data_list: List[Dict]) -> None:
        if not comment_data_list:
            return

        async with self._session_factory() as session:
            # 일괄 업데이트를 위한 효율적인 방법
            # 데이터 처리
            for comment_data in comment_data_list:
                if 'comment_id' not in comment_data:
                    continue

                update_values = {}
                if 'sentiment' in comment_data:
                    update_values['sentiment'] = comment_data['sentiment']
                if 'keywords' in comment_data:
                    update_values['key_words'] = comment_data['keywords']
                update_values['extract_yn'] = "Y"

                if update_values:
                    # 각 비디오에 대해 개별적인 업데이트 실행 (BULK 처리)
                    stmt = update(YoutubeComment).where(
                        YoutubeComment.comment_id == comment_data['comment_id']
                    ).values(**update_values)

                    await session.execute(stmt)

            # 한 번의 커밋으로 모든 변경사항 저장
            await session.commit()



    async def update_korean_wave_status_optimized(self, videos_data: List[Dict]) -> None:
        """
        비디오의 한류 상태를 하나의 IN 쿼리로 최적화하여 업데이트합니다.
        비디오 수가 매우 많을 때 유용한 방법입니다.
        
        참고: 이 메서드는 모든 비디오에 동일한 korean_wave_yn와 동일한 identify_reason이 적용될 때 사용됩니다.
        다양한 값을 각기 다른 비디오에 적용해야 할 경우 update_korean_wave_status를 사용하세요.
        """
        if not videos_data:
            return
            
        # video_id 목록 추출
        video_ids = [data['video_id'] for data in videos_data if 'video_id' in data]
        
        if not video_ids:
            return
            
        # 모든 비디오에 적용할 값이 같다고 가정
        # 첫 번째 항목의 값을 사용
        sample_data = videos_data[0]
        update_values = {}
        
        if 'korean_wave_yn' in sample_data:
            update_values['korean_wave_yn'] = sample_data['korean_wave_yn']
        if 'reason' in sample_data:
            update_values['identify_reason'] = sample_data['reason']
            
        if not update_values:
            return
            
        async with self._session_factory() as session:
            # IN 절을 사용한 단일 업데이트 쿼리
            stmt = update(YoutubeVideo).where(
                YoutubeVideo.video_id.in_(video_ids)
            ).values(**update_values)
            
            await session.execute(stmt)
            await session.commit()
