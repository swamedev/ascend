"""Auth router — register and login endpoints."""

import secrets

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter
from ascend.api.errors import api_error_response

router = APIRouter(tags=["auth"])

_tokens: dict[str, str] = {}


class AuthRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Builder username")


@router.post("/auth/register")
def register(
    body: AuthRequest,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    existing = adapter.get_builder_by_username(body.username)
    if existing.get("success") and existing.get("data"):
        return JSONResponse(
            status_code=409,
            content=api_error_response(
                409,
                {
                    "success": False,
                    "error": {
                        "code": "CONFLICT",
                        "message": f"Builder '{body.username}' already exists",
                        "details": None,
                        "correlationId": "",
                        "timestamp": __import__("datetime").datetime.now().isoformat(),
                    },
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                },
            ),
        )

    result = adapter.create_builder(username=body.username)
    if not result.get("success"):
        error = result.get("error", {})
        code = error.get("code", "INTERNAL_ERROR")
        status = _code_to_status(code)
        return JSONResponse(status_code=status, content=result)

    builder = result["data"]
    token = secrets.token_urlsafe(32)
    _tokens[builder["id"]] = token
    return {
        "builderId": builder["id"],
        "token": token,
    }


@router.post("/auth/login")
def login(
    body: AuthRequest,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    existing = adapter.get_builder_by_username(body.username)
    if not existing.get("success") or not existing.get("data"):
        return JSONResponse(
            status_code=404,
            content=api_error_response(
                404,
                {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Builder '{body.username}' not found",
                        "details": None,
                        "correlationId": "",
                        "timestamp": __import__("datetime").datetime.now().isoformat(),
                    },
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                },
            ),
        )

    builder = existing["data"]
    token = secrets.token_urlsafe(32)
    _tokens[builder["id"]] = token
    return {
        "builderId": builder["id"],
        "token": token,
    }


def _code_to_status(code: str) -> int:
    mapping = {
        "NOT_FOUND": 404,
        "VALIDATION_ERROR": 422,
        "CONFLICT": 409,
        "INTERNAL_ERROR": 500,
    }
    return mapping.get(code, 500)

    result = adapter.create_builder(username=body.username)
    if not result.get("success"):
        return handle_adapter_result(result)

    builder = result["data"]
    return {
        "builderId": builder["id"],
        "token": f"temp-token-{builder['id']}",
    }
