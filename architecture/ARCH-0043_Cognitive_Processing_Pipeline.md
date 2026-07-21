# ARCH-0043 — Cognitive Processing Pipeline

| Field | Value |
|-------|-------|
| **ID** | ARCH-0043 |
| **Name** | Cognitive Processing Pipeline |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000, DOC-0007, DOC-0009, ARCH-0030, ARCH-0033, ARCH-0039, ARCH-0040, ARCH-0041 |
| **Referenced by** | ARCH-0044, ARCH-0045, ARCH-0046, ARCH-0047, SPEC-0006 |
| **Principle** | Every cognitive output must be deterministically traceable through a strict, testable pipeline from raw observation to actionable recommendation |

---

## 1. Purpose

The Cognitive Processing Pipeline is the complete data flow from raw observations through to recommendations. It connects Observation Collection (F1.0) → Normalization (F1.05) → Signal Extraction (F1.1) → Pattern Detection (F1.2) → Insight Generation (F1.3) → Recommendation Engine (F2). Every stage is deterministic and testable.

This document defines the end-to-end pipeline that transforms raw domain events into actionable recommendations for the Builder. Each stage has a well-defined input type, output type, deterministic transformation logic, explicit failure model, and isolation boundary. No stage depends on AI — every transformation is a pure function or a composition of pure functions. The pipeline as a whole is replayable: given the same ordered sequence of raw events, it produces the same ordered sequence of recommendations, every time, regardless of environment or execution count.

The pipeline exists to enforce a strict separation of concerns across the cognitive processing chain. Collection does not extract signals. Extraction does not detect patterns. Pattern detection does not generate insights. Each stage owns its data store and communicates only by reading from the previous stage's store. This isolation guarantees that stages can be tested independently, replaced without side effects, and scaled independently of one another.

> **Core Guarantee:** Every recommendation can be traced back through every intermediate output — insight, pattern, signal, observation — to the exact raw events that produced it. The full chain is deterministic, testable, and replayable.

---

## 2. Pipeline Overview

The Cognitive Processing Pipeline consists of six sequential stages. Every raw observation that enters the pipeline passes through every stage. No stage is optional, no stage is skipped for performance, and no stage may be bypassed. If a stage fails to produce output for a given input, downstream stages simply receive no data for that input — the pipeline never stalls, deadlocks, or loses events silently.

### ASCII Flow

```
Raw Event
    │
    ▼
┌──────────────┐
│ F1.0         │  Collector — subscribe, wrap, persist
│ Observation  │
│ Collection   │
└──────┬───────┘
       │ Observation
       ▼
┌──────────────┐
│ F1.05        │  Normalizer — ULID, timestamp, fields, filtering
│ Observation  │
│ Normalization│
└──────┬───────┘
       │ NormalizedObservation
       ▼
┌──────────────┐
│ F1.1         │  Extractor — rules compute signals
│ Signal       │
│ Extraction   │
└──────┬───────┘
       │ Signal
       ▼
┌──────────────┐
│ F1.2         │  Detector — patterns from signals
│ Pattern      │
│ Detection    │
└──────┬───────┘
       │ Pattern
       ▼
┌──────────────┐
│ F1.3         │  Engine — insights from patterns
│ Insight      │
│ Generation   │
└──────┬───────┘
       │ Insight
       ▼
┌──────────────┐
│ F2           │  Engine — recommendations from insights
│              │
│ Recommend.   │
└──────────────┘
      Action
```

### Mermaid Diagram

```mermaid
flowchart LR
    subgraph F1_0["F1.0 Observation Collection"]
        C[Collector]
    end
    subgraph F1_05["F1.05 Observation Normalization"]
        N[Normalizer]
    end
    subgraph F1_1["F1.1 Signal Extraction"]
        E[Extractor]
    end
    subgraph F1_2["F1.2 Pattern Detection"]
        D[Detector]
    end
    subgraph F1_3["F1.3 Insight Generation"]
        G[Generator]
    end
    subgraph F2["F2 Recommendation"]
        R[Engine]
    end

    A[Raw Event] --> C
    C -->|Observation| N
    N -->|NormalizedObservation| E
    E -->|Signal[]| D
    D -->|Pattern[]| G
    G -->|Insight[]| R
    R -->|Recommendation[]| Z[Action]
```

### Data Accumulation

Each stage produces output that references the input that produced it. The data lineage chains as follows:

```
Observation → NormalizedObservation → Signal[] → Pattern[] → Insight[] → Recommendation[]
```

Every arrow represents a deterministic transformation. Every output object carries the IDs of its source objects, forming an unbroken provenance chain.

---

## 3. Determinism Guarantee

Every pipeline stage is a pure function of its input. Given the same input sequence, every stage produces identical output regardless of environment, time, or execution count. No randomness, no AI, no external state. This is Invariant I18.

### 3.1 What Determinism Means

For each stage, determinism means:
- **F1.0 (Collector):** Given the same sequence of domain events arriving from the same sources at the same times, the Collector produces the same sequence of Observation objects. Order is preserved within each source.
- **F1.05 (Normalizer):** Given the same Observation object, the Normalizer produces the same NormalizedObservation. ULID generation is deterministic when a seed or timestamp override is injected for testing.
- **F1.1 (Extractor):** Given the same NormalizedObservation and the same historical signal state, the Extractor produces the same Signal array. All extraction rules are pure functions.
- **F1.2 (Detector):** Given the same Signal array and the same historical pattern state, the Detector produces the same Pattern array. All detection rules are pure functions.
- **F1.3 (Generator):** Given the same Pattern array and the same historical insight state, the Generator produces the same Insight array. All generation rules are pure functions.
- **F2 (Recommender):** Given the same Insight array and the same historical recommendation state, the Recommender produces the same Recommendation array. All recommendation rules are pure functions.

### 3.2 Testability

Because every stage is deterministic, any sequence of raw events can be recorded and replayed to produce an identical output. This property is the foundation of the testing strategy:

```python
# Recorded sequence of raw events
events = load_fixture("builder_completes_first_mission.json")

# Replay through the entire pipeline
result = pipeline.run(events)

# Assertions on every stage output
assert result.observations == expected_observations
assert result.signals == expected_signals
assert result.patterns == expected_patterns
assert result.insights == expected_insights
assert result.recommendations == expected_recommendations
```

### 3.3 Non-Determinism Boundaries

The only sources of non-determinism in the pipeline are:
- **System clock** — used for ULID generation and timestamps. In test mode, the clock is injected and frozen.
- **Historical state** — the accumulated state of each stage's store. In test mode, the store is seeded with a known state or reset to empty.
- **External event arrival order** — in production, events arrive in real time. In test mode, events are provided in a fixed order.

All non-determinism is bounded to these three sources, each of which is controllable in test environments.

---

## 4. Stage Contracts

| Stage | Input Type | Output Type | Determinism | Test Strategy |
|-------|-----------|-------------|-------------|---------------|
| F1.0 | DomainEvent | Observation | Deterministic | Unit test per event type |
| F1.05 | Observation | NormalizedObservation | Deterministic | Property-based |
| F1.1 | NormalizedObservation | Signal[] | Deterministic | Rule-level tests |
| F1.2 | Signal[] | Pattern[] | Deterministic | Rule-level tests |
| F1.3 | Pattern[] | Insight[] | Deterministic | Rule-level tests |
| F2 | Insight[] | Recommendation[] | Deterministic | Integration tests |

### 4.1 F1.0 — Observation Collection

**Input:** `DomainEvent` — a raw event published by the Runtime, Experience, or Cognitive Layer on the event bus.

**Output:** `Observation` — a wrapped event with source metadata, receipt timestamp, and collector tag.

**Determinism:** Preserves event ordering within each source. For testing, recorded event sequences are replayed in fixed order.

**Test strategy:** One unit test per known event type (mission.completed, evidence.submitted, etc.) verifying that the Collector wraps the event correctly and assigns the correct source tag. Edge cases: unknown event types, malformed payloads, empty payloads.

### 4.2 F1.05 — Observation Normalization

**Input:** `Observation` — a raw wrapped event with source-native fields.

**Output:** `NormalizedObservation` — a canonical observation with ULID, standardized timestamp, mapped fields, and stripped sensitive data.

**Determinism:** Pure function — same Observation always produces the same NormalizedObservation. ULID generation is deterministic with injected clock.

**Test strategy:** Property-based tests that verify:
- Field mapping is bijective (canonical fields always map to source fields)
- Timestamp conversion is idempotent (normalizing twice produces the same result)
- Sensitive field stripping never removes non-sensitive data
- Unknown source fields are preserved under `data.raw`

### 4.3 F1.1 — Signal Extraction

**Input:** `NormalizedObservation` — a fully normalized, validated observation.

**Output:** `Signal[]` — zero or more quantitative signals extracted from the observation.

**Determinism:** Pure function — same NormalizedObservation always produces the same Signal array. Composite signals depend on historical signal state, which is deterministic when seeded.

**Test strategy:** One test per extraction rule (XP from mission.completed, quality from evidence.submitted, etc.). Property-based tests verify that every signal carries valid confidence in [0.0, 1.0] and traces to its source observation ID.

### 4.4 F1.2 — Pattern Detection

**Input:** `Signal[]` — one or more signals from the Extractor.

**Output:** `Pattern[]` — zero or more detected patterns. A pattern is a recognized structure in signal data, such as a streak, a trend, a gap, or a threshold crossing.

**Determinism:** Pure function — same Signal array always produces the same Pattern array. Composite patterns depend on historical signal state.

**Test strategy:** One test per detection rule (streak detection, trend detection, gap detection, threshold crossing). Property-based tests verify that every pattern references valid signal IDs and carries non-negative confidence.

### 4.5 F1.3 — Insight Generation

**Input:** `Pattern[]` — one or more detected patterns.

**Output:** `Insight[]` — zero or more generated insights. An insight is a human-interpretable statement about the builder's state, progress, or behavior, derived from one or more patterns.

**Determinism:** Pure function — same Pattern array always produces the same Insight array. Insights are generated from templates keyed by pattern type.

**Test strategy:** One test per insight template (streak insight, stagnation insight, velocity insight). Property-based tests verify that every insight carries a valid severity level and references its source pattern IDs.

### 4.6 F2 — Recommendation Engine

**Input:** `Insight[]` — one or more generated insights.

**Output:** `Recommendation[]` — zero or more actionable recommendations for the builder. A recommendation is a suggested action (e.g., "try the next mission", "review topic X", "take a break").

**Determinism:** Pure function — same Insight array always produces the same Recommendation array. Recommendations are selected from a deterministic rule table keyed by insight type and severity.

**Test strategy:** Integration tests that feed recorded insight sequences through the engine and verify the expected recommendation output. Edge cases: conflicting insights (two insights suggest opposite actions), empty insights, maximum severity.

---

## 5. Data Lineage

Every output carries a trace of its provenance. The lineage chain ensures that any output can be traced back to its root observations.

### 5.1 Lineage Chain

```
Recommendation
  └── source_insight_ids: str[]          ← Insight[]
        └── source_pattern_ids: str[]     ← Pattern[]
              └── source_signal_ids: str[] ← Signal[]
                    └── observation_id: str ← NormalizedObservation
                          └── id: str       ← Observation
```

### 5.2 Lineage in Practice

```typescript
interface Recommendation {
  id: string;
  type: RecommendationType;
  action: string;
  priority: 1 | 2 | 3;
  sourceInsightIds: string[];       // ← provenance
  createdAt: string;
}

interface Insight {
  id: string;
  type: InsightType;
  title: string;
  body: string;
  severity: 1 | 2 | 3 | 4 | 5;
  sourcePatternIds: string[];       // ← provenance
  createdAt: string;
}

interface Pattern {
  id: string;
  type: PatternType;
  label: string;
  confidence: number;
  sourceSignalIds: string[];        // ← provenance
  detectedAt: string;
}

interface Signal {
  id: string;
  observationId: string;            // ← provenance
  type: SignalType;
  value: number;
  confidence: number;
  metadata: Record<string, unknown>;
  extractedAt: string;
}
```

### 5.3 Replayability

The full chain is replayable. Given a recorded sequence of raw events, the pipeline can reproduce every intermediate and final output. This enables:

- **Regression testing:** After a code change, replay a known event sequence and compare outputs.
- **Audit trails:** For any recommendation, list every observation that contributed to it.
- **Debugging:** If a downstream stage produces unexpected output, trace back through the lineage to find the root cause.

### 5.4 Lineage Storage

Lineage metadata is stored alongside each output object in its respective store. Each store has a query interface that supports reverse traversal:

```python
# Given a recommendation, find all insights that produced it
insights = insight_store.get_by_ids(recommendation.source_insight_ids)

# Given those insights, find all patterns
patterns = pattern_store.get_by_ids(insight.source_pattern_ids for each insight)

# Given those patterns, find all signals
signals = signal_store.get_by_ids(pattern.source_signal_ids for each pattern)

# Given those signals, find all observations
observations = observation_store.get_by_ids(signal.observation_id for each signal)
```

Every traversal is O(n) where n is the number of IDs in the source array. No recursive or graph-based queries are required.

---

## 6. Failure Model

Each stage can reject inputs, emit partial results, or degrade gracefully. Stage failures never cascade destructively. A failed Pattern Detector does not delete Signals. A failed Signal Extractor does not delete Observations.

### 6.1 Failure Principles

1. **No destructive cascades.** A failure in stage N leaves stages 1 through N-1 unaffected. Data already persisted in earlier stores is never modified or deleted by a downstream failure.

2. **Partial output is valid.** If a stage can process 7 out of 10 inputs, it emits 7 outputs. The remaining 3 are logged and noted but do not block the pipeline.

3. **Stages degrade independently.** If the Signal Extractor is unavailable, the Collector and Normalizer continue to operate. If the Pattern Detector is unavailable, signals still accumulate in the Signal Store. The pipeline as a whole never stalls due to a single stage failure.

4. **Silent drops are forbidden.** If an input is rejected or dropped at any stage, the reason is always logged at WARNING or higher.

### 6.2 Per-Stage Failure Modes

| Stage | Failure Mode | Behavior | Log Level |
|-------|-------------|----------|-----------|
| F1.0 | Source unavailable | Retry connection (3x, backoff), skip source | WARNING |
| F1.0 | Malformed event | Discard event | DEBUG |
| F1.05 | Missing required field | Drop event | WARNING |
| F1.05 | Unparseable timestamp | Use receipt timestamp, flag warning | WARNING |
| F1.05 | Payload exceeds size limit | Drop event | WARNING |
| F1.1 | Unknown observation type | Return empty Signal[] | DEBUG |
| F1.1 | Missing field in observation | Rule returns None for that signal | WARNING |
| F1.1 | Division by zero | Clamp to 0 or max, flag metadata | WARNING |
| F1.2 | Unknown signal type | Return empty Pattern[] | DEBUG |
| F1.2 | Insufficient signals for rule | Rule returns None | INFO |
| F1.2 | Confidence below threshold | Emit pattern with degraded confidence | INFO |
| F1.3 | Unknown pattern type | Return empty Insight[] | DEBUG |
| F1.3 | Template not found for pattern | Skip insight, log ERROR | ERROR |
| F1.3 | Empty pattern array | Return empty Insight[] | INFO |
| F2 | Unknown insight type | Return empty Recommendation[] | DEBUG |
| F2 | Conflicting recommendations | Emit highest-priority recommendation only | INFO |
| F2 | Empty insight array | Return empty Recommendation[] | INFO |

### 6.3 Degraded Output

When a stage produces degraded output (e.g., a signal with confidence 0.3 because of insufficient data), the output carries metadata indicating the degradation reason:

```python
@dataclass
class DegradedOutput:
    reason: str
    original_input_id: str
    fallback_value: Any
```

Downstream stages may choose to ignore degraded outputs or factor them into confidence computations, depending on the rule.

---

## 7. Stage Isolation

Each stage operates on its own store. Stages communicate only through reading from the previous stage's store. No stage directly calls another stage's methods.

### 7.1 Store Ownership

| Stage | Owns Store | Reads From |
|-------|-----------|------------|
| F1.0 | Observation Store | — (receives events from bus) |
| F1.05 | NormalizedObservation Store | Observation Store |
| F1.1 | Signal Store | NormalizedObservation Store |
| F1.2 | Pattern Store | Signal Store |
| F1.3 | Insight Store | Pattern Store |
| F2 | Recommendation Store | Insight Store |

### 7.2 Communication Pattern

Stages communicate exclusively through their stores:

```python
class Pipeline:
    def __init__(self, stores: PipelineStores, stages: PipelineStages):
        self._stores = stores
        self._stages = stages

    def process_event(self, event: DomainEvent) -> None:
        # Stage 1: Collect
        observation = self._stages.collector.collect(event)
        self._stores.observation.save(observation)

        # Stage 2: Normalize (reads from observation store)
        normalized = self._stages.normalizer.normalize(
            self._stores.observation
        )
        self._stores.normalized.save(normalized)

        # Stage 3: Extract signals (reads from normalized store)
        signals = self._stages.extractor.extract(
            self._stores.normalized
        )
        self._stores.signal.save_many(signals)

        # Stage 4: Detect patterns (reads from signal store)
        patterns = self._stages.detector.detect(
            self._stores.signal
        )
        self._stores.pattern.save_many(patterns)

        # Stage 5: Generate insights (reads from pattern store)
        insights = self._stages.generator.generate(
            self._stores.pattern
        )
        self._stores.insight.save_many(insights)

        # Stage 6: Recommend (reads from insight store)
        recommendations = self._stages.recommender.recommend(
            self._stores.insight
        )
        self._stores.recommendation.save_many(recommendations)
```

### 7.3 Isolation Benefits

- **Independent testing:** Each stage can be tested in isolation by seeding its input store and asserting on its output store.
- **Independent replacement:** Any stage can be replaced with a different implementation as long as the store contract is preserved.
- **Independent scaling:** Stages can run on separate threads, processes, or machines if store access is over a network protocol.
- **Independent failure:** A stage crash does not corrupt another stage's data because each stage owns its store exclusively.

### 7.4 Store Contracts

Each store implements a read protocol that the downstream stage uses:

```python
class ObservationStore(Protocol):
    def save(self, observation: Observation) -> None: ...
    def get_unprocessed(self, limit: int = 100) -> list[Observation]: ...
    def mark_processed(self, observation_id: str) -> None: ...

class NormalizedObservationStore(Protocol):
    def save(self, normalized: NormalizedObservation) -> None: ...
    def get_unprocessed(self, limit: int = 100) -> list[NormalizedObservation]: ...
    def mark_processed(self, normalized_id: str) -> None: ...

# ... similar for SignalStore, PatternStore, InsightStore, RecommendationStore
```

The `get_unprocessed` / `mark_processed` pattern is the only mechanism for communicating progress between stages. No stage knows the internal implementation of any other stage.

---

## 8. Pipeline Configuration

All pipeline stages share a common configuration namespace under `cognitive.pipeline.*`. Configuration is loaded at startup from a TOML or JSON file and can be overridden by environment variables.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cognitive.pipeline.batchSize` | integer | 100 | Maximum items processed per stage per tick |
| `cognitive.pipeline.tickInterval` | integer | 1000 | Milliseconds between pipeline ticks |
| `cognitive.pipeline.maxRetries` | integer | 3 | Maximum retry attempts per stage |
| `cognitive.pipeline.stage.<name>.enabled` | boolean | true | Enable/disable specific stages |
| `cognitive.pipeline.stage.<name>.timeout` | integer | 5000 | Milliseconds before stage times out |
| `cognitive.pipeline.ulidSource` | string | `"system"` | ULID source: `"system"`, `"deterministic"`, `"sequential"` |

---

## 9. Testing Strategy

Every stage in the pipeline must be independently testable. The testing strategy mirrors the stage isolation architecture.

### 9.1 Unit Tests

Each stage has a unit test suite covering:
- Happy path (valid input produces expected output)
- Edge cases (empty payload, boundary values, null fields)
- Each failure mode (stage degrades gracefully)
- Determinism (same input always produces same output)

### 9.2 Property-Based Tests

Each stage has property-based tests verifying:
- **Idempotency:** Running the same stage twice on the same input produces the same output.
- **Lineage preservation:** Every output carries valid references to its source inputs.
- **Confidence bounds:** All confidence values are in [0.0, 1.0].
- **No side effects:** The stage does not modify its input or any store it does not own.

### 9.3 Integration Tests

Pipeline integration tests verify:
- End-to-end flow: a recorded sequence of raw events flows through all six stages and produces the expected recommendations
- Error propagation: a failure in one stage does not crash the pipeline or corrupt downstream data
- Replayability: the same event sequence always produces the same complete output

### 9.4 Replay Tests

The pipeline must be able to replay any recorded event sequence and produce identical output. Replay tests verify:
- Identical Observation sequence
- Identical Signal sequence
- Identical Pattern sequence
- Identical Insight sequence
- Identical Recommendation sequence

Replay tests use a deterministic ULID factory and frozen system clock to eliminate all sources of non-determinism.

---

## 10. Performance Characteristics

| Stage | Latency (p50) | Latency (p99) | Throughput | Memory per item |
|-------|---------------|---------------|------------|-----------------|
| F1.0 — Collector | < 1µs | < 100µs | 100,000/s | 512 bytes |
| F1.05 — Normalizer | < 10µs | < 1ms | 50,000/s | 1 KB |
| F1.1 — Extractor | < 50µs | < 5ms | 20,000/s | 512 bytes |
| F1.2 — Detector | < 100µs | < 10ms | 10,000/s | 1 KB |
| F1.3 — Generator | < 50µs | < 5ms | 20,000/s | 512 bytes |
| F2 — Recommender | < 50µs | < 5ms | 20,000/s | 512 bytes |

**End-to-end latency** (p50): < 1ms
**End-to-end latency** (p99): < 50ms
**Maximum sustainable throughput**: 10,000 events/second (detector-bound)

These targets assume all stores are in-memory or backed by SQLite in WAL mode on local SSD storage. Throughput degrades predictably with disk-bound stores.

---

## 11. References

| Reference | Description |
|-----------|-------------|
| DOC-0000 | North Star |
| DOC-0007 | Engineering Philosophy |
| DOC-0009 | Architectural Invariants (I15, I16, I18) |
| ARCH-0030 | Cognitive Architecture |
| ARCH-0033 | Observation Pipeline |
| ARCH-0039 | Observation Normalization |
| ARCH-0040 | Signal Extraction Architecture |
| ARCH-0041 | Pattern Detection Architecture |
| ARCH-0044 | Insight Generation Architecture |
| ARCH-0045 | Recommendation Engine Architecture |
| ARCH-0046 | Cognitive Store Architecture |
| ARCH-0047 | Cognitive Pipeline Testing |
| SPEC-0006 | Cognitive Pipeline Protocol |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version |
