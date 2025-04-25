# 🎥✨ YouTube 서비스 및 테스트 슈트 🧪

이 저장소에는 🚀 `httpx`를 활용한 비동기 🌐 `YouTubeBusinessService` 구현과 🧑‍🔬 pytest 기반의 종합 테스트 슈트가 포함되어 있어요.

## 🗂️ 프로젝트 구조

```
└── app/
    ├── service/
    │   └── youtube.py            # 🎬 YouTubeBusinessService 구현
    └── model/
        └── youtube/
            └── response.py       # 📝 Pydantic 모델

└── tests/
    ├── conftest.py              # 🔧 환경 변수 픽스처
    └── test_youtube_service.py  # 🧪 테스트 케이스
```

## 📋 사전 요구사항 ✅

- 🐍 Python 3.9 이상
- 🧪 `pytest` 및 `pytest-asyncio`
- 🌐 `httpx` (비동기 HTTP)
- 🔥 `fastapi` (HTTPException 처리)

## 🔧 환경 변수 🌐

테스트 슈트는 `tests/conftest.py`에서 다음 🔑 변수들을 자동 설정합니다:

- `YOUTUBE_API_KEY` — 🎫 API 키
- `YOUTUBE_API_BASE_URL` — 🏠 API 베이스 URL (`https://youtube.googleapis.com/youtube/v3`)

실제 운영 환경에서는 터미널에:

```bash
export YOUTUBE_API_KEY="<your_api_key>"
export YOUTUBE_API_BASE_URL="https://youtube.googleapis.com/youtube/v3"
```

## 🚀 YouTubeBusinessService 개요 📦

`app/service/youtube.py`의 `YouTubeBusinessService` 클래스는:

- `get_channel_by_handle(handle: str) → ChannelItem` 🕵️‍♂️ 채널 조회
- `get_uploads_playlist_id(channel_id: str) → str` 📂 업로드 플레이리스트 ID 반환
- `get_playlist_items(playlist_id: str, page_token: str?, max_results: int) → PlaylistItemsListResponse` 🎞️ 리스트 조회
- `get_video_details(video_id: str) → VideosListResponse` 📹 비디오 상세
- `get_comment_threads(video_id: str, page_token: str?, max_results: int) → CommentThreadsListResponse` 💬 댓글 스레드 조회

데이터가 없으면 `HTTPException(404)` 🚫 발생

## ▶️ 테스트 실행 방법 🎯

1. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-asyncio
   ```
2. 테스트 실행:
   ```bash
   pytest
   ```

테스트 커버리지:

- 📌 채널 조회 (성공/실패)
- 📌 업로드 리스트 ID 확인
- 📌 페이지네이션 & 빈 결과 처리
- 📌 클라이언트 세션 종료 확인 ✅

## 🛠️ 테스트 확장 가이드 🔄

1. `tests/test_youtube_service.py`에 새 🧪 비동기 함수 추가
2. `monkeypatch`로 `service.client.get` stub → `FakeResponse` 반환
3. 모델/예외 발생 여부 `assert`하기

---

*🗓️ 생성일: 2025-04-24*

