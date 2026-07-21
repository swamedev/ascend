# ARCH-0041 — Timeline and Replay

| Field | Value |
|-------|-------|
| **ID** | ARCH-0041 |
| **Name** | Timeline and Replay |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0030 Cognitive Architecture, ARCH-0031 Observation Model, ARCH-0038 Cognitive Timeline, ARCH-0035 Observation Storage |
| **Principle** | Every session is replayable. Every event is traceable. The past is deterministic. |

---

## 1. Purpose

The Cognitive Timeline (ARCH-0038) defines *what* a timeline is — an ordered sequence of entries with positions, timestamps, deltas, and types. This document defines *how* the timeline is constructed, managed, and replayed in code.

Timeline and Replay (F1.0–F1.2 enabling infrastructure) is not a standalone phase in the Milestone F roadmap — it is a cross-cutting capability that the Collector, Normalizer, and Signal Extractor all feed into. Every normalized observation becomes a timeline entry. Every timeline entry enables replay. Every replay verifies determinism.

This document specifies:
- How the timeline is constructed from normalized observations in real time
- How sessions are managed (start, end, gap detection, automatic closure)
- The Replay Engine architecture — how past sessions are reconstructed
- The timeline query interface for the Signal Extractor and downstream consumers
- Gap detection algorithms, delta computation, and session segmentation
- The formal determinism proof for timeline operations

> **Core Guarantee:** Given the same sequence of normalized observations, the timeline produces the same entries, the same deltas, the same session boundaries — every time, without exception.

---

## 2. Relationship to Existing Documents

| Document | Relationship |
|----------|-------------|
| ARCH-0038 | Defines the conceptual timeline model (entries, sessions, gaps). ARCH-0041 implements that model. |
| ARCH-0039 | NormalizedObservation is the unit of timeline construction. |
| ARCH-0040 | Signal Extractor queries the timeline for temporal context. |
| ARCH-0035 | Observations table is the single source of truth for timeline derivation. |
| I15 | Observation Determinism — timeline is deterministic by construction. |
| I16 | Observation Append Only — observations are never modified, guaranteeing replay fidelity. |

```
ARCH-0038 (conceptual)
    │
    ▼
ARCH-0041 (implementation architecture)
    │
    ├── TimelineBuilder (real-time construction)
    ├── SessionManager (session lifecycle)
    └── ReplayEngine (session reconstruction)
```

---

## 3. TimelineBuilder Architecture

The `TimelineBuilder` constructs timeline entries in real time as normalized observations arrive from the pipeline.

### 3.1 Component Model

```
NormalizedObservation (from Normalizer)
    │
    ▼
┌────────────────────────────────────┐
│  TimelineBuilder                    │
│                                    │
│  ┌──────────────┐  ┌────────────┐ │
│  │ SessionStore │  │ DeltaComp  │ │
│  │ (in-memory)  │  │ (pure fn)  │ │
│  └──────┬───────┘  └─────┬──────┘ │
│         │                │        │
│         ▼                ▼        │
│  ┌────────────────────────────────┐│
│  │  TimelineEntry Factory         ││
│  │  - assigns sequence_number     ││
│  │  - computes delta              ││
│  │  - generates label             ││
│  │  - tags session segment        ││
│  └──────────────┬─────────────────┘│
└─────────────────┼──────────────────┘
                  ▼
        TimelineEntry (output)
```

### 3.2 TimelineEntry Schema

```python
@dataclass
class TimelineEntry:
    sequenceNumber: int              # Monotonically increasing, gapless
    observationId: str               # ULID of the source observation
    timestamp: str                   # ISO 8601 UTC
    delta: int                       # Milliseconds since previous event
    sessionId: str                   # ULID of the session
    type: str                        # Event type (pass-through)
    label: str                       # Human-readable summary
    segment: str                     # 'session_start' | 'session_middle' | 'session_end'
```

### 3.3 Builder Interface

```python
class TimelineBuilder:
    def __init__(self, session_store: SessionStore | None = None):
        self._session_store = session_store or InMemorySessionStore()

    def append(self, observation: NormalizedObservation) -> TimelineEntry:
        """Append an observation to the timeline.
        
        Returns a TimelineEntry with sequence number, delta, and session metadata.
        Creates or continues a session as needed.
        """

    def get_session(self, session_id: str) -> CognitiveSession | None: ...

    def get_session_metrics(self, session_id: str) -> SessionMetrics: ...
```

### 3.4 Append Algorithm

```
function append(observation):
    builder_id = observation.context.builderId
    session = self._session_store.get_active(builder_id)

    if session is None:
        # No active session → create new one
        session = Session(
            id=generate_ulid(),
            builderId=builder_id,
            startedAt=observation.timestamp,
            sequenceCounter=1,
        )
        segment = 'session_start'
    else:
        # Check for macro-gap (session timeout)
        gap = observation.timestamp - session.lastEventTimestamp
        if gap > MACRO_GAP_THRESHOLD:  # 30 minutes
            self._session_store.close(session)
            session = Session(
                id=generate_ulid(),
                builderId=builder_id,
                startedAt=observation.timestamp,
                sequenceCounter=1,
            )
            segment = 'session_start'
        else:
            session.sequenceCounter += 1
            segment = 'session_middle'

    delta = 0 if segment == 'session_start' else gap_ms

    entry = TimelineEntry(
        sequenceNumber=session.sequenceCounter,
        observationId=observation.id,
        timestamp=observation.timestamp,
        delta=delta,
        sessionId=session.id,
        type=observation.type,
        label=generate_label(observation),
        segment=segment,
    )

    # Update session store
    session.lastEventTimestamp = observation.timestamp
    session.eventCount += 1
    self._session_store.save(session)

    return entry
```

### 3.5 Label Generation

Labels are deterministic, template-based strings derived from the observation type and data:

| Observation Type | Template | Example |
|-----------------|----------|---------|
| `builder.created` | `"Builder created: {username}"` | "Builder created: Alice" |
| `mission.started` | `"Started mission {missionId}"` | "Started mission variables-101" |
| `mission.completed` | `"Completed mission {missionId} (score: {score})"` | "Completed mission variables-101 (score: 85)" |
| `evidence.submitted` | `"Evidence submitted for {missionId}"` | "Evidence submitted for variables-101" |
| `assessment.completed` | `"Assessment completed: {score}"` | "Assessment completed: 0.85" |
| `competency.unlocked` | `"Unlocked {competencyId} (level {level})"` | "Unlocked python-basics (level 1)" |
| `achievement.earned` | `"Achievement earned: {achievementId}"` | "Achievement earned: first-mission" |
| `*` (fallback) | `"{type}"` | "evidence.submitted" |

The label generator is a pure function: `(observation: NormalizedObservation) → str`.

---

## 4. SessionManager

The `SessionManager` owns the session lifecycle — creation, tracking, gap detection, and closure.

### 4.1 Session Schema

```python
@dataclass
class Session:
    id: str                             # ULID
    builderId: str                      # Owner
    startedAt: str                      # ISO 8601 UTC
    endedAt: str | None                 # Set on session end
    lastEventTimestamp: str             # Updated on each event
    eventCount: int                     # Total events in session
    sequenceCounter: int                # Current max sequence number
    status: SessionStatus               # 'active' | 'closed' | 'orphaned'

class SessionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ORPHANED = "orphaned"
```

### 4.2 Session Boundaries

A session begins when the first observation arrives for a builder without an active session. A session ends when:

1. **Macro-gap detected**: No events for > 30 minutes (configurable).
2. **Explicit closure**: Builder or system explicitly ends the session.
3. **Application shutdown**: On graceful shutdown, all active sessions are closed.
4. **Crash recovery**: On startup, sessions older than 24 hours are auto-closed as orphaned.

### 4.3 SessionStore Interface

```python
class SessionStore(Protocol):
    def get_active(self, builder_id: str) -> Session | None: ...
    def save(self, session: Session) -> None: ...
    def close(self, session: Session, ended_at: str | None = None) -> None: ...
    def get_by_id(self, session_id: str) -> Session | None: ...
    def list_by_builder(self, builder_id: str, limit: int = 50) -> list[Session]: ...

class InMemorySessionStore:
    """Thread-safe in-memory implementation. Active sessions held in dict."""
    ...
```

### 4.4 Gap Detection

Gap detection is a pure function:

```python
class Gap:
    MICRO = "micro"    # 30s < delta < 5min
    MESO = "meso"      # 5min < delta < 30min
    MACRO = "macro"    # delta > 30min (session boundary)

def classify_gap(delta_ms: int) -> Gap | None:
    if delta_ms < 30_000:
        return None
    if delta_ms < 5 * 60_000:
        return Gap.MICRO
    if delta_ms < 30 * 60_000:
        return Gap.MESO
    return Gap.MACRO
```

Gaps are not stored as separate entities — they are computed on the fly from timeline deltas. The gap classification is used by:
- **TimelineBuilder**: macro-gaps trigger session closure.
- **Signal Extractor**: micro/meso gaps inform `focus_score` computation.
- **Pattern Detector**: gap patterns (e.g., micro-gaps clustered around a mission) may trigger insights.

---

## 5. ReplayEngine

The `ReplayEngine` reconstructs a past session from stored observations. It is the definitive test of pipeline determinism.

### 5.1 Component Model

```
Request: replay(session_id)
    │
    ▼
┌─────────────────────────────────────────────┐
│  ReplayEngine                                │
│                                             │
│  1. Load all observations for session       │
│     SELECT * FROM observations              │
│     WHERE builder_id = B                    │
│       AND session_id = S                    │
│     ORDER BY sequence_number ASC             │
│                                             │
│  2. Rebuild TimelineEntry[]                 │
│     For each observation:                   │
│       - compute delta                       │
│       - generate label                      │
│       - return TimelineEntry                │
│                                             │
│  3. Compute session metrics                 │
│     - duration, focus_score                 │
│     - missions_started/completed            │
│     - competencies_unlocked                 │
│     - xp_gained                             │
│                                             │
│  4. Return ReplayResult                     │
└─────────────────────────────────────────────┘
    │
    ▼
ReplayResult { session, timeline[], metrics }
```

### 5.2 ReplayResult Schema

```python
@dataclass
class ReplayResult:
    session: Session
    timeline: list[TimelineEntry]
    metrics: SessionMetrics
    integrity: IntegrityReport

@dataclass
class SessionMetrics:
    duration_seconds: int
    focus_score: float                 # 0.0–1.0
    missions_started: int
    missions_completed: int
    competencies_unlocked: int
    achievements_earned: int
    xp_gained: float
    event_rate: float                  # events per minute
    gaps: list[GapRecord]              # gaps classified by type

@dataclass
class GapRecord:
    type: Gap                          # MICRO | MESO | MACRO
    startedAt: str                     # timestamp of event before gap
    endedAt: str                       # timestamp of event after gap
    durationMs: int                    # gap duration

@dataclass
class IntegrityReport:
    observation_count: int
    sequence_gaps: list[int]           # missing sequence numbers, if any
    clock_skew_events: int             # count of negative-delta events
    checksum_valid: bool               # all checksums verified
```

### 5.3 Replay Algorithm

```
function replay(session_id: str) -> ReplayResult:
    # 1. Load session metadata
    session = session_store.get_by_id(session_id)
    if session is None:
        raise SessionNotFoundError(session_id)

    # 2. Load observations in order
    observations = observation_store.get_by_session(session_id)

    # 3. Rebuild timeline entries
    timeline = []
    integrity = IntegrityReport(observation_count=len(observations))

    for i, obs in enumerate(observations):
        delta = 0 if i == 0 else (
            parse_timestamp(obs.timestamp) -
            parse_timestamp(observations[i-1].timestamp)
        )
        if delta < 0:
            delta = 0
            integrity.clock_skew_events += 1

        entry = TimelineEntry(
            sequenceNumber=i + 1,
            observationId=obs.id,
            timestamp=obs.timestamp,
            delta=delta,
            sessionId=session_id,
            type=obs.type,
            label=generate_label_from_observation(obs),
            segment=(
                'session_start' if i == 0
                else 'session_end' if i == len(observations) - 1
                else 'session_middle'
            ),
        )
        timeline.append(entry)

    # 4. Check for sequence gaps
    seq_numbers = [obs.sequence_number for obs in observations]
    for seq in range(1, len(observations)):
        if seq not in seq_numbers:
            integrity.sequence_gaps.append(seq)

    # 5. Compute session metrics
    metrics = compute_session_metrics(timeline, observations, session)

    # 6. Detect gaps
    gaps = []
    for entry in timeline:
        gap_type = classify_gap(entry.delta)
        if gap_type is not None:
            gaps.append(GapRecord(
                type=gap_type,
                startedAt=...,  # previous event timestamp
                endedAt=entry.timestamp,
                durationMs=entry.delta,
            ))
    metrics.gaps = gaps

    return ReplayResult(
        session=session,
        timeline=timeline,
        metrics=metrics,
        integrity=integrity,
    )
```

### 5.4 Session Metrics Computation

```python
def compute_session_metrics(
    timeline: list[TimelineEntry],
    observations: list[NormalizedObservation],
    session: Session,
) -> SessionMetrics:
    duration = 0
    if session.endedAt:
        duration = (
            parse_timestamp(session.endedAt) -
            parse_timestamp(session.startedAt)
        ) // 1000

    missions_started = sum(
        1 for o in observations if o.type == 'mission.started'
    )
    missions_completed = sum(
        1 for o in observations if o.type == 'mission.completed'
    )
    competencies = sum(
        1 for o in observations if o.type == 'competency.unlocked'
    )
    achievements = sum(
        1 for o in observations if o.type == 'achievement.earned'
    )
    xp = sum(
        o.data.get('xpEarned', 0) or 0
        for o in observations if o.type == 'mission.completed'
    )

    # Focus score: ratio of non-gap time to total time
    gap_ms = sum(g.durationMs for g in gaps)
    total_ms = duration * 1000
    focus_score = max(0.0, 1.0 - (gap_ms / max(total_ms, 1)))

    event_rate = len(timeline) / max(duration / 60, 1)

    return SessionMetrics(
        duration_seconds=duration,
        focus_score=focus_score,
        missions_started=missions_started,
        missions_completed=missions_completed,
        competencies_unlocked=competencies,
        achievements_earned=achievements,
        xp_gained=xp,
        event_rate=event_rate,
        gaps=[],
    )
```

### 5.5 Determinism Proof

Given:
- A set of observations O stored in the `observations` table, each with `(builder_id, session_id, sequence_number, timestamp)`, where `sequence_number` is monotonically increasing within the session.
- A query Q: `SELECT * FROM observations WHERE builder_id = B AND session_id = S ORDER BY sequence_number ASC`.
- A pure function M that maps each observation to a `TimelineEntry`.

Then:
1. Q(O) always returns the same ordered sequence for the same `(B, S)` — the sort is deterministic.
2. M is a pure function — same observation always produces the same entry.
3. O is immutable (I16) — the set of observations for `(B, S)` never changes.

Therefore, `ReplayResult` is always identical for the same `session_id`. Q.E.D.

---

## 6. Timeline Operations

### 6.1 Real-Time Append

The `TimelineBuilder.append()` method is called synchronously for each normalized observation as it exits the Normalizer. It:

1. Reads or creates the session (via `SessionStore`).
2. Computes the delta from the previous event.
3. Assigns the sequence number.
4. Generates the label.
5. Returns the `TimelineEntry`.

The entry is not stored separately — it is derived from the observation and session state. If persistence is needed (for caching or export), the entry can be written to a `timeline_cache` table, but the canonical source is always the `observations` table.

### 6.2 Session Query

```python
# List all sessions for a builder
def list_sessions(builder_id: str, limit: int = 20):
    return session_store.list_by_builder(builder_id, limit=limit)

# Get full timeline for a session
def get_timeline(session_id: str) -> list[TimelineEntry]:
    return replay(session_id).timeline

# Get session summary metrics
def get_metrics(session_id: str) -> SessionMetrics:
    return replay(session_id).metrics
```

### 6.3 Timeline Export

```python
def export_timeline(session_id: str, format: str = "json") -> str:
    result = replay(session_id)
    if format == "json":
        return json.dumps(asdict(result), indent=2)
    elif format == "csv":
        # Header + rows
        ...
    elif format == "cli":
        # Compact CLI format per ARCH-0038 Section 9
        ...
```

---

## 7. Session Persistence

Session metadata is persisted to SQLite for crash recovery and long-term querying:

```sql
CREATE TABLE IF NOT EXISTS cognitive_sessions (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    duration_seconds INTEGER DEFAULT 0,
    event_count INTEGER DEFAULT 0,
    missions_started INTEGER DEFAULT 0,
    missions_completed INTEGER DEFAULT 0,
    competencies_unlocked INTEGER DEFAULT 0,
    achievements_earned INTEGER DEFAULT 0,
    xp_gained REAL DEFAULT 0.0,
    focus_score REAL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_cs_builder ON cognitive_sessions(builder_id);
CREATE INDEX idx_cs_status ON cognitive_sessions(status);
CREATE INDEX idx_cs_started ON cognitive_sessions(builder_id, started_at);
```

### 7.1 Session Recovery

On startup, the `SessionManager` runs recovery:

```python
def recover(self):
    """Close orphaned sessions and rebuild in-memory state."""
    orphans = self._db.query(
        "SELECT * FROM cognitive_sessions "
        "WHERE status = 'active' "
        "AND started_at < datetime('now', '-24 hours')"
    )
    for session in orphans:
        self._close_session(
            session.id,
            ended_at=session.started_at,  # approximate
        )
```

---

## 8. Gap Detection Architecture

### 8.1 Computation

Gaps are computed from timeline deltas. The `classify_gap()` function (Section 4.4) maps delta duration to a gap type.

### 8.2 Gap Events

When a macro-gap is detected during real-time append, the `TimelineBuilder`:

1. Closes the current session.
2. Creates a new session.
3. The gap itself is implicit in the new session's start — delta for the first entry of the new session is 0.

When computing replay metrics, gaps are explicit `GapRecord` objects in the result. The metric computation uses gap records to compute `focus_score`.

### 8.3 Gap Persistence

Gaps are not stored as a separate table. They are always computed from timeline entries. This avoids redundancy and maintains the single-source-of-truth constraint.

---

## 9. Relationship to Signal Extraction

The Signal Extractor (ARCH-0040) queries the timeline for temporal context:

- **Session frequency**: `list_sessions(builder_id)` → count sessions per day/week.
- **Time of day / day of week**: `get_timeline(session_id)` → extract hour/weekday from first entry.
- **Session duration**: `get_metrics(session_id).duration_seconds`.
- **Focus score**: `get_metrics(session_id).focus_score`.
- **Gap patterns**: `get_metrics(session_id).gaps` → detect micro-gap clusters.

These queries are read-only and deterministic. They depend only on stored observations, which are immutable.

---

## 10. Edge Cases

| Edge Case | Behavior |
|-----------|----------|
| Empty session (0 observations) | Replay returns empty timeline, zeroed metrics |
| Single-observation session | Delta = 0, segment = 'session_start' and 'session_end' |
| Clock skew (negative delta) | Clamp to 0, increment `clock_skew_events` counter |
| Very long session (10k+ events) | Paginate via `slice(sequence_start, sequence_end)` |
| Concurrent sessions (same builder, different devices) | Each has unique `sessionId`; timelines never mix |
| Orphaned session (crash without close) | Auto-closed on startup recovery |
| Missing observation (sequence gap) | Recorded in `integrity.sequence_gaps`; replay continues |
| Duplicate observation IDs | Second occurrence ignored (primary key conflict) |

---

## 11. Determinism Guarantee

The timeline is deterministic by construction (Section 5.5). This guarantee is the foundation of every downstream cognitive function:

- **Signal Extractor**: uses timeline-derived metrics (session count, duration, focus). Same session → same metrics → same signals.
- **Pattern Detector**: uses signal sequences. Same signal sequence → same patterns.
- **Insight Generator**: uses patterns. Same patterns → same insights.
- **Replay**: uses observations. Same observations → same replay.

Violating this guarantee (e.g., by mutating an observation after storage) breaks the entire cognitive chain. I16 (Observation Append Only) exists precisely to prevent this.

---

## 12. References

| Reference | Description |
|-----------|-------------|
| ARCH-0038 | Cognitive Timeline — conceptual model |
| ARCH-0039 | Observation Normalization — upstream |
| ARCH-0040 | Signal Extraction Architecture — downstream consumer |
| ARCH-0035 | Observation Storage — SQLite schema |
| DOC-0009 | Architectural Invariants — I15, I16 |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO PROMETHEUS |
