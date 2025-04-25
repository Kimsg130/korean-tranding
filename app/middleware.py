"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response

# 1) 로거 설정 (실제 사용 시 로깅 설정 파일에서 구성하세요)
logger = logging.getLogger("app.middleware")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # 요청 시작 시각 기록
        start_time = time.time()

        # 요청 정보 로깅
        client_host = request.client.host if request.client else "unknown"
        logger.info(f"→ {request.method} {request.url.path} from {client_host}")

        # 실제 핸들러(다음 미들웨어 혹은 라우터) 호출
        response = await call_next(request)

        # 응답 완료 후, 처리 시간 계산
        elapsed = (time.time() - start_time) * 1000  # ms 단위
        logger.info(
            f"← {request.method} {request.url.path} status={response.status_code} "
            f"in {elapsed:.2f}ms"
        )

        return response
