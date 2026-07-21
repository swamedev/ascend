from uuid import uuid4

from ascend.domain.events import DomainEvent, EventType
from ascend.infrastructure.events.memory_event_bus import MemoryEventBus

from .models import Observation, ObservationStore

EVENT_TYPE_MAP: dict[EventType, str] = {
    EventType.BUILDER_CREATED: "builder.created",
    EventType.MISSION_STARTED: "mission.started",
    EventType.EVIDENCE_SUBMITTED: "evidence.submitted",
    EventType.ASSESSMENT_COMPLETED: "assessment.completed",
    EventType.COMPETENCY_UNLOCKED: "competency.unlocked",
    EventType.ACHIEVEMENT_EARNED: "achievement.earned",
}


class ObservationCollector:
    def __init__(
        self,
        event_bus: MemoryEventBus,
        store: ObservationStore,
    ) -> None:
        self._store = store
        self._subscribe(event_bus)

    @property
    def store(self) -> ObservationStore:
        return self._store

    def _subscribe(self, event_bus: MemoryEventBus) -> None:
        for event_type in EventType:
            event_bus.subscribe(event_type.value, self._on_event)

    def _on_event(self, event: DomainEvent) -> None:
        observation = self._convert(event)
        self._store.save(observation)

    @staticmethod
    def _convert(event: DomainEvent) -> Observation:
        obs_type = EVENT_TYPE_MAP.get(
            event.event_type, f"domain.{event.event_type.value}"
        )
        builder_id = event.payload.get("builder_id", event.aggregate_id)

        context: dict[str, str] = {
            "builderId": builder_id,
        }
        if "mission_id" in event.payload:
            context["missionId"] = event.payload["mission_id"]
        if "journey_id" in event.payload:
            context["journeyId"] = event.payload["journey_id"]
        if "evidence_id" in event.payload:
            context["evidenceId"] = event.payload["evidence_id"]

        return Observation(
            id=str(uuid4()),
            type=obs_type,
            source="runtime",
            timestamp=event.timestamp.isoformat(),
            data=dict(event.payload),
            context=context,
            metadata={
                "observationSchema": "1.0",
                "collector": "observation-collector",
                "eventId": event.event_id,
            },
        )
