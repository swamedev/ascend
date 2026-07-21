"""Demo router — OPERAÇÃO AURORA.

Creates temporary demo builders with auto-seeded journeys
for quick-start evaluation sessions.
"""

from fastapi import APIRouter, Depends

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter
from ascend.api.errors import handle_adapter_result

router = APIRouter(prefix="/demo", tags=["demo"])


@router.post("/start")
async def start_demo(adapter: RuntimeAdapter = Depends(get_adapter)):
    adapter.seed_journeys()
    result = adapter.create_demo_builder()
    builder = handle_adapter_result(result)
    journeys = adapter.list_journeys(limit=1)
    journey_data = journeys.get("data", [])
    first_journey = journey_data[0] if journey_data else {}
    return {"builder": builder, "journey": first_journey}


@router.get("/status")
async def demo_status() -> dict:
    return {"status": "ok", "demo_builders_active": 0}
