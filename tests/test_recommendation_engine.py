from ascend.cognitive.models import (
    InMemoryInsightStore,
    InMemoryRecommendationStore,
    Insight,
    InsightType,
    InsightSeverity,
    RecommendationPriority,
    RecommendationType,
)
from ascend.cognitive.recommendation_engine import (
    AdvanceContentRule,
    CelebrateRule,
    ChangePaceRule,
    DEFAULT_RECOMMENDATION_RULES,
    ExploreNewAreaRule,
    FocusAreaRule,
    RecommendationEngine,
    RecommendationRule,
    RepeatContentRule,
    ReviewFoundationsRule,
    TakeBreakRule,
    TryMissionRule,
)

_BUILDER_ID = "builder-test-001"
_ulid_counter: int = 0


def _ulid() -> str:
    global _ulid_counter
    _ulid_counter += 1
    return "ulid-" + str(_ulid_counter).zfill(6)


def _now() -> str:
    return "2026-07-21T12:00:00Z"


def _make_insight(
    insight_type: str,
    severity: str = InsightSeverity.INFO.value,
    confidence: float = 1.0,
    builder_id: str = _BUILDER_ID,
) -> Insight:
    return Insight(
        id=_ulid(),
        insight_type=insight_type,
        title=f"Test {insight_type}",
        description="Test insight",
        severity=severity,
        confidence=confidence,
        source_pattern_ids=["pat-1"],
        generated_at=_now(),
        metadata={"builderId": builder_id},
    )


# ─── TryMissionRule ─────────────────────────────────────────────────────────


class TestTryMissionRule:
    def test_declining_performance(self) -> None:
        ins = _make_insight(InsightType.DECLINING_PERFORMANCE.value)
        rule = TryMissionRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.TRY_MISSION.value

    def test_other_insight_returns_empty(self) -> None:
        ins = _make_insight(InsightType.ACCELERATING_GROWTH.value)
        rule = TryMissionRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 0


# ─── RepeatContentRule ──────────────────────────────────────────────────────


class TestRepeatContentRule:
    def test_critical_declining(self) -> None:
        ins = _make_insight(InsightType.DECLINING_PERFORMANCE.value, severity=InsightSeverity.CRITICAL.value)
        rule = RepeatContentRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.REPEAT_CONTENT.value

    def test_info_declining_returns_empty(self) -> None:
        ins = _make_insight(InsightType.DECLINING_PERFORMANCE.value, severity=InsightSeverity.INFO.value)
        rule = RepeatContentRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 0


# ─── AdvanceContentRule ─────────────────────────────────────────────────────


class TestAdvanceContentRule:
    def test_accelerating_growth(self) -> None:
        ins = _make_insight(InsightType.ACCELERATING_GROWTH.value)
        rule = AdvanceContentRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.ADVANCE_CONTENT.value

    def test_strength_identified(self) -> None:
        ins = _make_insight(InsightType.STRENGTH_IDENTIFIED.value)
        rule = AdvanceContentRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1


# ─── ExploreNewAreaRule ─────────────────────────────────────────────────────


class TestExploreNewAreaRule:
    def test_stagnation(self) -> None:
        ins = _make_insight(InsightType.STAGNATION_WARNING.value)
        rule = ExploreNewAreaRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.EXPLORE_NEW_AREA.value


# ─── TakeBreakRule ──────────────────────────────────────────────────────────


class TestTakeBreakRule:
    def test_streak_milestone(self) -> None:
        ins = _make_insight(InsightType.STREAK_MILESTONE.value)
        rule = TakeBreakRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.TAKE_BREAK.value


# ─── ReviewFoundationsRule ──────────────────────────────────────────────────


class TestReviewFoundationsRule:
    def test_critical_consistency_break(self) -> None:
        ins = _make_insight(InsightType.CONSISTENCY_BREAK.value, severity=InsightSeverity.CRITICAL.value)
        rule = ReviewFoundationsRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.REVIEW_FOUNDATIONS.value


# ─── CelebrateRule ──────────────────────────────────────────────────────────


class TestCelebrateRule:
    def test_milestone_achieved(self) -> None:
        ins = _make_insight(InsightType.MILESTONE_ACHIEVED.value)
        rule = CelebrateRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.CELEBRATE.value


# ─── FocusAreaRule ──────────────────────────────────────────────────────────


class TestFocusAreaRule:
    def test_improvement_opportunity(self) -> None:
        ins = _make_insight(InsightType.IMPROVEMENT_OPPORTUNITY.value)
        rule = FocusAreaRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.FOCUS_AREA.value


# ─── ChangePaceRule ─────────────────────────────────────────────────────────


class TestChangePaceRule:
    def test_engagement_drop(self) -> None:
        ins = _make_insight(InsightType.ENGAGEMENT_DROP.value)
        rule = ChangePaceRule()
        result = rule.recommend([ins], _ulid)
        assert len(result) == 1
        assert result[0].recommendation_type == RecommendationType.CHANGE_PACE.value


# ─── RecommendationEngine (Orchestrator) ────────────────────────────────────


class TestRecommendationEngine:
    def test_generates_recommendations(self) -> None:
        ins_store = InMemoryInsightStore()
        rec_store = InMemoryRecommendationStore()
        ins = _make_insight(InsightType.STAGNATION_WARNING.value)
        ins_store.save(ins)

        engine = RecommendationEngine(
            store=rec_store,
            insight_store=ins_store,
            rules=[ExploreNewAreaRule()],
            ulid_factory=_ulid,
        )
        recs = engine.recommend(_BUILDER_ID)
        assert len(recs) == 1
        assert recs[0].recommendation_type == RecommendationType.EXPLORE_NEW_AREA.value

    def test_no_insights_returns_empty(self) -> None:
        ins_store = InMemoryInsightStore()
        rec_store = InMemoryRecommendationStore()
        engine = RecommendationEngine(
            store=rec_store,
            insight_store=ins_store,
            ulid_factory=_ulid,
        )
        recs = engine.recommend(_BUILDER_ID)
        assert len(recs) == 0

    def test_recommendations_persisted(self) -> None:
        ins_store = InMemoryInsightStore()
        rec_store = InMemoryRecommendationStore()
        ins = _make_insight(InsightType.STAGNATION_WARNING.value)
        ins_store.save(ins)

        engine = RecommendationEngine(
            store=rec_store,
            insight_store=ins_store,
            ulid_factory=_ulid,
        )
        engine.recommend(_BUILDER_ID)
        assert rec_store.count_all() >= 1

    def test_determinism(self) -> None:
        ins_store = InMemoryInsightStore()
        rec_store1 = InMemoryRecommendationStore()
        ins = _make_insight(InsightType.STAGNATION_WARNING.value)
        ins_store.save(ins)

        engine1 = RecommendationEngine(
            store=rec_store1,
            insight_store=ins_store,
            rules=[ExploreNewAreaRule()],
            ulid_factory=_ulid,
        )
        r1 = engine1.recommend(_BUILDER_ID)

        ins_store2 = InMemoryInsightStore()
        rec_store2 = InMemoryRecommendationStore()
        ins2 = _make_insight(InsightType.STAGNATION_WARNING.value)
        ins_store2.save(ins2)
        global _ulid_counter
        _ulid_counter = 0

        engine2 = RecommendationEngine(
            store=rec_store2,
            insight_store=ins_store2,
            rules=[ExploreNewAreaRule()],
            ulid_factory=_ulid,
        )
        r2 = engine2.recommend(_BUILDER_ID)

        assert len(r1) == len(r2)
        assert r1[0].recommendation_type == r2[0].recommendation_type

    def test_rule_failure_does_not_block(self) -> None:
        class FailingRule:
            def recommend(self, insights, ulid_factory):
                raise RuntimeError("fail")

        ins_store = InMemoryInsightStore()
        rec_store = InMemoryRecommendationStore()
        ins = _make_insight(InsightType.STAGNATION_WARNING.value)
        ins_store.save(ins)

        engine = RecommendationEngine(
            store=rec_store,
            insight_store=ins_store,
            rules=[FailingRule(), ExploreNewAreaRule()],  # type: ignore
            ulid_factory=_ulid,
        )
        recs = engine.recommend(_BUILDER_ID)
        assert len(recs) >= 1

    def test_default_rules_coverage(self) -> None:
        assert len(DEFAULT_RECOMMENDATION_RULES) >= 8
        for rule in DEFAULT_RECOMMENDATION_RULES:
            assert isinstance(rule, object)

    def test_recommendation_rule_protocol(self) -> None:
        rule: RecommendationRule = TryMissionRule()
        ins = _make_insight(InsightType.DECLINING_PERFORMANCE.value)
        result = rule.recommend([ins], _ulid)
        assert isinstance(result, list)
