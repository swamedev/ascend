# ARCH-0045 — Pattern Detection Architecture

| Field | Value |
|-------|-------|
| **ID** | ARCH-0045 |
| **Name** | Pattern Detection Architecture |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000, DOC-0009, ARCH-0030, ARCH-0033, ARCH-0043, ARCH-0044 |
| **Principle** | Every pattern is a deterministic relationship detected across one or more signals |

---

## 1. Purpose

Signals quantify what happened. Patterns identify what those measurements *mean*. While a signal says *"the builder gained 150 XP"*, a pattern says *"XP growth is accelerating"* or *"completion rate dropped below threshold."*

Pattern Detection (F1.2) is the second analytical stage of the Cognitive Pipeline. It consumes signals from F1.1 and produces patterns — the first analytical abstraction that carries semantic meaning. Patterns are deterministic relationships detected across one or more signals: trends, anomalies, thresholds, consistencies, and composite relationships.

This document defines:
- The Pattern model schema
- The PatternType taxonomy with detection rules
- The Pattern Detector component architecture
- The determinism guarantee
- The failure model

> **Core Guarantee:** Every pattern can be traced back to the exact signal(s) that triggered it. No pattern exists without a measurable signal root.

---

## 2. Pattern Model

```python
@dataclass
class Pattern:
    id: str                        # ULID
    pattern_type: PatternType      # Enum of known pattern types
    label: str                     # Human-readable description
    value: float                   # The detected value (magnitude, rate, count, etc.)
    confidence: float              # 0.0 to 1.0
    source_signal_ids: list[str]   # ULIDs of the signals that triggered detection
    observed_at: str               # ISO 8601 UTC
    metadata: dict[str, Any]       # Detection context, rule version, window params
```

| Field | Description |
|-------|-------------|
| `id` | ULID — globally unique, sortable by detection time |
| `pattern_type` | One of the registered PatternType enum values |
| `label` | Human-readable description, e.g. `"xp_growth_accelerating"` |
| `value` | Numeric result of the detection rule (slope, deviation, count, etc.) |
| `confidence` | How certain the rule is about this detection (0.0–1.0) |
| `source_signal_ids` | Links back to the exact signals that produced this pattern |
| `observed_at` | Timestamp of detection (not the signal's timestamp) |
| `metadata` | Rule name, version, window size, threshold, computation details |

---

## 3. Pattern Type Taxonomy

| PatternType | Category | Description | Detection Rule |
|---|---|---|---|
| `trend_up` | Trend | Value increasing over window | slope > threshold |
| `trend_down` | Trend | Value decreasing over window | slope < -threshold |
| `spike` | Anomaly | Value exceeds 2&sigma; from mean | deviation > 2 * std |
| `threshold_crossing` | Boundary | Value crosses configurable bound | value > max or < min |
| `consistency_score` | Quality | Low variance across signals | coefficient_of_variation < threshold |
| `acceleration` | Trend | Rate of change increasing | second_derivative > 0 |
| `stagnation` | Trend | No significant change | slope near 0 over window |
| `pattern_relationship` | Composite | Two or more patterns co-occur | cross-pattern rule |
| `frequency_burst` | Temporal | Signal fires unusually often | count > threshold over window |
| `performance_gap` | Comparative | Gap between two metrics widening | difference > threshold |

```python
class PatternType(str, Enum):
    TREND_UP = "trend_up"
    TREND_DOWN = "trend_down"
    SPIKE = "spike"
    THRESHOLD_CROSSING = "threshold_crossing"
    CONSISTENCY_SCORE = "consistency_score"
    ACCELERATION = "acceleration"
    STAGNATION = "stagnation"
    PATTERN_RELATIONSHIP = "pattern_relationship"
    FREQUENCY_BURST = "frequency_burst"
    PERFORMANCE_GAP = "performance_gap"
```

---

## 4. Detection Rules

### 4.1 Rule Interface

Every PatternType has a deterministic detection rule class that implements a single method:

```python
class PatternDetectionRule(Protocol):
    def detect(self, signals: list[Signal]) -> list[Pattern]: ...
```

Rules are:
- **Stateless** — no instance state; all parameters are passed as arguments or read from config
- **Pure** — no side effects, no I/O, no randomness
- **Isolated** — one rule's execution never affects another rule's input
- **Windowed** — each rule receives the signals relevant to its pattern type (filtered by the orchestrator)

### 4.2 Rule Examples

#### `TrendUpRule` / `TrendDownRule`

```python
class TrendUpRule:
    def __init__(self, window: int = 5, threshold: float = 0.1):
        self.window = window
        self.threshold = threshold

    def detect(self, signals: list[Signal]) -> list[Pattern]:
        if len(signals) < 2:
            return []
        values = [s.value for s in signals[-self.window:]]
        slope = self._linear_regression_slope(values)
        if slope > self.threshold:
            return [Pattern(
                id=generate_ulid(),
                pattern_type=PatternType.TREND_UP,
                label=f"{signals[-1].type}_trend_up",
                value=slope,
                confidence=min(1.0, abs(slope) / (self.threshold * 2)),
                source_signal_ids=[s.id for s in signals[-self.window:]],
                observed_at=now(),
            )]
        return []
```

#### `SpikeRule`

```python
class SpikeRule:
    def __init__(self, std_multiplier: float = 2.0, min_window: int = 3):
        self.std_multiplier = std_multiplier
        self.min_window = min_window

    def detect(self, signals: list[Signal]) -> list[Pattern]:
        if len(signals) < self.min_window + 1:
            return []
        mean = statistics.mean(s.value for s in signals[:-1])
        std = statistics.stdev(s.value for s in signals[:-1]) if len(signals) > 2 else 0
        latest = signals[-1].value
        if std > 0 and abs(latest - mean) > self.std_multiplier * std:
            return [Pattern(
                id=generate_ulid(),
                pattern_type=PatternType.SPIKE,
                label=f"{signals[-1].type}_spike",
                value=(latest - mean) / std,
                confidence=min(1.0, abs(latest - mean) / (self.std_multiplier * std)),
                source_signal_ids=[signals[-1].id],
                observed_at=now(),
            )]
        return []
```

### 4.3 Confidence Model

| Detection Type | Confidence Basis | Formula |
|----------------|-----------------|---------|
| Trend (slope-based) | Slope magnitude relative to threshold | `min(1.0, abs(slope) / (threshold * 2))` |
| Spike (deviation-based) | Deviation magnitude relative to threshold | `min(1.0, deviation / (std_multiplier * std))` |
| Threshold crossing | Distance from boundary | `min(1.0, abs(value - boundary) / boundary)` |
| Consistency | CV proximity to zero | `max(0.0, 1.0 - cv / threshold)` |
| Acceleration | Second derivative magnitude | `min(1.0, abs(d2) / acceleration_threshold)` |
| Stagnation | Slope proximity to zero | `max(0.0, 1.0 - abs(slope) / stagnation_threshold)` |
| Cross-pattern | Overlap ratio | `overlap_count / total_patterns` |
| Frequency burst | Excess over expected | `min(1.0, (count - expected) / expected)` |
| Performance gap | Gap ratio | `min(1.0, gap / threshold)` |

---

## 5. Pattern Detector Architecture

### 5.1 Component Model

```
Signal[]
    │
    ▼
┌─────────────────────────────────────────┐
│  PatternDetector (orchestrator)          │
│                                         │
│  ┌─────────────────────────────────┐    │
│  │  Rule Registry                   │    │  Maps PatternType → PatternDetectionRule
│  │  - type dispatch                │    │
│  │  - signal filtering by type     │    │
│  └──────────┬──────────────────────┘    │
│             ▼                           │
│  ┌─────────────────────────────────┐    │
│  │  Primitive Rules                 │    │  One per PatternType (stateless, pure)
│  │  - TrendUpRule                  │    │
│  │  - TrendDownRule               │    │
│  │  - SpikeRule                    │    │
│  │  - ThresholdCrossingRule        │    │
│  │  - ConsistencyScoreRule         │    │
│  │  - AccelerationRule             │    │
│  │  - StagnationRule               │    │
│  │  - FrequencyBurstRule           │    │
│  │  - PerformanceGapRule           │    │
│  └──────────┬──────────────────────┘    │
│             ▼                           │
│  ┌─────────────────────────────────┐    │
│  │  Composite Rules                 │    │  Cross-pattern detection
│  │  - PatternRelationshipRule     │    │
│  └──────────┬──────────────────────┘    │
│             ▼                           │
│  ┌─────────────────────────────────┐    │
│  │  PatternStore                   │    │  Persists patterns and makes them queryable
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
    │
    ▼
Pattern[]
```

### 5.2 PatternDetector (Orchestrator)

```python
class PatternDetector:
    def __init__(self, rules: list[PatternDetectionRule], store: PatternStore):
        self._rules = rules
        self._store = store

    def run(self, signals: list[Signal]) -> list[Pattern]:
        all_patterns: list[Pattern] = []
        for rule in self._rules:
            try:
                relevant = self._filter_signals(rule, signals)
                patterns = rule.detect(relevant)
                all_patterns.extend(patterns)
            except Exception as e:
                logger.warning(f"Rule {type(rule).__name__} failed: {e}")
        if all_patterns:
            self._store.save_many(all_patterns)
        return all_patterns
```

### 5.3 PatternStore

```python
class PatternStore(Protocol):
    def save(self, pattern: Pattern) -> None: ...
    def save_many(self, patterns: list[Pattern]) -> None: ...
    def list_by_builder(
        self, builder_id: str, pattern_type: str | None = None,
        limit: int = 50, offset: int = 0,
    ) -> list[Pattern]: ...
    def list_recent(
        self, builder_id: str, pattern_type: str | None = None,
        limit: int = 20,
    ) -> list[Pattern]: ...
```

### 5.4 Pattern Storage Schema

```sql
CREATE TABLE IF NOT EXISTS patterns (
    id TEXT PRIMARY KEY,
    pattern_type TEXT NOT NULL,
    label TEXT NOT NULL,
    value REAL NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    source_signal_ids TEXT NOT NULL DEFAULT '[]',
    observed_at TEXT NOT NULL,
    metadata TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_pat_type ON patterns(pattern_type);
CREATE INDEX idx_pat_observed ON patterns(observed_at);
CREATE INDEX idx_pat_label ON patterns(label);
```

---

## 6. Determinism

All detection rules are deterministic functions of their signal inputs. No randomness, no AI, no external state. Same signals → same patterns always.

This is guaranteed by:
- **Stateless rules**: no instance state persists between detections
- **Pure functions**: no I/O, no side effects, no network calls
- **Fixed window parameters**: window size and thresholds are configurable but fixed for a given rule instance
- **Deterministic arithmetic**: floating-point operations produce identical results for identical inputs

```python
detector = PatternDetector(
    rules=[
        TrendUpRule(window=5, threshold=0.1),
        TrendDownRule(window=5, threshold=0.1),
        SpikeRule(std_multiplier=2.0),
        ThresholdCrossingRule(max_value=100.0, min_value=0.0),
        ConsistencyScoreRule(cv_threshold=0.15),
        AccelerationRule(window=5),
        StagnationRule(window=5, stagnation_threshold=0.01),
        FrequencyBurstRule(window=10, count_threshold=5),
        PerformanceGapRule(threshold=20.0),
        PatternRelationshipRule(window=5),
    ],
    store=InMemoryPatternStore(),
)
patterns = detector.run(signals)
assert patterns[0].value == 0.15  # deterministic
```

This determinism supports I18 (Inspectable, Invariant, Immutable): because patterns are deterministic, any pattern can be reproduced, audited, and verified independently of when or where it was detected.

---

## 7. Failure Model

| Failure | Behavior |
|---------|----------|
| Rule raises exception | Catch, log WARNING with rule name, skip rule for this cycle |
| No signals for a rule type | Return empty list; log DEBUG |
| Zero signals in window | Return empty list; log DEBUG |
| Division by zero in rule | Clamp to valid range; log WARNING |
| PatternStore unavailable | Discard patterns for this cycle; log WARNING |
| Window too small for computation | Return empty list; log DEBUG |

Failed rules emit no patterns for that cycle. One failing rule never blocks other rules. The Detector logs which rules succeeded and which failed for each `run()` cycle.

```python
for rule in self._rules:
    try:
        patterns = rule.detect(relevant_signals)
        logger.info(f"Rule {type(rule).__name__}: {len(patterns)} patterns")
    except Exception as e:
        logger.warning(f"Rule {type(rule).__name__} failed: {e}")
```

No failure crashes the pipeline. Pattern detection degrades gracefully — missing patterns simply means less signal for downstream stages (F1.3 Metric Computation, F1.4 Insight Generation).

---

## 8. References

| Reference | Description |
|-----------|-------------|
| ARCH-0030 | Cognitive Architecture — owning layer |
| ARCH-0033 | Observation Pipeline — pipeline context |
| ARCH-0034 | Behavioral Metrics — downstream metric computation |
| ARCH-0040 | Signal Extraction — upstream signal source (F1.1) |
| ARCH-0043 | Metric Computation Architecture — downstream stage (F1.3) |
| ARCH-0044 | Insight Generation Architecture — downstream stage (F1.4) |
| DOC-0000 | North Star — first principles |
| DOC-0009 | Architectural Invariants — I18, determinism |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO PROMETHEUS |
