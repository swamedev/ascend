# ARCH-0039 — Observation Normalization

| Field | Value |
|-------|-------|
| **ID** | ARCH-0039 |
| **Name** | Observation Normalization |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0030 Cognitive Architecture, ARCH-0031 Observation Model, ARCH-0033 Observation Pipeline |
| **Principle** | Every raw event must become a canonical, traceable, and deterministic observation before it can be analyzed |

---

## 1. Purpose

The Observation Collector (F1.0) captures raw events from the Runtime and produces `Observation` objects. However, these raw observations carry source-native field names, source-native timestamps, and ephemeral identifiers (UUID v4) that are not ordered, not traceable across causal chains, and not guaranteed to be free of sensitive data.

Observation Normalization is the bridge between raw capture and structured analysis. It transforms every raw observation into a **canonical, immutable, traceable, and analysis-ready** `NormalizedObservation` that the remainder of the Cognitive Pipeline — Signal Extraction, Pattern Detection, Insight Generation — can consume without needing to understand Runtime internals.

The Normalizer is Stage 1.5 in the pipeline (F1.05 placement in the Milestone F roadmap): it receives raw `Observation` objects from the Collector and emits `NormalizedObservation` objects to the Signal Extractor.

> **Core Guarantee:** After normalization, every observation has the same shape, the same field semantics, a globally sortable identifier, a causal trace, and zero sensitive data — regardless of its source.

---

## 2. Normalization Principles

### 2.1 Immutability In, Immutability Out

The Normalizer never modifies its input. It reads a raw `Observation`, produces a `NormalizedObservation`, and passes the original along for audit logging if needed. This ensures that raw evidence is never lost and that normalization can be re-run with different rules.

### 2.2 Additive Only

Normalization only adds fields. It never removes fields from the original data payload — it may transform field names (mapping `mission_id` to `data.missionId`) but the original values are preserved under `data.raw` for debugging. The only exception is PII/sensitive data stripping, which removes values entirely (not just renames).

### 2.3 Deterministic

Given the same raw `Observation` and the same configuration, the Normalizer always produces the same `NormalizedObservation`. This is guaranteed by:
- Pure-function field mappings
- Deterministic ULID generation (ULIDs embed timestamp but are deterministic for the same timestamp input)
- Stable sort order for multi-field transformations

### 2.4 Zero AI

Normalization is entirely rule-based. No ML model, no LLM, no statistical inference. Every transformation is a lookup table, a regex, or a pure function.

---

## 3. Normalization Pipeline

The Normalizer applies the following transformations in strict order:

```
Raw Observation
    │
    ▼
┌─────────────────────────────┐
│ 1. Identifier Generation    │  Generate ULID, set as normalized ID
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 2. Timestamp Normalization  │  Convert to ISO 8601 UTC
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 3. Field Mapping            │  Map source-native → canonical names
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 4. Correlation & Causation  │  Link events in causal chains
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 5. PII / Sensitive Stripping│  Remove secrets, tokens, PII
└──────────┬──────────────────┘
           ▼
┌─────────────────────────────┐
│ 6. Schema Annotation        │  Set version, collector, source metadata
└──────────┬──────────────────┘
           ▼
    NormalizedObservation
```

Each step is independently testable. Any step may add a `warnings` entry to the observation's `metadata.warnings` array, but no step may fail the entire normalization — degraded normalization is preferred over dropped observations.

---

## 4. Step 1 — Identifier Generation

### 4.1 ULID over UUID

The Normalizer replaces the raw observation's UUID v4 `id` with a **ULID** (Universally Unique Lexicographically Sortable Identifier).

| Property | UUID v4 | ULID |
|----------|---------|------|
| Sortable | No | Yes (lexicographic = temporal) |
| Timestamp-encoded | No | Yes (first 10 chars = millisecond timestamp) |
| Length | 36 chars | 26 chars |
| Collision probability | Negligible | Negligible |
| Example | `550e8400-e29b-41d4-a716-446655440000` | `01ARZ3NDEKTSV4RRFFQ69G5FAV` |

**Why ULID:** Sortability is essential for timeline reconstruction. Observations produced in temporal order will have ULIDs that sort in the same order, enabling range queries without a separate timestamp index. This directly supports the Timeline (ARCH-0038) and Replay requirements.

### 4.2 Generation Rules

- Every `NormalizedObservation` receives a new ULID as its `id`.
- The ULID timestamp component is set to the observation's logical timestamp (not the system clock).
- The ULID random component is generated using `os.urandom` or `secrets.randbits`.
- The original observation ID is preserved in `metadata.originalId`.

### 4.3 Testability

For deterministic testing, the Normalizer accepts an optional ULID factory override. When injected, the factory produces predictable ULIDs based on a sequence number rather than random bits. This enables deterministic assertion in tests:

```python
def test_normalizer_deterministic():
    fake_factory = DeterministicUlidFactory(seed=42)
    normalizer = ObservationNormalizer(ulid_factory=fake_factory)
    result_1 = normalizer.normalize(raw_obs)
    result_2 = normalizer.normalize(raw_obs)
    assert result_1.id == result_2.id
```

---

## 5. Step 2 — Timestamp Normalization

### 5.1 Rules

Every observation must have a `timestamp` field in ISO 8601 UTC format. The Normalizer:

1. Reads the raw observation's `timestamp` field.
2. Attempts to parse it using the following strategies, in order:
   - ISO 8601 (any timezone) → convert to UTC
   - Unix epoch (seconds or milliseconds as integer/float) → convert to ISO 8601
   - RFC 2822 / RFC 3339 → convert to ISO 8601
   - Python `datetime` ISO format → ensure UTC suffix
3. If parsing succeeds, set `timestamp` to the normalized UTC ISO 8601 string.
4. If parsing fails:
   - Set `timestamp` to the current system clock in UTC.
   - Add `'unparseable_timestamp'` to `metadata.warnings`.

### 5.2 Edge Cases

| Input | Behavior |
|-------|----------|
| `2026-07-21T14:30:00Z` | Pass through (already UTC ISO 8601) |
| `2026-07-21T11:30:00-03:00` | Convert to `2026-07-21T14:30:00Z` |
| `1741500000` (Unix epoch, seconds) | Convert to ISO 8601 |
| `1741500000000` (Unix epoch, ms) | Convert to ISO 8601 |
| `"yesterday"` | Fall back to system clock, add warning |
| `null` / missing | Fall back to system clock, add warning |

---

## 6. Step 3 — Field Mapping

### 6.1 Purpose

Different event sources use different field naming conventions. The Runtime uses `snake_case` (`mission_id`, `builder_id`). Future Experience Layer events may use `camelCase` (`missionId`) or kebab-case (`mission-id`). The Normalizer maps all source-native field names to the canonical `camelCase` convention used throughout the Cognitive Layer.

### 6.2 Mapping Rules

The mapping is a two-level transformation:

**Top-level fields** (on the observation object itself):

| Raw Field | Canonical Field | Always Present |
|-----------|----------------|----------------|
| `id` | → `id` (regenerated as ULID) | Yes |
| `type` | → `type` (pass through) | Yes |
| `source` | → `source` (pass through) | Yes |
| `timestamp` | → `timestamp` (normalized) | Yes |
| `data` | → `data` (see nested mapping) | Yes |
| `context` | → `context` (see enrichment, not normalization) | Yes |
| `metadata` | → `metadata` (enriched by normalizer) | Yes |

**Nested `data` fields** (payload-specific):

| Source Field (snake_case) | Canonical Field (camelCase) | Applies to Types |
|--------------------------|----------------------------|------------------|
| `builder_id` | → `builderId` | All |
| `mission_id` | → `missionId` | `mission.*`, `evidence.*` |
| `evidence_id` | → `evidenceId` | `evidence.*`, `assessment.*` |
| `assessment_id` | → `assessmentId` | `assessment.*` |
| `competency_id` | → `competencyId` | `competency.*` |
| `achievement_id` | → `achievementId` | `achievement.*` |
| `journey_id` | → `journeyId` | `journey.*`, `mission.*` |
| `session_id` | → `sessionId` | All |
| `artifact` | → `content` | `evidence.*` |
| `score` | → `score` | `assessment.*` |

### 6.3 Unknown Fields

Fields not present in the mapping table are preserved under `data.raw` as a nested dictionary. This ensures no data is lost, while keeping the canonical fields predictable:

```python
{
    "data": {
        "builderId": "bld-42",
        "missionId": "m-101",
        "raw": {
            "legacy_field": "some_value",
            "unrecognized_flag": True
        }
    }
}
```

### 6.4 Transformation Implementation

The field mapper is a pure function that takes a `dict` (raw `data` payload) and returns a mapped `dict`. The mapping table is a configuration object, not hardcoded, enabling future source types to register their own mappings:

```python
class FieldMapper:
    def __init__(self, mappings: dict[str, str]):
        self._mappings = mappings

    def map(self, data: dict[str, Any]) -> dict[str, Any]:
        result = {}
        raw = {}
        for key, value in data.items():
            if key in self._mappings:
                result[self._mappings[key]] = value
            else:
                raw[key] = value
        if raw:
            result["raw"] = raw
        return result
```

---

## 7. Step 4 — Correlation & Causation

### 7.1 Correlation

Every observation is assigned a `correlationId` ULID. Observations that originate from the same triggering action share the same `correlationId`. For example:

- Builder submits evidence → triggers `evidence.submitted` event → triggers `assessment.completed` event.
- Both events share the same `correlationId`.

If the raw observation already carries a `correlationId` (set by the source), it is preserved. Otherwise, a new ULID is generated.

### 7.2 Causation

If an observation was caused by a specific previous observation, its `causationId` points to the `id` of that previous observation. This creates a causal chain:

```
Observation A (evidence.submitted)      id=ULID_1
    │
    └──→ Observation B (assessment.completed)
         causationId = ULID_1
```

The causation chain enables tracing any cognitive artifact (signal, pattern, insight) back through its causal ancestors to the root observation.

Causation is set by the source when it knows the causal relationship. If unknown, `causationId` is `null`.

### 7.3 Trace Structure

```python
trace: {
    "correlationId": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
    "causationId": "01ARZ3NDE000000000000000000",  # or null
}
```

---

## 8. Step 5 — PII / Sensitive Data Stripping

### 8.1 Principles

1. **Default deny.** Any field whose name matches a sensitive pattern is stripped before storage.
2. **Strip by field name pattern, not content.** The Normalizer does not inspect field values to determine sensitivity — it uses field name patterns. This is safer (no false negatives) and faster (no content scanning).
3. **Log the field name, not the value.** Stripped fields are logged at DEBUG level with their field names only. Values are never logged.
4. **Raw payload preservation.** The original unstripped payload is NEVER persisted. Stripping is irreversible.

### 8.2 Stripped Field Patterns

| Pattern | Matches | Example |
|---------|---------|---------|
| `*password*` | `password`, `passwd`, `master_password` | Stripped |
| `*token*` | `token`, `access_token`, `refresh_token` | Stripped |
| `*secret*` | `secret`, `secret_key`, `api_secret` | Stripped |
| `*key*` (when value looks like a key) | `api_key`, `private_key` | Stripped |
| `*email*` | `email`, `email_address` | Stripped |
| `*phone*` | `phone`, `phone_number`, `mobile` | Stripped |
| `*ssn*` | `ssn`, `social_security` | Stripped |
| `*address*` (when combined with personal context) | `address`, `home_address` | Stripped |
| Binary field (>64 KB) | Any field whose raw value exceeds 64 KB | Stripped |

### 8.3 Stripping Behavior

When a sensitive field is detected:
1. The field is removed from the `data` payload entirely.
2. An entry is added to `metadata.strippedFields`: `["field_name_1", "field_name_2"]`.
3. The event is logged at DEBUG level: `"Stripped sensitive field '{name}' from observation {id}"`.

No sensitive data is ever written to `data.raw`, logs, or any persistence layer.

---

## 9. Step 6 — Schema Annotation

The Normalizer enriches the `metadata` object with schema provenance information:

| Field | Value | Description |
|-------|-------|-------------|
| `observationSchema` | `"1.0"` | Schema version of the normalized format |
| `normalizer` | `"observation-normalizer"` | Component identifier |
| `normalizedAt` | ISO 8601 UTC | When normalization completed |
| `originalId` | Original UUID v4 | Traceability back to raw observation |
| `warnings` | `[]` or string array | Any warnings accumulated during normalization |

---

## 10. NormalizedObservation Schema

```python
@dataclass
class NormalizedObservation:
    id: str                             # ULID
    type: str                           # e.g. 'mission.completed'
    source: str                         # 'runtime' | 'cognitive' | 'builder'
    timestamp: str                      # ISO 8601 UTC, normalized
    data: dict[str, Any]                # CamelCase mapped payload
    context: dict[str, Any]             # builderId, sessionId, etc. (enriched later)
    metadata: dict[str, Any]            # Schema version, normalizer info, warnings
    trace: dict[str, str | None]        # correlationId, causationId
```

### 10.1 Field Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | ULID, globally unique, sortable |
| `type` | Yes | Dot-separated event type per ARCH-0031 taxonomy |
| `source` | Yes | One of: `runtime`, `cognitive`, `builder` |
| `timestamp` | Yes | ISO 8601 UTC |
| `data` | Yes | Canonical payload (may be empty `{}`) |
| `context` | Yes | At minimum `{"builderId": "..."}` |
| `metadata` | Yes | At minimum `{"observationSchema": "1.0"}` |
| `trace` | Yes | At minimum `{"correlationId": "...", "causationId": null}` |

### 10.2 Comparison to Raw Observation

| Aspect | Raw Observation (F1.0) | NormalizedObservation (F1.05) |
|--------|----------------------|------------------------------|
| ID | UUID v4 | ULID (sortable by time) |
| Timestamp | Any format | ISO 8601 UTC |
| Field names | Source-native (snake_case) | Canonical (camelCase) |
| PII | May be present | Stripped |
| Causation | Not tracked | `correlationId` + `causationId` |
| Sortability | Not sortable | Lexicographically sortable by time |
| Raw fallback | N/A | Original values in `data.raw` |

---

## 11. Normalizer Interface

```python
class ObservationNormalizer:
    def __init__(
        self,
        field_mappings: dict[str, str] | None = None,
        ulid_factory: Callable[[], str] | None = None,
    ) -> None: ...

    def normalize(self, observation: Observation) -> NormalizedObservation:
        """Transform a raw Observation into a NormalizedObservation.
        
        The normalization is deterministic, additive, and idempotent.
        No exception is raised for malformed input — degraded normalization
        is preferred over data loss.
        """

    def normalize_batch(
        self, observations: list[Observation]
    ) -> list[NormalizedObservation]:
        """Normalize multiple observations in batch.
        
        Each observation is normalized independently. Order is preserved.
        """
```

### 11.1 Batch Semantics

`normalize_batch` processes each observation independently through the full normalization pipeline. Observations in a batch do not share state — each gets its own ULID, correlation ID, and causation chain. This enables parallel processing of independent observations.

If batch-level correlation is needed (multiple observations from the same triggering action), the caller should set `correlationId` on each raw observation before passing to the normalizer.

---

## 12. Failure Modes

| Failure | Behavior |
|---------|----------|
| Missing `type` field | Set `type = 'unknown'`, add `warnings: ['missing_type']` |
| Missing `source` field | Set `source = 'unknown'`, add `warnings: ['missing_source']` |
| Missing `timestamp` field | Use system clock, add `warnings: ['missing_timestamp']` |
| Unparseable timestamp | Use system clock, add `warnings: ['unparseable_timestamp']` |
| Unknown source identifier | Set `source = 'unknown'`, add `warnings: ['unknown_source']` |
| Sensitive field detected | Strip silently, log DEBUG, add to `metadata.strippedFields` |
| ULID factory fails | Fall back to UUID v4, add `warnings: ['ulid_fallback']` |
| Empty payload (`data` is empty) | Treat as valid observation with empty data |
| Payload exceeds 1 MB total | Add `warnings: ['oversized_payload']`, truncate `data` to first 1 MB |

No failure mode crashes the pipeline. Every failure produces a valid `NormalizedObservation` with degraded data and a warning.

---

## 13. Determinism Guarantee

Given the same raw `Observation` and the same configuration (field mappings, ULID factory seed), the Normalizer always produces the identical `NormalizedObservation`.

This is guaranteed by:
- **Pure-function field mapping.** The mapper is a stateless lookup table.
- **Deterministic ULIDs.** When a deterministic factory is injected, ULIDs are reproducible.
- **Stable sort order.** Multi-field mappings iterate keys in a stable order (insertion order in Python 3.7+).
- **Fixed timestamp normalization.** Given the same input timestamp, the output is always the same UTC ISO 8601 string.
- **No external state.** The Normalizer reads no files, calls no network, and queries no database.

For testing, inject a `DeterministicUlidFactory` seeded with a known value. This enables assertions like:

```python
normalizer = ObservationNormalizer(ulid_factory=DeterministicUlidFactory(seed=1))
result = normalizer.normalize(raw_obs)
assert result.id == "01ARZ3NDEKTSV4RRFFQ69G5FAV"  # deterministic
```

---

## 14. Relationship to the Pipeline

In the Observation Pipeline (ARCH-0033), the Normalizer occupies Stage 2 (between Collector Stage 1 and Validator Stage 3). In the Milestone F roadmap, it occupies F1.05 (between F1.0 Collector and F1.1 Signal Extractor):

```
F1.0 Collector ──→ F1.05 Normalizer ──→ F1.1 Signal Extractor
```

The relationship to other stages:

| Upstream | This Stage | Downstream |
|----------|------------|------------|
| F1.0 Collector (raw `Observation`) | **F1.05 Normalizer** (`NormalizedObservation`) | F1.1 Signal Extractor (extracts signals from normalized data) |
| Stage 1: Collector (ARCH-0033) | Stage 2: Normalizer (ARCH-0039) | Stage 3: Validator (ARCH-0033) |

The Validator (Stage 3) validates `NormalizedObservation` objects — it checks that the normalized event conforms to the taxonomy. The Signal Extractor (F1.1) consumes `NormalizedObservation` objects and produces `Signal` objects.

---

## 15. References

| Reference | Description |
|-----------|-------------|
| ARCH-0030 | Cognitive Architecture — the owning layer |
| ARCH-0031 | Observation Model — input data model |
| ARCH-0033 | Observation Pipeline — pipeline context |
| ARCH-0032 | Observation Event Taxonomy — event type validation |
| ARCH-0040 | Signal Extraction Architecture — downstream consumer |
| SPEC-0005 | ASCEND Cognitive Protocol — protocol for insight delivery |
| DOC-0009 | Architectural Invariants — I15 Observation Determinism, I16 Observation Append Only |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO PROMETHEUS |
