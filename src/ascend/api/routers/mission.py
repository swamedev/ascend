"""Mission router.

Start, submit evidence, and complete missions.
"""

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from ascend.adapter.runtime_adapter import RuntimeAdapter
from ascend.api.dependencies import get_adapter
from ascend.api.errors import handle_adapter_result

router = APIRouter(prefix="/missions", tags=["missions"])


class StartMissionRequest(BaseModel):
    builder_id: str = Field(..., description="Builder ID")


class SubmitEvidenceRequest(BaseModel):
    builder_id: str = Field(...)
    artifact: str = Field(..., description="Evidence artifact content")
    type: str = Field("document", description="Evidence type")


class CompleteMissionRequest(BaseModel):
    builder_id: str = Field(...)


@router.get("")
def list_missions(
    adapter: RuntimeAdapter = Depends(get_adapter),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    return adapter.list_missions_by_journey(journey_id="", limit=limit, offset=offset)


@router.post("/{mission_id}/start")
def start_mission(
    mission_id: str,
    body: StartMissionRequest,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    result = adapter.start_mission(
        builder_id=body.builder_id, mission_id=mission_id
    )
    return handle_adapter_result(result)


@router.post("/{mission_id}/evidence")
def submit_evidence(
    mission_id: str,
    body: SubmitEvidenceRequest,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    result = adapter.submit_evidence(
        builder_id=body.builder_id,
        mission_id=mission_id,
        artifact=body.artifact,
        evidence_type=body.type,
    )
    return handle_adapter_result(result)


@router.post("/{mission_id}/complete")
def complete_mission(
    mission_id: str,
    body: CompleteMissionRequest,
    adapter: RuntimeAdapter = Depends(get_adapter),
) -> dict:
    from ascend.application.use_cases.complete_mission import (
        CompleteMissionUseCase,
    )

    uc = CompleteMissionUseCase(adapter)
    return uc.execute(builder_id=body.builder_id, mission_id=mission_id)
