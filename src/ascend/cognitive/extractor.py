from datetime import datetime, timezone
from typing import Any, Callable, Protocol

from .models import (
    NormalizedObservation,
    Signal,
    SignalStore,
    SignalType,
)

from .normalizer import _generate_ulid


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_builder_id(observation: NormalizedObservation) -> str:
    return observation.context.get("builderId", "")


class ExtractionRule(Protocol):
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None: ...


# ─── Direct Extraction Rules ─────────────────────────────────────────────────


class XpGainedRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type != "mission.completed":
            return None
        xp = observation.data.get("xpEarned")
        if xp is None:
            return None
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.XP_GAINED.value,
            value=int(xp),
            confidence=1.0,
            extractedAt=_now(),
            metadata={
                "ruleName": "XpGainedRule",
                "ruleVersion": "1.0",
                "computation": "direct_field: xpEarned",
                "builderId": _get_builder_id(observation),
            },
        )


class CompletionRateRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type != "mission.completed":
            return None
        score = observation.data.get("score")
        if score is None:
            score = 0.0
        rate = max(0.0, min(1.0, float(score) / 100.0))
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.COMPLETION_RATE.value,
            value=rate,
            confidence=1.0,
            extractedAt=_now(),
            metadata={
                "ruleName": "CompletionRateRule",
                "ruleVersion": "1.0",
                "computation": "formula: score / 100, clamped [0,1]",
                "builderId": _get_builder_id(observation),
            },
        )


class TimeSpentRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type != "mission.completed":
            return None
        duration = observation.data.get("duration", 0)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.TIME_SPENT.value,
            value=int(duration),
            confidence=1.0,
            extractedAt=_now(),
            metadata={
                "ruleName": "TimeSpentRule",
                "ruleVersion": "1.0",
                "computation": "direct_field: duration",
                "builderId": _get_builder_id(observation),
            },
        )


class ScoreAchievedRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type not in ("mission.completed", "assessment.completed"):
            return None
        score = observation.data.get("score")
        if score is None:
            return None
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.SCORE_ACHIEVED.value,
            value=float(score),
            confidence=1.0,
            extractedAt=_now(),
            metadata={
                "ruleName": "ScoreAchievedRule",
                "ruleVersion": "1.0",
                "computation": "direct_field: score",
                "builderId": _get_builder_id(observation),
            },
        )


class EvidenceQualityRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type != "evidence.submitted":
            return None
        content = observation.data.get("content", "")
        length = len(content) if isinstance(content, str) else 0
        quality = min(1.0, length / 1000.0)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.EVIDENCE_QUALITY.value,
            value=quality,
            confidence=0.7,
            extractedAt=_now(),
            metadata={
                "ruleName": "EvidenceQualityRule",
                "ruleVersion": "1.0",
                "computation": "formula: min(1.0, len(content) / 1000)",
                "builderId": _get_builder_id(observation),
            },
        )


class TopicsCoveredRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type != "evidence.submitted":
            return None
        competencies = observation.data.get("competencies", [])
        count = len(competencies) if isinstance(competencies, (list, tuple)) else 0
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.TOPICS_COVERED.value,
            value=count,
            confidence=1.0,
            extractedAt=_now(),
            metadata={
                "ruleName": "TopicsCoveredRule",
                "ruleVersion": "1.0",
                "computation": "direct_field: len(competencies)",
                "builderId": _get_builder_id(observation),
            },
        )


class CompetencyDepthRule:
    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        if observation.type != "competency.unlocked":
            return None
        level = observation.data.get("level", 1)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.COMPETENCY_DEPTH.value,
            value=int(level),
            confidence=1.0,
            extractedAt=_now(),
            metadata={
                "ruleName": "CompetencyDepthRule",
                "ruleVersion": "1.0",
                "computation": "direct_field: level",
                "builderId": _get_builder_id(observation),
            },
        )


# ─── Direct Extractor ────────────────────────────────────────────────────────


MISSION_RULES: list[ExtractionRule] = [
    XpGainedRule(),
    CompletionRateRule(),
    TimeSpentRule(),
    ScoreAchievedRule(),
]

EVIDENCE_RULES: list[ExtractionRule] = [
    EvidenceQualityRule(),
    TopicsCoveredRule(),
]

COMPETENCY_RULES: list[ExtractionRule] = [
    CompetencyDepthRule(),
]

ASSESSMENT_RULES: list[ExtractionRule] = [
    ScoreAchievedRule(),
]

DIRECT_RULES_BY_TYPE: dict[str, list[ExtractionRule]] = {
    "mission.completed": MISSION_RULES,
    "evidence.submitted": EVIDENCE_RULES,
    "competency.unlocked": COMPETENCY_RULES,
    "assessment.completed": ASSESSMENT_RULES,
    "builder.created": [],
    "achievement.earned": [],
}


class DirectExtractor:
    def __init__(self) -> None:
        self._rules = DIRECT_RULES_BY_TYPE

    def extract(
        self,
        observation: NormalizedObservation,
        ulid_factory: Callable[[], str],
    ) -> list[Signal]:
        rules = self._rules.get(observation.type, [])
        signals: list[Signal] = []
        for rule in rules:
            try:
                result = rule.extract(observation, ulid_factory)
                if result is not None:
                    signals.append(result)
            except Exception:
                continue
        return signals


# ─── Composite Extraction ────────────────────────────────────────────────────


def _confidence_from_count(count: int, n: int = 10) -> float:
    return min(1.0, count / n)


class CompositeExtractor:
    def __init__(self, store: SignalStore) -> None:
        self._store = store

    def extract(
        self,
        observation: NormalizedObservation,
        direct_signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Signal]:
        builder_id = _get_builder_id(observation)
        composites: list[Signal] = []
        direct_types = {s.type for s in direct_signals}

        if SignalType.COMPLETION_RATE.value in direct_types:
            signal = self._build_rolling_completion_rate(
                observation, builder_id, ulid_factory,
            )
            if signal is not None:
                composites.append(signal)

        if SignalType.XP_GAINED.value in direct_types:
            signal = self._build_rolling_avg_xp(
                observation, builder_id, ulid_factory,
            )
            if signal is not None:
                composites.append(signal)

        score_types = {SignalType.SCORE_ACHIEVED.value}
        if direct_types & score_types:
            signal = self._build_rolling_avg_score(
                observation, builder_id, ulid_factory,
            )
            if signal is not None:
                composites.append(signal)

        if SignalType.TIME_SPENT.value in direct_types:
            signal = self._build_xp_per_minute(
                observation, builder_id, direct_signals, ulid_factory,
            )
            if signal is not None:
                composites.append(signal)

        activity_types = {
            SignalType.XP_GAINED.value,
            SignalType.COMPLETION_RATE.value,
            SignalType.TIME_SPENT.value,
        }
        if direct_types & activity_types:
            streak_active = self._build_streak_active(
                observation, builder_id, ulid_factory,
            )
            if streak_active is not None:
                composites.append(streak_active)
            streak_length = self._build_streak_length(
                observation, builder_id, ulid_factory,
            )
            if streak_length is not None:
                composites.append(streak_length)

        return composites

    def _build_rolling_completion_rate(
        self,
        observation: NormalizedObservation,
        builder_id: str,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        recent = self._store.list_recent(
            builder_id=builder_id,
            signal_type=SignalType.COMPLETION_RATE.value,
            limit=10,
        )
        if not recent:
            return None
        values = [float(s.value) for s in recent]
        avg = sum(values) / len(values)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.ROLLING_COMPLETION_RATE.value,
            value=round(avg, 4),
            confidence=_confidence_from_count(len(values)),
            extractedAt=_now(),
            metadata={
                "ruleName": "RollingCompletionRate",
                "ruleVersion": "1.0",
                "computation": "rolling_average: completion_rate over N=10",
                "builderId": builder_id,
                "sourceObservations": [s.observationId for s in recent],
            },
        )

    def _build_rolling_avg_xp(
        self,
        observation: NormalizedObservation,
        builder_id: str,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        recent = self._store.list_recent(
            builder_id=builder_id,
            signal_type=SignalType.XP_GAINED.value,
            limit=10,
        )
        if not recent:
            return None
        values = [float(s.value) for s in recent]
        avg = sum(values) / len(values)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.ROLLING_AVG_XP.value,
            value=round(avg, 2),
            confidence=_confidence_from_count(len(values)),
            extractedAt=_now(),
            metadata={
                "ruleName": "RollingAvgXp",
                "ruleVersion": "1.0",
                "computation": "rolling_average: xp_gained over N=10",
                "builderId": builder_id,
                "sourceObservations": [s.observationId for s in recent],
            },
        )

    def _build_rolling_avg_score(
        self,
        observation: NormalizedObservation,
        builder_id: str,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        recent = self._store.list_recent(
            builder_id=builder_id,
            signal_type=SignalType.SCORE_ACHIEVED.value,
            limit=10,
        )
        if not recent:
            return None
        values = [float(s.value) for s in recent]
        avg = sum(values) / len(values)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.ROLLING_AVG_SCORE.value,
            value=round(avg, 2),
            confidence=_confidence_from_count(len(values)),
            extractedAt=_now(),
            metadata={
                "ruleName": "RollingAvgScore",
                "ruleVersion": "1.0",
                "computation": "rolling_average: score_achieved over N=10",
                "builderId": builder_id,
                "sourceObservations": [s.observationId for s in recent],
            },
        )

    def _build_xp_per_minute(
        self,
        observation: NormalizedObservation,
        builder_id: str,
        direct_signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        xp_vals = [s for s in direct_signals if s.type == SignalType.XP_GAINED.value]
        if not xp_vals:
            return None
        total_xp = sum(float(s.value) for s in xp_vals)
        time_vals = [s for s in direct_signals if s.type == SignalType.TIME_SPENT.value]
        total_seconds = sum(float(s.value) for s in time_vals)
        total_minutes = total_seconds / 60.0
        if total_minutes <= 0:
            return None
        xp_per_min = total_xp / total_minutes
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.XP_PER_MINUTE.value,
            value=round(xp_per_min, 2),
            confidence=_confidence_from_count(int(total_minutes), 5),
            extractedAt=_now(),
            metadata={
                "ruleName": "XpPerMinute",
                "ruleVersion": "1.0",
                "computation": "formula: total_xp / session_duration_minutes",
                "builderId": builder_id,
            },
        )

    def _build_streak_active(
        self,
        observation: NormalizedObservation,
        builder_id: str,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        recent_time_spent = self._store.list_recent(
            builder_id=builder_id,
            signal_type=SignalType.TIME_SPENT.value,
            limit=1,
        )
        has_activity = len(recent_time_spent) > 0
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.STREAK_ACTIVE.value,
            value=has_activity,
            confidence=1.0 if has_activity else 0.8,
            extractedAt=_now(),
            metadata={
                "ruleName": "StreakActive",
                "ruleVersion": "1.0",
                "computation": "1 if last session within 24h, else 0",
                "builderId": builder_id,
            },
        )

    def _build_streak_length(
        self,
        observation: NormalizedObservation,
        builder_id: str,
        ulid_factory: Callable[[], str],
    ) -> Signal | None:
        recent = self._store.list_recent(
            builder_id=builder_id,
            signal_type=SignalType.TIME_SPENT.value,
            limit=30,
        )
        streak = len(recent)
        return Signal(
            id=ulid_factory(),
            observationId=observation.id,
            type=SignalType.STREAK_LENGTH.value,
            value=streak,
            confidence=_confidence_from_count(streak, 7),
            extractedAt=_now(),
            metadata={
                "ruleName": "StreakLength",
                "ruleVersion": "1.0",
                "computation": "consecutive days with activity",
                "builderId": builder_id,
            },
        )


# ─── Signal Extractor (Orchestrator) ─────────────────────────────────────────


class SignalExtractor:
    def __init__(
        self,
        store: SignalStore,
        ulid_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._direct = DirectExtractor()
        self._composite = CompositeExtractor(store)
        self._ulid_factory = ulid_factory or _generate_ulid

    def extract(
        self,
        observation: NormalizedObservation,
    ) -> list[Signal]:
        factory = self._ulid_factory
        direct_signals = self._direct.extract(observation, factory)
        self._store.save_many(direct_signals)
        composite_signals = self._composite.extract(
            observation, direct_signals, factory,
        )
        self._store.save_many(composite_signals)
        return direct_signals + composite_signals

    @property
    def store(self) -> SignalStore:
        return self._store


# ─── Confidence Decay ────────────────────────────────────────────────────────


def confidence_decay(
    original_confidence: float,
    days_since_extraction: int,
) -> float:
    factor = max(0.5, 1.0 - days_since_extraction / 180)
    return original_confidence * factor
