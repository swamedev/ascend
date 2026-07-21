# ARCH-0047 — Recommendation Engine Architecture

| Field | Value |
|-------|-------|
| **ID** | ARCH-0047 |
| **Name** | Recommendation Engine Architecture |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0009 Architectural Invariants, ARCH-0030 Cognitive Architecture, ARCH-0033 Observation Pipeline, ARCH-0043 Insight Architecture, ARCH-0046 Recommendation Protocol |
| **Principle** | Every recommendation is an actionable suggestion derived deterministically from one or more insights |

---

## 1. Purpose

Recommendations are the terminal stage of the Cognitive Pipeline. They translate insights into concrete, actionable suggestions that guide builder behavior. While an insight says *"your completion rate is declining,"* a recommendation says *"try mission X — it covers the same topics at a lower difficulty level."*

This document defines the architecture of the Recommendation Engine (F2). It specifies:
- The recommendation data model and type taxonomy
- The engine's component architecture
- The rule-based mapping from insights to recommendations
- The priority computation model
- Actionability constraints and suppression logic
- The determinism guarantee that supports I18

> **Core Guarantee:** Every recommendation is traceable to the insight(s) that produced it, and every recommendation's target exists in the content library. No recommendation is generated without a valid, actionable target.

---

## 2. Recommendation Model

### 2.1 Schema

```python
@dataclass
class Recommendation:
    id: str                           # ULID
    recommendation_type: str          # From RecommendationType enum
    title: str                        # Short, action-oriented label
    description: str                  # Full recommendation text
    priority: PriorityLevel           # low, medium, high, critical
    source_insight_ids: list[str]     # ULIDs of the insight(s) that triggered this rec
    target: RecommendationTarget | None  # The actionable target (journey, mission, skill)
    generated_at: str                 # ISO 8601 UTC
    metadata: dict[str, Any]          # Rule name, rule version, confidence, etc.
```

### 2.2 RecommendationTarget

```python
@dataclass
class RecommendationTarget:
    target_type: str       # "journey", "mission", "skill"
    target_id: str         # ULID of the target entity
    label: str             # Human-readable target name (for display)
```

### 2.3 PriorityLevel Enum

```python
class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
```

### 2.4 RecommendationType Enum

```python
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
```

---

## 3. Recommendation Type Taxonomy

| RecType | Category | Trigger | Action |
|---------|----------|---------|--------|
| `try_mission` | Suggestion | `declining_performance` | Recommend easier mission |
| `repeat_content` | Practice | `low_confidence` | Repeat recent content |
| `advance_content` | Challenge | `accelerating_growth` | Suggest harder content |
| `explore_new_area` | Exploration | `stagnation` | Suggest different topic |
| `take_break` | Wellness | `streak_milestone` | Suggest rest |
| `review_foundations` | Remediation | `consistency_break` | Review fundamentals |
| `celebrate` | Motivation | `milestone_achieved` | Celebrate achievement |
| `focus_area` | Suggestion | `performance_gap` | Focus on weak area |
| `change_pace` | Suggestion | `engagement_drop` | Adjust mission frequency |

### 3.1 Trigger Mapping

Each trigger is a deterministic pattern detected in the insight stream by the Recommendation Engine. The mapping from insight type to trigger is defined in the rule configuration:

| Insight Pattern | Trigger |
|-----------------|---------|
| `completion_rate < 0.5` AND `trend = declining` | `declining_performance` |
| `average_confidence < 0.6` | `low_confidence` |
| `xp_growth_rate > 2σ` above builder's baseline | `accelerating_growth` |
| `topics_explored < 2` AND `sessions > 10` | `stagnation` |
| `current_streak >= 7` | `streak_milestone` |
| `streak_broken = true` | `consistency_break` |
| `milestone_completed = true` AND `milestone_type = achievement` | `milestone_achieved` |
| `score_variance > 0.3` AND `avg_score < 0.7` | `performance_gap` |
| `session_frequency < 0.5 × baseline` | `engagement_drop` |

---

## 4. Recommendation Engine Architecture

### 4.1 Component Model

```
Insight[]
    │
    ▼
┌─────────────────────────────────────────────┐
│  RecommendationEngine                        │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  Rule Dispatcher                     │    │  Maps insights to matching rules
│  │  - insight type matching            │    │
│  │  - priority sorting                 │    │
│  │  - deduplication                    │    │
│  └──────────┬──────────────────────────┘    │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  Recommendation Rules               │    │  Concrete rules, one per RecType
│  │  - TryMissionRule                   │    │
│  │  - RepeatContentRule                │    │
│  │  - AdvanceContentRule               │    │
│  │  - ExploreNewAreaRule               │    │
│  │  - TakeBreakRule                    │    │
│  │  - ReviewFoundationsRule            │    │
│  │  - CelebrateRule                    │    │
│  │  - FocusAreaRule                    │    │
│  │  - ChangePaceRule                   │    │
│  └──────────┬──────────────────────────┘    │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  Actionability Verifier              │    │  Checks target existence in library
│  └──────────┬──────────────────────────┘    │
│             ▼                               │
│  ┌─────────────────────────────────────┐    │
│  │  RecommendationStore                 │    │  Persists and queries recommendations
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
    │
    ▼
Recommendation[]
```

### 4.2 RecommendationEngine (Orchestrator)

```python
class RecommendationEngine:
    def __init__(
        self,
        rules: list[RecommendationRule],
        verifier: ActionabilityVerifier,
        store: RecommendationStore,
    ):
        self._rules = rules
        self._verifier = verifier
        self._store = store

    def process(self, insights: list[Insight]) -> list[Recommendation]:
        recommendations = []
        for rule in self._rules:
            for insight in insights:
                rec = rule.evaluate(insight)
                if rec is None:
                    continue
                if not self._verifier.is_actionable(rec):
                    continue
                recommendations.append(rec)
        self._store.save_many(recommendations)
        return recommendations
```

### 4.3 RecommendationRule (Protocol)

```python
class RecommendationRule(Protocol):
    @property
    def rec_type(self) -> RecommendationType: ...

    def evaluate(self, insight: Insight) -> Recommendation | None: ...
```

Each rule:
- Matches on a specific insight pattern (insight type + threshold or condition)
- Returns a `Recommendation` if the insight triggers the rule, or `None` if it does not
- Is a pure function (no side effects, no I/O, no state)
- Sets the recommendation's `target` based on available content (queried at rule evaluation time or provided via context)

### 4.4 RecommendationStore (Protocol)

```python
class RecommendationStore(Protocol):
    def save(self, recommendation: Recommendation) -> None: ...
    def save_many(self, recommendations: list[Recommendation]) -> None: ...
    def get_by_id(self, rec_id: str) -> Recommendation | None: ...
    def list_by_builder(
        self, builder_id: str,
        rec_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Recommendation]: ...
    def list_recent(
        self, builder_id: str,
        limit: int = 10,
    ) -> list[Recommendation]: ...
```

### 4.5 Concrete Rule Examples

#### 4.5.1 TryMissionRule

```
Trigger: declining_performance
Input insight: completion_rate < 0.5 AND trend = "declining"
Target query: Find mission with difficulty < current_mission_difficulty
             AND shared_topics >= 3
Fallback: Find any mission with shared_topics >= 3, regardless of difficulty
Suppression: If builder already has an active try_mission recommendation
```

#### 4.5.2 CelebrateRule

```
Trigger: milestone_achieved
Input insight: milestone_completed = true AND milestone_type = "achievement"
Target: null (celebration has no target — it is informational)
Priority: high
Suppression: Never suppressed; celebrations are always shown
```

#### 4.5.3 ReviewFoundationsRule

```
Trigger: consistency_break
Input insight: streak_broken = true AND days_since_last_activity > 3
Target query: Find the most recently completed mission with score < 0.8
             OR the journey's entry-level mission
Fallback: Find the builder's first-ever mission
Suppression: If builder has already reviewed foundations this streak cycle
```

---

## 5. Priority Model

Priority is a composite function of insight severity and rule confidence. Every recommendation rule declares a base priority, which is then modulated by the severity of the triggering insight.

### 5.1 Priority Matrix

| Insight Severity | Confidence >= 0.8 | Confidence >= 0.5 | Confidence < 0.5 |
|-----------------|-------------------|-------------------|-------------------|
| Critical | critical | high | medium |
| High | high | high | medium |
| Medium | medium | medium | low |
| Low | low | low | low |

### 5.2 Severity Classification

Severity is determined by the insight that triggered the recommendation:

| Severity | Insight Characteristics |
|----------|------------------------|
| Critical | Streak broken, performance crash (>40% decline), stagnation >14 days |
| High | Declining performance, engagement drop, recurring low confidence |
| Medium | Performance gap detected, accelerating growth detected |
| Low | Milestone achieved, streak milestone reached, minor fluctuations |

### 5.3 Confidence in Recommendation Context

Confidence in a recommendation is derived from two factors:
- **Insight confidence** — how confident the Insight Generator was in the triggering insight
- **Rule confidence** — a fixed value per rule based on how well the rule maps to builder outcomes

```python
def compute_priority(
    base_priority: PriorityLevel,
    insight_severity: str,
    insight_confidence: float,
) -> PriorityLevel:
    """Map base_priority + severity + confidence to final priority."""
    matrix = {
        ("critical", 0.8): PriorityLevel.CRITICAL,
        ("critical", 0.5): PriorityLevel.HIGH,
        ("critical", 0.0): PriorityLevel.MEDIUM,
        ("high",    0.8): PriorityLevel.HIGH,
        ("high",    0.5): PriorityLevel.HIGH,
        ("high",    0.0): PriorityLevel.MEDIUM,
        ("medium",  0.8): PriorityLevel.MEDIUM,
        ("medium",  0.5): PriorityLevel.MEDIUM,
        ("medium",  0.0): PriorityLevel.LOW,
        ("low",     0.8): PriorityLevel.LOW,
        ("low",     0.5): PriorityLevel.LOW,
        ("low",     0.0): PriorityLevel.LOW,
    }
    key = (insight_severity, _confidence_bucket(insight_confidence))
    return matrix.get(key, base_priority)

def _confidence_bucket(confidence: float) -> float:
    if confidence >= 0.8:
        return 0.8
    elif confidence >= 0.5:
        return 0.5
    return 0.0
```

---

## 6. Actionability

Every recommendation must have a target that exists in the content library. Recommendations without valid targets are suppressed. The engine queries available packages through the Package Loader to verify target existence.

### 6.1 ActionabilityVerifier

```python
class ActionabilityVerifier:
    def __init__(self, package_loader: PackageLoader):
        self._loader = package_loader

    def is_actionable(self, recommendation: Recommendation) -> bool:
        if recommendation.target is None:
            # Informational recommendations (celebrate, take_break)
            # have no target and are always actionable
            return recommendation.recommendation_type in (
                RecommendationType.CELEBRATE,
                RecommendationType.TAKE_BREAK,
            )
        return self._target_exists(recommendation.target)

    def _target_exists(self, target: RecommendationTarget) -> bool:
        """Check that the target journey, mission, or skill exists
        in the loaded content packages."""
        try:
            if target.target_type == "journey":
                return self._loader.get_journey(target.target_id) is not None
            elif target.target_type == "mission":
                return self._loader.get_mission(target.target_id) is not None
            elif target.target_type == "skill":
                return self._loader.get_skill(target.target_id) is not None
            return False
        except PackageNotFoundError:
            return False
```

### 6.2 Suppression Rules

| Condition | Behavior |
|-----------|----------|
| Target journey not found in any loaded package | Suppress recommendation; log WARNING |
| Target mission not found in any loaded package | Suppress recommendation; log WARNING |
| Target skill not found in any loaded package | Suppress recommendation; log WARNING |
| Target is null and rec type is not informational | Suppress recommendation; log ERROR |
| Duplicate recommendation (same type + same target within 24h) | Suppress duplicate; log INFO |
| Builder has already completed the target mission | Suppress recommendation; log INFO |

### 6.3 Package Integration

The Recommendation Engine does not load packages directly. It receives a `PackageLoader` reference at initialization that exposes read-only access to the content library. The PackageLoader is the same instance used by the Runtime Engine (ARCH-0003 Core Engine Specification), ensuring consistency between what the builder can actually access and what the engine recommends.

---

## 7. Determinism Guarantee

Given the exact same ordered sequence of insights and the same content library state, the Recommendation Engine always produces the identical sequence of recommendations.

This is guaranteed by:

- **Rule evaluation is a pure function**: same insight pattern → same recommendation (or None).
- **Priority computation is deterministic**: same severity + confidence → same priority.
- **Actionability check is deterministic**: same target → same existence check result (given the same content library state).
- **No random or time-dependent components**: ULIDs are the only non-deterministic element, and they carry no semantic meaning for recommendation values.

For testing, inject a deterministic ULID factory, a known insight sequence, and a frozen content library:

```python
engine = RecommendationEngine(
    rules=ALL_RULES,
    verifier=ActionabilityVerifier(package_loader=FrozenPackageLoader(test_packages)),
    store=InMemoryRecommendationStore(),
    ulid_factory=DeterministicUlidFactory(seed=42),
)
recommendations = engine.process(test_insights)
assert recommendations[0].title == "Try Mission: Variables 101"
assert recommendations[0].priority == PriorityLevel.HIGH
```

This determinism supports Architectural Invariant I18: *The cognitive layer must produce identical output given identical input, regardless of when or where it runs.*

---

## 8. References

| Reference | Description |
|-----------|-------------|
| DOC-0000 | North Star — guiding principles |
| DOC-0009 | Architectural Invariants — I18 determinism guarantee |
| ARCH-0030 | Cognitive Architecture — owning layer |
| ARCH-0033 | Observation Pipeline — pipeline context |
| ARCH-0043 | Insight Architecture — upstream insight generation |
| ARCH-0046 | Recommendation Protocol — delivery protocol |
| ARCH-0003 | Core Engine Specification — PackageLoader integration |
| SPEC-0005 | ASCEND Cognitive Protocol — delivery and acknowledgment |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO PROMETHEUS |
