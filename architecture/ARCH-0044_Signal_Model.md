# ARCH-0044 — Signal Model

| Field | Value |
|-------|-------|
| **ID** | ARCH-0044 |
| **Name** | Signal Model |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000, DOC-0009, ARCH-0031, ARCH-0033, ARCH-0040, ARCH-0043 |
| **Referenced by** | ARCH-0045, SPEC-0006 |
| **Principle** | Every signal is a typed, measurable, traceable fact derived exclusively from normalized observations |

---

## 1. Purpose

This document formalizes the Signal data model — the canonical type system, storage contracts, and lifecycle rules that govern every signal produced by the Cognitive Pipeline. It is the single source of truth for what a signal *is*, how it is *identified*, what *types* exist, how it is *stored* and *queried*, and what *guarantees* the system provides around its creation and consumption.

While ARCH-0040 defines *how* signals are extracted from observations, this document defines the *shape*, *type taxonomy*, and *persistence contract* of the signal itself. Downstream consumers — Pattern Detector (F1.2), Metric Computation (F1.3), Insight Generator (F1.4) — depend on this contract.

---

## 2. Signal Schema

Every signal in the system conforms to the following canonical schema:

```python
@dataclass
class Signal:
    id: str                          # ULID — globally unique, sortable by time
    signal_type: str                 # SignalType enum value (e.g. "xp_gained")
    value: float                     # Numeric value only (float, 0.0+)
    confidence: float                # 0.0 (no confidence) to 1.0 (certain)
    source_observation_ids: list[str]  # ULID(s) of source NormalizedObservation(s)
    timestamp: str                   # ISO 8601 UTC — when the signal was extracted
    metadata: dict[str, object]      # Extraction context, rule version, computation trace
```

### 2.1 Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | `str` (ULID) | Yes | Globally unique identifier. ULID chosen over UUID for time-sortability: ULIDs encode a millisecond-precision timestamp in their first 10 characters, enabling chronological ordering without a separate index. Format: 26-character Crockford Base32. |
| `signal_type` | `str` (enum) | Yes | Canonical signal type identifier. Must be a value from the `SignalType` enum (Section 3). Downstream consumers dispatch on this field. |
| `value` | `float` | Yes | The quantitative payload. Always a float — signals are numeric by design. Integer-like values (streak length, mission count) are encoded as `float`. Boolean signals use `1.0` / `0.0`. |
| `confidence` | `float` | Yes | How certain the system is that this signal is accurate. `1.0` for direct extractions from observed fields. Lower values for computed, estimated, or proxy-derived signals. See ARCH-0040 Section 6 for the full confidence model. |
| `source_observation_ids` | `list[str]` | Yes | One or more ULIDs of the `NormalizedObservation`(s) that produced this signal. Direct signals have exactly one. Composite signals have two or more. This is the traceability anchor — every signal can be walked back to its observational root. |
| `timestamp` | `str` (ISO 8601) | Yes | When the signal was extracted, not when the observation occurred. This allows the system to reason about *when a signal became known* independently of *when the event happened*. Format: `2026-07-21T14:30:00.123Z`. |
| `metadata` | `dict[str, object]` | No | Extensible container for extraction context. Reserved keys: `ruleName` (ExtractionRule class name), `ruleVersion` (semver), `extractionDurationMs` (int), `computation` (string describing the formula), `builderId` (for filtering), `sourceObservationIds` (redundant with the field above, retained for query convenience). |

### 2.2 Key Design Decisions

- **`value` is `float` only.** Unlike the earlier `Signal` dataclass that allowed `float | int | str | bool`, the canonical model restricts values to `float`. Strings and booleans are not quantitative and should be encoded as observation metadata or as `1.0`/`0.0` respectively. This simplifies downstream math: every signal value can be fed directly into an aggregate, average, or threshold check without type dispatch.
- **`source_observation_ids` is a list.** Direct signals always have length 1. Composites may reference 2+. Empty lists are invalid — every signal must trace to at least one observation.
- **No `extractedAt` / `observationId`.** The canonical schema uses `timestamp` and `source_observation_ids` respectively. The existing codebase's `extractedAt` and `observationId` are legacy field names; the canonical model supersedes them.

---

## 3. Signal Type Taxonomy

The `SignalType` enum defines every signal that can exist in the system. Each signal type is categorized by analytical domain, linked to its source observations, and defined by a formula.

### 3.1 Taxonomy Table

| SignalType | Category | Source Observations | Formula |
|------------|----------|-------------------|---------|
| `xp_gained` | XP | `mission.completed` | Direct: `data.xpEarned` |
| `xp_total` | XP | `mission.completed` (cumulative) | `sum(xp_gained)` over all missions |
| `rolling_xp_rate` | XP | Composite (xp_gained) | `avg(last N xp_gained)` |
| `completion_rate` | Performance | `mission.completed` | `data.score / 100`, clamped [0.0, 1.0] |
| `rolling_completion_rate` | Performance | Composite (completion_rate) | `avg(last N completion_rate)` |
| `score_achieved` | Performance | `mission.completed`, `assessment.completed` | Direct: `data.score` |
| `time_spent` | Performance | `mission.completed` | Direct: `data.duration` (seconds) |
| `evidence_quality` | Quality | `evidence.submitted` | `min(1.0, len(data.content) / 1000)` |
| `topic_coverage` | Quality | `evidence.submitted` | Direct: `len(data.competencies)` |
| `competency_depth` | Quality | `competency.unlocked` | Direct: `data.level` |
| `streak_active` | Temporal | Composite (time_spent, session_duration) | `1.0` if session within 24h, else `0.0` |
| `streak_length` | Temporal | Composite (streak_active) | Consecutive days with activity |
| `rolling_avg_xp_per_min` | Temporal | Composite (xp_gained, time_spent) | `total_xp / total_minutes` over last N sessions |
| `xp_per_min` | Composite | Composite (xp_gained, time_spent) | `xp_gained / (duration_sec / 60)` |
| `rolling_avg_score` | Composite | Composite (score_achieved) | `avg(last N score_achieved)` |

### 3.2 Mapping to Existing Enum

The canonical taxonomy maps to the codebase's `SignalType` enum as follows:

| Canonical Name | Codebase Equivalent | Notes |
|----------------|-------------------|-------|
| `xp_gained` | `XP_GAINED` | Unchanged |
| `xp_total` | `XP_TOTAL` | Unchanged |
| `rolling_xp_rate` | `ROLLING_AVG_XP` | Renamed for clarity |
| `completion_rate` | `COMPLETION_RATE` | Unchanged |
| `rolling_completion_rate` | `ROLLING_COMPLETION_RATE` | Unchanged |
| `score_achieved` | `SCORE_ACHIEVED` | Unchanged |
| `time_spent` | `TIME_SPENT` | Unchanged |
| `evidence_quality` | `EVIDENCE_QUALITY` | Unchanged |
| `topic_coverage` | `TOPICS_COVERED` | Renamed from `topics_covered` |
| `competency_depth` | `COMPETENCY_DEPTH` | Unchanged |
| `streak_active` | `STREAK_ACTIVE` | Unchanged |
| `streak_length` | `STREAK_LENGTH` | Unchanged |
| `rolling_avg_xp_per_min` | `XP_PER_MINUTE` | Renamed to disambiguate from point-in-time `xp_per_min` |
| `xp_per_min` | (new) | Session-local xp/minute |
| `rolling_avg_score` | `ROLLING_AVG_SCORE` | Unchanged |

New types introduced by this document (`rolling_xp_rate`, `topic_coverage`, `xp_per_min`, `rolling_avg_xp_per_min`) represent canonical names that should be adopted in the next enum revision. The codebase enum retains backward compatibility.

---

## 4. Signal Store Protocol

The `SignalStore` defines the interface for persisting and querying signals. This is the contract that every storage backend (SQLite, in-memory, future backends) must implement.

```python
class SignalStore(Protocol):
    def save(self, signal: Signal) -> None: ...
    def get_by_id(self, id: str) -> Signal | None: ...
    def get_by_type(self, signal_type: str) -> list[Signal]: ...
    def get_by_observation(self, observation_id: str) -> list[Signal]: ...
    def get_by_time_range(self, start: str, end: str) -> list[Signal]: ...
    def get_recent(self, limit: int, offset: int = 0) -> list[Signal]: ...
    def count(self) -> int: ...
```

### 4.1 Method Semantics

| Method | Returns | Behavior |
|--------|---------|----------|
| `save(signal)` | `None` | Persists a single signal. Raises `DuplicateSignalError` if a signal with the same `id` already exists. Signals are write-once — overwrite is never permitted. |
| `get_by_id(id)` | `Signal \| None` | Exact lookup by ULID. Returns `None` if not found. O(1) expected. |
| `get_by_type(type)` | `list[Signal]` | All signals of the given type, ordered by `timestamp` ascending. Returns empty list if none exist. |
| `get_by_observation(obs_id)` | `list[Signal]` | All signals derived from the given observation ULID. Direct signals will typically return 1–4 records; composites may return 0. |
| `get_by_time_range(start, end)` | `list[Signal]` | All signals with `timestamp` in `[start, end)` (half-open interval). Both arguments are ISO 8601 strings. |
| `get_recent(limit, offset)` | `list[Signal]` | Most recent signals by `timestamp`, descending. Standard pagination via `offset`. Default `offset = 0`. |
| `count()` | `int` | Total number of signals in the store. Used for health checks and telemetry. |

### 4.2 Error Conditions

| Condition | Behavior |
|-----------|----------|
| Duplicate `id` on `save` | Raise `DuplicateSignalError` |
| Invalid ULID for `get_by_id` | Return `None` (no matching signal) |
| Unknown `signal_type` for `get_by_type` | Return empty list |
| `start` > `end` in `get_by_time_range` | Raise `ValueError` |
| `limit` <= 0 in `get_recent` | Raise `ValueError` |
| Store connection failure | Raise `StoreConnectionError` |

### 4.3 Implementation Note

The existing codebase `SignalStore` protocol (ARCH-0040, Section 3.4) defines `list_by_builder` and `list_recent` in addition to the methods above. The canonical protocol in this document supersedes those with `get_by_time_range` and `get_recent` for broader applicability. Implementations may provide both legacy and canonical methods during transition.

---

## 5. Signal Lifecycle

Signals follow a strict lifecycle with exactly three phases:

```
EXTRACTED → STORED → READ
    │                   
    └── (never mutated)
```

### 5.1 Phase 1: Extracted (F1.1)

The Signal Extractor produces a new `Signal` instance. At this point the signal exists only in memory:

- `id` is assigned via ULID generation
- `timestamp` is set to the current wall clock (ISO 8601 UTC)
- `confidence` is computed per the extraction rule
- `source_observation_ids` is populated from the source observation(s)
- `metadata` is populated with extraction context (`ruleName`, `ruleVersion`, etc.)

The signal is **not yet available** to downstream consumers.

### 5.2 Phase 2: Stored

The signal is persisted via `SignalStore.save()`. After this call completes:

- The signal is queryable by all `SignalStore` methods
- The signal is visible to the Pattern Detector (F1.2)
- The signal is visible to the Metric Computer (F1.3)
- The signal is visible to the Insight Generator (F1.4)

The signal is **immutable from this point forward**.

### 5.3 Phase 3: Read (F1.2, F1.3, F1.4)

Downstream stages read signals via the `SignalStore` protocol:

- **Pattern Detector (F1.2):** Reads signals by type and time range to detect behavioral patterns (streaks, trends, anomalies).
- **Metric Computer (F1.3):** Reads signals to compute higher-level metrics (velocity scores, engagement indices, competency heatmaps).
- **Insight Generator (F1.4):** Reads signals and patterns to produce human-readable insights.

No stage ever modifies a signal. If new computation is needed (e.g., a new composite that depends on a newly arrived signal), a **new** signal is created and stored. The original signal remains untouched.

### 5.4 Lifecycle Diagram

```
NormalizedObservation
    │
    ▼
┌─────────────────────┐
│  Signal Extractor   │  F1.1 — creates Signal in memory
│  (DirectComposite)  │
└─────────┬───────────┘
          │ Signal (memory)
          ▼
┌─────────────────────┐
│   SignalStore.save  │  F1.1 — persists, becomes immutable
└─────────┬───────────┘
          │ Signal (stored, immutable)
          ▼
┌─────────────────────┐
│  Pattern Detector   │  F1.2 — reads only
├─────────────────────┤
│  Metric Computer    │  F1.3 — reads only
├─────────────────────┤
│  Insight Generator  │  F1.4 — reads only
└─────────────────────┘
```

---

## 6. Consistency Guarantees

The Signal Model provides the following guarantees:

### 6.1 One-to-Many Observation Traceability

Every signal has exactly one source observation (direct signals) or two or more (composite signals). The `source_observation_ids` field is never empty. This ensures a complete, traversable graph from signal back to observation.

**Invariant:** For every signal `S`, there exists at least one normalized observation `O` such that `O.id in S.source_observation_ids`.

### 6.2 Write-Once, Read-Many

Once a signal is persisted via `SignalStore.save()`, it is never modified, updated, or deleted. If a downstream process needs a corrected or recomputed value, it must create a new signal with a new `id`.

**Implication:** The signal store is an append-only log. There is no `update` or `delete` operation in the `SignalStore` protocol.

### 6.3 No Partial Updates

A signal is written atomically — all fields are populated at creation time. There is no mechanism to write a signal in stages (e.g., create without `value`, then fill in later). Partial signals are never visible to consumers.

### 6.4 Temporal Ordering

Signals are ordered by `timestamp`, which is set at extraction time. This ordering is monotonic within a single extraction session but makes no global ordering guarantee across distributed extractors. ULIDs provide an alternative ordering by creation time that is globally consistent.

### 6.5 No Historical Mutation

Composite signals represent the state of knowledge at a point in time. If a new observation arrives that would change a rolling average, a **new** composite signal is created. The old composite signals remain in the store, representing what the system *knew* at each point in time. This enables time-travel queries and historical replay.

**Example:** A builder completes missions M1, M2, M3. After each mission, a `rolling_completion_rate` signal is created:
- After M1: `rolling_completion_rate = 1.0` (only 1 data point)
- After M2: `rolling_completion_rate = 0.9` (average of 2)
- After M3: `rolling_completion_rate = 0.93` (average of 3)

All three signals exist. No signal is overwritten.

### 6.6 Summary Table

| Guarantee | Description | Enforced By |
|-----------|-------------|-------------|
| Traceability | Every signal links to ≥1 observation | Schema validation |
| Immutability | No update, no delete | Store protocol |
| Atomic write | All fields set at creation | Constructor + Store.save |
| Temporal ordering | Signals sortable by timestamp | ULID + ISO 8601 |
| Historical preservation | All signals retained forever | Append-only store |
| Type safety | Every signal has a valid SignalType | Enum validation |

---

## 7. References

| Reference | Description |
|-----------|-------------|
| DOC-0000 | North Star — foundational principles |
| DOC-0009 | Architectural Invariants — I15 (traceability), I16 (immutability) |
| ARCH-0031 | Observation Model — upstream data model |
| ARCH-0033 | Observation Pipeline — pipeline integration context |
| ARCH-0040 | Signal Extraction Architecture — extraction engine, rules, confidence |
| ARCH-0043 | Store Protocol Specification — storage layer contracts |
| ARCH-0045 | Pattern Detection Model (planned) — downstream consumer |
| SPEC-0006 | Signal Type Registry (planned) — formal type registration |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version |

