from datetime import datetime, timezone
from statistics import mean, stdev
from typing import Any, Callable, Protocol

from .models import (
    Pattern,
    PatternStore,
    PatternType,
    Signal,
    SignalStore,
    SignalType,
)

from .normalizer import _generate_ulid


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_builder_id(signal: Signal) -> str:
    return signal.metadata.get("builderId", "")


TREND_WINDOW_MIN = 3
STAGNATION_SLOPE_THRESHOLD = 0.01
SIGMA_THRESHOLD = 2.0


def _compute_slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    n = len(values)
    xs = list(range(n))
    x_mean = mean(xs)
    y_mean = mean(values)
    num = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, values))
    den = sum((x - x_mean) ** 2 for x in xs)
    if den == 0:
        return 0.0
    return num / den


def _compute_second_derivative(values: list[float]) -> float:
    if len(values) < 3:
        return 0.0
    first_derivs = [values[i] - values[i - 1] for i in range(1, len(values))]
    return first_derivs[-1] - first_derivs[-2] if len(first_derivs) >= 2 else 0.0


def _compute_cv(values: list[float]) -> float:
    if len(values) < 2:
        return 1.0
    m = mean(values)
    if m == 0:
        return 1.0
    return stdev(values) / m


class DetectionRule(Protocol):
    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]: ...


class TrendUpRule:
    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < TREND_WINDOW_MIN:
            return []
        values = [float(s.value) for s in signals]
        slope = _compute_slope(values)
        if slope <= 0:
            return []
        confidence = min(1.0, abs(slope) / max(abs(mean(values)) / 100, 0.001))
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.TREND_UP.value,
                label=f"Trend up detected (slope={slope:.4f})",
                value=round(slope, 4),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "TrendUpRule",
                    "ruleVersion": "1.0",
                    "slope": round(slope, 4),
                    "window": len(signals),
                    "builderId": _get_builder_id(signals[0]),
                },
            )
        ]


class TrendDownRule:
    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < TREND_WINDOW_MIN:
            return []
        values = [float(s.value) for s in signals]
        slope = _compute_slope(values)
        if slope >= 0:
            return []
        confidence = min(1.0, abs(slope) / max(abs(mean(values)) / 100, 0.001))
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.TREND_DOWN.value,
                label=f"Trend down detected (slope={slope:.4f})",
                value=round(slope, 4),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "TrendDownRule",
                    "ruleVersion": "1.0",
                    "slope": round(slope, 4),
                    "window": len(signals),
                    "builderId": _get_builder_id(signals[0]),
                },
            )
        ]


class SpikeRule:
    def __init__(self, sigma_threshold: float = SIGMA_THRESHOLD) -> None:
        self._sigma_threshold = sigma_threshold

    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < 4:
            return []
        values = [float(s.value) for s in signals]
        for i, signal in enumerate(signals):
            others = values[:i] + values[i + 1:]
            if len(others) < 2:
                continue
            m = mean(others)
            s = stdev(others)
            if s == 0:
                continue
            deviation = (values[i] - m) / s
            if abs(deviation) > self._sigma_threshold:
                source_ids = [signal.id]
                label = "Upward spike" if deviation > 0 else "Downward spike"
                return [
                    Pattern(
                        id=ulid_factory(),
                        pattern_type=PatternType.SPIKE.value,
                        label=f"{label} (z-score={deviation:.2f})",
                        value=round(deviation, 4),
                        confidence=round(
                            min(1.0, abs(deviation) / (self._sigma_threshold * 2)), 4
                        ),
                        source_signal_ids=source_ids,
                        observed_at=_now(),
                        metadata={
                            "ruleName": "SpikeRule",
                            "ruleVersion": "1.0",
                            "sigmaThreshold": self._sigma_threshold,
                            "zScore": round(deviation, 4),
                            "builderId": _get_builder_id(signal),
                        },
                    )
                ]
        return []


class ThresholdCrossingRule:
    def __init__(self, min_value: float | None = None, max_value: float | None = None) -> None:
        self._min = min_value
        self._max = max_value

    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        results: list[Pattern] = []
        for signal in signals:
            val = float(signal.value)
            crossed = False
            label = ""
            if self._min is not None and val < self._min:
                crossed = True
                label = f"Below minimum threshold ({val:.2f} < {self._min})"
            if self._max is not None and val > self._max:
                crossed = True
                label = f"Above maximum threshold ({val:.2f} > {self._max})"
            if crossed:
                results.append(
                    Pattern(
                        id=ulid_factory(),
                        pattern_type=PatternType.THRESHOLD_CROSSING.value,
                        label=label,
                        value=val,
                        confidence=1.0,
                        source_signal_ids=[signal.id],
                        observed_at=_now(),
                        metadata={
                            "ruleName": "ThresholdCrossingRule",
                            "ruleVersion": "1.0",
                            "min": self._min,
                            "max": self._max,
                            "builderId": _get_builder_id(signal),
                        },
                    )
                )
        return results


class ConsistencyScoreRule:
    def __init__(self, cv_threshold: float = 0.3) -> None:
        self._cv_threshold = cv_threshold

    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < 3:
            return []
        values = [float(s.value) for s in signals]
        cv = _compute_cv(values)
        is_consistent = cv <= self._cv_threshold
        confidence = max(0.0, 1.0 - (cv / self._cv_threshold)) if is_consistent else max(0.0, cv - self._cv_threshold) / self._cv_threshold
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.CONSISTENCY_SCORE.value,
                label="Consistent performance" if is_consistent else "Inconsistent performance",
                value=round(cv, 4),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "ConsistencyScoreRule",
                    "ruleVersion": "1.0",
                    "cvThreshold": self._cv_threshold,
                    "isConsistent": is_consistent,
                    "builderId": _get_builder_id(signals[0]),
                },
            )
        ]


class AccelerationRule:
    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < 3:
            return []
        values = [float(s.value) for s in signals]
        slope = _compute_slope(values)
        if slope <= 0:
            return []
        second_deriv = _compute_second_derivative(values)
        if second_deriv <= 0:
            return []
        confidence = min(1.0, abs(second_deriv) / (abs(slope) + 0.001))
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.ACCELERATION.value,
                label=f"Acceleration detected (2nd deriv={second_deriv:.4f})",
                value=round(second_deriv, 4),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "AccelerationRule",
                    "ruleVersion": "1.0",
                    "secondDerivative": round(second_deriv, 4),
                    "window": len(signals),
                    "builderId": _get_builder_id(signals[0]),
                },
            )
        ]


class StagnationRule:
    def __init__(self, slope_threshold: float = STAGNATION_SLOPE_THRESHOLD) -> None:
        self._slope_threshold = slope_threshold

    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < TREND_WINDOW_MIN:
            return []
        values = [float(s.value) for s in signals]
        slope = abs(_compute_slope(values))
        if slope > self._slope_threshold:
            return []
        cv = _compute_cv(values)
        confidence = max(0.0, 1.0 - (cv * 2))
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.STAGNATION.value,
                label="No significant change detected",
                value=round(slope, 4),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "StagnationRule",
                    "ruleVersion": "1.0",
                    "slopeThreshold": self._slope_threshold,
                    "absSlope": round(slope, 4),
                    "window": len(signals),
                    "builderId": _get_builder_id(signals[0]),
                },
            )
        ]


class FrequencyBurstRule:
    def __init__(self, burst_threshold: int = 10, window_hours: int = 24) -> None:
        self._burst_threshold = burst_threshold
        self._window_hours = window_hours

    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < self._burst_threshold:
            return []
        count = len(signals)
        rate_ratio = count / self._burst_threshold
        confidence = min(1.0, (rate_ratio - 1.0) / 2.0) if rate_ratio > 1.0 else 0.5
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.FREQUENCY_BURST.value,
                label=f"Frequency burst ({count} signals in {self._window_hours}h window)",
                value=float(count),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "FrequencyBurstRule",
                    "ruleVersion": "1.0",
                    "burstThreshold": self._burst_threshold,
                    "windowHours": self._window_hours,
                    "signalCount": count,
                    "builderId": _get_builder_id(signals[0]),
                },
            )
        ]


class PerformanceGapRule:
    def __init__(self, gap_threshold: float = 0.2) -> None:
        self._gap_threshold = gap_threshold

    def detect(
        self,
        signals: list[Signal],
        ulid_factory: Callable[[], str],
    ) -> list[Pattern]:
        if len(signals) < 2:
            return []
        values = [float(s.value) for s in signals]
        gap = abs(values[-1] - mean(values[:-1]))
        if gap < self._gap_threshold:
            return []
        confidence = min(1.0, gap / (self._gap_threshold * 3))
        source_ids = [s.id for s in signals]
        return [
            Pattern(
                id=ulid_factory(),
                pattern_type=PatternType.PERFORMANCE_GAP.value,
                label=f"Performance gap detected (gap={gap:.2f})",
                value=round(gap, 4),
                confidence=round(min(1.0, confidence), 4),
                source_signal_ids=source_ids,
                observed_at=_now(),
                metadata={
                    "ruleName": "PerformanceGapRule",
                    "ruleVersion": "1.0",
                    "gapThreshold": self._gap_threshold,
                    "gap": round(gap, 4),
                    "builderId": _get_builder_id(signals[-1]),
                },
            )
        ]


# ─── Rule Dispatch ───────────────────────────────────────────────────────────


DEFAULT_RULES: dict[str, list[DetectionRule]] = {
    SignalType.COMPLETION_RATE.value: [
        TrendUpRule(),
        TrendDownRule(),
        StagnationRule(),
        ThresholdCrossingRule(min_value=0.0, max_value=1.0),
        SpikeRule(),
    ],
    SignalType.XP_GAINED.value: [
        TrendUpRule(),
        TrendDownRule(),
        AccelerationRule(),
        StagnationRule(),
        SpikeRule(),
    ],
    SignalType.SCORE_ACHIEVED.value: [
        TrendUpRule(),
        TrendDownRule(),
        ConsistencyScoreRule(),
        ThresholdCrossingRule(min_value=0.0, max_value=100.0),
        SpikeRule(),
    ],
    SignalType.TIME_SPENT.value: [
        TrendUpRule(),
        TrendDownRule(),
        SpikeRule(),
    ],
    SignalType.EVIDENCE_QUALITY.value: [
        TrendUpRule(),
        TrendDownRule(),
        ConsistencyScoreRule(),
    ],
    SignalType.TOPICS_COVERED.value: [
        TrendUpRule(),
        TrendDownRule(),
    ],
    SignalType.ROLLING_COMPLETION_RATE.value: [
        TrendUpRule(),
        TrendDownRule(),
        AccelerationRule(),
        StagnationRule(),
    ],
    SignalType.ROLLING_AVG_XP.value: [
        TrendUpRule(),
        TrendDownRule(),
        AccelerationRule(),
    ],
    SignalType.ROLLING_AVG_SCORE.value: [
        TrendUpRule(),
        TrendDownRule(),
        ConsistencyScoreRule(),
    ],
    SignalType.XP_PER_MINUTE.value: [
        TrendUpRule(),
        TrendDownRule(),
        SpikeRule(),
    ],
    SignalType.STREAK_ACTIVE.value: [
        FrequencyBurstRule(),
    ],
    SignalType.STREAK_LENGTH.value: [
        TrendUpRule(),
        AccelerationRule(),
    ],
}


class PatternDetector:
    def __init__(
        self,
        store: PatternStore,
        signal_store: SignalStore,
        rules: dict[str, list[DetectionRule]] | None = None,
        ulid_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._signal_store = signal_store
        self._rules = DEFAULT_RULES if rules is None else rules
        self._ulid_factory = ulid_factory or _generate_ulid

    def detect(self, builder_id: str) -> list[Pattern]:
        all_patterns: list[Pattern] = []
        factory = self._ulid_factory

        for signal_type, rules in self._rules.items():
            signals = self._signal_store.list_recent(
                builder_id=builder_id,
                signal_type=signal_type,
                limit=30,
            )
            if not signals:
                continue

            for rule in rules:
                try:
                    patterns = rule.detect(signals, factory)
                    if patterns:
                        self._store.save_many(patterns)
                        all_patterns.extend(patterns)
                except Exception:
                    continue

        return all_patterns

    @property
    def store(self) -> PatternStore:
        return self._store
