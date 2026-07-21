"""Journey router.

Seed, list, and detail journeys loaded from ASCEND packages.
"""

from fastapi import APIRouter, Depends, Query

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter

router = APIRouter(prefix="/journeys", tags=["journeys"])


@router.post("/seed")
def seed_journeys(
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    return adapter.seed_journeys()


@router.get("")
def list_journeys(
    adapter: RuntimeAdapter = Depends(get_adapter),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    return adapter.list_journeys(limit=limit, offset=offset)


@router.get("/{journey_id}")
def get_journey(
    journey_id: str,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    result = adapter.get_journey(journey_id)
    if result.get("data") is None:
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Journey '{journey_id}' not found",
                    "details": None,
                    "correlationId": "",
                    "timestamp": __import__("datetime")
                    .datetime.now()
                    .isoformat(),
                },
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            },
        )
    return result
