"""
Author: sg.kim
Date: 2025-04-25
Description:
"""

from typing import Optional, List
from datetime import datetime

from sqlalchemy import MetaData
from sqlmodel import Field, SQLModel, Relationship

metadata = MetaData(schema="public")

class YoutubeVideo(SQLModel, table=True):
    __tablename__ = "youtube_video"
    __table_args__ = {"comment": "youtube video"}  # 테이블 주석

    metadata = metadata

    video_id: str = Field(
        ...,
        primary_key=True,
        sa_column_kwargs={"comment": "비디오ID"}  # COMMENT ON COLUMN ... IS '비디오ID';
    )
    published_at: datetime = Field(
        ...,
        sa_column_kwargs={"comment": "개시 날자"}  # COMMENT ON COLUMN ... IS '개시 날자';
    )
    channel_id: str = Field(
        ...,
        sa_column_kwargs={"comment": "채널ID"}  # COMMENT ON COLUMN ... IS '채널ID';
    )
    title: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "제목"}  # COMMENT ON COLUMN ... IS '제목';
    )
    description: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "설명"}  # COMMENT ON COLUMN ... IS '설명';
    )
    channel_title: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "채널 타이틀"}  # COMMENT ON COLUMN ... IS '채널 타이틀';
    )
    live_broadcast_content: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": (
            "동영상이 예정된/진행 중인 라이브 방송인지를 나타냅니다. "
            "라이브가 아니면 'none'"  # COMMENT ON COLUMN ... IS '...';
        )}
    )
    default_language: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment":"video 리소스의 snippet.title 및 snippet.description 텍스트의 언어"}
    )
    view_count: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "동영상의 조회수입니다."}  # COMMENT ON COLUMN ... IS '동영상의 조회수입니다.';
    )
    like_count: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "동영상에 좋아요를 표시한 사용자 수입니다."}  # COMMENT ON COLUMN ... IS '동영상에 좋아요를 표시한 사용자 수입니다.';
    )
    comment_count: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "동영상의 댓글 수입니다."}  # COMMENT ON COLUMN ... IS '동영상의 댓글 수입니다.';
    )
    korean_wave_yn: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "한류 관련 영상 Y/N, Null일 떄는 아직 판별 전"}
    )
    identify_reason: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "한류 판별 이유"}
    )

    # Relationship with YoutubeComment
    comments: List["YoutubeComment"] = Relationship(back_populates="video")

    def __repr__(self):
        return f"<YoutubeVideo(video_id='{self.video_id}', title='{self.title}')>"

class YoutubeComment(SQLModel, table=True):
    __tablename__ = "youtube_comment"
    __table_args__ = {"comment": "유튜브 댓글"}

    metadata = metadata

    comment_id: str = Field(
        ...,
        primary_key=True,
        sa_column_kwargs={"comment": "댓글ID"}  # COMMENT ON COLUMN ... IS '댓글ID';
    )
    video_id: str = Field(
        ...,
        foreign_key="youtube_video.video_id",
        sa_column_kwargs={"comment": "비디오ID"}  # COMMENT ON COLUMN ... IS '비디오ID';
    )
    parent_comment_id: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "상위 댓글ID"}  # COMMENT ON COLUMN ... IS '상위 댓글ID';
    )
    etag: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "etag"}  # COMMENT ON COLUMN ... IS 'etag';
    )
    author_display_name: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "작성자 이름"}  # COMMENT ON COLUMN ... IS '작성자 이름';
    )
    author_channel_id: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "작성자 채널ID"}  # COMMENT ON COLUMN ... IS '작성자 채널ID';
    )
    text_display: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "댓글의 텍스트입니다. 텍스트는 일반 텍스트 또는 HTML로 검색할 수 있습니다."}
    )
    published_at: Optional[datetime] = Field(
        None,
        sa_column_kwargs={"comment": "댓글이 처음 게시된 날짜 및 시간입니다."}
    )
    updated_at: Optional[datetime] = Field(
        None,
        sa_column_kwargs={"comment": "의견이 마지막으로 업데이트된 날짜 및 시간입니다."}
    )
    viewer_rating: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "시청자가 댓글에 긍정적 평가를 한 경우 like, 그 외에는 none"}
    )
    like_count: Optional[int] = Field(
        None,
        sa_column_kwargs={"comment": "댓글에 받은 총 좋아요 (긍정적인 평점) 수입니다."}
    )
    sentiment: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "감성분석결과 (긍정/부정/중립)"}
    )
    key_words: Optional[str] = Field(
        None,
        sa_column_kwargs={"comment": "해당 댓글의 키워드(','로 분리)"}
    )
    extract_yn: str = Field(
        default="N",
        sa_column_kwargs={"comment": "추출 수행 Y/N"}
    )

    # Relationship with YoutubeVideo
    video: "YoutubeVideo" = Relationship(back_populates="comments")

    def __repr__(self):
        return f"<YoutubeComment(comment_id='{self.comment_id}', author='{self.author_display_name}')>"