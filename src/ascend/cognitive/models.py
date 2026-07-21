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


class PatternType(str, Enum):
    TREND_UP = "trend_up"
    TREND_DOWN = "trend_down"
    SPIKE = "spike"
    THRESHOLD_CROSSING = "threshold_crossing"
    CONSISTENCY_SCORE = "consistency_score"
    ACCELERATION = "acceleration"
    STAGNATION = "stagnation"
    FREQUENCY_BURST = "frequency_burst"
    PERFORMANCE_GAP = "performance_gap"


@dataclass
class Pattern:
    id: str
    pattern_type: str
    label: str
    value: float
    confidence: float
    source_signal_ids: list[str]
    observed_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


class PatternStore(Protocol):
    def save(self, pattern: Pattern) -> None: ...
    def save_many(self, patterns: list[Pattern]) -> None: ...
    def get_by_type(self, pattern_type: str) -> list[Pattern]: ...
    def list_by_builder(
        self, builder_id: str,
        pattern_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Pattern]: ...
    def list_recent(
        self, builder_id: str, pattern_type: str,
        limit: int = 10,
    ) -> list[Pattern]: ...
    def count_all(self) -> int: ...


class InMemoryPatternStore:
    def __init__(self) -> None:
        self._patterns: list[Pattern] = []

    def save(self, pattern: Pattern) -> None:
        self._patterns.append(pattern)

    def save_many(self, patterns: list[Pattern]) -> None:
        self._patterns.extend(patterns)

    def get_by_type(self, pattern_type: str) -> list[Pattern]:
        return [p for p in self._patterns if p.pattern_type == pattern_type]

    def list_by_builder(
        self, builder_id: str,
        pattern_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Pattern]:
        filtered = [
            p for p in self._patterns
            if p.metadata.get("builderId") == builder_id
            and (pattern_type is None or p.pattern_type == pattern_type)
        ]
        return filtered[offset: offset + limit]

    def list_recent(
        self, builder_id: str, pattern_type: str,
        limit: int = 10,
    ) -> list[Pattern]:
        filtered = [
            p for p in self._patterns
            if p.metadata.get("builderId") == builder_id
            and p.pattern_type == pattern_type
        ]
        return filtered[-limit:]

    def count_all(self) -> int:
        return len(self._patterns)


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


# === Insight Models ===


class InsightType(str, Enum):
    DECLINING_PERFORMANCE = "declining_performance"
    ACCELERATING_GROWTH = "accelerating_growth"
    CONSISTENCY_BREAK = "consistency_break"
    STRENGTH_IDENTIFIED = "strength_identified"
    STAGNATION_WARNING = "stagnation_warning"
    MILESTONE_ACHIEVED = "milestone_achieved"
    IMPROVEMENT_OPPORTUNITY = "improvement_opportunity"
    ENGAGEMENT_DROP = "engagement_drop"
    STREAK_MILESTONE = "streak_milestone"


class InsightSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class Insight:
    id: str
    insight_type: str
    title: str
    description: str
    severity: str
    confidence: float
    source_pattern_ids: list[str]
    generated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)


class InsightStore(Protocol):
    def save(self, insight: Insight) -> None: ...
    def save_many(self, insights: list[Insight]) -> None: ...
    def list_by_builder(
        self, builder_id: str,
        insight_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Insight]: ...
    def list_recent(
        self, builder_id: str, insight_type: str,
        limit: int = 10,
    ) -> list[Insight]: ...
    def count_all(self) -> int: ...


class InMemoryInsightStore:
    def __init__(self) -> None:
        self._insights: list[Insight] = []

    def save(self, insight: Insight) -> None:
        self._insights.append(insight)

    def save_many(self, insights: list[Insight]) -> None:
        self._insights.extend(insights)

    def list_by_builder(
        self, builder_id: str,
        insight_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Insight]:
        filtered = [
            i for i in self._insights
            if i.metadata.get("builderId") == builder_id
            and (insight_type is None or i.insight_type == insight_type)
        ]
        return filtered[offset: offset + limit]

    def list_recent(
        self, builder_id: str, insight_type: str,
        limit: int = 10,
    ) -> list[Insight]:
        filtered = [
            i for i in self._insights
            if i.metadata.get("builderId") == builder_id
            and i.insight_type == insight_type
        ]
        return filtered[-limit:]

    def count_all(self) -> int:
        return len(self._insights)


# === Recommendation Models ===


class RecommendationType(str, Enum):
    TRY_MISSION = "try_mission"
    REPEAT_CONTENT = "repeat_content"
    ADVANCE_CONTENT = "advance_content"
    EXPLORE_NEW_AREA = "explore_new_area"
    TAKE_BREAK = "take_break"
    REVIEW_FOUNDATIONS = "review_foundations"
    CELEBRATE = "celebrate"
    FOCUS_AREA = "focus_area"
    CHANGE_PACE = "change_pace"


class RecommendationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Recommendation:
    id: str
    recommendation_type: str
    title: str
    description: str
    priority: str
    source_insight_ids: list[str]
    generated_at: str
    target: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class RecommendationStore(Protocol):
    def save(self, recommendation: Recommendation) -> None: ...
    def save_many(self, recommendations: list[Recommendation]) -> None: ...
    def list_by_builder(
        self, builder_id: str,
        recommendation_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Recommendation]: ...
    def list_recent(
        self, builder_id: str, recommendation_type: str,
        limit: int = 10,
    ) -> list[Recommendation]: ...
    def count_all(self) -> int: ...


class InMemoryRecommendationStore:
    def __init__(self) -> None:
        self._recommendations: list[Recommendation] = []

    def save(self, recommendation: Recommendation) -> None:
        self._recommendations.append(recommendation)

    def save_many(self, recommendations: list[Recommendation]) -> None:
        self._recommendations.extend(recommendations)

    def list_by_builder(
        self, builder_id: str,
        recommendation_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Recommendation]:
        filtered = [
            r for r in self._recommendations
            if r.metadata.get("builderId") == builder_id
            and (recommendation_type is None
                 or r.recommendation_type == recommendation_type)
        ]
        return filtered[offset: offset + limit]

    def list_recent(
        self, builder_id: str, recommendation_type: str,
        limit: int = 10,
    ) -> list[Recommendation]:
        filtered = [
            r for r in self._recommendations
            if r.metadata.get("builderId") == builder_id
            and r.recommendation_type == recommendation_type
        ]
        return filtered[-limit:]

    def count_all(self) -> int:
        return len(self._recommendations)


# === Timeline Models ===


@dataclass
class TimelineSnapshot:
    id: str
    builder_id: str
    timestamp: str
    signals: list[Signal] = field(default_factory=list)
    patterns: list[Pattern] = field(default_factory=list)
    insights: list[Insight] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvolutionPeriod:
    start: str
    end: str


@dataclass
class EvolutionViewResult:
    builder_id: str
    period: EvolutionPeriod
    xp_growth: float = 0.0
    completion_rate_avg: float = 0.0
    pattern_counts: dict[str, int] = field(default_factory=dict)
    insight_counts: dict[str, int] = field(default_factory=dict)
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    trends: list[dict[str, Any]] = field(default_factory=list)
