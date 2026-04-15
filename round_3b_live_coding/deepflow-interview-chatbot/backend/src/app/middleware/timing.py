"""Request timing middleware.

Adds X-Response-Time header to all responses and logs slow requests.
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

SLOW_REQUEST_THRESHOLD_MS = 5000


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        t0 = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        response.headers["X-Response-Time"] = f"{elapsed_ms:.1f}ms"

        if elapsed_ms > SLOW_REQUEST_THRESHOLD_MS:
            logger.warning(
                "slow request method=%s path=%s time_ms=%.1f",
                request.method,
                request.url.path,
                elapsed_ms,
            )

        return response
