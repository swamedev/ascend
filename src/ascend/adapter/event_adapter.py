"""Domain events → ARCH-0026 canonical event envelope.

Translates Runtime DomainEvent objects into the canonical event
format defined in ARCH-0026 Domain Event Catalog and @ascend/contracts.
"""

from datetime import datetime
from typing import Any
from uuid import uuid4

from ascend.domain.events import DomainEvent, EventType


def to_canonical_envelope(event: DomainEvent) -> dict[str, Any]:
    event_type = _map_event_type(event.event_type)
    return {
        "id": event.event_id,
        "type": event_type,
        "version": 1,
        "timestamp": event.timestamp.isoformat(),
        "source": "runtime",
        "correlationId": str(uuid4()),
        "causationId": None,
        "actorId": event.payload.get("builder_id"),
        "payload": _map_payload(event.event_type, event.payload),
    }


DOMAIN_EVENT_MAP: dict[EventType, str] = {
    EventType.BUILDER_CREATED: "builder.created",
    EventType.MISSION_STARTED: "mission.started",
    EventType.EVIDENCE_SUBMITTED: "evidence.submitted",
    EventType.ASSESSMENT_COMPLETED: "assessment.completed",
    EventType.COMPETENCY_UNLOCKED: "competency.unlocked",
    EventType.ACHIEVEMENT_EARNED: "achievement.granted",
}


def _map_event_type(event_type: EventType) -> str:
    return DOMAIN_EVENT_MAP.get(event_type, f"domain.{event_type.value}")


def _map_payload(event_type: EventType, payload: dict[str, Any]) -> dict[str, Any]:
    now = datetime.now().isoformat()

    if event_type == EventType.BUILDER_CREATED:
        return {
            "builderId": payload.get("builder_id", ""),
            "name": payload.get("username", ""),
            "joinedAt": now,
            "initialLevel": 1,
        }

    if event_type == EventType.MISSION_STARTED:
        return {
            "missionId": payload.get("mission_id", ""),
            "builderId": payload.get("builder_id", ""),
            "journeyId": payload.get("journey_id"),
            "startedAt": now,
        }

    if event_type == EventType.EVIDENCE_SUBMITTED:
        return {
            "evidenceId": payload.get("evidence_id", ""),
            "missionId": payload.get("mission_id", ""),
            "builderId": payload.get("builder_id", ""),
            "type": payload.get("type", "document"),
            "content": payload.get("artifact", ""),
            "submittedAt": now,
        }

    if event_type == EventType.ASSESSMENT_COMPLETED:
        return {
            "assessmentId": payload.get("assessment_id", ""),
            "builderId": payload.get("builder_id", ""),
            "score": payload.get("score", 0),
            "total": 100,
            "passed": float(payload.get("score", 0)) >= 0.7,
            "completedAt": now,
        }

    if event_type == EventType.COMPETENCY_UNLOCKED:
        return {
            "competencyId": payload.get("competency_id", ""),
            "builderId": payload.get("builder_id", ""),
            "name": payload.get("name", ""),
            "level": payload.get("level", 1),
            "unlockedAt": now,
            "evidenceIds": [],
        }

    if event_type == EventType.ACHIEVEMENT_EARNED:
        return {
            "achievementId": payload.get("achievement_id", ""),
            "builderId": payload.get("builder_id", ""),
            "name": payload.get("name", payload.get("achievement_id", "")),
            "category": "general",
            "rarity": "common",
            "grantedAt": now,
        }

    return payload
