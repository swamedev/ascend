from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EventType(Enum):
    BUILDER_CREATED = "builder_created"
    MISSION_STARTED = "mission_started"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    ASSESSMENT_COMPLETED = "assessment_completed"
    COMPETENCY_UNLOCKED = "competency_unlocked"
    ACHIEVEMENT_EARNED = "achievement_earned"


@dataclass
class DomainEvent:
    event_id: str
    event_type: EventType
    aggregate_id: str
    payload: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


def BuilderCreated(builder_id: str, username: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{builder_id}-created",
        event_type=EventType.BUILDER_CREATED,
        aggregate_id=builder_id,
        payload={"builder_id": builder_id, "username": username},
    )


def MissionStarted(mission_id: str, builder_id: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{mission_id}-started",
        event_type=EventType.MISSION_STARTED,
        aggregate_id=mission_id,
        payload={"mission_id": mission_id, "builder_id": builder_id},
    )


def EvidenceSubmitted(evidence_id: str, mission_id: str, builder_id: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{evidence_id}-submitted",
        event_type=EventType.EVIDENCE_SUBMITTED,
        aggregate_id=evidence_id,
        payload={
            "evidence_id": evidence_id,
            "mission_id": mission_id,
            "builder_id": builder_id,
        },
    )


def AssessmentCompleted(assessment_id: str, evidence_id: str, score: float) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{assessment_id}-completed",
        event_type=EventType.ASSESSMENT_COMPLETED,
        aggregate_id=assessment_id,
        payload={
            "assessment_id": assessment_id,
            "evidence_id": evidence_id,
            "score": score,
        },
    )


def CompetencyUnlocked(competency_id: str, builder_id: str, level: int) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{competency_id}-unlocked",
        event_type=EventType.COMPETENCY_UNLOCKED,
        aggregate_id=competency_id,
        payload={
            "competency_id": competency_id,
            "builder_id": builder_id,
            "level": level,
        },
    )


def AchievementEarned(achievement_id: str, builder_id: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{achievement_id}-earned",
        event_type=EventType.ACHIEVEMENT_EARNED,
        aggregate_id=achievement_id,
        payload={
            "achievement_id": achievement_id,
            "builder_id": builder_id,
        },
    )
