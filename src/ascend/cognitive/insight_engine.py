from datetime import datetime, timezone
from typing import Any, Callable, Protocol

from .models import (
    Pattern,
    PatternStore,
    PatternType,
    Insight,
    InsightStore,
    InsightType,
    InsightSeverity,
    SignalType,
)

from .normalizer import _generate_ulid


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_builder_id(pattern: Pattern) -> str:
    return pattern.metadata.get("builderId", "")


class InsightRule(Protocol):
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]: ...


class DecliningPerformanceRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.TREND_DOWN.value:
                continue
            slope = p.metadata.get("slope", 0.0)
            if slope < -0.1:
                severity = InsightSeverity.CRITICAL.value
                desc = (
                    f"Performance is declining steeply (slope={slope:.4f}). "
                    "Immediate attention recommended."
                )
            elif slope < -0.05:
                severity = InsightSeverity.WARNING.value
                desc = (
                    f"Performance is declining moderately (slope={slope:.4f}). "
                    "Monitor closely."
                )
            else:
                severity = InsightSeverity.INFO.value
                desc = (
                    f"Slight downward trend detected (slope={slope:.4f}). "
                    "Keep an eye on this metric."
                )
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.DECLINING_PERFORMANCE.value,
                    title="Declining Performance",
                    description=desc,
                    severity=severity,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "DecliningPerformanceRule",
                        "ruleVersion": "1.0",
                        "slope": slope,
                        "severityLabel": severity,
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class AcceleratingGrowthRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type not in (
                PatternType.TREND_UP.value,
                PatternType.ACCELERATION.value,
            ):
                continue
            if p.pattern_type == PatternType.ACCELERATION.value:
                desc = (
                    f"Growth is accelerating (2nd derivative={p.value:.4f}). "
                    "Momentum is building."
                )
            else:
                slope = p.metadata.get("slope", 0.0)
                desc = (
                    f"Consistent upward trend detected (slope={slope:.4f}). "
                    "Performance is on the rise."
                )
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.ACCELERATING_GROWTH.value,
                    title="Accelerating Growth",
                    description=desc,
                    severity=InsightSeverity.INFO.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "AcceleratingGrowthRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class ConsistencyBreakRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.CONSISTENCY_SCORE.value:
                continue
            if p.metadata.get("isConsistent") is not False:
                continue
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.CONSISTENCY_BREAK.value,
                    title="Consistency Break",
                    description=(
                        f"Performance variability detected (CV={p.value:.4f}). "
                        "Patterns are becoming unpredictable."
                    ),
                    severity=InsightSeverity.WARNING.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "ConsistencyBreakRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class StrengthIdentifiedRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.CONSISTENCY_SCORE.value:
                continue
            if p.metadata.get("isConsistent") is not True:
                continue
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.STRENGTH_IDENTIFIED.value,
                    title="Strength Identified",
                    description=(
                        f"Consistent high performance detected (CV={p.value:.4f}). "
                        "This is a reliable area of strength."
                    ),
                    severity=InsightSeverity.INFO.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "StrengthIdentifiedRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class StagnationWarningRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.STAGNATION.value:
                continue
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.STAGNATION_WARNING.value,
                    title="Stagnation Warning",
                    description=(
                        f"No significant progress detected (slope={p.value:.4f}). "
                        "Consider introducing new challenges or varying the approach."
                    ),
                    severity=InsightSeverity.WARNING.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "StagnationWarningRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class MilestoneAchievedRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.THRESHOLD_CROSSING.value:
                continue
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.MILESTONE_ACHIEVED.value,
                    title="Milestone Reached!",
                    description=(
                        f"A threshold was crossed at value {p.value:.2f}. "
                        f"{p.label}"
                    ),
                    severity=InsightSeverity.INFO.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "MilestoneAchievedRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class ImprovementOpportunityRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.PERFORMANCE_GAP.value:
                continue
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.IMPROVEMENT_OPPORTUNITY.value,
                    title="Improvement Opportunity",
                    description=(
                        f"Performance gap identified (gap={p.value:.4f}). "
                        "Targeting this area could yield meaningful gains."
                    ),
                    severity=InsightSeverity.INFO.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "ImprovementOpportunityRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class EngagementDropRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type not in (
                PatternType.TREND_DOWN.value,
                PatternType.FREQUENCY_BURST.value,
            ):
                continue
            if p.pattern_type == PatternType.TREND_DOWN.value:
                desc = (
                    f"Engagement is declining (slope={p.value:.4f}). "
                    "User activity is trending downward."
                )
            else:
                desc = (
                    f"Activity frequency is dropping (signal count={int(p.value)}). "
                    "The user may be disengaging."
                )
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.ENGAGEMENT_DROP.value,
                    title="Engagement Drop",
                    description=desc,
                    severity=InsightSeverity.WARNING.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "EngagementDropRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


class StreakMilestoneRule:
    def generate(
        self,
        patterns: list[Pattern],
        ulid_factory: Callable[[], str],
    ) -> list[Insight]:
        results: list[Insight] = []
        for p in patterns:
            if p.pattern_type != PatternType.TREND_UP.value:
                continue
            results.append(
                Insight(
                    id=ulid_factory(),
                    insight_type=InsightType.STREAK_MILESTONE.value,
                    title="Streak Milestone",
                    description=(
                        f"Streak length is growing (slope={p.value:.4f}). "
                        "Keep the momentum going!"
                    ),
                    severity=InsightSeverity.INFO.value,
                    confidence=p.confidence,
                    source_pattern_ids=[p.id],
                    generated_at=_now(),
                    metadata={
                        "ruleName": "StreakMilestoneRule",
                        "ruleVersion": "1.0",
                        "builderId": _get_builder_id(p),
                    },
                )
            )
        return results


DEFAULT_INSIGHT_RULES: list[InsightRule] = [
    DecliningPerformanceRule(),
    AcceleratingGrowthRule(),
    ConsistencyBreakRule(),
    StrengthIdentifiedRule(),
    StagnationWarningRule(),
    MilestoneAchievedRule(),
    ImprovementOpportunityRule(),
    EngagementDropRule(),
    StreakMilestoneRule(),
]


class InsightEngine:
    def __init__(
        self,
        store: InsightStore,
        pattern_store: PatternStore,
        rules: list[InsightRule] | None = None,
        ulid_factory: Callable[[], str] | None = None,
    ) -> None:
        self._store = store
        self._pattern_store = pattern_store
        self._rules = DEFAULT_INSIGHT_RULES if rules is None else rules
        self._ulid_factory = ulid_factory or _generate_ulid

    def generate(self, builder_id: str) -> list[Insight]:
        all_insights: list[Insight] = []
        factory = self._ulid_factory

        all_patterns = self._pattern_store.list_by_builder(
            builder_id=builder_id,
            limit=200,
        )

        if not all_patterns:
            return []

        for rule in self._rules:
            try:
                insights = rule.generate(all_patterns, factory)
                if insights:
                    self._store.save_many(insights)
                    all_insights.extend(insights)
            except Exception:
                continue

        return all_insights

    @property
    def store(self) -> InsightStore:
        return self._store
