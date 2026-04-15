"""Global exception handler middleware.

Catches unhandled exceptions and returns structured JSON error responses
instead of raw 500 HTML pages.
"""

import logging
import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_id = id(exc)
    logger.error(
        "unhandled exception error_id=%d method=%s path=%s",
        error_id,
        request.method,
        request.url.path,
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again.",
            "error_id": error_id,
            "path": str(request.url.path),
        },
    )


class ErrorContext:
    """Utility for building structured error responses."""

    @staticmethod
    def validation_error(
        detail: str, field: str | None = None
    ) -> dict[str, str | None]:
        return {
            "error": "validation_error",
            "message": detail,
            "field": field,
        }

    @staticmethod
    def not_found(resource: str, resource_id: str) -> dict[str, str]:
        return {
            "error": "not_found",
            "message": f"{resource} '{resource_id}' not found",
            "resource": resource,
            "resource_id": resource_id,
        }

    @staticmethod
    def rate_limited(retry_after_seconds: int = 60) -> dict[str, str | int]:
        return {
            "error": "rate_limited",
            "message": "Too many requests. Please slow down.",
            "retry_after_seconds": retry_after_seconds,
        }

    @staticmethod
    def format_traceback(exc: Exception) -> str:
        return "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
