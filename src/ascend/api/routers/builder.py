"""Builder CRUD router.

Zero business logic — validates, delegates to RuntimeAdapter, serializes.
"""

from fastapi import APIRouter, Depends, Query

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter
from ascend.api.errors import handle_adapter_result
from ascend.api.schemas.builder import BuilderCreate, BuilderOut, BuilderUpdate

router = APIRouter(prefix="/builders", tags=["builders"])


@router.get("")
def list_builders(
    adapter: RuntimeAdapter = Depends(get_adapter),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    return adapter.list_builders(limit=limit, offset=offset)


@router.post("", response_model=BuilderOut, status_code=201)
def create_builder(
    body: BuilderCreate,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    result = adapter.create_builder(
        username=body.username,
        display_name=body.display_name,
    )
    return handle_adapter_result(result)


@router.get("/{builder_id}", response_model=BuilderOut)
def get_builder(
    builder_id: str,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict | None:
    result = adapter.get_builder(builder_id)
    if result.get("success") and result["data"] is None:
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Builder '{builder_id}' not found",
                    "details": None,
                    "correlationId": "",
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                },
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            },
        )
    return handle_adapter_result(result)


@router.patch("/{builder_id}", response_model=BuilderOut)
def update_builder(
    builder_id: str,
    body: BuilderUpdate,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    updates = {}
    if body.display_name is not None:
        updates["name"] = body.display_name
    result = adapter.update_profile(builder_id, updates)
    if result.get("success") and result["data"] is None:
        from fastapi.responses import JSONResponse

        return JSONResponse(
            status_code=404,
            content={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Builder '{builder_id}' not found",
                    "details": None,
                    "correlationId": "",
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                },
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            },
        )
    return handle_adapter_result(result)


@router.delete("/{builder_id}", status_code=204)
def delete_builder(
    builder_id: str,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> None:
    adapter.delete_builder(builder_id)
    return None


@router.get("/{builder_id}/competencies")
def list_builder_competencies(
    builder_id: str,
    adapter: RuntimeAdapter = Depends(get_adapter),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    return adapter.list_competencies_by_builder(builder_id, limit=limit, offset=offset)


@router.get("/{builder_id}/achievements")
def list_builder_achievements(
    builder_id: str,
    adapter: RuntimeAdapter = Depends(get_adapter),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    return adapter.list_achievements_by_builder(builder_id, limit=limit, offset=offset)


@router.get("/{builder_id}/evidence")
def list_builder_evidence(
    builder_id: str,
    adapter: RuntimeAdapter = Depends(get_adapter),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    return adapter.list_evidence_by_builder(builder_id, limit=limit, offset=offset)
