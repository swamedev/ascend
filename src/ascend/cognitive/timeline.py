from datetime import datetime, timedelta, timezone
from typing import Any

from .models import (
    Observation,
    ObservationStore,
    SignalStore,
    Signal,
    SignalType,
    PatternStore,
    Pattern,
    PatternType,
    InsightStore,
    Insight,
    InsightType,
    RecommendationStore,
    Recommendation,
    TimelineSnapshot,
    EvolutionPeriod,
    EvolutionViewResult,
)
from .normalizer import _generate_ulid


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _filter_by_date(
    items: list,
    ts_field: str,
    start: datetime | None = None,
    end: datetime | None = None,
) -> list:
    if start is None and end is None:
        return list(items)
    result = []
    for item in items:
        ts_str = getattr(item, ts_field, None)
        if ts_str is None:
            continue
        ts = _parse_ts(ts_str)
        if start and ts < start:
            continue
        if end and ts > end:
            continue
        result.append(item)
    return result


class TimelineBuilder:
    def __init__(
        self,
        observation_store: ObservationStore,
        signal_store: SignalStore,
        pattern_store: PatternStore,
        insight_store: InsightStore,
        recommendation_store: RecommendationStore,
    ) -> None:
        self._obs_store = observation_store
        self._sig_store = signal_store
        self._pat_store = pattern_store
        self._ins_store = insight_store
        self._rec_store = recommendation_store

    def build(
        self,
        builder_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        start_dt = _parse_ts(start_date) if start_date else None
        end_dt = _parse_ts(end_date) if end_date else None

        period = {"start": start_date or "", "end": end_date or ""}

        observations = _filter_by_date(
            self._obs_store.list_by_builder(builder_id, limit=1000),
            "timestamp", start_dt, end_dt,
        )
        signals = _filter_by_date(
            self._sig_store.list_by_builder(builder_id, limit=1000),
            "extractedAt", start_dt, end_dt,
        )
        patterns = _filter_by_date(
            self._pat_store.list_by_builder(builder_id, limit=1000),
            "observed_at", start_dt, end_dt,
        )
        insights = _filter_by_date(
            self._ins_store.list_by_builder(builder_id, limit=1000),
            "generated_at", start_dt, end_dt,
        )
        recommendations = _filter_by_date(
            self._rec_store.list_by_builder(builder_id, limit=1000),
            "generated_at", start_dt, end_dt,
        )

        return {
            "builder_id": builder_id,
            "observations": [self._obs_to_dict(o) for o in observations],
            "signals": [self._sig_to_dict(s) for s in signals],
            "patterns": [self._pat_to_dict(p) for p in patterns],
            "insights": [self._ins_to_dict(i) for i in insights],
            "recommendations": [self._rec_to_dict(r) for r in recommendations],
            "period": period,
        }

    @staticmethod
    def _obs_to_dict(o: Observation) -> dict[str, Any]:
        return {
            "id": o.id,
            "type": o.type,
            "source": o.source,
            "timestamp": o.timestamp,
            "data": o.data,
            "context": o.context,
        }

    @staticmethod
    def _sig_to_dict(s: Signal) -> dict[str, Any]:
        return {
            "id": s.id,
            "observationId": s.observationId,
            "type": s.type,
            "value": s.value,
            "confidence": s.confidence,
            "extractedAt": s.extractedAt,
        }

    @staticmethod
    def _pat_to_dict(p: Pattern) -> dict[str, Any]:
        return {
            "id": p.id,
            "pattern_type": p.pattern_type,
            "label": p.label,
            "value": p.value,
            "confidence": p.confidence,
            "observed_at": p.observed_at,
        }

    @staticmethod
    def _ins_to_dict(i: Insight) -> dict[str, Any]:
        return {
            "id": i.id,
            "insight_type": i.insight_type,
            "title": i.title,
            "description": i.description,
            "severity": i.severity,
            "confidence": i.confidence,
            "generated_at": i.generated_at,
        }

    @staticmethod
    def _rec_to_dict(r: Recommendation) -> dict[str, Any]:
        return {
            "id": r.id,
            "recommendation_type": r.recommendation_type,
            "title": r.title,
            "description": r.description,
            "priority": r.priority,
            "generated_at": r.generated_at,
        }


class ReplayEngine:
    def __init__(self, timeline_builder: TimelineBuilder) -> None:
        self._builder = timeline_builder

    def replay(
        self,
        builder_id: str,
        start_date: str,
        end_date: str,
    ) -> dict[str, Any]:
        return self._builder.build(
            builder_id, start_date=start_date, end_date=end_date,
        )


class SnapshotBuilder:
    def __init__(
        self,
        signal_store: SignalStore,
        pattern_store: PatternStore,
        insight_store: InsightStore,
        recommendation_store: RecommendationStore,
    ) -> None:
        self._sig_store = signal_store
        self._pat_store = pattern_store
        self._ins_store = insight_store
        self._rec_store = recommendation_store

    def snapshot(self, builder_id: str) -> TimelineSnapshot:
        signals = self._sig_store.list_by_builder(builder_id, limit=1000)
        patterns = self._pat_store.list_by_builder(builder_id, limit=1000)
        insights = self._ins_store.list_by_builder(builder_id, limit=1000)
        recommendations = self._rec_store.list_by_builder(
            builder_id, limit=1000,
        )

        avg_signal_conf = (
            sum(s.confidence for s in signals) / len(signals)
            if signals else 0.0
        )
        avg_pattern_conf = (
            sum(p.confidence for p in patterns) / len(patterns)
            if patterns else 0.0
        )
        avg_insight_conf = (
            sum(i.confidence for i in insights) / len(insights)
            if insights else 0.0
        )

        pattern_type_counts: dict[str, int] = {}
        for p in patterns:
            key = p.pattern_type
            pattern_type_counts[key] = pattern_type_counts.get(key, 0) + 1

        insight_type_counts: dict[str, int] = {}
        for i in insights:
            key = i.insight_type
            insight_type_counts[key] = insight_type_counts.get(key, 0) + 1

        summary: dict[str, Any] = {
            "signal_count": len(signals),
            "pattern_count": len(patterns),
            "insight_count": len(insights),
            "recommendation_count": len(recommendations),
            "avg_signal_confidence": round(avg_signal_conf, 4),
            "avg_pattern_confidence": round(avg_pattern_conf, 4),
            "avg_insight_confidence": round(avg_insight_conf, 4),
            "pattern_type_counts": pattern_type_counts,
            "insight_type_counts": insight_type_counts,
        }

        return TimelineSnapshot(
            id=_generate_ulid(),
            builder_id=builder_id,
            timestamp=_now(),
            signals=signals,
            patterns=patterns,
            insights=insights,
            recommendations=recommendations,
            summary=summary,
        )


class EvolutionView:
    def __init__(
        self,
        signal_store: SignalStore,
        pattern_store: PatternStore,
    ) -> None:
        self._sig_store = signal_store
        self._pat_store = pattern_store

    def compare(
        self,
        builder_id: str,
        period: EvolutionPeriod,
    ) -> EvolutionViewResult:
        start_dt = _parse_ts(period.start)
        end_dt = _parse_ts(period.end)

        all_signals = self._sig_store.list_by_builder(builder_id, limit=1000)
        period_signals = _filter_by_date(
            all_signals, "extractedAt", start_dt, end_dt,
        )
        signal_by_id = {s.id: s for s in all_signals}

        all_patterns = self._pat_store.list_by_builder(builder_id, limit=1000)
        period_patterns = _filter_by_date(
            all_patterns, "observed_at", start_dt, end_dt,
        )

        xp_signals = [
            s for s in period_signals
            if s.type == SignalType.XP_GAINED.value
        ]
        xp_growth = self._compute_growth(xp_signals)

        cr_signal_types = {
            SignalType.COMPLETION_RATE.value,
            SignalType.ROLLING_COMPLETION_RATE.value,
        }
        cr_signals = [
            s for s in period_signals
            if s.type in cr_signal_types
        ]
        completion_rate_avg = (
            sum(float(s.value) for s in cr_signals) / len(cr_signals)
            if cr_signals else 0.0
        )

        pattern_counts: dict[str, int] = {}
        for p in period_patterns:
            pattern_counts[p.pattern_type] = (
                pattern_counts.get(p.pattern_type, 0) + 1
            )

        insight_counts: dict[str, int] = {}

        strengths = self._identify_strengths(period_patterns)
        weaknesses = self._identify_weaknesses(period_patterns)
        trends = self._generate_trends(period_patterns, signal_by_id)

        return EvolutionViewResult(
            builder_id=builder_id,
            period=period,
            xp_growth=round(xp_growth, 4),
            completion_rate_avg=round(completion_rate_avg, 4),
            pattern_counts=pattern_counts,
            insight_counts=insight_counts,
            strengths=strengths,
            weaknesses=weaknesses,
            trends=trends,
        )

    def evolution_over_90_days(
        self,
        builder_id: str,
    ) -> EvolutionViewResult:
        end = _now()
        start_dt = datetime.now(timezone.utc) - timedelta(days=90)
        start = start_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        period = EvolutionPeriod(start=start, end=end)
        return self.compare(builder_id, period)

    @staticmethod
    def _compute_growth(xp_signals: list[Signal]) -> float:
        if len(xp_signals) < 2:
            return 0.0
        values = [float(s.value) for s in xp_signals]
        if values[0] == 0.0:
            return 0.0
        return (values[-1] - values[0]) / values[0]

    @staticmethod
    def _identify_strengths(patterns: list[Pattern]) -> list[str]:
        strengths: list[str] = []
        seen: set[str] = set()
        for p in patterns:
            if p.pattern_type == PatternType.TREND_UP.value:
                if p.confidence > 0.5 and p.label not in seen:
                    strengths.append(p.label)
                    seen.add(p.label)
            elif p.pattern_type == PatternType.ACCELERATION.value:
                if p.label not in seen:
                    strengths.append(p.label)
                    seen.add(p.label)
            elif p.pattern_type == PatternType.CONSISTENCY_SCORE.value:
                if p.metadata.get("isConsistent", False):
                    key = "consistent_performance"
                    if key not in seen:
                        strengths.append("Consistent performance")
                        seen.add(key)
        return strengths

    @staticmethod
    def _identify_weaknesses(patterns: list[Pattern]) -> list[str]:
        weaknesses: list[str] = []
        seen: set[str] = set()
        for p in patterns:
            if p.pattern_type == PatternType.TREND_DOWN.value:
                if p.confidence > 0.5 and p.label not in seen:
                    weaknesses.append(p.label)
                    seen.add(p.label)
            elif p.pattern_type == PatternType.STAGNATION.value:
                key = "stagnation"
                if key not in seen:
                    weaknesses.append("Stagnation detected")
                    seen.add(key)
            elif p.pattern_type == PatternType.PERFORMANCE_GAP.value:
                if p.label not in seen:
                    weaknesses.append(p.label)
                    seen.add(p.label)
        return weaknesses

    @staticmethod
    def _generate_trends(
        patterns: list[Pattern],
        signal_by_id: dict[str, Signal],
    ) -> list[dict]:
        trends: list[dict] = []
        seen: set[str] = set()
        for p in patterns:
            source_types: set[str] = set()
            for sid in p.source_signal_ids:
                sig = signal_by_id.get(sid)
                if sig:
                    source_types.add(sig.type)
            if not source_types:
                source_types.add("unknown")
            for st in sorted(source_types):
                direction = (
                    "up"
                    if p.pattern_type in (
                        PatternType.TREND_UP.value,
                        PatternType.ACCELERATION.value,
                    )
                    else "down"
                    if p.pattern_type in (
                        PatternType.TREND_DOWN.value,
                        PatternType.STAGNATION.value,
                    )
                    else "neutral"
                )
                dedup_key = f"{st}:{p.id}"
                if dedup_key not in seen:
                    seen.add(dedup_key)
                    trends.append({
                        "signal_type": st,
                        "pattern_type": p.pattern_type,
                        "direction": direction,
                        "confidence": p.confidence,
                        "label": p.label,
                    })
        return trends
