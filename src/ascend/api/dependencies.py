"""FastAPI dependency injection."""

from fastapi import Request

from ascend.adapter.runtime_adapter import RuntimeAdapter


def get_adapter(request: Request) -> RuntimeAdapter:
    return request.app.state.adapter
