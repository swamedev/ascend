from datetime import datetime, timezone
from typing import Any, Callable, Protocol

from .models import (
    Insight,
    InsightStore,
    InsightType,
    InsightSeverity,
    Recommendation,
    RecommendationStore,
    RecommendationType,
    RecommendationPriority,
)

from .normalizer import _generate_ulid


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_builder_id(insight: Insight) -> str:
    return insight.metadata.get("builderId", "")


class RecommendationRule(Protocol):
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]: ...


class TryMissionRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type not in (
                InsightType.DECLINING_PERFORMANCE.value,
                InsightType.CONSISTENCY_BREAK.value,
            ):
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.TRY_MISSION.value,
                    title="Try an easier mission",
                    description=(
                        "Consider selecting a less difficult mission to "
                        "rebuild confidence and regain momentum."
                    ),
                    priority=RecommendationPriority.HIGH.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "TryMissionRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class RepeatContentRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type != InsightType.DECLINING_PERFORMANCE.value:
                continue
            if insight.severity != InsightSeverity.CRITICAL.value:
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.REPEAT_CONTENT.value,
                    title="Repeat recent content",
                    description=(
                        "Review and re-attempt recent missions to strengthen "
                        "understanding and close performance gaps."
                    ),
                    priority=RecommendationPriority.HIGH.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "RepeatContentRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class AdvanceContentRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type not in (
                InsightType.ACCELERATING_GROWTH.value,
                InsightType.STRENGTH_IDENTIFIED.value,
            ):
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.ADVANCE_CONTENT.value,
                    title="Try harder content",
                    description=(
                        "You are ready for more challenging material. "
                        "Increase mission difficulty to sustain growth."
                    ),
                    priority=RecommendationPriority.MEDIUM.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "AdvanceContentRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class ExploreNewAreaRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type != InsightType.STAGNATION_WARNING.value:
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.EXPLORE_NEW_AREA.value,
                    title="Explore a new topic",
                    description=(
                        "Progress has plateaued. Exploring a different subject "
                        "may reignite engagement and unlock fresh growth."
                    ),
                    priority=RecommendationPriority.MEDIUM.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "ExploreNewAreaRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class TakeBreakRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type != InsightType.STREAK_MILESTONE.value:
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.TAKE_BREAK.value,
                    title="Take a break",
                    description=(
                        "You have reached a streak milestone. Rest and "
                        "recovery help maintain long-term consistency."
                    ),
                    priority=RecommendationPriority.LOW.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "TakeBreakRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class ReviewFoundationsRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type != InsightType.CONSISTENCY_BREAK.value:
                continue
            if insight.severity != InsightSeverity.CRITICAL.value:
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.REVIEW_FOUNDATIONS.value,
                    title="Review fundamentals",
                    description=(
                        "A critical consistency break suggests foundational "
                        "gaps. Revisit core concepts before moving forward."
                    ),
                    priority=RecommendationPriority.HIGH.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "ReviewFoundationsRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class CelebrateRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type != InsightType.MILESTONE_ACHIEVED.value:
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.CELEBRATE.value,
                    title="Celebrate achievement",
                    description=(
                        "A milestone has been reached. Acknowledge the "
                        "progress and share the accomplishment."
                    ),
                    priority=RecommendationPriority.LOW.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "CelebrateRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class FocusAreaRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type not in (
                InsightType.IMPROVEMENT_OPPORTUNITY.value,
            ):
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.FOCUS_AREA.value,
                    title="Focus on weak area",
                    description=(
                        "Target the identified skill gap with deliberate "
                        "practice and dedicated missions."
                    ),
                    priority=RecommendationPriority.MEDIUM.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "FocusAreaRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


class ChangePaceRule:
    def recommend(
        self,
        insights: list[Insight],
        ulid_factory: Callable[[], str],
    ) -> list[Recommendation]:
        results: list[Recommendation] = []
        for insight in insights:
            if insight.insight_type != InsightType.ENGAGEMENT_DROP.value:
                continue
            results.append(
                Recommendation(
                    id=ulid_factory(),
                    recommendation_type=RecommendationType.CHANGE_PACE.value,
                    title="Adjust mission frequency",
                    description=(
                        "Engagement is dropping. Consider reducing mission "
                        "frequency or introducing variety to re-engage."
                    ),
                    priority=RecommendationPriority.MEDIUM.value,
                    source_insight_ids=[insight.id],
                    target=None,
                    generated_at=_now(),
                    metadata={
                        "ruleName": "ChangePaceRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(insight),
                    },
                )
            )
        return results


DEFAULT_RECOMMENDATION_RULES: list[RecommendationRule] = [
    TryMissionRule(),
    RepeatContentRule(),
    AdvanceContentRule(),
    ExploreNewAreaRule(),
    TakeBreakRule(),
    ReviewFoundationsRule(),
    CelebrateRule(),
    FocusAreaRule(),
    ChangePaceRule(),
]


class RecommendationEngine:
    def __init__(
        self,
        store: RecommendationStore,
        insight_store: InsightStore,
        rules: list[RecommendationRule] | None = None,
        ulid_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._insight_store = insight_store
        self._rules = DEFAULT_RECOMMENDATION_RULES if rules is None else rules
        self._ulid_factory = ulid_factory or _generate_ulid

    def recommend(self, builder_id: str) -> list[Recommendation]:
        all_recommendations: list[Recommendation] = []
        factory = self._ulid_factory

        insights = self._insight_store.list_by_builder(
            builder_id=builder_id,
            limit=50,
        )
        if not insights:
            return []

        for rule in self._rules:
            try:
                recommendations = rule.recommend(insights, factory)
                if recommendations:
                    self._store.save_many(recommendations)
                    all_recommendations.extend(recommendations)
            except Exception:
                continue

        return all_recommendations

    @property
    def store(self) -> RecommendationStore:
        return self._store
