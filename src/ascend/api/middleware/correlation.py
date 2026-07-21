"""Correlation ID middleware.

Every request receives an X-Correlation-ID. If the client sends one,
it is reused. Otherwise, a new UUID v4 is generated.

The ID is injected into:
  - request.state.correlation_id
  - response headers
  - logs (via request.state)
"""

import uuid
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

CORRELATION_HEADER = "X-Correlation-ID"


class CorrelationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        correlation_id = request.headers.get(CORRELATION_HEADER)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers[CORRELATION_HEADER] = correlation_id
        return response
