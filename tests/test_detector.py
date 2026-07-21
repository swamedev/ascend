from datetime import datetime, timezone
from typing import Callable

import pytest

from ascend.cognitive.models import (
    InMemoryPatternStore,
    InMemorySignalStore,
    Pattern,
    PatternType,
    Signal,
    SignalType,
)
from ascend.cognitive.detector import (
    AccelerationRule,
    ConsistencyScoreRule,
    DetectionRule,
    FrequencyBurstRule,
    PatternDetector,
    PerformanceGapRule,
    SpikeRule,
    StagnationRule,
    ThresholdCrossingRule,
    TrendDownRule,
    TrendUpRule,
    DEFAULT_RULES,
)


_BUILDER_ID = "builder-test-001"


_ulid_counter: int = 0

def _ulid() -> str:
    global _ulid_counter
    _ulid_counter += 1
    return "ulid-" + str(_ulid_counter).zfill(6)


def _now() -> str:
    return "2026-07-21T12:00:00Z"


def _make_signal(
    signal_type: str,
    value: float,
    builder_id: str = _BUILDER_ID,
    signal_id: str | None = None,
) -> Signal:
    return Signal(
        id=signal_id or _ulid(),
        observationId="obs-" + _ulid(),
        type=signal_type,
        value=value,
        confidence=1.0,
        extractedAt=_now(),
        metadata={"builderId": builder_id},
    )


def _make_signals(
    signal_type: str,
    values: list[float],
    builder_id: str = _BUILDER_ID,
) -> list[Signal]:
    return [_make_signal(signal_type, v, builder_id) for v in values]


def _make_stored_signals(
    store: InMemorySignalStore,
    signal_type: str,
    values: list[float],
    builder_id: str = _BUILDER_ID,
) -> list[Signal]:
    signals = _make_signals(signal_type, values, builder_id)
    for s in signals:
        store.save(s)
    return signals


# ─── TrendUpRule ─────────────────────────────────────────────────────────────


class TestTrendUpRule:
    def test_ascending_values_detects_trend(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.3, 0.5, 0.7, 0.9])
        rule = TrendUpRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.TREND_UP.value
        assert result[0].value > 0

    def test_descending_values_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.9, 0.7, 0.5, 0.3])
        rule = TrendUpRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_flat_values_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.5, 0.5, 0.5, 0.5])
        rule = TrendUpRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.5, 0.6])
        rule = TrendUpRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_empty_list_returns_empty(self) -> None:
        rule = TrendUpRule()
        result = rule.detect([], _ulid)
        assert len(result) == 0

    def test_determinism(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 20, 30, 40, 50])
        rule = TrendUpRule()
        result1 = rule.detect(signals, _ulid)
        global _ulid_counter
        _ulid_counter = 0
        result2 = rule.detect(signals, _ulid)
        assert len(result1) == len(result2)
        assert result1[0].value == result2[0].value


# ─── TrendDownRule ───────────────────────────────────────────────────────────


class TestTrendDownRule:
    def test_descending_values_detects_trend(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.9, 0.7, 0.5, 0.3])
        rule = TrendDownRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.TREND_DOWN.value
        assert result[0].value < 0

    def test_ascending_values_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.3, 0.5, 0.7, 0.9])
        rule = TrendDownRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.5])
        rule = TrendDownRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0


# ─── SpikeRule ───────────────────────────────────────────────────────────────


class TestSpikeRule:
    def test_detects_upward_spike(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 12, 11, 100])
        rule = SpikeRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.SPIKE.value
        assert result[0].value > 0

    def test_detects_downward_spike(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [50, 48, 52, 5])
        rule = SpikeRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].value < 0

    def test_no_spike_in_uniform_data(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 10, 10, 11])
        rule = SpikeRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 11, 12])
        rule = SpikeRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0


# ─── ThresholdCrossingRule ───────────────────────────────────────────────────


class TestThresholdCrossingRule:
    def test_below_minimum(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [50, 30, 80])
        rule = ThresholdCrossingRule(min_value=40.0)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.THRESHOLD_CROSSING.value

    def test_above_maximum(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [50, 110, 80])
        rule = ThresholdCrossingRule(max_value=100.0)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1

    def test_no_crossing_within_bounds(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [50, 60, 80])
        rule = ThresholdCrossingRule(min_value=0.0, max_value=100.0)
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_multiple_crossings(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [120, 50, 130])
        rule = ThresholdCrossingRule(max_value=100.0)
        result = rule.detect(signals, _ulid)
        assert len(result) == 2


# ─── ConsistencyScoreRule ────────────────────────────────────────────────────


class TestConsistencyScoreRule:
    def test_consistent_values(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [85, 86, 84, 87])
        rule = ConsistencyScoreRule(cv_threshold=0.3)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.CONSISTENCY_SCORE.value
        assert "Consistent" in result[0].label

    def test_inconsistent_values(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [90, 40, 95, 30])
        rule = ConsistencyScoreRule(cv_threshold=0.3)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert "Inconsistent" in result[0].label

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [85, 86])
        rule = ConsistencyScoreRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0


# ─── AccelerationRule ────────────────────────────────────────────────────────


class TestAccelerationRule:
    def test_accelerating_values(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 20, 40, 80])
        rule = AccelerationRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.ACCELERATION.value
        assert result[0].value > 0

    def test_linear_values_returns_empty(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 20, 30, 40])
        rule = AccelerationRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_decelerating_returns_empty(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [80, 60, 30, 10])
        rule = AccelerationRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.XP_GAINED.value, [10, 20])
        rule = AccelerationRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0


# ─── StagnationRule ──────────────────────────────────────────────────────────


class TestStagnationRule:
    def test_stagnant_values_detected(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.5, 0.51, 0.49, 0.5])
        rule = StagnationRule(slope_threshold=0.05)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.STAGNATION.value

    def test_trending_values_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.3, 0.5, 0.7, 0.9])
        rule = StagnationRule(slope_threshold=0.01)
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.COMPLETION_RATE.value, [0.5, 0.51])
        rule = StagnationRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0


# ─── FrequencyBurstRule ──────────────────────────────────────────────────────


class TestFrequencyBurstRule:
    def test_high_frequency_detects_burst(self) -> None:
        signals = _make_signals(SignalType.STREAK_ACTIVE.value, [1] * 15)
        rule = FrequencyBurstRule(burst_threshold=10)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.FREQUENCY_BURST.value
        assert result[0].value == 15

    def test_low_frequency_returns_empty(self) -> None:
        signals = _make_signals(SignalType.STREAK_ACTIVE.value, [1] * 5)
        rule = FrequencyBurstRule(burst_threshold=10)
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_empty_returns_empty(self) -> None:
        rule = FrequencyBurstRule()
        result = rule.detect([], _ulid)
        assert len(result) == 0


# ─── PerformanceGapRule ──────────────────────────────────────────────────────


class TestPerformanceGapRule:
    def test_large_gap_detected(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [80, 85, 90, 40])
        rule = PerformanceGapRule(gap_threshold=0.2)
        result = rule.detect(signals, _ulid)
        assert len(result) == 1
        assert result[0].pattern_type == PatternType.PERFORMANCE_GAP.value

    def test_small_gap_returns_empty(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [80, 81, 79, 80])
        rule = PerformanceGapRule(gap_threshold=5.0)
        result = rule.detect(signals, _ulid)
        assert len(result) == 0

    def test_insufficient_data_returns_empty(self) -> None:
        signals = _make_signals(SignalType.SCORE_ACHIEVED.value, [80])
        rule = PerformanceGapRule()
        result = rule.detect(signals, _ulid)
        assert len(result) == 0


# ─── PatternDetector (Orchestrator) ──────────────────────────────────────────


class TestPatternDetector:
    def test_detect_returns_patterns_from_stored_signals(self) -> None:
        signal_store = InMemorySignalStore()
        pattern_store = InMemoryPatternStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.3, 0.5, 0.7, 0.9],
        )

        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)

        assert len(patterns) >= 1

    def test_no_signals_returns_empty(self) -> None:
        signal_store = InMemorySignalStore()
        pattern_store = InMemoryPatternStore()
        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)
        assert len(patterns) == 0

    def test_detected_patterns_are_persisted(self) -> None:
        signal_store = InMemorySignalStore()
        pattern_store = InMemoryPatternStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.3, 0.5, 0.7, 0.9],
        )

        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            ulid_factory=_ulid,
        )
        detector.detect(_BUILDER_ID)

        assert pattern_store.count_all() >= 1

    def test_determinism_with_same_signals(self) -> None:
        signal_store = InMemorySignalStore()
        pattern_store = InMemoryPatternStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.2, 0.4, 0.6, 0.8],
        )

        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            rules={SignalType.COMPLETION_RATE.value: [TrendUpRule()]},
            ulid_factory=_ulid,
        )
        patterns1 = detector.detect(_BUILDER_ID)

        signal_store2 = InMemorySignalStore()
        pattern_store2 = InMemoryPatternStore()
        _make_stored_signals(
            signal_store2, SignalType.COMPLETION_RATE.value,
            [0.2, 0.4, 0.6, 0.8],
        )
        global _ulid_counter
        _ulid_counter = 0
        detector2 = PatternDetector(
            store=pattern_store2,
            signal_store=signal_store2,
            rules={SignalType.COMPLETION_RATE.value: [TrendUpRule()]},
            ulid_factory=_ulid,
        )
        patterns2 = detector2.detect(_BUILDER_ID)

        assert len(patterns1) == len(patterns2)
        assert patterns1[0].value == patterns2[0].value
        assert patterns1[0].pattern_type == patterns2[0].pattern_type

    def test_detects_multiple_pattern_types(self) -> None:
        signal_store = InMemorySignalStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.1, 0.3, 0.5, 0.7, 0.9],
        )
        _make_stored_signals(
            signal_store, SignalType.XP_GAINED.value,
            [10, 20, 30, 40, 50],
        )

        pattern_store = InMemoryPatternStore()
        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)

        types_found = {p.pattern_type for p in patterns}
        assert PatternType.TREND_UP.value in types_found

    def test_rule_failure_does_not_block_other_rules(self) -> None:
        class FailingRule:
            def detect(self, signals, ulid_factory):
                raise RuntimeError("Intentional failure")

        signal_store = InMemorySignalStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.3, 0.5, 0.7],
        )

        pattern_store = InMemoryPatternStore()
        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            rules={
                SignalType.COMPLETION_RATE.value: [
                    FailingRule(),  # type: ignore
                    TrendUpRule(),
                ],
            },
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)
        assert len(patterns) >= 1


# ─── Edge Cases ──────────────────────────────────────────────────────────────


class TestPatternEdgeCases:
    def test_signal_with_zero_confidence_skipped(self) -> None:
        signal_store = InMemorySignalStore()
        signal = _make_signal(SignalType.COMPLETION_RATE.value, 0.5)
        signal_store.save(signal)

        pattern_store = InMemoryPatternStore()
        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)
        assert len(patterns) == 0

    def test_different_builder_isolation(self) -> None:
        signal_store = InMemorySignalStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.3, 0.5, 0.7, 0.9],
            builder_id="builder-other",
        )

        pattern_store = InMemoryPatternStore()
        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)
        assert len(patterns) == 0

    def test_pattern_store_persistence(self) -> None:
        store = InMemoryPatternStore()
        pattern = Pattern(
            id=_ulid(),
            pattern_type=PatternType.TREND_UP.value,
            label="Test pattern",
            value=0.5,
            confidence=0.8,
            source_signal_ids=["sig-1", "sig-2"],
            observed_at=_now(),
            metadata={"builderId": _BUILDER_ID},
        )
        store.save(pattern)
        assert store.count_all() == 1
        retrieved = store.list_by_builder(_BUILDER_ID)
        assert len(retrieved) == 1
        assert retrieved[0].id == pattern.id

    def test_pattern_store_filter_by_type(self) -> None:
        store = InMemoryPatternStore()
        for pt in [PatternType.TREND_UP, PatternType.SPIKE, PatternType.TREND_UP]:
            store.save(Pattern(
                id=_ulid(),
                pattern_type=pt.value,
                label="test",
                value=1.0,
                confidence=0.5,
                source_signal_ids=[],
                observed_at=_now(),
                metadata={"builderId": _BUILDER_ID},
            ))
        up_patterns = store.get_by_type(PatternType.TREND_UP.value)
        assert len(up_patterns) == 2

    def test_detection_rule_protocol(self) -> None:
        rule: DetectionRule = TrendUpRule()
        signals = _make_signals(SignalType.XP_GAINED.value, [1, 2, 3])
        result = rule.detect(signals, _ulid)
        assert isinstance(result, list)

    def test_empty_rule_list(self) -> None:
        signal_store = InMemorySignalStore()
        _make_stored_signals(
            signal_store, SignalType.COMPLETION_RATE.value,
            [0.3, 0.5, 0.7],
        )
        pattern_store = InMemoryPatternStore()
        detector = PatternDetector(
            store=pattern_store,
            signal_store=signal_store,
            rules={},
            ulid_factory=_ulid,
        )
        patterns = detector.detect(_BUILDER_ID)
        assert len(patterns) == 0

    def test_default_rules_coverage(self) -> None:
        for signal_type, rules in DEFAULT_RULES.items():
            assert len(rules) >= 1, f"{signal_type} has no rules"
            for rule in rules:
                assert isinstance(rule, object)
