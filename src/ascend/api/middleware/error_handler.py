"""Global exception handler middleware.

Every exception is caught and returned as an ASCEND_ERROR envelope.
No stack traces leak to the client. No HTML is ever returned.
"""

from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from ascend.api.errors import python_error_to_ascend


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            return python_error_to_ascend(request, exc)
