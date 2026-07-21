from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


SENSITIVE_PATTERNS: list[str] = [
    "password", "passwd", "token", "secret", "api_key", "private_key",
    "email", "phone", "ssn", "social_security",
]


class SignalType(str, Enum):
    XP_GAINED = "xp_gained"
    XP_TOTAL = "xp_total"
    MISSION_COUNT = "mission_count"
    COMPLETION_RATE = "completion_rate"
    TIME_SPENT = "time_spent"
    SCORE_ACHIEVED = "score_achieved"
    EVIDENCE_QUALITY = "evidence_quality"
    ERROR_RATE = "error_rate"
    STREAK_LENGTH = "streak_length"
    TOPICS_COVERED = "topics_covered"
    SESSION_DURATION = "session_duration"
    SESSION_FREQUENCY = "session_frequency"
    TIME_OF_DAY = "time_of_day"
    DAY_OF_WEEK = "day_of_week"
    COMPETENCY_COUNT = "competency_count"
    COMPETENCY_DEPTH = "competency_depth"
    LEVEL_PROGRESSION_RATE = "level_progression_rate"
    ROLLING_COMPLETION_RATE = "rolling_completion_rate"
    ROLLING_AVG_XP = "rolling_avg_xp"
    ROLLING_AVG_SCORE = "rolling_avg_score"
    XP_PER_MINUTE = "xp_per_minute"
    STREAK_ACTIVE = "streak_active"


@dataclass
class Signal:
    id: str
    observationId: str
    type: str
    value: float | int | str | bool
    confidence: float
    extractedAt: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Observation:
    id: str
    type: str
    source: str
    timestamp: str
    data: dict[str, Any]
    context: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedObservation:
    id: str
    type: str
    source: str
    timestamp: str
    data: dict[str, Any]
    context: dict[str, Any]
    metadata: dict[str, Any]
    trace: dict[str, str | None]


class ObservationStore(Protocol):
    def save(self, observation: Observation) -> None: ...

    def list_by_builder(
        self, builder_id: str, limit: int = 50, offset: int = 0
    ) -> list[Observation]: ...

    def count_by_builder(self, builder_id: str) -> int: ...

    def list_all(
        self, limit: int = 50, offset: int = 0
    ) -> list[Observation]: ...

    def count_all(self) -> int: ...


class InMemoryObservationStore:
    def __init__(self) -> None:
        self._observations: list[Observation] = []

    def save(self, observation: Observation) -> None:
        self._observations.append(observation)

    def list_by_builder(
        self, builder_id: str, limit: int = 50, offset: int = 0
    ) -> list[Observation]:
        filtered = [
            o for o in self._observations
            if o.context.get("builderId") == builder_id
        ]
        return filtered[offset: offset + limit]

    def count_by_builder(self, builder_id: str) -> int:
        return sum(
            1 for o in self._observations
            if o.context.get("builderId") == builder_id
        )

    def list_all(
        self, limit: int = 50, offset: int = 0
    ) -> list[Observation]:
        return self._observations[offset: offset + limit]

    def count_all(self) -> int:
        return len(self._observations)


class SignalStore(Protocol):
    def save(self, signal: Signal) -> None: ...
    def save_many(self, signals: list[Signal]) -> None: ...
    def get_by_observation(self, observation_id: str) -> list[Signal]: ...
    def list_by_builder(
        self, builder_id: str, signal_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Signal]: ...
    def list_recent(
        self, builder_id: str, signal_type: str,
        limit: int = 10,
    ) -> list[Signal]: ...


class InMemorySignalStore:
    def __init__(self) -> None:
        self._signals: list[Signal] = []

    def save(self, signal: Signal) -> None:
        self._signals.append(signal)

    def save_many(self, signals: list[Signal]) -> None:
        self._signals.extend(signals)

    def get_by_observation(self, observation_id: str) -> list[Signal]:
        return [s for s in self._signals if s.observationId == observation_id]

    def list_by_builder(
        self, builder_id: str, signal_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Signal]:
        filtered = [
            s for s in self._signals
            if s.metadata.get("builderId") == builder_id
            and (signal_type is None or s.type == signal_type)
        ]
        return filtered[offset: offset + limit]

    def list_recent(
        self, builder_id: str, signal_type: str,
        limit: int = 10,
    ) -> list[Signal]:
        filtered = [
            s for s in self._signals
            if s.metadata.get("builderId") == builder_id
            and s.type == signal_type
        ]
        return filtered[-limit:]

    def count_all(self) -> int:
        return len(self._signals)
