"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
from pydantic import BaseModel


# 1) 공통 에러 응답 포맷 정의
class ErrorResponse(BaseModel):
    code: int          # HTTP status code
    error: str         # 에러 타입 or message key
    message: str       # 사용자용 메시지
    details: dict = {} # 추가 정보 (optional)
