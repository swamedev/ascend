# ARCH-0036 — Observation SDK

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0036 |
| **Nome** | Observation SDK |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0003 Core Engine Specification, ARCH-0030 Cognitive Architecture, ARCH-0031 Observation Model, ARCH-0032 Event Taxonomy |
| **Será utilizado por** | Runtime Layer, Experience Layer, Cognitive Layer, Frontend SDK, Adoption Strategy V2 |

---

## 1. Purpose

The Observation SDK is the official API for all observation operations. Every component — Runtime, Experience, Cognitive — observes through this SDK. No component accesses SQLite or the Observation Storage directly. This SDK is the single entry point for the entire cognitive pipeline.

The SDK exists to enforce a hard architectural boundary: **observation is an abstraction, not a storage concern.** The Runtime emits events. The Experience Layer captures user interactions. The Cognitive Layer processes state snapshots. None of these components know or care how observations are stored, buffered, batched, or flushed. They call the SDK, and the SDK handles the rest.

This separation serves five architectural goals:

1. **Decoupling.** Storage technology can change without affecting any producer. SQLite can be replaced by PostgreSQL, a cloud data lake, or an in-memory store — and no producer needs to be modified.

2. **Observability.** Because all observation flows through a single entry point, tracing, debugging, and telemetry are centralized. A single instrumentation point can measure throughput, latency, error rates, and buffer depth across the entire system.

3. **Contract enforcement.** The SDK validates event structure, enforces schema versions, and rejects malformed observations before they reach storage. Producers cannot accidentally corrupt the observation stream.

4. **Fire and forget.** Producers are never blocked by storage latency, buffer backpressure, or network failures. The SDK guarantees non-blocking observation regardless of underlying storage performance.

5. **Auditability.** Every observation passes through the SDK's sequence-numbering layer, producing a gap-free, monotonic stream that enables deterministic replay and cryptographic audit trails.

The SDK does not interpret, analyze, or transform observation data. It is a pure conduit — capture, validate, sequence, buffer, store, and replay. All interpretation belongs to the Cognitive Layer, which consumes observations through the same SDK's Query API.

---

## 2. Design Principles

### 2.1 Single Entry Point

All observations — regardless of source, type, or urgency — flow through the `observe()` method. There is no backdoor, no direct storage access, no bypass mechanism. This principle is enforced by convention (documented in every relevant ARCH document) and by dependency injection: the SDK instance is the only object with access to the storage backend.

### 2.2 Fire and Forget

Observation never blocks the caller. The SDK accepts the event, assigns a sequence number, enqueues it in an in-memory buffer, and returns immediately. Storage is asynchronous. If the caller needs confirmation of persistence, it may await the returned Promise, but the SDK guarantees that the Promise resolves within 1ms regardless of storage state.

### 2.3 Batched

Events are buffered in memory and flushed to storage periodically or when the buffer reaches a configurable threshold. Batching reduces write pressure on storage, enables atomic batch commits, and improves overall throughput. The flush interval and batch size are configurable through the Configuration API.

### 2.4 Deterministic

Same input always produces the same storage output. Sequence numbers are monotonic and gap-free within a session. Replaying the same sequence of events from the same session produces identical results. The SDK does not introduce randomness, does not reorder events within a session, and does not drop events silently (except under ring-buffer overflow, which is documented in section 9).

### 2.5 Offline-First

The SDK requires no network connectivity. All storage is local. The SDK never phones home, never contacts a remote server, and never depends on cloud infrastructure. This is a hard requirement derived from ASCEND's Local First principle — observation data belongs to the user and must never leave their device without explicit consent.

### 2.6 Zero Business Logic

The SDK captures, validates, sequences, buffers, and stores. It does not interpret. It does not compute metrics. It does not detect patterns. It does not generate insights. It does not recommend. All business logic — aggregation, analysis, inference, recommendation — belongs to the Cognitive Layer, which consumes observations via the SDK's Query API. This separation ensures that the SDK remains stable, testable, and replaceable independent of the cognitive pipeline.

### 2.7 Schema Agnostic

The SDK does not understand the semantics of event types. It validates structure (required fields, types, format constraints) but does not interpret meaning. New event types can be introduced without modifying the SDK. The SDK stores whatever valid event it receives and returns it unchanged on replay.

---

## 3. Core API

### 3.1 `observe(event: ObservationEvent): Promise<ObservationReceipt>`

The universal observation method. Every event type uses this single entry point. There is no specialized path for different event types — all events flow through the same pipeline.

**Input:** `ObservationEvent` — the canonical event payload as defined by ARCH-0032 Event Taxonomy. The event must conform to the `Observation` interface defined in ARCH-0031 section 3.1, with a valid `type`, `source`, `timestamp`, `context`, and `data` field.

**Output:** `ObservationReceipt` — a lightweight confirmation object containing the assigned ID, sequence number, and timestamp.

```typescript
interface ObservationReceipt {
  id: string
  sequenceNumber: number
  timestamp: string
  queued: boolean
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID v4 assigned to the observation. This is the canonical identifier used for annotation, querying, and cross-referencing. |
| `sequenceNumber` | `number` | Monotonic, gap-free integer within the current session. Sequence numbers start at 1 for each session and increment by 1 for each event. |
| `timestamp` | `string` | ISO 8601 UTC timestamp of when the SDK accepted the event. This may differ from the event's own timestamp by microseconds (the event timestamp reflects when the event occurred; the receipt timestamp reflects when the SDK processed it). |
| `queued` | `boolean` | Indicates whether the event was queued to the in-memory buffer (`true`) or synchronously persisted (`false`). Under normal operation this is `true`; it is `false` only when the SDK is configured with synchronous mode for testing. |

**Constraints:**

- Must not throw. If the event is invalid, the SDK logs the error and returns a receipt with `queued: false` and an empty `id`. The caller must never wrap `observe()` in a try-catch for observation logic.
- Must not block for more than 1ms in the hot path. The event is enqueued and the receipt is returned immediately. Storage I/O happens on a background thread.
- Must accept any valid `ObservationEvent`. There is no whitelist of allowed types. If the event satisfies the structural contract (valid UUID, valid type pattern, valid ISO timestamp, required context fields), it is accepted.
- Must reject events that violate the structural contract by logging the error and returning a no-op receipt. Rejection reasons include: missing `builderId`, malformed UUID in `id`, invalid `type` format, missing `timestamp`, non-ISO `timestamp`, empty `data`.

**Behavioral guarantees:**

- The receipt's `sequenceNumber` is assigned synchronously at enqueue time. If two events are observed in the same microtask, they receive consecutive sequence numbers in call order.
- The `id` in the receipt matches the `event.id` if one was provided. If the event has no `id`, the SDK generates one (UUID v4).
- The `timestamp` in the receipt is set at the moment the SDK processes the call, not when the event occurred. This enables latency measurement between event production and SDK ingestion.

### 3.2 `track(eventName: string, data?: Record<string, unknown>): Promise<ObservationReceipt>`

Simplified observation for Experience Layer events where the full event type is known from the taxonomy. This is syntactic sugar over `observe()` — it constructs the `ObservationEvent` from the event name and data, adding source and collector metadata automatically.

**Input:**
- `eventName` — a dotted string matching the `ObservationType` pattern defined in ARCH-0031 section 3.2 (e.g., `"behavior.mission.started"`, `"session.ended"`, `"competency.unlocked"`).
- `data` — optional key-value payload. The SDK places this directly into the event's `data` field.

**Output:** `ObservationReceipt` — identical to the receipt returned by `observe()`.

**Automatic metadata injection:**

The SDK automatically populates the following fields that would otherwise need to be set manually:
- `source`: set to the configured source for this SDK instance (defaults to `"experience"` when used from Experience Layer, `"runtime"` when used from Runtime Layer).
- `context.builderId`: injected from the current session context.
- `metadata.collector`: set to the TrackingCollector identifier.
- `metadata.observationSchema`: set to the current schema version.
- `timestamp`: set to the current system time in ISO 8601 UTC.

**When to use `track` vs `observe`:**

| Use `track` | Use `observe` |
|-------------|---------------|
| Simple event with known type from taxonomy | Complex event with custom structure |
| Experience Layer UI interactions | Runtime domain events |
| Quick instrumentation where full event construction is overhead | Cross-component events with rich context |
| Prototyping and rapid iteration | Production-critical events requiring explicit field control |
| Events where source is always the same | Events from multiple sources routed through one SDK instance |

### 3.3 `measure(metricName: string, value: number, metadata?: Record<string, unknown>): Promise<void>`

Records a direct metric measurement. Metrics are numeric observations that represent a point-in-time measurement — a score, a count, a duration, a ratio. Unlike events, which capture something that *happened*, metrics capture something that *was measured*.

**Input:**
- `metricName` — a dotted string identifying the metric (e.g., `"focus_score"`, `"session_duration_seconds"`, `"evidence_submission_rate"`). Metric names should follow the convention `noun.qualifier` or `domain.metric`.
- `value` — a numeric measurement. Must be finite (`NaN`, `Infinity`, and `-Infinity` are rejected and logged).
- `metadata` — optional key-value metadata providing context about the measurement (e.g., `{ unit: "seconds" }`, `{ missionId: "vars-101" }`).

**Output:** `Promise<void>` — resolves immediately after enqueuing. The caller cannot observe the storage outcome (fire and forget).

**Internal behavior:**

The SDK transforms the `measure()` call into an internal `ObservationEvent` with:
- `type`: `"metric.recorded"`
- `data`: `{ metricName, value, metadata }`
- `source`: set to the configured source

This event enters the same observation pipeline as any other event. It is sequenced, buffered, batched, and flushed identically. This means metrics are fully replayable, queryable, and auditable through the same Query API.

**Example:**

```typescript
sdk.measure("focus_score", 0.85)
sdk.measure("session_duration_seconds", 2400, { unit: "seconds" })
sdk.measure("evidence_quality_score", 0.92, { evidenceId: "ev-123" })
```

**Constraints:**
- Must not throw for any input (invalid metric names are logged and discarded).
- Metric names must match `^[a-z][a-z0-9_.]+$`. Invalid names are logged and the call is a no-op.
- Values must be finite numbers. Non-finite values are logged and the call is a no-op.
- Metadata is optional. If provided, it is shallow-validated (keys must be strings, values must be JSON-serializable).

### 3.4 `checkpoint(label?: string): Promise<CheckpointReceipt>`

Marks a point in the observation stream. Checkpoints have no data payload — they are purely positional markers. They serve as session boundaries, milestone markers, or user-defined breakpoints that enable efficient replay and time-range queries.

**Input:**
- `label` — optional string label identifying the checkpoint (e.g., `"session_start"`, `"onboarding_complete"`, `"mid_session"`, `"user_pause"`). If omitted, the SDK generates a label based on the sequence number (`"checkpoint_<seq>"`).

**Output:**

```typescript
interface CheckpointReceipt {
  id: string
  sequenceNumber: number
  label: string
  timestamp: string
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | UUID v4 assigned to the checkpoint event. |
| `sequenceNumber` | `number` | Sequence number in the current session. Checkpoints consume sequence numbers like any other event. |
| `label` | `string` | The resolved label (either the provided value or the auto-generated fallback). |
| `timestamp` | `string` | ISO 8601 UTC timestamp of the checkpoint. |

**Use cases:**

- **Session boundaries:** A checkpoint at session start and end allows replay queries to efficiently locate session boundaries without scanning event data.
- **Milestone tracking:** Missions, journeys, and achievement unlocks can emit checkpoints alongside their primary events, enabling timeline visualization without loading all events.
- **Stream segmentation:** Long-running sessions can use checkpoints to create logical segments for partial replay.
- **User-defined markers:** The Experience Layer can allow builders to place manual checkpoints ("I want to remember this moment"), which appear as labeled markers in the observation stream.

**Internal behavior:**

Checkpoints are stored as `ObservationEvent` objects with `type: "checkpoint"` and `data: { label }`. They enter the standard observation pipeline and are fully queryable through the Query API.

### 3.5 `snapshot(): Promise<SnapshotReceipt>`

Triggers a full state snapshot. Snapshots capture the current state of the observation system — buffer depth, sequence number, session metadata, and a compressed digest of recent events. Unlike checkpoints, which are lightweight positional markers, snapshots are heavyweight state captures intended for recovery, audit, and session summary computation.

**Output:**

```typescript
interface SnapshotReceipt {
  snapshotId: string
  timestamp: string
  size: number
}
```

| Field | Type | Description |
|-------|------|-------------|
| `snapshotId` | `string` | UUID v4 identifying this snapshot. |
| `timestamp` | `string` | ISO 8601 UTC timestamp of when the snapshot was taken. |
| `size` | `number` | Compressed size of the snapshot in bytes. |

**When snapshots are taken:**

- **Session end.** When `endSession()` is called, a snapshot is automatically triggered.
- **Periodic.** The SDK can be configured to take snapshots every N events or every M minutes through SDK options.
- **Manual.** Any component may call `snapshot()` to capture state at a specific moment.
- **Before shutdown.** The `flush()` method can be configured to trigger a pre-shutdown snapshot.

**Snapshot contents:**

A snapshot includes:
- Current sequence number position
- Compressed event digest (count, time range, type distribution)
- Session metadata (session ID, builder ID, start time, event count)
- Buffer state (current depth, high-water mark, dropped event count)
- Configuration snapshot (effective SDK options at snapshot time)

Snapshots are stored as special observation events with `type: "snapshot"`. They are queryable through the standard Query API.

### 3.6 `annotate(observationId: string, annotation: Annotation): Promise<void>`

Adds metadata to a previously observed event. Annotations are stored separately from the original event and do not modify it. This preserves immutability — the original observation is never altered after storage.

**Input:**
- `observationId` — the UUID of the observation to annotate. If the observation does not exist, the annotation is logged and discarded.
- `annotation` — an annotation object containing a key, value, and timestamp.

```typescript
interface Annotation {
  key: string
  value: unknown
  timestamp: string
}
```

| Field | Type | Description |
|-------|------|-------------|
| `key` | `string` | Annotation key. Convention is dotted notation (e.g., `"cognitive.insight_id"`, `"reviewer.comment"`, `"workflow.status"`). |
| `value` | `unknown` | Any JSON-serializable value. |
| `timestamp` | `string` | ISO 8601 UTC timestamp of when the annotation was created. |

**Output:** `Promise<void>` — resolves when the annotation has been stored.

**Use cases:**

- **Cognitive Layer insights.** When the Cognitive Layer generates an insight based on an observation, it annotates the observation with the insight ID, linking the raw data to the derived conclusion.
- **Human review.** A mentor or reviewer can annotate observations with comments, assessments, or contextual notes.
- **Workflow state.** Observations can be annotated with workflow status (e.g., `"reviewed"`, `"escalated"`, `"archived"`) without altering the original event.
- **Correction metadata.** If an observation is later found to contain an error, a correction annotation can be attached without modifying the original (ensuring audit trail integrity).

**Constraints:**
- Annotations are append-only. There is no `updateAnnotation` or `deleteAnnotation` method. Immutability extends to annotations.
- Multiple annotations can be attached to the same observation. Each annotation is stored as an independent record.
- The SDK does not enforce uniqueness of keys. Multiple annotations with the same key are allowed and stored in timestamp order.
- Annotations are not replayed as part of the event stream. They are retrieved separately through the Query API (`getEvents` returns events without annotations; annotations are fetched by observation ID).

### 3.7 `replay(builderId: string, options?: ReplayOptions): AsyncIterable<ObservationEvent>`

Replays all observations for a builder within the specified time range. Returns an async iterable for memory-efficient processing. This is the primary mechanism for the Cognitive Layer to consume historical observation data.

```typescript
interface ReplayOptions {
  from?: string      // ISO 8601
  to?: string        // ISO 8601
  types?: string[]   // filter by event type
  limit?: number
  offset?: number
  order?: 'asc' | 'desc'
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `from` | `string` | Session start | Inclusive start of the time range. |
| `to` | `string` | Current time | Inclusive end of the time range. |
| `types` | `string[]` | All types | Filter to specific event type(s). |
| `limit` | `number` | Unlimited | Maximum number of events to return. |
| `offset` | `number` | 0 | Number of events to skip. |
| `order` | `'asc' \| 'desc'` | `'asc'` | Chronological order of returned events. |

**Output:** `AsyncIterable<ObservationEvent>` — a stream of observation events that can be consumed with `for await...of` or with a streaming consumer. The async iterable lazily loads events from storage, enabling processing of arbitrarily large datasets without loading them entirely into memory.

**Memory efficiency guarantees:**

- The async iterable fetches events in pages (default page size: 100). Only one page is held in memory at a time.
- If the consumer breaks out of the iteration loop, the underlying cursor is closed and any remaining pages are not fetched.
- The async iterable is single-use. Attempting to iterate twice over the same object returns an empty stream.

**Determinism guarantee:**

Replaying the same `builderId`, `from`, `to`, and `order` values at any time produces the identical sequence of events. Event order within a session is guaranteed by monotonic sequence numbers. Between sessions, events are ordered by `timestamp` (primary) and `sequenceNumber` (secondary tiebreaker).

### 3.8 `flush(): Promise<void>`

Force-flushes the observation buffer. All buffered events are immediately written to storage. The Promise resolves when the flush is complete and all events are persisted.

**Use cases:**

- **Before shutdown.** Applications should call `flush()` before exiting to ensure no observations are lost.
- **Before snapshot.** Taking a snapshot after a flush ensures the snapshot reflects a consistent state.
- **Testing.** Test suites should flush before assertions to ensure storage is in a predictable state.
- **Low-memory conditions.** The application can call `flush()` to drain the buffer and free memory.

**Behavioral guarantees:**

- After `flush()` resolves, all events observed before the `flush()` call are persisted.
- If `flush()` is called while a flush is already in progress, the returned Promise resolves when the in-progress flush completes (coalescing behavior).
- If a flush fails (e.g., storage write error), the Promise rejects and the buffer retains the events for the next flush cycle. The caller may retry.
- `flush()` does not prevent new events from being added to the buffer during its execution. Events observed during a flush are included in the next flush cycle.

---

## 4. Batch API

### 4.1 `observeBatch(events: ObservationEvent[]): Promise<ObservationReceipt[]>`

Observes multiple events atomically. All events in a batch share the same session context. This is the preferred method for high-throughput observation scenarios such as bulk state snapshots, session initialization, and migration imports.

```typescript
sdk.observeBatch([
  { type: "mission.completed", ... },
  { type: "competency.leveled_up", ... },
  { type: "achievement.earned", ... }
])
```

**Input:** `ObservationEvent[]` — an array of valid observation events. The array may be empty (returns an empty array of receipts). If any event in the batch is invalid, the invalid event is logged and discarded, but the remaining valid events are still processed.

**Output:** `ObservationReceipt[]` — an array of receipts in the same order as the input events. Each receipt corresponds to the event at the same index. If an event was invalid, its receipt has an empty `id` and `queued: false`.

**Atomicity guarantees:**

- All events in the batch receive consecutive sequence numbers. No event from outside the batch can be interleaved between batch events.
- The batch is written to storage in a single transaction when flushed. Either all events in the batch are persisted, or none are (if the flush fails before committing the transaction).
- The batch semantics apply to the in-memory buffer only. If the system crashes before the buffer is flushed, the entire batch is lost (or saved, depending on flush timing). This is consistent with the fire-and-forget design — durability is a storage concern, not an observation concern.

**Performance characteristics:**

- Batching reduces per-event overhead by amortizing validation, sequencing, and buffer locking across multiple events.
- Recommended batch size: 10–100 events. Larger batches increase latency for the last event in the batch (since sequence numbers are assigned sequentially).
- For batches exceeding the configured `batchSize`, the SDK internally splits the batch into multiple buffer inserts but preserves atomicity at the transaction level.

---

## 5. Query API (Read-Only)

The Query API is a read-only interface. It never mutates observation data. It is the exclusive mechanism for the Cognitive Layer, Experience Layer, and external consumers to retrieve observation data from storage.

### 5.1 `getEvents(builderId: string, filters?: EventFilters): Promise<PaginatedResult<ObservationEvent>>`

Query events by builder, type, time range, session, source, and other filters.

```typescript
interface EventFilters {
  types?: string[]
  from?: string
  to?: string
  sessionId?: string
  source?: string
  limit?: number
  offset?: number
}
```

| Field | Type | Description |
|-------|------|-------------|
| `types` | `string[]` | Filter by one or more event types. Supports partial prefix matching (e.g., `"mission."` matches all mission events). |
| `from` | `string` | ISO 8601 inclusive start of the time range. |
| `to` | `string` | ISO 8601 inclusive end of the time range. |
| `sessionId` | `string` | Filter to a specific session. |
| `source` | `string` | Filter by source (`"runtime"`, `"cognitive"`, `"builder"`, or custom source). |
| `limit` | `number` | Maximum events per page. Default: 50. Maximum: 1000. |
| `offset` | `number` | Pagination offset. Default: 0. |

```typescript
interface PaginatedResult<T> {
  data: T[]
  total: number
  offset: number
  limit: number
  hasMore: boolean
}
```

**Constraints:**

- `builderId` is always required. Cross-builder queries are not supported through this method (privacy boundary).
- Time range filters (`from`, `to`) default to the session's entire time range. If no session is specified, defaults to all time.
- Results are ordered by `timestamp` ascending by default. Use the `order` parameter in `ReplayOptions` (not `EventFilters`) for descending order.
- Pagination is cursor-based in the background but exposed as offset-based for simplicity. The `offset` parameter is the number of events to skip, not the page number.

### 5.2 `getMetrics(builderId: string, metricNames?: string[]): Promise<MetricSnapshot[]>`

Query metric snapshots. Metrics are stored as observation events of type `"metric.recorded"`. This method provides a convenient query interface specifically for metrics, returning them as structured `MetricSnapshot` objects.

```typescript
interface MetricSnapshot {
  metricName: string
  value: number
  metadata?: Record<string, unknown>
  timestamp: string
  sessionId: string
}
```

**Input:**
- `builderId` — the builder whose metrics to query.
- `metricNames` — optional filter to specific metric names. If omitted, all metrics are returned.

**Output:** `MetricSnapshot[]` — an array of metric snapshots ordered by timestamp descending (most recent first).

**Constraints:**
- Returns up to 1000 metric snapshots per call. Use time-range filtering (via `EventFilters` passed to `getEvents()`) for large datasets.
- Metric values are raw — no aggregation or statistical processing is applied by the SDK. Aggregation is the responsibility of the Cognitive Layer.

### 5.3 `getInsights(builderId: string, status?: string): Promise<Insight[]>`

Query insights generated by the Cognitive Layer. Insights are stored as observation events of type `"insight.generated"`. This method provides a dedicated query interface for the Cognitive Layer's primary output.

```typescript
interface Insight {
  id: string
  type: string
  title: string
  description: string
  confidence: number
  status: 'active' | 'dismissed' | 'actioned'
  relatedObservationIds: string[]
  generatedAt: string
}
```

**Input:**
- `builderId` — the builder whose insights to query.
- `status` — optional filter by insight status (`"active"`, `"dismissed"`, `"actioned"`). If omitted, all statuses are returned.

**Output:** `Insight[]` — an array of insights ordered by `generatedAt` descending.

**Constraints:**
- Insights are read-only through the SDK. Status updates (e.g., dismissing an insight) are performed by the Cognitive Layer by emitting a new observation event (`"insight.dismissed"`), not by modifying the insight record.
- The SDK does not validate the insight schema beyond ensuring it conforms to the `ObservationEvent` interface. Semantic validation is the Cognitive Layer's responsibility.

### 5.4 `getRecommendations(builderId: string, status?: string): Promise<Recommendation[]>`

Query recommendations generated by the Cognitive Layer. Recommendations are stored as observation events of type `"recommendation.generated"`.

```typescript
interface Recommendation {
  id: string
  type: string
  title: string
  description: string
  action: string
  priority: 'low' | 'medium' | 'high' | 'critical'
  status: 'active' | 'accepted' | 'rejected' | 'expired'
  relatedInsightIds: string[]
  generatedAt: string
}
```

**Input:**
- `builderId` — the builder whose recommendations to query.
- `status` — optional filter by recommendation status.

**Output:** `Recommendation[]` — an array of recommendations ordered by priority (descending), then by `generatedAt` (descending).

**Constraints:**
- Same immutability constraints as insights. Status changes are emitted as new events, not in-place updates.
- The SDK does not evaluate recommendation priority or expiration. These are Cognitive Layer concerns computed from observation data and stored as event data.

---

## 6. Session API

Sessions are the unit of observation grouping. All observations belong to exactly one session. Sessions provide the context for sequence numbering, checkpoint boundaries, and snapshot triggers.

### 6.1 `startSession(builderId: string, metadata?: Record<string, unknown>): Promise<SessionReceipt>`

Begins a new observation session. This is the first call that must be made before any observation can occur. Until a session is started, `observe()`, `track()`, `measure()`, and `checkpoint()` will no-op (returning empty receipts).

**Input:**
- `builderId` — the builder this session belongs to. A builder may have multiple concurrent sessions (e.g., multiple browser tabs), though this is discouraged.
- `metadata` — optional key-value metadata describing the session context (e.g., `{ version: "1.0", platform: "web", locale: "en-US" }`).

**Output:**

```typescript
interface SessionReceipt {
  sessionId: string
  startedAt: string
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sessionId` | `string` | UUID v4 identifying this session. |
| `startedAt` | `string` | ISO 8601 UTC timestamp of session start. |

**Internal behavior:**
- The SDK emits an internal `"session.started"` observation event.
- Sequence numbers are reset to 1 for the new session.
- The session context is stored in memory and automatically injected into all subsequent observation calls.
- If a session is already active when `startSession` is called, the existing session is ended (as if `endSession` were called) before the new session begins.

### 6.2 `endSession(sessionId: string): Promise<void>`

Ends the current session. This triggers:
1. A forced flush of any buffered events.
2. A full state snapshot.
3. Computation of session summary metrics (event count, type distribution, duration, checkpoint count).
4. Emission of a `"session.ended"` observation event with the session summary.
5. Release of session memory (context, sequence counter, buffer).

**Input:**
- `sessionId` — the ID of the session to end. If the session ID does not match the current active session, the call is a no-op.

**Output:** `Promise<void>` — resolves when the session has been fully ended, flushed, and snapshotted.

**Constraints:**
- After `endSession` resolves, no further observations can be made until `startSession` is called again.
- Calling `endSession` twice with the same session ID is safe (second call is a no-op).
- If the process crashes before `endSession` completes, the session is implicitly ended on the next `startSession` call (stale session detection).

### 6.3 `getSession(sessionId: string): Promise<SessionSummary>`

Returns session metadata and summary metrics for a completed or in-progress session.

```typescript
interface SessionSummary {
  sessionId: string
  builderId: string
  startedAt: string
  endedAt?: string
  eventCount: number
  metricCount: number
  checkpointCount: number
  duration?: number           // seconds, available after end
  typeDistribution: Record<string, number>
  sourceDistribution: Record<string, number>
  metadata?: Record<string, unknown>
}
```

**Input:**
- `sessionId` — the ID of the session to retrieve.

**Output:** `SessionSummary` — session metadata and computed summary. For in-progress sessions, `endedAt` and `duration` are omitted.

**Constraints:**
- Session summaries are computed lazily. For active sessions, the summary reflects the current state. For completed sessions, the summary was computed at session end and stored in the snapshot.
- The summary is generated from observation data, not from a separate session store. This ensures consistency — the session summary is always derivable from the raw events.

---

## 7. Export API

The Export API provides data portability — a core requirement of ASCEND's Local First and data ownership principles. Every builder must be able to export their complete observation history in a standard format.

### 7.1 `exportData(builderId: string, format?: 'json' | 'csv'): Promise<Blob>`

Exports all observations for a builder. The export includes all events, metrics, annotations, checkpoints, snapshots, and session summaries for the builder across all sessions.

**Input:**
- `builderId` — the builder whose data to export.
- `format` — export format:
  - `"json"` (default): A JSON array of observation events. Each event is a complete `ObservationEvent` object. Annotations are included as a nested `annotations` array on each event. Sessions are included as a top-level `sessions` array.
  - `"csv"`: A CSV file with one row per event. Columns include all `ObservationEvent` fields flattened. Annotations and nested objects are JSON-encoded within cells.

**Output:** `Blob` — a blob containing the exported data in the requested format.

**Behavioral guarantees:**
- The export includes all data from session start to the moment of the export call. Events buffered but not yet flushed are included (an implicit flush is performed before export).
- The export is a point-in-time snapshot. Events observed during the export are not included (they belong to a later point in time).
- The export file is self-contained and can be imported into a fresh SDK instance to reconstruct the observation history for that builder.
- Sensitive data is exported as stored. The SDK does not filter, redact, or transform export data. Data minimization and privacy filtering are the responsibility of the calling layer.

### 7.2 `deleteData(builderId: string, options?: DeleteOptions): Promise<void>`

Deletes all observation data for a builder. This is a destructive operation that cannot be undone.

```typescript
interface DeleteOptions {
  confirm: boolean
  exportFirst?: boolean
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `confirm` | `boolean` | — | Must be explicitly `true`. If `false` or omitted, the operation is rejected. |
| `exportFirst` | `boolean` | `false` | If `true`, automatically exports the builder's data before deletion. The export is returned as the resolution value of the Promise (the return type becomes `Promise<Blob>` instead of `Promise<void>`). |

**Input:**
- `builderId` — the builder whose data to delete.
- `options` — deletion options.

**Output:** `Promise<void>` (or `Promise<Blob>` if `exportFirst` is `true`).

**Behavioral guarantees:**
- Deletion is transactional. Either all data for the builder is deleted, or none is.
- Deletion includes all events, metrics, annotations, checkpoints, snapshots, session summaries, and any other observation data for the builder.
- Deletion does not affect data for other builders.
- After deletion, the builder's sequence numbers restart from 1 on the next session.
- The SDK logs the deletion event (builder ID, timestamp, initiator) for audit purposes. This log entry is stored in a separate audit table that is not deleted by `deleteData`.

---

## 8. Configuration API

### 8.1 `configure(options: SDKOptions): void`

Configures the SDK instance. This method may be called at any time during the SDK's lifecycle. Configuration changes take effect immediately for new batches and flushes; in-progress operations use the configuration that was active when they began.

```typescript
interface SDKOptions {
  batchSize?: number
  flushInterval?: number
  storage?: 'auto' | 'sqlite' | 'memory'
  maxBufferSize?: number
  enabled?: boolean
  sampling?: {
    rate?: number
    types?: string[]
  }
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `batchSize` | `number` | `50` | Maximum number of events in a single batch write. Larger batches improve throughput but increase latency. |
| `flushInterval` | `number` | `1000` | Interval in milliseconds between automatic buffer flushes. Set to `0` to disable automatic flushes (manual flush only). |
| `storage` | `'auto' \| 'sqlite' \| 'memory'` | `'auto'` | Storage backend selection. `'auto'` selects SQLite if available, falling back to in-memory storage. `'sqlite'` explicitly selects SQLite (fails if unavailable). `'memory'` uses an in-memory store (data is lost on process exit). |
| `maxBufferSize` | `number` | `10000` | Maximum number of events in the in-memory buffer. When exceeded, the oldest events are dropped (ring buffer behavior). |
| `enabled` | `boolean` | `true` | Master switch. When `false`, all observation methods become no-ops. Useful for testing and for disabling observation in resource-constrained environments. |
| `sampling.rate` | `number` | `1.0` | Sampling rate between `0.0` (no events sampled) and `1.0` (all events sampled). Events not selected by the sampling algorithm are silently dropped. |
| `sampling.types` | `string[]` | All types | When specified, sampling is only applied to events of the specified types. Events of other types are always observed. |

**Configuration examples:**

```typescript
// Default configuration (no call needed)
sdk.configure({})

// High-throughput configuration
sdk.configure({
  batchSize: 200,
  flushInterval: 500,
  maxBufferSize: 50000
})

// Memory-constrained environment
sdk.configure({
  batchSize: 10,
  flushInterval: 5000,
  maxBufferSize: 1000
})

// Testing configuration (disabled observation)
sdk.configure({
  enabled: false,
  storage: 'memory'
})

// Sampling configuration (50% of metric events only)
sdk.configure({
  sampling: {
    rate: 0.5,
    types: ['metric.recorded']
  }
})
```

**Constraints:**
- Calling `configure()` does not reset the SDK. Active sessions, buffered events, and storage connections are preserved unless the `storage` option changes (in which case a migration may occur — see section 8.2).
- Invalid option values are silently clamped to valid ranges (e.g., `sampling.rate` is clamped to `[0.0, 1.0]`).
- Configuration changes are not persisted. On process restart, the SDK uses defaults until `configure()` is called.

### 8.2 Runtime Configuration

Some configuration options are read-only after SDK initialization:

| Option | Settable After Init | Notes |
|--------|---------------------|-------|
| `batchSize` | Yes | Affects next batch. |
| `flushInterval` | Yes | Affects next flush cycle. |
| `storage` | No | Must be set before first `startSession()`. Changes require re-initialization. |
| `maxBufferSize` | Yes | Affects buffer immediately. |
| `enabled` | Yes | Affects next observation call. |
| `sampling` | Yes | Affects next observation call. |

---

## 9. Error Handling

### 9.1 Queue Full (Ring Buffer Behavior)

When the in-memory buffer reaches `maxBufferSize`, the SDK drops the oldest events to make room for new ones. This is ring buffer behavior — the buffer is a fixed-size circular queue.

- **Detection:** The SDK logs a warning with the count of dropped events and the sequence number range of dropped events.
- **Impact:** The oldest events are lost. Sequence numbers are preserved for the remaining events, creating a gap in the sequence number space.
- **Mitigation:** Increase `maxBufferSize`, reduce `flushInterval`, or increase `batchSize` to drain the buffer faster. Alternatively, reduce observation volume through sampling.
- **Auditability:** The SDK records a `"buffer.overflow"` observation event with the dropped sequence range, ensuring that data loss is itself observable.

### 9.2 Storage Failure

If the storage backend fails (e.g., SQLite disk full, write permission denied, connection lost), the SDK continues to buffer events in memory and retries the flush on the next cycle.

- **Retry strategy:** Exponential backoff (1s, 2s, 4s, 8s, max 60s) with a maximum of 5 retries per flush. After 5 failed retries, the buffer is held until the next flush interval.
- **Persistence:** If the process exits before storage recovers, buffered events are lost. The SDK logs a critical error in this case.
- **Recovery:** When storage recovers, the buffer drains normally. No events are lost beyond those in the failed flush attempt (which remain in the buffer).
- **Monitoring:** Applications can listen for storage failure events through an optional event emitter (not part of this spec — see implementation notes).

### 9.3 Invalid Events

When an event fails validation, the SDK logs the validation error and returns an empty receipt. Valid events in the same batch are still processed.

- **Validation failures:** Missing required fields, invalid format (type pattern, UUID pattern, ISO timestamp), non-finite metric values, empty builder ID.
- **Logging:** Each validation failure is logged with the event ID (if available), the validation error, and a stack trace for debugging.
- **No cascading failure:** An invalid event does not affect other events in the same batch or buffer.
- **No retry:** Invalid events are discarded permanently. The producer is responsible for correcting and re-observing.

### 9.4 SDK Disabled

When `enabled` is `false`, all observation methods become no-ops:

- `observe()` returns a receipt with `id: ""`, `sequenceNumber: 0`, `timestamp: ""`, `queued: false`.
- `track()` returns the same no-op receipt.
- `measure()` resolves immediately.
- `checkpoint()` returns an empty receipt.
- `snapshot()` returns an empty receipt.
- `annotate()` resolves immediately.
- `observeBatch()` returns an array of no-op receipts.
- Session API methods (`startSession`, `endSession`, `getSession`) still function for session lifecycle management but no events are recorded.
- Query API methods still function (reading previously stored data).
- Export and delete methods still function.
- `flush()` resolves immediately (no buffer to flush).

This enables the Experience Layer to conditionally disable observation based on user consent, resource constraints, or testing requirements.

---

## 10. Determinism Guarantees

Determinism in the Observation SDK is a first-class property, not an incidental behavior. The following guarantees define what consumers can rely on.

### 10.1 Observation Order

Events observed in order are stored in order. If two calls to `observe()` are made sequentially (not concurrently), their sequence numbers are consecutive and their storage order matches their observation order.

For concurrent calls (e.g., two `observe()` calls made simultaneously from different threads or event loop ticks), the SDK guarantees that:
- Sequence numbers are assigned in the order the SDK processes the calls.
- Storage order matches sequence number order.
- No event is stored before an earlier-sequence-numbered event from the same session.

### 10.2 Sequence Number Monotonicity

Within a session, sequence numbers are:
- **Monotonic:** Each event receives a sequence number greater than all previous events.
- **Gap-free:** Sequence numbers increment by exactly 1 for each event. There are no skipped sequence numbers except when the ring buffer drops events (section 9.1), in which case the gap is documented in a buffer overflow event.
- **Per-session:** Sequence numbers restart at 1 for each new session. They are not globally unique — the combination of `sessionId` and `sequenceNumber` is unique.

### 10.3 Replay Determinism

Replaying the same sequence (same `builderId`, session range, `from`, `to`, `order`) at any time produces:
- The identical set of events.
- Events in the identical order.
- Events with the identical field values (no transformed data, no enriched fields).

This holds true regardless of:
- Number of times replayed.
- State of the SDK at replay time.
- Configuration changes between observations and replay.
- Storage backend in use.

### 10.4 Immutability

No event is ever modified after storage. Annotations are stored separately and do not modify the original event. There is no `updateEvent`, `deleteEvent`, or `patchEvent` method. The only deletion mechanism is `deleteData()`, which removes all data for a builder.

### 10.5 Non-Deterministic Behaviors (Documented)

The following are intentionally non-deterministic and must not be relied upon:
- **Flush timing:** When buffered events are flushed to storage depends on buffer fill level, flush interval, and system load.
- **Ring buffer drops:** Which events are dropped when the buffer overflows depends on the order and timing of observations.
- **Error timing:** When a storage failure occurs and how long recovery takes is environment-dependent.

---

## 11. No-Dependency Guarantee

The Observation SDK has zero external dependencies. It depends on:

- **No network calls.** The SDK never initiates HTTP requests, WebSocket connections, or any form of network communication. All storage is local.
- **No AI models.** The SDK does not load, invoke, or depend on any machine learning model, inference engine, or AI service.
- **No cloud services.** The SDK does not authenticate with, upload to, or depend on any cloud platform, SaaS provider, or remote API.
- **No vendor SDKs.** The SDK does not import, wrap, or depend on any third-party SDK (Segment, PostHog, Amplitude, Sentry, DataDog, etc.).
- **No system dependencies.** The SDK depends only on the language runtime's standard library and, optionally, a SQLite binding for persistent storage. Even SQLite is optional — the SDK functions in pure in-memory mode.

This guarantee is rooted in ASCEND's First Principles:
- **Local First:** Data belongs to the user and must never leave their device without explicit consent.
- **No Vendor Lock-In:** The SDK must never create a dependency on a third-party service that could change pricing, terms, or availability.
- **Offline-First:** The SDK must function identically whether the device is online or offline.
- **AI as a Layer:** AI is an optional enhancement, not a core dependency. The SDK works without it.

---

## 12. SDK Lifecycle

### 12.1 Initialization

1. `configure()` is called (optional — defaults are used if omitted).
2. The SDK initializes the storage backend based on the `storage` option.
3. The SDK starts the background flush timer.
4. The SDK is ready for use.

### 12.2 Active

1. `startSession()` is called to begin a new observation session.
2. Observation methods (`observe`, `track`, `measure`, `checkpoint`) are called.
3. The background flush timer periodically drains the buffer.
4. `snapshot()` may be called at any time.
5. `endSession()` ends the session and triggers a final flush and snapshot.

### 12.3 Query

Query API methods may be called at any time, regardless of whether a session is active. They are independent of the observation lifecycle.

### 12.4 Shutdown

1. `flush()` is called to drain any remaining buffered events.
2. The current session is ended (if any).
3. The background flush timer is stopped.
4. The storage backend is closed.
5. SDK resources are released.

---

## 13. Thread Safety

The SDK is designed for single-threaded environments (JavaScript, Python asyncio) but must also function correctly in multi-threaded environments (Python threading, Java).

- All public methods are thread-safe. Multiple threads may call any method concurrently.
- Sequence number assignment is atomic (protected by a mutex/lock).
- Buffer insertion is atomic.
- Flush operations are serialized (only one flush executes at a time; concurrent flush calls are coalesced).
- Configuration changes are atomic (a `configure()` call while observations are in flight will not corrupt state).

In single-threaded environments (JavaScript, Python asyncio), the SDK relies on the event loop for concurrency safety. In multi-threaded environments, it uses a reentrant lock to protect critical sections.

---

## 14. Integration Patterns

### 14.1 Runtime Integration

The Runtime Layer uses the SDK to observe domain events:

```typescript
// Inside the Runtime's event handler
sdk.observe({
  id: uuid(),
  type: "mission.completed",
  source: "runtime",
  timestamp: now(),
  data: { missionId, score, xpGained, completionTime },
  context: { builderId, sessionId, missionId }
})
```

The Runtime does not call `track()` or `measure()` directly — it uses `observe()` with explicit event construction. This preserves the full expressiveness of the domain model.

### 14.2 Experience Layer Integration

The Experience Layer uses `track()` for UI interactions and `measure()` for performance metrics:

```typescript
// User clicked a button
sdk.track("ui.mission.start.clicked", { missionId })

// Page load time
sdk.measure("page_load_ms", performance.now(), { page: "/missions" })

// Session start
sdk.startSession(builderId, { platform: "web", version: "1.0" })
```

### 14.3 Cognitive Layer Integration

The Cognitive Layer uses the Query API to consume observations and the observation methods to emit its outputs:

```typescript
// Consume observations
for await (const event of sdk.replay(builderId, { from: sessionStart, types: ["mission.completed"] })) {
  // Detect patterns, compute insights
}

// Emit insight
sdk.observe({
  id: uuid(),
  type: "insight.generated",
  source: "cognitive",
  timestamp: now(),
  data: { insightId, title, description, confidence, relatedEvents },
  context: { builderId, sessionId }
})

// Annotate source event
sdk.annotate(event.id, {
  key: "cognitive.insight_id",
  value: insightId,
  timestamp: now()
})
```

---

## 15. Versioning

The Observation SDK follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes to the public API (method signature changes, removed methods, changed behavior contracts).
- **MINOR:** Additions to the public API (new methods, new options, new event types).
- **PATCH:** Internal changes, bug fixes, performance improvements, documentation.

The `metadata.observationSchema` field in each observation event records the SDK version that produced it. This enables consumers to handle schema evolution across SDK versions.

---

## 16. Related Documents

| Document | Relation |
|----------|----------|
| ARCH-0030 Cognitive Architecture | Defines the cognitive pipeline that consumes observations |
| ARCH-0031 Observation Model | Defines the Observation data type and lifecycle |
| ARCH-0032 Event Taxonomy | Defines the canonical event types and their payloads |
| ARCH-0033 Signal Processing | Defines how signals are extracted from observations |
| ARCH-0034 Pattern Detection | Defines how patterns are detected from signals |
| ARCH-0035 Insight Engine | Defines how insights are generated from patterns |
| ARCH-0016 Frontend SDK | Defines the frontend SDK that may consume this API |
| ARCH-0025 SDK Lifecycle | Defines the lifecycle contract for all SDKs |
