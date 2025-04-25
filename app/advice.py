"""
Author: sg.kim
Date: 2025-04-24
Description:
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import logging

from .config.exception import ErrorResponse


def register_exception_handlers(app: FastAPI):
    # 2) HTTPException 처리기
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logging.error(f"HTTPException: {exc.detail}")
        payload = ErrorResponse(
            code=exc.status_code,
            error=exc.__class__.__name__,
            message=exc.detail if isinstance(exc.detail, str) else "Bad Request",
            details={"headers": dict(exc.headers) if exc.headers else {}},
        )
        return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

    # 3) Pydantic 검증 오류 처리기
    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request: Request, exc: ValidationError):
        logging.error(f"ValidationError: {exc.errors()}")
        payload = ErrorResponse(
            code=422,
            error="ValidationError",
            message="입력값이 유효하지 않습니다.",
            details={"errors": exc.errors()},
        )
        return JSONResponse(status_code=422, content=payload.model_dump())

    # 4) 그 외 모든 Exception 처리기
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.exception(f"Unhandled exception occurred: {exc}")
        payload = ErrorResponse(
            code=500,
            error="InternalServerError",
            message="서버에서 알 수 없는 오류가 발생했습니다.",
            details={"errors": f"{exc}"},
        )
        return JSONResponse(status_code=500, content=payload.model_dump())