"""Health check endpoints.

Three levels:
  GET /health          — simple OK
  GET /health/live     — is the runtime alive?
  GET /health/ready    — is the runtime ready to serve?
"""

from fastapi import APIRouter, Depends

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_simple() -> dict:
    return {"status": "ok"}


@router.get("/health/live")
def health_live(adapter: RuntimeAdapter = Depends(get_adapter)) -> dict:
    result = adapter.health()
    return {"status": "alive", "checks": result["data"]["checks"]}


@router.get("/health/ready")
def health_ready(adapter: RuntimeAdapter = Depends(get_adapter)) -> dict:
    result = adapter.health()
    checks = result["data"]["checks"]
    all_ok = all(checks.values())
    return {
        "status": "ready" if all_ok else "degraded",
        "checks": checks,
    }
