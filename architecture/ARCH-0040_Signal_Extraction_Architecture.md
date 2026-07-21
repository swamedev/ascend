# ARCH-0040 — Signal Extraction Architecture

| Field | Value |
|-------|-------|
| **ID** | ARCH-0040 |
| **Name** | Signal Extraction Architecture |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0030 Cognitive Architecture, ARCH-0031 Observation Model (Sections 4–13), ARCH-0033 Observation Pipeline, ARCH-0039 Observation Normalization |
| **Principle** | Every signal must be a deterministic, measurable, and traceable extraction from one or more normalized observations |

---

## 1. Purpose

Observations recorded what happened. Signals quantify what happened. While an observation says *"the builder completed mission variables-101 with score 85"*, a signal says *"the builder gained 150 XP, achieved a completion rate of 0.85, and spent 1800 seconds on task."*

Signal Extraction is the first analytical stage of the Cognitive Pipeline. It transforms structured, normalized observations into quantitative, measurable data points that downstream stages — Pattern Detection, Metric Computation, Insight Generation — can operate on. Without signals, the cognitive layer has rich descriptions of events but no raw material for analysis.

This document defines the architecture of the Signal Extractor (F1.1). It specifies:
- The extraction engine design and component model
- Every extraction rule — which observations produce which signals, with which formulas
- The confidence computation model for deterministic (No-AI) mode
- The `Signal` schema and storage interface
- Extraction rules for all current observation types
- Composite signals derived from multiple observations
- Failure modes, error recovery, and determinism guarantees

> **Core Guarantee:** Every signal can be traced back to the exact observation(s) that produced it. No signal exists without an observed root.

---

## 2. Signal Extraction Principles

### 2.1 One Observation, Many Signals

A single normalized observation may produce multiple signals. A `mission.completed` observation yields `xp_gained`, `completion_rate`, `time_spent`, and `score_achieved`. Each signal addresses a different analytical dimension.

### 2.2 Deterministic Extraction

Signal extraction is a pure function: `(NormalizedObservation, SignalContext) → Signal[]`. Given the same observation and the same context (historical data for composite signals), the same signals are always produced. No randomness, no model inference, no external state.

### 2.3 Direct Before Composite

Extraction rules are classified into two categories:
- **Direct signals** extracted from a single observation (e.g., `xp_gained` from `mission.completed`). These have confidence 1.0.
- **Composite signals** computed across multiple observations (e.g., `completion_rate` computed as a rolling average). These have confidence < 1.0 based on data point count.

Direct signals are extracted first. Composite signals are computed from the accumulated direct signals.

### 2.4 Zero AI

Every extraction rule is a deterministic formula, lookup table, or conditional mapping. No ML model, no LLM, no statistical inference beyond basic arithmetic. The Signal Extractor operates identically with zero AI dependencies.

### 2.5 Immutable Extraction

Once extracted, a signal is immutable. If new observations arrive that would change a composite signal's value (e.g., a new mission completion shifts the rolling average), a new signal record is created. Previous signal values are never modified — they represent what was known at that point in time.

---

## 3. Architecture Overview

### 3.1 Component Model

```
NormalizedObservation
    │
    ▼
┌─────────────────────────────────────────┐
│  Signal Extractor                        │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  Direct Extractor               │    │  Maps observation type → direct signal rules
│  │  - type dispatch                │    │
│  │  - field extraction             │    │
│  │  - confidence = 1.0            │    │
│  └──────────┬──────────────────────┘    │
│             ▼                           │
│  ┌─────────────────────────────────┐    │
│  │  Composite Extractor             │    │  Computes derived signals across observations
│  │  - rolling windows              │    │
│  │  - moving averages              │    │
│  │  - confidence < 1.0            │    │
│  └──────────┬──────────────────────┘    │
│             ▼                           │
│  ┌─────────────────────────────────┐    │
│  │  Signal Store                   │    │  Persists signals and makes them queryable
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
    │
    ▼
Signal[]
```

### 3.2 Direct Extractor

The Direct Extractor is a dispatcher that maps `observation.type` to a set of extraction rules. Each rule is a pure function that reads specific fields from the observation's `data` payload and produces zero or more `Signal` objects.

```python
class DirectExtractor:
    def __init__(self):
        self._rules: dict[str, list[ExtractionRule]] = {
            "mission.completed": [
                XpGainedRule(),
                CompletionRateRule(),
                TimeSpentRule(),
                ScoreAchievedRule(),
            ],
            "evidence.submitted": [
                EvidenceQualityRule(),
            ],
            "competency.unlocked": [
                CompetencyDepthRule(),
            ],
            # ... more observation types
        }

    def extract(self, observation: NormalizedObservation) -> list[Signal]:
        rules = self._rules.get(observation.type, [])
        signals = []
        for rule in rules:
            result = rule.extract(observation)
            if result is not None:
                signals.append(result)
        return signals
```

### 3.3 Composite Extractor

The Composite Extractor operates on accumulated direct signals. It computes derived metrics that require historical context:

```python
class CompositeExtractor:
    def __init__(self, signal_store: SignalStore):
        self._signal_store = signal_store

    def extract(
        self,
        observation: NormalizedObservation,
        signals: list[Signal],
    ) -> list[Signal]:
        composites = []
        builder_id = observation.context.get("builderId", "")
        # Rolling completion rate over last N observations
        if self._has_type(signals, "completion_rate"):
            recent = self._signal_store.list_recent(
                builder_id=builder_id,
                signal_type="completion_rate",
                limit=10,
            )
            rate = self._compute_rolling_average(recent, signals)
            composites.append(Signal(
                id=generate_ulid(),
                observationId=observation.id,
                type="rolling_completion_rate",
                value=rate,
                confidence=self._confidence_from_count(len(recent) + 1, minimum=5),
                extractedAt=now(),
            ))
        return composites
```

### 3.4 Signal Store

The Signal Store is an interface (protocol) for persisting and querying signals:

```python
class SignalStore(Protocol):
    def save(self, signal: Signal) -> None: ...
    def save_many(self, signals: list[Signal]) -> None: ...
    def get_by_observation(self, observation_id: str) -> list[Signal]: ...
    def list_by_builder(
        self, builder_id: str, signal_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Signal]: ...
    def list_recent(
        self, builder_id: str, signal_type: str,
        limit: int = 10,
    ) -> list[Signal]: ...
```

---

## 4. Signal Schema

### 4.1 Definition

```python
@dataclass
class Signal:
    id: str                         # ULID
    observationId: str              # ULID of the source NormalizedObservation
    type: SignalType                # Enum of known signal types
    value: float | int | str | bool # The extracted value
    confidence: float               # 0.0 to 1.0
    extractedAt: str                # ISO 8601 UTC
    metadata: dict[str, Any]        # Extraction context, rule version, etc.
```

### 4.2 SignalType Enum

```python
class SignalType(str, Enum):
    # Progress signals
    XP_GAINED = "xp_gained"
    XP_TOTAL = "xp_total"
    MISSION_COUNT = "mission_count"
    COMPLETION_RATE = "completion_rate"
    TIME_SPENT = "time_spent"
    SCORE_ACHIEVED = "score_achieved"

    # Quality signals
    EVIDENCE_QUALITY = "evidence_quality"
    ERROR_RATE = "error_rate"
    STREAK_LENGTH = "streak_length"
    TOPICS_COVERED = "topics_covered"

    # Engagement signals
    SESSION_DURATION = "session_duration"
    SESSION_FREQUENCY = "session_frequency"
    TIME_OF_DAY = "time_of_day"
    DAY_OF_WEEK = "day_of_week"

    # Competency signals
    COMPETENCY_COUNT = "competency_count"
    COMPETENCY_DEPTH = "competency_depth"
    LEVEL_PROGRESSION_RATE = "level_progression_rate"

    # Composite / derived
    ROLLING_COMPLETION_RATE = "rolling_completion_rate"
    ROLLING_AVG_XP = "rolling_avg_xp"
    ROLLING_AVG_SCORE = "rolling_avg_score"
    XP_PER_MINUTE = "xp_per_minute"
    STREAK_ACTIVE = "streak_active"
```

### 4.3 Signal Metadata

| Field | Description |
|-------|-------------|
| `ruleName` | Name of the extraction rule that produced this signal |
| `ruleVersion` | Version of the extraction rule |
| `extractionDuration` | Milliseconds taken to extract |
| `computation` | Description of the computation (e.g., `"direct_field: xpEarned"`, `"formula: value / total"`) |
| `sourceObservations` | List of observation IDs used for composite signals |

---

## 5. Extraction Rules

### 5.1 Rule Interface

```python
class ExtractionRule(Protocol):
    def extract(self, observation: NormalizedObservation) -> Signal | None: ...
```

Each rule:
- Receives a fully normalized observation
- Returns a `Signal` if the rule applies, or `None` if the observation does not carry the relevant data
- Is a pure function (no side effects, no I/O, no state)

### 5.2 Direct Extraction Rules

#### 5.2.1 `mission.completed`

| Signal Type | Value Source | Confidence | Formula |
|-------------|-------------|------------|---------|
| `xp_gained` | `data.xpEarned` | 1.0 | Direct field read |
| `completion_rate` | `data.score / 100` | 1.0 | `score / 100`, clamped to [0.0, 1.0] |
| `time_spent` | `data.duration` | 1.0 | Direct field read (seconds) |
| `score_achieved` | `data.score` | 1.0 | Direct field read |

**Edge cases:**
- Missing `xpEarned`: signal not emitted (return None)
- Missing `score`: `completion_rate` defaults to `0.0`
- Missing `duration`: `time_spent` defaults to `0`
- Zero `duration`: `time_spent = 0`, valid signal

#### 5.2.2 `evidence.submitted`

| Signal Type | Value Source | Confidence | Formula |
|-------------|-------------|------------|---------|
| `evidence_quality` | `data.content.length` | 0.7 | Normalized to 0.0–1.0: `min(1.0, length / 1000)` |
| `topics_covered` | `data.competencies.length` | 1.0 | Direct field read |

**Note:** `evidence_quality` has confidence 0.7 because content length is a proxy, not a direct quality measure. Future versions may incorporate rubric-based scoring for higher confidence.

#### 5.2.3 `competency.unlocked`

| Signal Type | Value Source | Confidence | Formula |
|-------------|-------------|------------|---------|
| `competency_depth` | `data.level` | 1.0 | Direct field read |
| `competency_count` | Computed from store | 0.9 | `store.count_by_builder(builder_id)` |

**Note:** `competency_count` is a composite that queries existing signals. It has confidence 0.9 because it depends on store availability and completeness.

#### 5.2.4 `assessment.completed`

| Signal Type | Value Source | Confidence | Formula |
|-------------|-------------|------------|---------|
| `score_achieved` | `data.score` | 1.0 | Direct field read (0.0–1.0) |

#### 5.2.5 `builder.created`

| Signal Type | Value Source | Confidence | Formula |
|-------------|-------------|------------|---------|
| (none) | | | Builder creation is a foundational event with no measurable signal |

#### 5.2.6 `achievement.earned`

| Signal Type | Value Source | Confidence | Formula |
|-------------|-------------|------------|---------|
| (none) | | | Achievement events are qualitative; their impact is reflected in composite signals |

### 5.3 Composite Extraction Rules

Composite signals require historical context. They are computed by the `CompositeExtractor` after direct signals are extracted and stored.

#### 5.3.1 Rolling Completion Rate

```
signal_type = rolling_completion_rate
value = average of last N completion_rate signals
confidence = min(1.0, actual_count / N)
N = 10 (configurable window)
```

**Example:** If only 3 completion events exist in the window, confidence = `min(1.0, 3/10) = 0.3`.

#### 5.3.2 Rolling Average XP

```
signal_type = rolling_avg_xp
value = average of last N xp_gained signals
confidence = min(1.0, actual_count / N)
N = 10
```

#### 5.3.3 Rolling Average Score

```
signal_type = rolling_avg_score
value = average of last N score_achieved signals (from mission.completed)
confidence = min(1.0, actual_count / N)
N = 10
```

#### 5.3.4 XP Per Minute

```
signal_type = xp_per_minute
value = total_xp_in_session / session_duration_minutes
confidence = min(1.0, session_duration_minutes / 5.0)
```

Only computed when `time_spent` signals exist for the current session. Sessions shorter than 5 minutes have proportionally lower confidence.

#### 5.3.5 Streak Active

```
signal_type = streak_active
value = 1 if last session was within 24 hours of now, else 0
confidence = 1.0 if `session_duration` exists for today, else 0.8
```

#### 5.3.6 Streak Length

```
signal_type = streak_length
value = consecutive days with at least one mission.completed or evidence.submitted
confidence = min(1.0, streak_length / 7)
```

Streaks shorter than 7 days have proportionally lower confidence.

---

## 6. Confidence Model

In No-AI mode, confidence is computed using simple statistical measures:

| Category | Formula | Examples |
|----------|---------|----------|
| Direct extraction | `1.0` | `xp_gained`, `time_spent`, `score_achieved` |
| Computed from single observation | `0.7`–`0.9` | `evidence_quality` (0.7), `competency_count` (0.9) |
| Rolling window with sufficient data | `min(1.0, count / N)` | `rolling_completion_rate` with N=10 |
| Rolling window with insufficient data | `< 1.0` | `rolling_avg_xp` with only 2 data points → 0.2 |
| Heuristic with known bias | `0.6`–`0.8` | `xp_per_minute` based on short sessions |

### 6.1 Confidence Decay

Signals older than 90 days have their confidence multiplied by a decay factor:

```
decayed_confidence = original_confidence × max(0.5, 1.0 - days_since_extraction / 180)
```

This ensures that very old signals contribute less to pattern detection without being entirely discounted.

---

## 7. Extraction Pipeline

```
NormalizedObservation arrives
    │
    ▼
DirectExtractor.extract(observation)
    │
    ├── dispatches by observation.type
    ├── applies each matching ExtractionRule
    ├── collects Signal[] (confidence mostly 1.0)
    │
    ▼
SignalStore.save_many(signals)
    │
    ▼
CompositeExtractor.extract(observation, signals)
    │
    ├── queries SignalStore for historical context
    ├── computes composite signals
    ├── assigns confidence based on data count
    │
    ▼
SignalStore.save_many(composite_signals)
    │
    ▼
Signals ready for Pattern Detector (F1.2)
```

Both direct and composite extraction happen synchronously within the same pipeline stage. The observation is not passed to the next stage until all signals are extracted and persisted.

---

## 8. Signal Storage

Signals are stored in the same SQLite cognitive database as observations. The schema follows ARCH-0035 conventions:

```sql
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    observation_id TEXT NOT NULL,
    type TEXT NOT NULL,
    value REAL NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    extracted_at TEXT NOT NULL,
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_sig_observation ON signals(observation_id);
CREATE INDEX idx_sig_type ON signals(type);
CREATE INDEX idx_sig_extracted ON signals(extracted_at);
CREATE INDEX idx_sig_obs_type ON signals(observation_id, type);
```

### 8.1 InMemorySignalStore

For testing and lightweight deployments, an in-memory implementation:

```python
class InMemorySignalStore:
    def __init__(self):
        self._signals: list[Signal] = []

    def save(self, signal: Signal) -> None:
        self._signals.append(signal)

    def save_many(self, signals: list[Signal]) -> None:
        self._signals.extend(signals)

    def get_by_observation(self, observation_id: str) -> list[Signal]:
        return [s for s in self._signals if s.observationId == observation_id]

    def list_by_builder(self, builder_id, signal_type=None, limit=50, offset=0):
        filtered = [s for s in self._signals if s.observationId ...]  # filtered by builder
        return filtered[offset:offset + limit]

    def list_recent(self, builder_id, signal_type, limit=10):
        filtered = [s for s in self._signals if s.type == signal_type]
        return filtered[-limit:]
```

---

## 9. Failure Modes

| Failure | Behavior |
|---------|----------|
| Unknown observation type | Return empty list (no signals); log DEBUG |
| Missing field in observation | Rule returns None for that signal; log WARNING |
| Division by zero in formula | Clamp to 0 or max value; add warning to signal metadata |
| Overflow | Clamp to valid range; log WARNING |
| Signal store unavailable | Buffer signals in memory (max 500); retry on next interval |
| Composite query returns empty | Skip composite; log INFO |

No failure crashes the pipeline. Extraction degrades gracefully — missing signals simply means less data for pattern detection.

---

## 10. Determinism Guarantee

Given the exact same ordered sequence of normalized observations and the same signal store state (or a fresh store), the Signal Extractor always produces the identical sequence of signals.

This is guaranteed by:
- **Direct extraction is a pure function**: same observation → same signals.
- **Composite extraction is deterministic given the same historical signals**: same store state → same composites.
- **Fixed confidence formulas**: same input values → same confidence scores.
- **No random or time-dependent components**: ULIDs are the only non-deterministic element, and they carry no semantic meaning for signal values.

For testing, inject a deterministic ULID factory and a known signal store state:

```python
extractor = SignalExtractor(
    direct=DirectExtractor(rules=ALL_RULES),
    composite=CompositeExtractor(store=InMemorySignalStore()),
    ulid_factory=DeterministicUlidFactory(seed=42),
)
signals = extractor.extract(observation)
assert signals[0].value == 150  # deterministic
```

---

## 11. References

| Reference | Description |
|-----------|-------------|
| ARCH-0030 | Cognitive Architecture — owning layer |
| ARCH-0031 | Observation Model — Signal definition (Section 4) |
| ARCH-0033 | Observation Pipeline — pipeline context |
| ARCH-0039 | Observation Normalization — upstream normalizer |
| ARCH-0034 | Behavioral Metrics — downstream metric computation |
| ARCH-0035 | Observation Storage — SQLite schema for signals |
| DOC-0009 | Architectural Invariants — I15, I16 |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO PROMETHEUS |
