from ascend.cognitive.models import (
    InMemoryPatternStore,
    InMemoryInsightStore,
    Pattern,
    PatternType,
    Insight,
    InsightType,
    InsightSeverity,
)
from ascend.cognitive.insight_engine import (
    AcceleratingGrowthRule,
    ConsistencyBreakRule,
    DecliningPerformanceRule,
    DEFAULT_INSIGHT_RULES,
    EngagementDropRule,
    ImprovementOpportunityRule,
    InsightEngine,
    InsightRule,
    MilestoneAchievedRule,
    StagnationWarningRule,
    StrengthIdentifiedRule,
    StreakMilestoneRule,
)

_BUILDER_ID = "builder-test-001"
_ulid_counter: int = 0


def _ulid() -> str:
    global _ulid_counter
    _ulid_counter += 1
    return "ulid-" + str(_ulid_counter).zfill(6)


def _now() -> str:
    return "2026-07-21T12:00:00Z"


def _make_pattern(
    pattern_type: str,
    value: float = 0.0,
    confidence: float = 1.0,
    slope: float = 0.0,
    is_consistent: bool | None = None,
    label: str = "",
    builder_id: str = _BUILDER_ID,
) -> Pattern:
    md: dict = {"builderId": builder_id, "ruleName": "test"}
    if slope != 0:
        md["slope"] = slope
    if is_consistent is not None:
        md["isConsistent"] = is_consistent
    if not label:
        label = f"Pattern {pattern_type}"
    return Pattern(
        id=_ulid(),
        pattern_type=pattern_type,
        label=label,
        value=value,
        confidence=confidence,
        source_signal_ids=["sig-1"],
        observed_at=_now(),
        metadata=md,
    )


# ─── DecliningPerformanceRule ───────────────────────────────────────────────


class TestDecliningPerformanceRule:
    def test_declining_critical(self) -> None:
        pat = _make_pattern(PatternType.TREND_DOWN.value, slope=-0.15)
        rule = DecliningPerformanceRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.DECLINING_PERFORMANCE.value
        assert result[0].severity == InsightSeverity.CRITICAL.value

    def test_declining_warning(self) -> None:
        pat = _make_pattern(PatternType.TREND_DOWN.value, slope=-0.07)
        rule = DecliningPerformanceRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].severity == InsightSeverity.WARNING.value

    def test_declining_info(self) -> None:
        pat = _make_pattern(PatternType.TREND_DOWN.value, slope=-0.02)
        rule = DecliningPerformanceRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].severity == InsightSeverity.INFO.value

    def test_non_declining_returns_empty(self) -> None:
        pat = _make_pattern(PatternType.TREND_UP.value)
        rule = DecliningPerformanceRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 0


# ─── AcceleratingGrowthRule ─────────────────────────────────────────────────


class TestAcceleratingGrowthRule:
    def test_acceleration_detected(self) -> None:
        pat = _make_pattern(PatternType.ACCELERATION.value)
        rule = AcceleratingGrowthRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.ACCELERATING_GROWTH.value

    def test_trend_up_detected(self) -> None:
        pat = _make_pattern(PatternType.TREND_UP.value)
        rule = AcceleratingGrowthRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1

    def test_other_pattern_returns_empty(self) -> None:
        pat = _make_pattern(PatternType.SPIKE.value)
        rule = AcceleratingGrowthRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 0


# ─── ConsistencyBreakRule ───────────────────────────────────────────────────


class TestConsistencyBreakRule:
    def test_inconsistent_detected(self) -> None:
        pat = _make_pattern(PatternType.CONSISTENCY_SCORE.value, is_consistent=False)
        rule = ConsistencyBreakRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.CONSISTENCY_BREAK.value

    def test_consistent_returns_empty(self) -> None:
        pat = _make_pattern(PatternType.CONSISTENCY_SCORE.value, is_consistent=True)
        rule = ConsistencyBreakRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 0


# ─── StrengthIdentifiedRule ─────────────────────────────────────────────────


class TestStrengthIdentifiedRule:
    def test_consistent_and_trend_up(self) -> None:
        pat1 = _make_pattern(PatternType.CONSISTENCY_SCORE.value, is_consistent=True)
        pat2 = _make_pattern(PatternType.TREND_UP.value)
        rule = StrengthIdentifiedRule()
        result = rule.generate([pat1, pat2], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.STRENGTH_IDENTIFIED.value

    def test_strength_from_consistency_alone(self) -> None:
        pat = _make_pattern(PatternType.CONSISTENCY_SCORE.value, is_consistent=True)
        rule = StrengthIdentifiedRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.STRENGTH_IDENTIFIED.value


# ─── StagnationWarningRule ──────────────────────────────────────────────────


class TestStagnationWarningRule:
    def test_stagnation_detected(self) -> None:
        pat = _make_pattern(PatternType.STAGNATION.value)
        rule = StagnationWarningRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.STAGNATION_WARNING.value

    def test_other_pattern_returns_empty(self) -> None:
        pat = _make_pattern(PatternType.SPIKE.value)
        rule = StagnationWarningRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 0


# ─── MilestoneAchievedRule ──────────────────────────────────────────────────


class TestMilestoneAchievedRule:
    def test_threshold_crossing_detected(self) -> None:
        pat = _make_pattern(PatternType.THRESHOLD_CROSSING.value)
        rule = MilestoneAchievedRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.MILESTONE_ACHIEVED.value


# ─── ImprovementOpportunityRule ─────────────────────────────────────────────


class TestImprovementOpportunityRule:
    def test_performance_gap_detected(self) -> None:
        pat = _make_pattern(PatternType.PERFORMANCE_GAP.value)
        rule = ImprovementOpportunityRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.IMPROVEMENT_OPPORTUNITY.value

    def test_other_pattern_returns_empty(self) -> None:
        pat = _make_pattern(PatternType.TREND_UP.value)
        rule = ImprovementOpportunityRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 0


# ─── EngagementDropRule ─────────────────────────────────────────────────────


class TestEngagementDropRule:
    def test_trend_down_on_streak(self) -> None:
        pat = _make_pattern(PatternType.TREND_DOWN.value, label="streak")
        rule = EngagementDropRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.ENGAGEMENT_DROP.value


# ─── StreakMilestoneRule ────────────────────────────────────────────────────


class TestStreakMilestoneRule:
    def test_streak_trend_up(self) -> None:
        pat = _make_pattern(PatternType.TREND_UP.value, label="streak")
        rule = StreakMilestoneRule()
        result = rule.generate([pat], _ulid)
        assert len(result) == 1
        assert result[0].insight_type == InsightType.STREAK_MILESTONE.value


# ─── InsightEngine (Orchestrator) ───────────────────────────────────────────


class TestInsightEngine:
    def test_generates_insights_from_patterns(self) -> None:
        pat_store = InMemoryPatternStore()
        ins_store = InMemoryInsightStore()
        pat1 = _make_pattern(PatternType.TREND_DOWN.value, slope=-0.15)
        pat2 = _make_pattern(PatternType.STAGNATION.value)
        pat_store.save_many([pat1, pat2])

        engine = InsightEngine(
            store=ins_store,
            pattern_store=pat_store,
            rules=[DecliningPerformanceRule(), StagnationWarningRule()],
            ulid_factory=_ulid,
        )
        insights = engine.generate(_BUILDER_ID)
        assert len(insights) >= 2

    def test_no_patterns_returns_empty(self) -> None:
        pat_store = InMemoryPatternStore()
        ins_store = InMemoryInsightStore()
        engine = InsightEngine(
            store=ins_store,
            pattern_store=pat_store,
            ulid_factory=_ulid,
        )
        insights = engine.generate(_BUILDER_ID)
        assert len(insights) == 0

    def test_insights_are_persisted(self) -> None:
        pat_store = InMemoryPatternStore()
        ins_store = InMemoryInsightStore()
        pat = _make_pattern(PatternType.STAGNATION.value)
        pat_store.save(pat)

        engine = InsightEngine(
            store=ins_store,
            pattern_store=pat_store,
            ulid_factory=_ulid,
        )
        engine.generate(_BUILDER_ID)
        assert ins_store.count_all() >= 1

    def test_determinism(self) -> None:
        pat_store = InMemoryPatternStore()
        ins_store1 = InMemoryInsightStore()
        pat = _make_pattern(PatternType.TREND_DOWN.value, slope=-0.15)
        pat_store.save(pat)

        engine1 = InsightEngine(
            store=ins_store1,
            pattern_store=pat_store,
            rules=[DecliningPerformanceRule()],
            ulid_factory=_ulid,
        )
        r1 = engine1.generate(_BUILDER_ID)

        pat_store2 = InMemoryPatternStore()
        ins_store2 = InMemoryInsightStore()
        pat2 = _make_pattern(PatternType.TREND_DOWN.value, slope=-0.15)
        pat_store2.save(pat2)
        global _ulid_counter
        _ulid_counter = 0

        engine2 = InsightEngine(
            store=ins_store2,
            pattern_store=pat_store2,
            rules=[DecliningPerformanceRule()],
            ulid_factory=_ulid,
        )
        r2 = engine2.generate(_BUILDER_ID)

        assert len(r1) == len(r2)
        assert r1[0].severity == r2[0].severity
        assert r1[0].insight_type == r2[0].insight_type

    def test_rule_failure_does_not_block(self) -> None:
        class FailingRule:
            def generate(self, patterns, ulid_factory):
                raise RuntimeError("fail")

        pat_store = InMemoryPatternStore()
        ins_store = InMemoryInsightStore()
        pat = _make_pattern(PatternType.STAGNATION.value)
        pat_store.save(pat)

        engine = InsightEngine(
            store=ins_store,
            pattern_store=pat_store,
            rules=[FailingRule(), StagnationWarningRule()],  # type: ignore
            ulid_factory=_ulid,
        )
        insights = engine.generate(_BUILDER_ID)
        assert len(insights) >= 1

    def test_default_rules_coverage(self) -> None:
        assert len(DEFAULT_INSIGHT_RULES) >= 8
        for rule in DEFAULT_INSIGHT_RULES:
            assert isinstance(rule, object)

    def test_insight_rule_protocol(self) -> None:
        rule: InsightRule = DecliningPerformanceRule()
        pat = _make_pattern(PatternType.TREND_DOWN.value)
        result = rule.generate([pat], _ulid)
        assert isinstance(result, list)
