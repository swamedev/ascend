"""ASCEND_ERROR API integration.

Wraps the adapter error_mapper for use in FastAPI exception handlers.
Consolidated _code_to_status mapping for use by all routers (A1.7).
"""

from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse

from ascend.adapter.error_mapper import map_error as adapter_map_error

_CODE_STATUS_MAP: dict[str, int] = {
    "NOT_FOUND": 404,
    "VALIDATION_ERROR": 422,
    "CONFLICT": 409,
    "MISSION_ALREADY_STARTED": 409,
    "MISSION_LOCKED": 409,
    "COMPETENCY_LOCKED": 409,
    "INTERNAL_ERROR": 500,
}


def _code_to_status(code: str) -> int:
    return _CODE_STATUS_MAP.get(code, 500)


def handle_adapter_result(result: dict[str, Any]) -> Any:
    if result.get("success"):
        return result["data"]
    error = result.get("error", {})
    code = error.get("code", "INTERNAL_ERROR")
    status = _code_to_status(code)
    return JSONResponse(status_code=status, content=result)


def api_error_response(status_code: int, error_body: dict[str, Any]) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=error_body,
        headers={"Content-Type": "application/json"},
    )


def python_error_to_ascend(request: Request, exc: Exception) -> JSONResponse:
    corr_id = getattr(request.state, "correlation_id", None)
    envelope = adapter_map_error(exc, correlation_id=corr_id)
    status = _extract_status(envelope)
    return api_error_response(status, envelope)


def _extract_status(envelope: dict[str, Any]) -> int:
    error = envelope.get("error", {})
    code = error.get("code", "INTERNAL_ERROR")
    return _code_to_status(code)
