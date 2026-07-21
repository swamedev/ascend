"""Cognitive Pipeline — Read-Only API.

I14 (Cognitive Independence): these endpoints never write to the Runtime.
Every endpoint is read-only. No mutations. No side effects.
"""

from fastapi import APIRouter, Depends, Query

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter

router = APIRouter(prefix="/cognitive", tags=["cognitive"])


def _extract_store(adapter: RuntimeAdapter) -> dict:
    stores: dict = getattr(adapter, "_stores", {})
    if not stores:
        from ascend.cognitive.models import (
            InMemoryObservationStore,
            InMemorySignalStore,
            InMemoryPatternStore,
            InMemoryInsightStore,
            InMemoryRecommendationStore,
        )
        stores = {
            "observation": InMemoryObservationStore(),
            "signal": InMemorySignalStore(),
            "pattern": InMemoryPatternStore(),
            "insight": InMemoryInsightStore(),
            "recommendation": InMemoryRecommendationStore(),
        }
        adapter._stores = stores
    return stores


@router.get("/observations")
def list_observations(
    builder_id: str = Query(..., description="Builder ID"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    stores = _extract_store(adapter)
    obs = stores["observation"].list_by_builder(builder_id, limit=limit, offset=offset)
    return {"data": [o.__dict__ for o in obs], "total": len(obs), "limit": limit, "offset": offset}


@router.get("/signals")
def list_signals(
    builder_id: str = Query(..., description="Builder ID"),
    signal_type: str | None = Query(None, description="Filter by signal type"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    stores = _extract_store(adapter)
    sigs = stores["signal"].list_by_builder(builder_id, signal_type=signal_type, limit=limit, offset=offset)
    return {"data": [s.__dict__ for s in sigs], "total": len(sigs), "limit": limit, "offset": offset}


@router.get("/patterns")
def list_patterns(
    builder_id: str = Query(..., description="Builder ID"),
    pattern_type: str | None = Query(None, description="Filter by pattern type"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    stores = _extract_store(adapter)
    pats = stores["pattern"].list_by_builder(builder_id, pattern_type=pattern_type, limit=limit, offset=offset)
    return {"data": [p.__dict__ for p in pats], "total": len(pats), "limit": limit, "offset": offset}


@router.get("/insights")
def list_insights(
    builder_id: str = Query(..., description="Builder ID"),
    insight_type: str | None = Query(None, description="Filter by insight type"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    stores = _extract_store(adapter)
    ins = stores["insight"].list_by_builder(builder_id, insight_type=insight_type, limit=limit, offset=offset)
    return {"data": [i.__dict__ for i in ins], "total": len(ins), "limit": limit, "offset": offset}


@router.get("/recommendations")
def list_recommendations(
    builder_id: str = Query(..., description="Builder ID"),
    recommendation_type: str | None = Query(None, description="Filter by recommendation type"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    stores = _extract_store(adapter)
    recs = stores["recommendation"].list_by_builder(
        builder_id, recommendation_type=recommendation_type, limit=limit, offset=offset,
    )
    return {"data": [r.__dict__ for r in recs], "total": len(recs), "limit": limit, "offset": offset}


@router.get("/timeline")
def get_timeline(
    builder_id: str = Query(..., description="Builder ID"),
    start_date: str | None = Query(None, description="Start date (ISO 8601)"),
    end_date: str | None = Query(None, description="End date (ISO 8601)"),
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    from ascend.cognitive.timeline import TimelineBuilder

    stores = _extract_store(adapter)
    builder = TimelineBuilder(
        observation_store=stores["observation"],
        signal_store=stores["signal"],
        pattern_store=stores["pattern"],
        insight_store=stores["insight"],
        recommendation_store=stores["recommendation"],
    )
    return builder.build(builder_id, start_date=start_date, end_date=end_date)
