"""Runtime exception → ASCEND_ERROR canonical mapper.

Maps every Runtime exception to the canonical error envelope
defined in @ascend/errors and ARCH-0021 Error Architecture.

Tracebacks are logged server-side, never sent to the client.
"""

import logging
from datetime import datetime
from typing import Any
from uuid import uuid4

from ascend.application.exceptions import (
    BuilderNotFound,
    CompetencyLocked,
    CompetencyNotFound,
    EvidenceNotFound,
    EvidenceRequired,
    MissionAlreadyStarted,
    MissionLocked,
    MissionNotFound,
)

logger = logging.getLogger(__name__)


def map_error(
    error: Exception, correlation_id: str | None = None
) -> dict[str, Any]:
    return _to_envelope(_classify(error), error, correlation_id)


def _classify(error: Exception) -> dict[str, Any]:
    if isinstance(error, BuilderNotFound):
        return {
            "code": "NOT_FOUND",
            "http_status": 404,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.builder",
        }
    if isinstance(error, MissionNotFound):
        return {
            "code": "NOT_FOUND",
            "http_status": 404,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.mission",
        }
    if isinstance(error, EvidenceNotFound):
        return {
            "code": "NOT_FOUND",
            "http_status": 404,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.evidence",
        }
    if isinstance(error, CompetencyNotFound):
        return {
            "code": "NOT_FOUND",
            "http_status": 404,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.competency",
        }
    if isinstance(error, MissionAlreadyStarted):
        return {
            "code": "MISSION_ALREADY_STARTED",
            "http_status": 409,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.mission",
        }
    if isinstance(error, EvidenceRequired):
        return {
            "code": "VALIDATION_ERROR",
            "http_status": 422,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.evidence",
        }
    if isinstance(error, MissionLocked):
        return {
            "code": "MISSION_LOCKED",
            "http_status": 409,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.mission",
        }
    if isinstance(error, CompetencyLocked):
        return {
            "code": "COMPETENCY_LOCKED",
            "http_status": 409,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.competency",
        }
    if isinstance(error, ValueError):
        return {
            "code": "VALIDATION_ERROR",
            "http_status": 422,
            "severity": "warning",
            "recoverable": False,
            "source": "adapter.domain",
        }
    return {
        "code": "INTERNAL_ERROR",
        "http_status": 500,
        "severity": "error",
        "recoverable": True,
        "source": "adapter",
    }


def _to_envelope(
    classified: dict[str, Any],
    error: Exception,
    correlation_id: str | None = None,
) -> dict[str, Any]:
    now = datetime.now().isoformat()

    if classified.get("severity") in ("critical", "error"):
        logger.exception("ASCEND_ERROR [%s]: %s", classified["code"], error)

    return {
        "success": False,
        "error": {
            "code": classified["code"],
            "message": str(error),
            "details": {
                "error_type": type(error).__name__,
            },
            "severity": classified.get("severity", "error"),
            "recoverable": classified.get("recoverable", False),
            "source": classified.get("source", "adapter"),
            "correlationId": correlation_id or str(uuid4()),
            "timestamp": now,
        },
        "timestamp": now,
    }


def success_response(data: Any, total: int | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "success": True,
        "data": data,
        "timestamp": datetime.now().isoformat(),
    }
    if total is not None:
        body["total"] = total
    return body
