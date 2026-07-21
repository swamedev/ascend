# SPEC-0006 — Cognitive Pipeline Contracts

**Status:** Draft  
**Version:** 1.0  
**License:** MIT

---

## 1. Purpose

This document defines the formal contracts (Protocols / interfaces) for every stage in the Cognitive Pipeline. These contracts are the source of truth for implementation — any component that implements a pipeline stage MUST conform to the corresponding Protocol defined here.

Contracts are derived from the following architecture decisions:

| Document | Relation |
|---|---|
| ARCH-0030 | Cognitive Pipeline decomposition into discrete processing stages |
| ARCH-0033 | Data entity hierarchy and identity model |
| ARCH-0040 | Store abstraction for each pipeline stage |
| ARCH-0043 | Orchestration contract for linear multi-stage processing |
| ARCH-0044 | Lineage tracing from outputs back to source events |
| ARCH-0045 | ProcessingResult envelope for batched pipeline output |
| ARCH-0046 | Window semantics for composite signal extraction |
| ARCH-0047 | Confidence scoring across all derived entities |

The contracts follow the **no-surprise principle**: the shape of every input, output, and side-effect is declared upfront. Implementations may differ in strategy but must never differ in signature.

---

## 2. Pipeline Stage Contracts

Each stage in the Cognitive Pipeline is defined as a Python-style `Protocol`. All stages are stateless — state is managed by the stores (see Section 4).

```python
from typing import Protocol
from datetime import datetime


class ObservationCollector(Protocol):
    """Stage 1: Convert a raw DomainEvent into an internal Observation."""

    def collect(self, event: DomainEvent) -> Observation: ...


class ObservationNormalizer(Protocol):
    """Stage 2: Normalize an Observation into a canonical form."""

    def normalize(self, observation: Observation) -> NormalizedObservation: ...


class SignalExtractor(Protocol):
    """Stage 3: Extract quantitative Signals from normalized observations."""

    def extract(self, normalized: NormalizedObservation) -> list[Signal]: ...

    def extract_composite(
        self, signals: list[Signal], window: Window
    ) -> list[Signal]: ...


class PatternDetector(Protocol):
    """Stage 4: Detect Patterns from collections of Signals."""

    def detect(self, signals: list[Signal]) -> list[Pattern]: ...


class InsightEngine(Protocol):
    """Stage 5: Generate Insights from detected Patterns."""

    def generate(self, patterns: list[Pattern]) -> list[Insight]: ...


class RecommendationEngine(Protocol):
    """Stage 6: Produce Recommendations from Insights."""

    def recommend(self, insights: list[Insight]) -> list[Recommendation]: ...
```

### 2.1 Stage Invariants

| # | Invariant | Applies To |
|---|---|---|
| 1 | Input MUST NOT be mutated | All stages |
| 2 | Output MUST be a new object graph | All stages |
| 3 | Stage MUST be idempotent (same input → same output) | All stages |
| 4 | `extract_composite` window MUST be a closed interval `[start, end]` | SignalExtractor |
| 5 | Confidence MUST be in `[0.0, 1.0]` | PatternDetector, InsightEngine, RecommendationEngine |
| 6 | Empty input MUST produce empty output (never `None`) | All stages |

---

## 3. Data Contracts

Every entity flowing through the pipeline has a fixed schema. Fields marked `|None` are optional.

### 3.1 Observation

```python
@dataclass
class Observation:
    id: str                     # ULID
    event_type: EventType
    entity_id: str
    occurred_at: datetime
    data: dict
    raw: dict                   # original event payload, preserved for audit
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | str (ULID) | yes | Globally unique observation identifier |
| `event_type` | EventType | yes | The domain event type that produced this observation |
| `entity_id` | str | yes | The domain entity this observation refers to |
| `occurred_at` | datetime | yes | When the original event occurred (UTC) |
| `data` | dict | yes | Structured observation payload |
| `raw` | dict | yes | Original event payload, preserved for audit and replay |

### 3.2 NormalizedObservation

```python
@dataclass
class NormalizedObservation:
    id: str                     # ULID
    original_id: str            # Observation.id
    event_type: str
    entity_id: str
    occurred_at: datetime
    normalized_at: datetime
    fields: dict
    sensitive_filtered: bool
    correlation_id: str | None
    causation_id: str | None
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | str (ULID) | yes | Unique identifier for this normalized version |
| `original_id` | str | yes | Back-reference to the source Observation |
| `event_type` | str | yes | Denormalized event type string |
| `entity_id` | str | yes | Denormalized entity identifier |
| `occurred_at` | datetime | yes | Original event timestamp (copied from Observation) |
| `normalized_at` | datetime | yes | When normalization was applied |
| `fields` | dict | yes | Canonical key-value representation after normalization |
| `sensitive_filtered` | bool | yes | Whether sensitive fields were stripped |
| `correlation_id` | str | None | Links related observations across entities |
| `causation_id` | str | None | Identifies the observation that caused this one |

### 3.3 Signal

```python
@dataclass
class Signal:
    id: str                     # ULID
    signal_type: SignalType
    value: float
    confidence: float           # 0.0 to 1.0
    source_observation_ids: list[str]
    timestamp: datetime
    metadata: dict
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | str (ULID) | yes | Unique signal identifier |
| `signal_type` | SignalType | yes | Typed classification of the signal |
| `value` | float | yes | Quantitative value extracted from observations |
| `confidence` | float | yes | Confidence in the signal's accuracy `[0.0, 1.0]` |
| `source_observation_ids` | list[str] | yes | One or more observation IDs that produced this signal |
| `timestamp` | datetime | yes | When the signal was computed (UTC) |
| `metadata` | dict | yes | Extensible metadata (algorithm version, parameters, etc.) |

### 3.4 Pattern

```python
@dataclass
class Pattern:
    id: str                     # ULID
    pattern_type: PatternType
    label: str
    value: float
    confidence: float           # 0.0 to 1.0
    source_signal_ids: list[str]
    observed_at: datetime
    metadata: dict
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | str (ULID) | yes | Unique pattern identifier |
| `pattern_type` | PatternType | yes | Typed classification of the pattern |
| `label` | str | yes | Human-readable pattern name |
| `value` | float | yes | Computed magnitude or score of the pattern |
| `confidence` | float | yes | Confidence in the pattern detection `[0.0, 1.0]` |
| `source_signal_ids` | list[str] | yes | Signal IDs that constitute this pattern |
| `observed_at` | datetime | yes | When the pattern was detected (UTC) |
| `metadata` | dict | yes | Extensible metadata (detection algorithm, thresholds, etc.) |

### 3.5 Insight

```python
@dataclass
class Insight:
    id: str                     # ULID
    insight_type: InsightType
    title: str
    description: str
    severity: str
    confidence: float           # 0.0 to 1.0
    source_pattern_ids: list[str]
    generated_at: datetime
    metadata: dict
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | str (ULID) | yes | Unique insight identifier |
| `insight_type` | InsightType | yes | Typed classification of the insight |
| `title` | str | yes | Short human-readable title |
| `description` | str | yes | Detailed explanation of the insight |
| `severity` | str | yes | One of `info`, `warning`, `critical` |
| `confidence` | float | yes | Confidence in the insight's validity `[0.0, 1.0]` |
| `source_pattern_ids` | list[str] | yes | Pattern IDs that informed this insight |
| `generated_at` | datetime | yes | When the insight was generated (UTC) |
| `metadata` | dict | yes | Extensible metadata (generator, model version, etc.) |

### 3.6 Recommendation

```python
@dataclass
class Recommendation:
    id: str                     # ULID
    recommendation_type: RecommendationType
    title: str
    description: str
    priority: str               # low, medium, high, critical
    source_insight_ids: list[str]
    target: dict | None
    generated_at: datetime
    metadata: dict
```

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | str (ULID) | yes | Unique recommendation identifier |
| `recommendation_type` | RecommendationType | yes | Typed classification of the recommendation |
| `title` | str | yes | Short human-readable title |
| `description` | str | yes | Detailed explanation and rationale |
| `priority` | str | yes | One of `low`, `medium`, `high`, `critical` |
| `source_insight_ids` | list[str] | yes | Insight IDs that motivated this recommendation |
| `target` | dict | None | Optional target descriptor (entity, action, parameters) |
| `generated_at` | datetime | yes | When the recommendation was generated (UTC) |
| `metadata` | dict | yes | Extensible metadata (generator, model version, etc.) |

### 3.7 Enum Types

Each entity references a typed enum. The enum values are defined per-domain and registered in the package schema (see SPEC-0001). Typical members include:

| Enum | Example Values |
|---|---|
| `EventType` | `mission_started`, `evidence_submitted`, `competency_unlocked` |
| `SignalType` | `score_delta`, `frequency`, `latency`, `completion_rate` |
| `PatternType` | `streak`, `stagnation`, `acceleration`, `anomaly` |
| `InsightType` | `momentum`, `gap`, `achievement`, `milestone`, `trend` |
| `RecommendationType` | `next_mission`, `review_evidence`, `retry`, `focus_area` |

---

## 4. Store Contracts

Each pipeline stage persists its output to a dedicated store. Stores are write-heavy (append-mostly) and optimized for time-range queries.

```python
class ObservationStore(Protocol):
    def save(self, observation: Observation) -> None: ...
    def get_by_id(self, id: str) -> Observation | None: ...
    def get_by_time_range(
        self, start: datetime, end: datetime
    ) -> list[Observation]: ...
    def get_recent(self, limit: int = 100) -> list[Observation]: ...


class NormalizedObservationStore(Protocol):
    def save(self, normalized: NormalizedObservation) -> None: ...
    def get_by_id(self, id: str) -> NormalizedObservation | None: ...
    def get_by_original_id(
        self, original_id: str
    ) -> NormalizedObservation | None: ...
    def get_by_time_range(
        self, start: datetime, end: datetime
    ) -> list[NormalizedObservation]: ...
    def get_recent(self, limit: int = 100) -> list[NormalizedObservation]: ...
    def count(self) -> int: ...


class SignalStore(Protocol):
    def save(self, signal: Signal) -> None: ...
    def save_many(self, signals: list[Signal]) -> None: ...
    def get_by_id(self, id: str) -> Signal | None: ...
    def get_by_type(self, type: SignalType) -> list[Signal]: ...
    def get_by_observation(
        self, obs_id: str
    ) -> list[Signal]: ...
    def get_by_time_range(
        self, start: datetime, end: datetime
    ) -> list[Signal]: ...
    def get_recent(
        self, limit: int = 100, offset: int = 0
    ) -> list[Signal]: ...
    def count(self) -> int: ...


class PatternStore(Protocol):
    def save(self, pattern: Pattern) -> None: ...
    def save_many(self, patterns: list[Pattern]) -> None: ...
    def get_by_id(self, id: str) -> Pattern | None: ...
    def get_by_type(self, type: PatternType) -> list[Pattern]: ...
    def get_by_time_range(
        self, start: datetime, end: datetime
    ) -> list[Pattern]: ...
    def get_recent(
        self, limit: int = 100, offset: int = 0
    ) -> list[Pattern]: ...
    def count(self) -> int: ...


class InsightStore(Protocol):
    def save(self, insight: Insight) -> None: ...
    def save_many(self, insights: list[Insight]) -> None: ...
    def get_by_id(self, id: str) -> Insight | None: ...
    def get_by_type(self, type: InsightType) -> list[Insight]: ...
    def get_by_severity(self, severity: str) -> list[Insight]: ...
    def get_by_time_range(
        self, start: datetime, end: datetime
    ) -> list[Insight]: ...
    def get_recent(
        self, limit: int = 100, offset: int = 0
    ) -> list[Insight]: ...
    def count(self) -> int: ...


class RecommendationStore(Protocol):
    def save(self, recommendation: Recommendation) -> None: ...
    def save_many(
        self, recommendations: list[Recommendation]
    ) -> None: ...
    def get_by_id(self, id: str) -> Recommendation | None: ...
    def get_by_type(
        self, type: RecommendationType
    ) -> list[Recommendation]: ...
    def get_by_priority(self, priority: str) -> list[Recommendation]: ...
    def get_by_time_range(
        self, start: datetime, end: datetime
    ) -> list[Recommendation]: ...
    def get_recent(
        self, limit: int = 100, offset: int = 0
    ) -> list[Recommendation]: ...
    def count(self) -> int: ...
```

### 4.1 Store Invariants

| # | Invariant |
|---|---|
| 1 | `save` MUST be idempotent — calling twice with the same ID overwrites silently |
| 2 | `get_by_id` MUST return `None` (not raise) for missing keys |
| 3 | `get_by_time_range` MUST return results in chronological order (ascending) |
| 4 | `get_recent` MUST return results in reverse chronological order (descending) |
| 5 | `count` MUST reflect committed records only (uncommitted transactions excluded) |

---

## 5. Orchestration Contract

The pipeline orchestrator coordinates the six stages sequentially.

```python
class CognitivePipeline(Protocol):
    def process_event(
        self, event: DomainEvent
    ) -> ProcessingResult: ...

    def process_batch(
        self, events: list[DomainEvent]
    ) -> list[ProcessingResult]: ...

    def get_lineage(
        self, output_id: str
    ) -> Lineage: ...
```

### 5.1 Orchestration Rules

1. Stages execute in order: Collect → Normalize → Extract → Detect → Generate → Recommend.
2. Each stage receives the output of the previous stage.
3. If any stage returns an empty list, subsequent stages that depend on that output receive an empty list (they do not short-circuit).
4. `process_batch` MUST process events independently — a failure in one event MUST NOT affect others.
5. `get_lineage` MUST resolve any output ID (Signal, Pattern, Insight, Recommendation) back to its source chain.

---

## 6. ProcessingResult

`ProcessingResult` is the envelope returned by `process_event` and `process_batch`. It captures every artifact produced for a single event.

```python
@dataclass
class ProcessingResult:
    event_id: str                    # DomainEvent.id
    success: bool
    error: str | None
    observation: Observation | None
    normalized: NormalizedObservation | None
    signals: list[Signal]
    patterns: list[Pattern]
    insights: list[Insight]
    recommendations: list[Recommendation]
    processing_time_ms: float
    processed_at: datetime
```

| Field | Type | Description |
|---|---|---|
| `event_id` | str | The source domain event identifier |
| `success` | bool | Whether the pipeline completed without error |
| `error` | str | None | Error message if `success` is `False` |
| `observation` | Observation | None | Stage 1 output (or `None` on failure) |
| `normalized` | NormalizedObservation | None | Stage 2 output (or `None` on failure) |
| `signals` | list[Signal] | Stage 3 outputs (empty list if none detected) |
| `patterns` | list[Pattern] | Stage 4 outputs (empty list if none detected) |
| `insights` | list[Insight] | Stage 5 outputs (empty list if none generated) |
| `recommendations` | list[Recommendation] | Stage 6 outputs (empty list if none generated) |
| `processing_time_ms` | float | Total wall-clock time for the pipeline run |
| `processed_at` | datetime | When processing completed (UTC) |

---

## 7. Lineage

`Lineage` provides a full trace from any output entity back to the source events that produced it.

```python
@dataclass
class Lineage:
    target_id: str                   # the entity being traced
    target_type: str                 # 'signal' | 'pattern' | 'insight' | 'recommendation'
    source_events: list[str]         # DomainEvent IDs
    source_observations: list[str]   # Observation IDs
    source_signals: list[str]        # Signal IDs (if applicable)
    source_patterns: list[str]       # Pattern IDs (if applicable)
    source_insights: list[str]       # Insight IDs (if applicable)
    depth: int                       # number of hops from source to target
    resolved_at: datetime
```

| Field | Type | Description |
|---|---|---|
| `target_id` | str | The entity being traced |
| `target_type` | str | One of `signal`, `pattern`, `insight`, `recommendation` |
| `source_events` | list[str] | Original domain event IDs |
| `source_observations` | list[str] | Observation IDs in the chain |
| `source_signals` | list[str] | Signal IDs in the chain (empty for signal targets) |
| `source_patterns` | list[str] | Pattern IDs in the chain (empty for signal/pattern targets) |
| `source_insights` | list[str] | Insight IDs in the chain (empty for non-recommendation targets) |
| `depth` | int | Number of hops from source event to target |
| `resolved_at` | datetime | When the lineage was resolved |

### 7.1 Lineage Resolution Rules

1. For a **Signal**, depth is always 1 (Observation → Signal).
2. For a **Pattern**, depth is 2 (Observation → Signal → Pattern).
3. For an **Insight**, depth is 3 (Observation → Signal → Pattern → Insight).
4. For a **Recommendation**, depth is 4 (Observation → Signal → Pattern → Insight → Recommendation).
5. If a store lookup fails for any ID in the chain, the corresponding field contains the unresolved ID and lineage is marked as `partial`.

---

## 8. References

| Document | Relation |
|---|---|
| ARCH-0030 | Cognitive Pipeline decomposition into six discrete stages |
| ARCH-0033 | Data entity hierarchy and identity model (ULID, entity_id) |
| ARCH-0040 | Store abstraction for each pipeline stage |
| ARCH-0043 | Orchestration contract for linear multi-stage processing |
| ARCH-0044 | Lineage tracing from outputs back to source events |
| ARCH-0045 | ProcessingResult envelope for batched pipeline output |
| ARCH-0046 | Window semantics for composite signal extraction |
| ARCH-0047 | Confidence scoring across all derived entities |
| SPEC-0005 | ACP v1 — Cognitive Protocol (complementary: protocol vs. pipeline contracts) |
