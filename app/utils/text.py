"""
Author: sg.kim
Date: 2025-04-25
Description:
"""
import codecs, re
import json
from datetime import datetime, timezone


class TextUtils:
    @staticmethod
    def parse_ts(ts: str) -> datetime:
        # "2025-04-25T04:00:44Z" → offset-aware
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        # UTC 기준 naive datetime으로 변환
        return dt.astimezone(timezone.utc).replace(tzinfo=None)

    @staticmethod
    def escape_control_chars(s: str) -> str:
        # 모든 제어문자를 \uXXXX 또는 \xXX 형태로 이스케이프
        return s.encode("unicode_escape").decode("ascii")

    @staticmethod
    def unescape_control_chars(s: str) -> str:
        # 저장된 이스케이프 문자열을 원래 텍스트로 복원
        return codecs.decode(s, "unicode_escape")

    @staticmethod
    def parse_response_with_regex(raw: str):
        # 1) ```json 또는 ``` 제거
        no_fence = re.sub(r"```(?:json)?\s*", "", raw)
        # 2) 남은 트레일링 ``` 제거
        no_fence = re.sub(r"\s*```$", "", no_fence)

        json_str = no_fence.replace("'", '"')

        # 3) JSON 파싱
        return json.loads(json_str)