"""Request logging middleware.

Logs method, path, status, latency, and correlation ID.
No sensitive data is logged.
"""

import logging
import time
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

logger = logging.getLogger(__name__)


class RequestLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start

        corr_id = getattr(request.state, "correlation_id", "-")
        logger.info(
            "[%s] %s %s %s (%.1fms)",
            corr_id[:8],
            request.method,
            request.url.path,
            response.status_code,
            elapsed * 1000,
        )
        return response
