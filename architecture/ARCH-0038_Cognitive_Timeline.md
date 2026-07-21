# ARCH-0038 — Cognitive Timeline

| Field | Value |
|-------|-------|
| **ID** | ARCH-0038 |
| **Name** | Cognitive Timeline |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, ARCH-0030 Cognitive Architecture, ARCH-0031 Observation Model, ARCH-0005 Data Model Specification |
| **Principle** | Every session is replayable. Every event has a timestamp. Any past can be reconstructed. |

---

## 1. Purpose

Every learning session is a sequence of events unfolding in time. A builder starts a mission, enters focus mode, submits evidence, unlocks a competency, reflects — each action follows the last in a causal chain. The Cognitive Timeline is the canonical representation of this chain. It defines how events are ordered, how time is measured, and how the past can be faithfully reconstructed.

Without a formal timeline, the system has no sense of *when* things happened. It cannot distinguish between a builder who completed a mission in thirty seconds and one who took thirty minutes. It cannot detect pauses, measure pacing, or replay a session for audit. The timeline provides this temporal dimension.

The timeline is **derived**, not stored. It is computed from the `observations` table by querying events ordered by sequence number for a given builder and session. This ensures consistency: the timeline is always an exact projection of what was observed, never an independent record that could drift out of sync.

> **Core Principle:** Time is not metadata. Time is structure. Every insight, every recommendation, every metric must be traceable to a position on the timeline.

---

## 2. The Timeline Concept

A timeline is an ordered sequence of observations. Each entry in the sequence carries enough information to reconstruct the moment it represents — what happened, when it happened, how long after the previous event it happened, and which session it belongs to.

### 2.1 Timeline Entry

```typescript
interface TimelineEntry {
  sequenceNumber: number
  observationId: string
  timestamp: string            // ISO 8601, UTC
  delta: number                // milliseconds since previous event
  sessionId: string
  type: string
  label: string                // human-readable summary
}
```

| Field | Description |
|-------|-------------|
| `sequenceNumber` | Monotonically increasing integer. Establishes global order. No gaps. |
| `observationId` | Foreign key to the `observations` table. Links timeline entry to raw observation data. |
| `timestamp` | Wall-clock time when the event occurred. ISO 8601 in UTC. Immutable after capture. |
| `delta` | Milliseconds elapsed since the previous entry in the timeline. Zero for the first entry. Enables pacing analysis without recomputation. |
| `sessionId` | The session this event belongs to. All events in one timeline share the same session ID. |
| `type` | Event type string (e.g., `behavior.mission.started`, `focus.mode.entered`). Used for filtering. |
| `label` | Short human-readable summary. Suitable for CLI display, log output, and UI tooltips. |

### 2.2 Timeline Properties

- **Ordered:** Entries are sorted by `sequenceNumber` ascending. Within event bursts that share the same sequence number (rare), `timestamp` ascending serves as a tiebreaker.
- **Immutable:** Once appended, an entry is never modified. The timeline is append-only.
- **Deterministic:** Given the same ordered observations, reconstruction always produces the identical timeline.
- **Continuous:** Every event is accounted for. There are no gaps in the sequence number space.
- **Derived:** The timeline is never stored as a separate table. It is computed on demand from observations.

### 2.3 Relationship to Observations

Each timeline entry corresponds to exactly one observation. The observation carries the full payload — the raw data, the state snapshot, the metadata. The timeline entry carries the temporal context — the position, the delta, the label. Together, they provide the complete picture: *what* happened and *when*.

---

## 3. Example Timeline Flow

The following example shows a typical mission session rendered as a timeline. Each line shows the offset from session start (`T+0s`), the event type, and a human-readable label.

```
Mission 'variables-101'
  │
  ├── [T+0s]    behavior.mission.started         → Reading briefing
  ├── [T+15s]   focus.mode.entered               → Entered Focus Mode
  ├── [T+45s]   interaction.help.requested        → Opened help
  ├── [T+120s]  behavior.evidence.submitted       → Submitted evidence
  ├── [T+121s]  focus.mode.exited                 → Exited Focus Mode
  ├── [T+125s]  behavior.mission.completed        → Mission completed
  ├── [T+126s]  learning.competency.unlocked      → Competency unlocked!
  ├── [T+130s]  reflection.assessment.completed   → Self-assessment
  └── [T+135s]  reflection.note.created           → Reflection note
```

This example illustrates several timeline features:

- **Session start** (`T+0s`) is always the first event. It anchors the timeline.
- **Deltas vary** — some events are seconds apart (`focus.exited` to `evidence.submitted`), others have wider spacing (the help interaction took 30 seconds).
- **Event types** categorize the action: `behavior.*` for mission actions, `focus.*` for attention state, `interaction.*` for system use, `learning.*` for outcomes, `reflection.*` for meta-cognition.
- **The label** provides context without requiring the reader to open the raw observation payload.

---

## 4. Session Definition

A session is a contiguous span of builder activity. It has a start time, an end time, and a collection of events that occurred within it. The session aggregates timeline data into summary metrics.

```typescript
interface CognitiveSession {
  id: string
  builderId: string
  startedAt: string             // ISO 8601, UTC
  endedAt?: string              // ISO 8601, UTC; absent if session is active
  duration: number              // seconds (endedAt - startedAt)
  eventCount: number            // total timeline entries
  focusTime: number             // seconds spent in Focus Mode
  missionsStarted: number
  missionsCompleted: number
  competenciesUnlocked: number
  achievementsEarned: number
  timeline: TimelineEntry[]
  summary: {
    focusScore: number           // 0.0 – 1.0, focusTime / duration
    learningVelocity: number     // competenciesUnlocked / duration (hours)
    persistenceIndex: number     // missionsCompleted / missionsStarted
  }
}
```

### 4.1 Session Boundaries

A session begins when the first observation is captured for a given builder-scope combination. It ends when:

- The builder explicitly ends the session (via CLI or API).
- A macro-gap is detected (see Section 10 — Gap Detection).
- The builder closes the application.

The session is the atomic unit of replay. Every replay request targets a single session.

### 4.2 Session Summary Metrics

Three summary metrics are computed from the timeline:

| Metric | Formula | Meaning |
|--------|---------|---------|
| **Focus Score** | `focusTime / duration` | Proportion of session time spent in Focus Mode. Higher values indicate deeper engagement. |
| **Learning Velocity** | `competenciesUnlocked / (duration / 3600)` | Competencies unlocked per hour of session time. Measures rate of demonstrated growth. |
| **Persistence Index** | `missionsCompleted / missionsStarted` | Ratio of completed to started missions. Values near 1.0 indicate high follow-through. |

These metrics are computed from timeline events alone. They require no additional data sources.

---

## 5. Timeline Operations

The timeline supports a set of formal operations. Each operation is deterministic — given the same inputs, it always produces the same outputs.

### 5.1 Append

Appends an event to the end of the timeline. Computes the delta from the previous event automatically.

```
function append(
  observation: Observation,
  sessionId: string
): TimelineEntry

  let lastEntry = getLastEntry(sessionId)
  let delta = lastEntry
    ? observation.timestamp - lastEntry.timestamp
    : 0
  let entry = {
    sequenceNumber: lastEntry
      ? lastEntry.sequenceNumber + 1
      : 1,
    observationId: observation.id,
    timestamp: observation.timestamp,
    delta: delta,
    sessionId: sessionId,
    type: observation.type,
    label: generateLabel(observation)
  }
  store(entry)
  return entry
```

**Rules:**
- Sequence numbers are assigned monotonically. No gaps.
- The delta is computed from the wall-clock timestamps of consecutive entries.
- The first entry of a session always has `delta = 0`.
- Append is the only write operation. There is no insert, update, or delete.

### 5.2 Query by Time

Returns all entries within a time window, inclusive of both bounds.

```
function getTimeRange(
  from: string,    // ISO 8601
  to: string       // ISO 8601
): TimelineEntry[]

  return observations
    .where(o => o.timestamp >= from
             && o.timestamp <= to
             && o.sessionId != null)
    .orderBy(o => o.sequenceNumber)
    .map(toTimelineEntry)
```

**Use cases:**
- "What happened in the last five minutes?"
- "Show me activity between 14:00 and 15:00 yesterday."
- "Extract the events surrounding a specific incident."

### 5.3 Query by Type

Returns all entries matching a given event type. Supports prefix matching for hierarchical types.

```
function getEventsByType(
  type: string    // exact or prefix (e.g., "behavior.mission.*")
): TimelineEntry[]

  return observations
    .where(o => o.type matches type)
    .orderBy(o => o.sequenceNumber)
    .map(toTimelineEntry)
```

**Use cases:**
- "Show all help requests during this session."
- "List all evidence submissions."
- "Extract every focus mode transition."

### 5.4 Query by Session

Returns the complete timeline for a single session, ordered by sequence number.

```
function getSessionTimeline(
  sessionId: string
): TimelineEntry[]

  return observations
    .where(o => o.sessionId == sessionId)
    .orderBy(o => o.sequenceNumber)
    .map(toTimelineEntry)
```

**Use cases:**
- Replay a session.
- Export a session for audit.
- Compute session summary metrics.

### 5.5 Slice

Returns a contiguous subsequence of the timeline by sequence number range.

```
function slice(
  sequenceStart: number,
  sequenceEnd: number
): TimelineEntry[]

  return observations
    .where(o => o.sequenceNumber >= sequenceStart
             && o.sequenceNumber <= sequenceEnd)
    .orderBy(o => o.sequenceNumber)
    .map(toTimelineEntry)
```

**Use cases:**
- Paginate a long timeline.
- Extract a specific segment for analysis.
- Isolate events around a known sequence number.

### 5.6 Diff

Compares two timelines and returns the differences. Useful for comparing replays, before/after states, or expected vs. actual timelines.

```
function diff(
  timelineA: TimelineEntry[],
  timelineB: TimelineEntry[]
): TimelineDiff

  let diff = {
    added: [] as TimelineEntry[],
    removed: [] as TimelineEntry[],
    changed: [] as TimelineChange[],
    same: [] as [TimelineEntry, TimelineEntry][]
  }

  let bySeqA = groupBySeqNumber(timelineA)
  let bySeqB = groupBySeqNumber(timelineB)

  for seq in union(keys(bySeqA), keys(bySeqB)):
    if seq not in bySeqA:
      diff.added.push(bySeqB[seq])
    else if seq not in bySeqB:
      diff.removed.push(bySeqA[seq])
    else if bySeqA[seq].observationId
          != bySeqB[seq].observationId:
      diff.changed.push({
        sequenceNumber: seq,
        old: bySeqA[seq],
        new: bySeqB[seq]
      })
    else:
      diff.same.push([bySeqA[seq], bySeqB[seq]])

  return diff
```

**Use cases:**
- Verify that a replay produced the same timeline as the original session.
- Compare two sessions from the same builder to identify behavioral changes.
- Validate that a software update did not alter timeline computation.

---

## 6. Timeline Storage

Timelines are not stored as separate entities. They are **derived** from the `observations` table. The timeline is computed by querying observations ordered by `sequence_number` for a given `builder_id` and `session_id`.

### 6.1 Why Derived?

| Approach | Drawback |
|----------|----------|
| Separate timeline table | Redundant data, synchronization risk, dual-write complexity |
| Timeline as a materialized view | Stale data, maintenance burden |
| Derived from observations | Single source of truth, always consistent, no sync needed |

### 6.2 Implications

- **No redundant storage.** The timeline adds zero bytes to the database. It is a query, not a table.
- **Always consistent.** Because the timeline is computed from the same observations that drive every other system, it can never diverge. If the observation exists, the timeline entry exists.
- **Replay is trivial.** Loading the timeline for replay is a simple ordered query. No joins, no materialization, no caching invalidation.
- **Performance is bounded.** Timeline queries filter by `builder_id` and `session_id`, both of which are indexed. For sessions with very large event counts (thousands), pagination via `slice` is available.

### 6.3 Indexing Strategy

The `observations` table must have the following composite indexes to support efficient timeline queries:

```
INDEX idx_timeline_session
  ON observations (builder_id, session_id, sequence_number ASC)

INDEX idx_timeline_time
  ON observations (builder_id, timestamp, sequence_number ASC)

INDEX idx_timeline_type
  ON observations (builder_id, session_id, type, sequence_number ASC)
```

These indexes cover the three primary query patterns: by session (replay), by time (range queries), and by type (filtered queries).

---

## 7. Replay

Replay reconstructs a builder's session from stored observations. It is the defining capability of the timeline — the guarantee that any past session can be faithfully reconstructed.

### 7.1 Replay Algorithm

```
1. Load all observations for builder + session,
   ordered by sequence_number ASC
2. Load the closest snapshot before the session
   (for initial state)
3. Rebuild state by applying each observation
   in order:
     a. Load observation payload
     b. Apply to current state
     c. Record resulting state at this frame
     d. Compute metrics at this frame
4. Return the frame-by-frame reconstruction
```

**Step 2** (snapshot loading) is an optimization. Without it, replay would need to replay every observation since the builder's creation. The snapshot closest to (but before) the session start provides the initial state, and only observations within the session need to be replayed.

### 7.2 Replay Output

The output of a replay is a sequence of frames:

```typescript
interface ReplayFrame {
  sequenceNumber: number
  timestamp: string
  type: string
  delta: number
  stateBefore: object    // state snapshot before applying event
  stateAfter: object     // state snapshot after applying event
  metrics: {
    xp: number
    level: number
    competencies: number
    focusScore: number
  }
}
```

Each frame captures the system state immediately before and after the event, plus the metrics at that point in time. This enables frame-by-frame stepping through the session.

### 7.3 Use Cases for Replay

**Debugging the Cognitive Layer.**
Did the insight fire at the right time? By replaying the session, a developer can step through each event, inspect the state at each frame, and verify that cognitive signals were emitted at the correct moments.

**Audit Trail.**
What did the builder see and when? Replay provides an exact reconstruction of the builder's session, including every event they triggered and every system response. This is essential for compliance, dispute resolution, and transparency.

**Testing.**
Replay a known session to verify that metric computation produces the expected values. Regression tests can include a library of recorded sessions that are replayed after every change to the cognitive layer.

**Research.**
With builder consent, anonymized sessions can be replayed to study learning patterns. Researchers can examine how different builders approach the same mission, where they get stuck, and what interventions are most effective.

### 7.4 Determinism Guarantee

Replay is deterministic if and only if the observations are unchanged. The system guarantees:

- **Monotonic sequence numbers:** No gaps, no reordering. Sequence numbers increase monotonically within a session.
- **Immutable events:** Once an observation is stored, it is never modified. Update and delete are prohibited.
- **Deterministic sort order:** Primary sort by `sequence_number ASC`, tiebreaker by `timestamp ASC`.

Given these guarantees, replay always produces the identical sequence of frames for the same session.

---

## 8. Delta Computation

The delta between consecutive events is the fundamental unit of temporal analysis.

### 8.1 Definition

```
delta_i = timestamp_i - timestamp_{i-1}
```

Where `timestamp_i` and `timestamp_{i-1}` are wall-clock times in milliseconds since Unix epoch. The first event in any session has `delta_1 = 0`.

### 8.2 What Deltas Enable

**Detection of Pauses.**
A large delta indicates that the builder stopped interacting. This could mean they are thinking, they were distracted, or they left the application. The system can use delta thresholds to classify pauses (see Section 10 — Gap Detection).

**Session Pacing.**
The distribution of deltas reveals the rhythm of the session. A session with many small deltas (sub-second) suggests rapid, fluent action. A session with mixed deltas (short bursts separated by longer pauses) suggests a more reflective, stop-and-think pattern.

**Rapid Action Sequences.**
Consecutive events with very small deltas (milliseconds) indicate automation or macro-triggered actions. For example, a builder who completes a mission, unlocks a competency, and earns an achievement in under two seconds likely triggered a chain reaction. These sequences are candidates for special handling in the cognitive layer.

### 8.3 Delta Storage

Deltas are computed at append time and stored as part of the `TimelineEntry`. This avoids recomputation during queries and ensures consistent values across all consumers.

---

## 9. Timeline Visualization

The CLI provides a compact, readable format for timeline inspection. The goal is to convey the full temporal shape of a session at a glance.

### 9.1 CLI Format

```
SESSION  abc123  |  2026-07-20T14:30:00Z  |  5m 12s  |  23 events
─────────────────────────────────────────────────────
  #1  +0.0s     mission.started          │ variables-101
  #2  +2.3s     focus.entered            │ Focus Mode ON
  #3  +12.1s    help.requested           │ "What is a variable?"
  #4  +45.0s    evidence.submitted       │ Evidence #1
  #5  +0.8s     mission.completed        │ Score: 85
  #6  +0.5s     competency.unlocked      │ "Python Basics" Lv.1
  #7  +5.2s     reflection.done          │ "I learned about types"
```

### 9.2 Header Line

The header shows:
- **Session ID:** `abc123` — truncated for display; full ID available on request.
- **Start time:** `2026-07-20T14:30:00Z` — ISO 8601 in UTC.
- **Duration:** `5m 12s` — wall-clock duration of the session.
- **Event count:** `23 events` — total timeline entries.

### 9.3 Event Lines

Each event line shows:
- **Position:** `#1`, `#2`, etc. — the sequence number.
- **Offset:** `+0.0s`, `+2.3s`, etc. — time since the previous event.
- **Type:** `mission.started`, `focus.entered`, etc. — the event type.
- **Label:** Everything after the `│` — the human-readable summary.

### 9.4 Visual Encoding

- Offsets are color-coded in terminal output: green for sub-second, yellow for 1–30 seconds, red for >30 seconds.
- Event types are grouped by prefix: `behavior.*` in one hue, `focus.*` in another, `reflection.*` in a third.
- Gaps are visually represented by a blank line and a `…` marker when the delta exceeds a configurable threshold.

---

## 10. Gap Detection

The timeline enables systematic gap analysis. Gaps are periods where no events were recorded. They are classified by duration into three categories.

### 10.1 Gap Classification

| Category | Duration | Interpretation |
|----------|----------|----------------|
| **Micro-gap** | 30s < delta < 5min | Possible hesitation. The builder may be thinking, reading, or stuck. |
| **Meso-gap** | 5min < delta < 30min | Break or distraction. The builder likely stepped away or switched contexts. |
| **Macro-gap** | delta > 30min | Session boundary. The builder has likely ended the session. |

### 10.2 Micro-gap

A micro-gap indicates a pause within the flow of activity. The builder is still present but not generating events. Possible causes:

- Reading mission instructions.
- Composing a reflection note.
- Solving a problem in an external environment (e.g., writing code in an IDE).
- Experiencing confusion or uncertainty.

**System response:** The cognitive layer may flag micro-gaps as potential friction points. If micro-gaps cluster around a specific mission or concept, that area is a candidate for content improvement.

### 10.3 Meso-gap

A meso-gap indicates the builder has disengaged from the session. They may have:

- Switched to another application.
- Taken a break.
- Been interrupted.

**System response:** The session remains open. If activity resumes, the timeline continues. If the session is queried while a meso-gap is active, the system reports the session as "paused."

### 10.4 Macro-gap

A macro-gap indicates a session boundary. The builder is unlikely to return. The session is automatically closed and a new session will be created when activity resumes.

**System response:**
- The session is marked as ended.
- Summary metrics are finalized.
- A new session will be created on the next observed event.

### 10.5 Gap Detection Configuration

Gap thresholds are configurable per deployment:

```
gap:
  micro:
    min: 30000       # 30 seconds
    max: 300000      # 5 minutes
  meso:
    min: 300000      # 5 minutes
    max: 1800000     # 30 minutes
  macro:
    min: 1800000     # 30 minutes
```

These values can be overridden via environment variables or configuration files. The defaults are chosen for general-purpose learning sessions.

---

## 11. Timeline Compression

For storage efficiency and query performance, the timeline supports optional compression. Compression is lossy (some events are removed or aggregated) and is used only for long-term storage or export. The canonical timeline, derived directly from observations, is never compressed.

### 11.1 Compressible Event Types

Some event types are high-volume but low-value for replay. These can be removed during compression:

| Event Type | Compressible? | Rationale |
|------------|---------------|-----------|
| `navigation.*` | Yes | High volume, low semantic value. Click paths are rarely needed for replay. |
| `ui.*` | Yes | UI interactions (scroll, hover, resize) are voluminous and rarely useful. |
| `heartbeat.*` | Yes | Periodic heartbeats are implicit in the timeline structure. |
| `behavior.*` | No | Core learning events must be preserved. |
| `focus.*` | No | Attention state transitions are critical for metrics. |
| `learning.*` | No | Competency and achievement events define progress. |
| `reflection.*` | No | Meta-cognitive events are essential for insight generation. |
| `interaction.*` | Maybe | Help requests and system interactions may or may not be relevant depending on the use case. |

### 11.2 Compression Strategies

**Filter compression.** Remove all events matching a list of compressible types. The resulting timeline contains only core events.

**Aggregation compression.** Consecutive events of the same type within a short time window (e.g., multiple `navigation.*` events within 1 second) are aggregated into a single entry with a count.

```
Before:  navigation.page.view   → 3 events in 1.2s
After:   navigation.page.view   × 3  [aggregated]
```

**Delta-only compression.** For bandwidth-constrained exports, the timeline can be stored as a sequence of deltas and types only, omitting absolute timestamps and labels. The absolute time can be reconstructed from the session start time.

### 11.3 When to Compress

- **Long-term archival:** Sessions older than 90 days may be compressed to save storage.
- **Export:** When exporting a session for external analysis, compression reduces file size.
- **Bandwidth-constrained environments:** Mobile or low-bandwidth clients may request compressed timelines.

---

## 12. Determinism Guarantee

The timeline is deterministic by construction. Given the same ordered sequence of observations, the timeline is identical on every reconstruction. This guarantee rests on three invariants.

### 12.1 Monotonic Sequence Numbers

Sequence numbers are assigned in strictly increasing order within a session. There are no gaps. If a session produces twenty events, the sequence numbers are 1 through 20.

**Why this matters:** Gaps in sequence numbers would introduce ambiguity. Does sequence 5 followed by sequence 7 mean an event was deleted? Or was sequence 6 never written? Monotonic, gapless sequence numbers eliminate this ambiguity.

### 12.2 Immutable Events

Once an observation is stored, it is never modified. The `observations` table is append-only. Update and delete operations are prohibited at the database level.

**Why this matters:** If observations could be modified after storage, replay would become non-deterministic. The same session could produce different timelines on different days. Immutability guarantees that the past is fixed.

### 12.3 Deterministic Sort Order

The sort order for timeline reconstruction is:

1. Primary: `sequence_number ASC`
2. Tiebreaker: `timestamp ASC`

**Why this matters:** In rare cases (event bursts, clock skew within a single process), two events may share the same sequence number. The timestamp tiebreaker ensures that the order is still deterministic. The `ASC` direction on both fields ensures that the order matches the chronological flow.

### 12.4 Proof of Determinism

Given:
- A set of observations O, each with a unique `(sequence_number, timestamp)` pair.
- A query Q that returns O ordered by `(sequence_number ASC, timestamp ASC)`.
- A mapping M that converts each observation to a `TimelineEntry`.

The timeline T = M(Q(O)) is deterministic because:
- Q(O) always returns the same order for the same O (deterministic sort).
- M is a pure function (same input always produces same output).
- O is immutable (same set always, no insertions or deletions after storage).

Therefore, T is identical on every reconstruction. Q.E.D.

---

## 13. Timeline as a First-Class Artifact

While the timeline is derived, it is treated as a first-class artifact in the system. This means:

- **First-class in documentation.** The timeline format, operations, and guarantees are specified here, in an architecture document, not buried in code comments.
- **First-class in testing.** The timeline operations (append, query, slice, diff) have dedicated test suites. Replay tests verify determinism.
- **First-class in the API.** The timeline can be queried, sliced, and exported via the public API. External tools can consume timeline data.
- **First-class in the CLI.** The `ascend timeline` command provides direct access to timeline inspection, replay, and export.

### 13.1 CLI Commands

```
ascend timeline list          # List sessions for the current builder
ascend timeline show <id>     # Display a session's timeline
ascend timeline replay <id>   # Step through a session frame by frame
ascend timeline export <id>   # Export timeline as JSON or CSV
ascend timeline diff <a> <b>  # Compare two timelines
```

These commands make the timeline an interactive tool for developers, auditors, and researchers, not just an internal data structure.

---

## 14. Relationship to the Cognitive Cycle

The timeline sits at the boundary between Observation and Signal in the Cognitive Cycle (defined in ARCH-0030 and ARCH-0031).

```
Observation
  │
  ▼
Timeline ←─── orders events, computes deltas
  │
  ▼
Signal
  │
  ▼
Pattern → Insight → Recommendation → Decision
```

- **Observation** produces raw events. The timeline orders them.
- **Signal** extraction queries the timeline for temporal context (e.g., "was this event preceded by a micro-gap?").
- **Pattern** detection uses timeline-derived metrics (e.g., focus score trend, learning velocity).
- **Insight** generation interprets patterns in temporal context (e.g., "builder is accelerating — they started slow but are now completing missions rapidly").
- **Recommendation** timing is informed by timeline position (e.g., "don't interrupt during a rapid action sequence").
- **Decision** logging includes the timeline position for auditability.

---

## 15. Edge Cases

### 15.1 Clock Skew

If the system clock is adjusted between two events within a session, the delta could be negative or anomalously large.

**Mitigation:** Deltas are clamped to `>= 0`. Negative deltas are treated as 0. Anomalously large deltas (> 1 hour) trigger a warning log but do not break the timeline.

### 15.2 Concurrent Sessions

A builder may have multiple sessions active (e.g., two browser tabs, or a CLI session and a web session).

**Handling:** Each session has a unique `sessionId`. Events from different sessions never mix in the same timeline. Queries always filter by `sessionId`.

### 15.3 Session Size Limits

A session with tens of thousands of events could produce a very long timeline.

**Handling:** The `slice` operation enables pagination. The `ascend timeline show` command defaults to showing the first 50 entries, with a `--more` flag for subsequent pages. No hard limit is imposed on session size.

### 15.4 Orphaned Events

An observation without a `sessionId` cannot be placed on any timeline.

**Handling:** The append operation requires a valid `sessionId`. If an observation arrives without one, a new session is created automatically. This ensures every observation belongs to exactly one timeline.

### 15.5 Empty Timeline

A session with zero events has an empty timeline.

**Handling:** The session exists in the database (it was created when the first observation arrived), but `getSessionTimeline()` returns an empty array. Summary metrics default to 0.

---

## 16. Summary

The Cognitive Timeline is the canonical representation of temporal order in the ASCEND system. It defines:

- **What a timeline is** — an ordered sequence of entries, each with a position, timestamp, delta, and type.
- **How timelines are stored** — they are derived from the `observations` table, not stored separately.
- **How timelines are queried** — by time range, by event type, by session, by sequence slice, or by diff against another timeline.
- **How timelines are replayed** — observations are loaded in order, state is rebuilt, and frames are produced.
- **How time is measured** — deltas between consecutive events, classified into micro, meso, and macro gaps.
- **How determinism is guaranteed** — monotonic sequence numbers, immutable events, deterministic sort order.

The timeline transforms a stream of raw observations into a structured, queryable, replayable record of learning. It is the foundation upon which every cognitive function — signal extraction, pattern detection, insight generation, recommendation — is built.

Without the timeline, the system knows *what* happened but not *when*. With the timeline, it knows both — and can reconstruct the past with perfect fidelity.
