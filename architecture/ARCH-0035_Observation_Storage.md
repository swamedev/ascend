# ARCH-0035 — Observation Storage

| Field | Value |
|-------|-------|
| **ID** | ARCH-0035 |
| **Name** | Observation Storage |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0003 Core Engine Specification, ARCH-0031 Observation Model |
| **Principle** | Every observation persisted is every session reproducible |

---

## 1. Purpose

The Observation Storage subsystem is the persistent layer for all cognitive observations. It stores every event, every metric snapshot, every insight. It is designed for determinism, replayability, and full Builder sovereignty.

Observation Storage exists because the cognitive layer requires more than transient in-memory processing. Every artifact in the cognitive cycle — observations, signals, patterns, insights, recommendations, decisions, outcomes — must survive restarts, support historical analysis, and enable deterministic replay. Without a dedicated storage subsystem, the cognitive layer would lose its memory between sessions, making longitudinal pattern detection impossible and rendering every insight ephemeral.

The subsystem serves four primary functions:

- **Persistence:** All cognitive artifacts are written to durable storage at the moment of creation. No artifact is held exclusively in memory.
- **Query:** The cognitive layer and any dashboard or export tool can query historical artifacts by type, builder, session, time range, or custom filters.
- **Replay:** Any previous Builder session can be reconstructed exactly by reading stored observations and replaying them through the cognitive pipeline in sequence.
- **Governance:** Retention, pruning, export, and deletion are managed through a unified policy that respects Builder sovereignty.

This document defines the complete schema, indexing strategy, compression approach, replay mechanism, retention policy, pruning logic, migration strategy, and storage budget for the Observation Storage subsystem. It is the implementation specification for Section 11 of ARCH-0031 (Observation Storage & Lifecycle).

---

## 2. Storage Philosophy

The Observation Storage subsystem is grounded in five immutable principles that govern every design decision below.

### 2.1 Local-First

All observations are stored locally on the Builder's device. No cognitive data is transmitted to any external server without the Builder's explicit, informed consent. The default configuration is fully offline. Sync to remote storage, if any, is an opt-in feature that must be enabled by the Builder after clear disclosure of what data will be shared.

The local-first principle has three implications:
- The storage engine must be embeddable, requiring zero server infrastructure.
- The database file must be portable — the Builder can copy it, back it up, or move it between devices.
- All queries and analytics must run locally. No cloud dependency exists for any storage operation.

### 2.2 Immutable

Once an observation is written, it is never modified. The data payload, the timestamp, the type, the source — every field is frozen at write time. Immutability guarantees that replay is deterministic: given the same sequence of observations, the cognitive pipeline always produces the same outputs.

Immutability does not mean data cannot be removed. Retention and pruning delete entire rows. But no row is ever updated after creation. This distinction is critical: the cognitive layer can trust that historical observations are exactly as they were when captured.

The only exceptions to immutability are status fields on derived entities (insights, recommendations), which may transition through a lifecycle (e.g., `pending` → `accepted`). These transitions are logged separately and do not alter the original observation data.

### 2.3 Replayable

Every Builder session can be reconstructed from stored events. Replay is the process of reading all observations for a given session in sequence order and feeding them through the cognitive pipeline. The result is an exact replica of the Builder's state at any point during that session.

Replay serves three use cases:
- **Debugging:** A developer can replay a session to reproduce a bug in pattern detection or insight generation.
- **Auditing:** A Builder can examine what was observed and what cognitive artifacts were produced at any point in their history.
- **Migration:** When the cognitive pipeline is upgraded, historical sessions can be replayed through the new pipeline to generate updated insights without losing the original observations.

### 2.4 Portable

The Builder owns their data completely. Observation Storage must support full export in an open, human-readable format (JSON). The export must include all artifacts — observations, signals, patterns, insights, recommendations, decisions, outcomes, sessions, metric snapshots, and state snapshots.

Portability means:
- The Builder can export their entire cognitive history at any time.
- The export format is self-describing and does not require the ASCEND database schema to interpret.
- The Builder can delete their data after export, knowing they have a complete copy.
- The Builder can import their data into another ASCEND instance or into any external tool that processes the open format.

### 2.5 Efficient

Storage must remain manageable over years of use. Efficiency is achieved through three mechanisms:

- **Compression:** Large payloads and all snapshots are compressed on write and decompressed on read. Compression is transparent to the application layer.
- **Pruning:** Data older than the configured retention window is automatically removed. Pruning is configurable by the Builder and runs on a schedule.
- **Indexing:** All query patterns are covered by indexes, ensuring that reads — especially replay reads and dashboard queries — remain fast even as the database grows.

The target storage budget is under 1 MB per Builder per 90 days of typical usage (approximately 10 events per day). This ensures that even a power user generating 100 events per day will use under 10 MB per 90 days, keeping the total database well under 100 MB for years of use.

---

## 3. Database Choice: SQLite

Observation Storage uses SQLite as its database engine. This decision is consistent with ARCH-0006 (MVP Technical Specification) and the existing Runtime infrastructure.

### 3.1 Rationale

SQLite is chosen for the following reasons:

- **Already a dependency:** The ASCEND Runtime already uses SQLite. Adding Observation Storage does not introduce a new database technology, new connection pools, or new operational complexity.
- **Zero configuration:** SQLite requires no server process, no configuration files, no network setup. The database file is created on first write and managed entirely by the application.
- **Local-first:** The database file lives on the Builder's device. No network access is required for any read or write operation.
- **Embeddable:** SQLite runs in-process. There is no client-server overhead, no context switching, no serialization cost for local queries.
- **Battle-tested:** SQLite is used in billions of devices worldwide. It has decades of field testing, rigorous SQL standards compliance, and excellent documentation.
- **Single-file portability:** The entire cognitive history of a Builder is a single `.db` file. The Builder can back it up, archive it, or transfer it to another device by copying one file.
- **ACID compliance:** SQLite supports full ACID transactions. Writes are atomic, consistent, isolated, and durable. If a crash occurs during a write, the database is automatically recovered on next open using the write-ahead log (WAL).
- **No network attack surface:** Because SQLite is not a network service, there is no port to attack, no authentication to bypass, no network exposure of cognitive data.

### 3.2 WAL Mode

The database operates in Write-Ahead Log (WAL) mode. WAL mode allows concurrent reads while a write is in progress — the cognitive layer can query the database without blocking the observation collector that is writing new data. WAL mode also improves write performance by batching transactions.

The WAL file and shared memory file are stored alongside the main database file in the same directory. These auxiliary files are automatically managed by SQLite and are included in any file-level backup.

### 3.3 Database Location

The database file is stored at:

```
<ASCEND_DATA_DIR>/cognitive/cognitive.db
```

Where `ASCEND_DATA_DIR` defaults to `~/.ascend/` on Unix systems and `%APPDATA%\Ascend\` on Windows. The directory structure is:

```
~/.ascend/
  cognitive/
    cognitive.db       — Observation Storage database
    cognitive.db-wal   — Write-ahead log (auto-managed)
    cognitive.db-shm   — Shared memory (auto-managed)
```

The `cognitive/` subdirectory ensures separation from the Runtime database and any other data stores. It also simplifies backup and export — the Builder can archive the entire `cognitive/` directory to capture all cognitive data.

### 3.4 Connection Management

The application opens a single connection to the database at startup and uses it for all operations. SQLite supports multiple simultaneous readers but only one writer at a time. Writes are serialized through a write queue in the cognitive layer — the observation collector, signal extractor, and insight generator all write through a shared writer that serializes access.

For read-heavy operations (dashboard queries, export), read transactions are used exclusively. No read operation ever blocks a write operation (in WAL mode), and no write operation blocks a read.

### 3.5 Security

The database file is not encrypted by default. However, SQLite supports encryption extensions, and the Builder can optionally enable encryption via a passphrase. Encryption is a configuration option, not a default, because it introduces key management complexity. The recommendation is that Builders who require encryption should use filesystem-level encryption (e.g., BitLocker, FileVault, LUKS) rather than application-level encryption, because filesystem encryption protects all files in the ASCEND data directory uniformly.

---

## 4. Schema Design

The schema consists of six tables. Each table corresponds to a distinct entity in the cognitive model defined in ARCH-0031. All tables use ULIDs as primary keys. ULIDs are chosen over UUIDs because they are sortable by time, which enables efficient range queries without a separate timestamp index on the primary key.

### 4.1 The observations Table

The `observations` table is the central store for all raw observations. Every observation captured by a collector is written to this table exactly once. The table is append-only — no row is ever updated after insertion.

```sql
CREATE TABLE observations (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    timestamp TEXT NOT NULL,
    builder_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    correlation_id TEXT,
    causation_id TEXT,
    data TEXT NOT NULL,
    source TEXT NOT NULL,
    collector TEXT NOT NULL,
    client_timestamp TEXT,
    server_timestamp TEXT,
    environment TEXT NOT NULL DEFAULT 'local',
    sequence_number INTEGER NOT NULL,
    checksum TEXT,
    compressed INTEGER NOT NULL DEFAULT 0,
    original_size INTEGER,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_obs_type ON observations(type);
CREATE INDEX idx_obs_builder ON observations(builder_id);
CREATE INDEX idx_obs_session ON observations(session_id);
CREATE INDEX idx_obs_timestamp ON observations(timestamp);
CREATE INDEX idx_obs_builder_type ON observations(builder_id, type);
CREATE INDEX idx_obs_builder_time ON observations(builder_id, timestamp);
CREATE INDEX idx_obs_builder_seq ON observations(builder_id, sequence_number);
CREATE INDEX idx_obs_session_time ON observations(session_id, timestamp);
CREATE INDEX idx_obs_source ON observations(source);
CREATE INDEX idx_obs_collector ON observations(collector);
CREATE INDEX idx_obs_correlation ON observations(correlation_id);
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT | ULID primary key. Globally unique, sortable by creation time. |
| `type` | TEXT | Observation type per ARCH-0031 classification. Examples: `mission.completed`, `evidence.submitted`, `session.started`. The type follows the dot-separated convention defined in ARCH-0031 Section 3.2. |
| `version` | INTEGER | Schema version of the observation data. Starts at 1 and increments if the structure of `data` changes in a future revision. This enables forward compatibility — the system can interpret old observations based on their version number. |
| `timestamp` | TEXT | ISO 8601 UTC timestamp of when the observation occurred. This is the logical timestamp, not the database write time. For runtime events, this is the domain event timestamp. For cognitive events, this is the time the collector captured the event. |
| `builder_id` | TEXT | The ULID of the Builder to whom this observation belongs. Every observation is owned by exactly one Builder. |
| `session_id` | TEXT | The ULID of the session during which this observation was captured. A session is a contiguous period of Builder activity. All observations captured between `session.started` and `session.ended` share the same `session_id`. |
| `correlation_id` | TEXT | Optional ULID linking this observation to a broader correlation context. Observations that are part of the same cognitive cycle share the same `correlation_id`. This enables tracing an entire chain from observation through outcome. |
| `causation_id` | TEXT | Optional ULID of the observation that caused this one. For example, if an `insight.generated` observation is caused by a `mission.completed` observation, the `causation_id` points to the `mission.completed` observation. This creates a causal chain through the cognitive cycle. |
| `data` | TEXT | The observation payload as a JSON string. The structure of the JSON is determined by the `type` and `version` fields. This field may be compressed (see Section 5). |
| `source` | TEXT | The origin of the observation. One of: `runtime` (domain events from the ASCEND Runtime), `cognitive` (events produced by the cognitive layer itself), `builder` (explicit Builder actions such as navigation or preference changes). |
| `collector` | TEXT | The name of the collector component that captured this observation. Examples: `runtime-event-collector`, `state-snapshot-collector`, `builder-action-tracker`. This field is used for debugging and observability — it enables tracing an observation back to its producing component. |
| `client_timestamp` | TEXT | Optional ISO 8601 timestamp set by the client device at the moment of capture. This may differ from `timestamp` if the observation was captured on a remote device and synced later. In local-first mode, `client_timestamp` and `timestamp` are identical. |
| `server_timestamp` | TEXT | Optional ISO 8601 timestamp set by a sync server when the observation was received. This is only populated in sync-enabled configurations. In local-first mode, this field is NULL. |
| `environment` | TEXT | The deployment environment where the observation was captured. Defaults to `local`. Other values: `staging`, `production` (used only if the Builder has opted into sync). |
| `sequence_number` | INTEGER | A monotonically increasing integer per Builder. Every new observation for a given Builder receives the next sequence number. Sequence numbers are gapless — if sequence 42 is missing, the replay will detect the gap and flag it. Sequence numbers are the authoritative ordering mechanism for replay. |
| `checksum` | TEXT | Optional SHA-256 checksum of the `data` field before compression. Computed at write time and stored for integrity verification. The replay engine can verify that data has not been corrupted by recomputing the checksum on read. |
| `compressed` | INTEGER | Boolean flag indicating whether the `data` field is compressed. 0 = uncompressed (plain JSON text), 1 = compressed (zlib-compressed binary encoded as base64). |
| `original_size` | INTEGER | The byte size of the `data` field before compression. Only populated if `compressed = 1`. Useful for reporting storage savings. |
| `created_at` | TEXT | The database write timestamp. This is set by SQLite's `datetime('now')` default and represents when the row was physically written to disk. It is not used for logical ordering (use `timestamp` or `sequence_number` for that). |

#### Indexes Explained

The index set is designed to cover every query pattern identified in the cognitive layer requirements:

- **idx_obs_type:** Fast filtering by observation type. Used by the pattern detector when it queries for all observations of a specific type within a time window.
- **idx_obs_builder:** Fast lookup of all observations for a Builder. Used by the export tool and data deletion operations.
- **idx_obs_session:** Fast lookup of all observations in a session. Used by the replay engine to load all observations for a specific session.
- **idx_obs_timestamp:** Fast time-range queries. Used by the dashboard to show observations in a date range.
- **idx_obs_builder_type:** Composite index for the most common query pattern: "all observations of type X for Builder Y". Used extensively by the pattern detector and signal extractor.
- **idx_obs_builder_time:** Composite index for time-ordered queries per Builder. Used by the replay engine and trend analysis.
- **idx_obs_builder_seq:** Composite index for sequence-number-ordered queries per Builder. The authoritative replay ordering index. Essential for deterministic replay.
- **idx_obs_session_time:** Composite index for loading a session's observations in time order. Used by the replay engine.
- **idx_obs_source:** Filter by source type. Used for debugging and cognitive layer statistics.
- **idx_obs_collector:** Filter by collector name. Used for debugging and collector health monitoring.
- **idx_obs_correlation:** Correlation chain lookups. Used to trace a complete cognitive cycle from a single observation.

### 4.2 The metric_snapshots Table

The `metric_snapshots` table stores periodic captures of computed metrics. Unlike observations (which record discrete events), metric snapshots record continuous or derived metrics at a point in time. Metrics are produced by the signal extractor or pattern detector and represent quantitative measures of Builder state.

```sql
CREATE TABLE metric_snapshots (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL,
    session_id TEXT,
    metric_name TEXT NOT NULL,
    value REAL NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    timestamp TEXT NOT NULL,
    observation_id TEXT,
    source TEXT NOT NULL DEFAULT 'signal',
    metadata TEXT,
    compressed INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_met_builder ON metric_snapshots(builder_id);
CREATE INDEX idx_met_name ON metric_snapshots(metric_name);
CREATE INDEX idx_met_builder_name ON metric_snapshots(builder_id, metric_name);
CREATE INDEX idx_met_builder_time ON metric_snapshots(builder_id, timestamp);
CREATE INDEX idx_met_builder_name_time ON metric_snapshots(builder_id, metric_name, timestamp);
CREATE INDEX idx_met_session ON metric_snapshots(session_id);
CREATE INDEX idx_met_source ON metric_snapshots(source);
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT | ULID primary key. |
| `builder_id` | TEXT | The Builder to whom this metric belongs. |
| `session_id` | TEXT | Optional session ID. Populated if the metric was captured during an active session. |
| `metric_name` | TEXT | The name of the metric. Convention: lowercase with underscores. Examples: `focus_score`, `learning_velocity`, `completion_rate`, `streak_length`, `engagement_score`, `fatigue_index`, `session_frequency`, `topic_coverage`. The metric name must be registered in the metrics registry (defined in the cognitive layer configuration). |
| `value` | REAL | The numeric value of the metric. All metrics are represented as real numbers. Boolean metrics use 0.0 and 1.0. Discrete metrics (e.g., streak length in days) are stored as real numbers for consistency. |
| `confidence` | REAL | The confidence in this metric value, from 0.0 to 1.0. Direct extractions have confidence 1.0. Computed or inferred metrics have lower confidence based on the quality and quantity of source data. |
| `timestamp` | TEXT | ISO 8601 UTC timestamp of when the metric was computed. |
| `observation_id` | TEXT | Optional. If this metric was derived from a single observation, the ID of that observation. This enables traceability from metric back to source observation. |
| `source` | TEXT | The component that produced this metric. Values: `signal` (extracted from observations), `pattern` (computed from multiple signals), `insight` (derived from pattern interpretation), `external` (imported from an external system). |
| `metadata` | TEXT | Optional JSON string containing additional context. Examples: the number of data points used to compute the metric, the algorithm version, the window size for a moving average. |
| `compressed` | INTEGER | Boolean flag for metadata compression. |
| `created_at` | TEXT | Database write timestamp. |

#### Use Cases for Metric Snapshots

- **Trend analysis:** Dashboard queries can chart `focus_score` over the last 30 days by querying `metric_snapshots` with `metric_name = 'focus_score'` and a time range filter.
- **Threshold alerts:** The cognitive layer can query for metrics that exceed or fall below configurable thresholds and generate insights accordingly.
- **Correlation analysis:** Multiple metric series can be correlated to detect relationships between engagement and learning velocity.
- **Anomaly detection:** A metric that deviates significantly from its historical range may trigger a pattern detection or insight generation.

### 4.3 The insights Table

The `insights` table stores interpreted findings produced by the pattern detector and insight generator. Each insight represents a meaningful conclusion about the Builder's learning state.

```sql
CREATE TABLE insights (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL,
    session_id TEXT,
    type TEXT NOT NULL,
    pattern_id TEXT,
    title TEXT NOT NULL,
    description TEXT,
    confidence REAL NOT NULL,
    severity TEXT NOT NULL,
    source_pattern_type TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    tags TEXT,
    data TEXT,
    created_at TEXT NOT NULL,
    triggered_by_obs_id TEXT,
    dismissed_at TEXT,
    accepted_at TEXT,
    expired_at TEXT,
    metadata TEXT,
    created_at_db TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_ins_builder ON insights(builder_id);
CREATE INDEX idx_ins_status ON insights(status);
CREATE INDEX idx_ins_builder_status ON insights(builder_id, status);
CREATE INDEX idx_ins_severity ON insights(severity);
CREATE INDEX idx_ins_type ON insights(type);
CREATE INDEX idx_ins_builder_created ON insights(builder_id, created_at);
CREATE INDEX idx_ins_builder_type_status ON insights(builder_id, type, status);
CREATE INDEX idx_ins_pattern ON insights(pattern_id);
CREATE INDEX idx_ins_triggered_by ON insights(triggered_by_obs_id);
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT | ULID primary key. |
| `builder_id` | TEXT | The Builder to whom this insight belongs. |
| `session_id` | TEXT | Optional session ID if the insight was generated during an active session. |
| `type` | TEXT | Insight type per ARCH-0031 Section 6.2. Examples: `knowledge_gap`, `momentum`, `burnout_risk`, `strength_identified`, `stagnation_risk`, `goal_proximity`, `topic_mastery`, `learning_style`, `consistency_praise`, `resilience_noted`. |
| `pattern_id` | TEXT | Optional. The ID of the pattern that triggered this insight. Links back to the pattern detector output. |
| `title` | TEXT | Human-readable short title. Examples: "Strong Progress", "Knowledge Gap Detected", "Burnout Risk Increasing". |
| `description` | TEXT | Human-readable detailed explanation. Examples: "You've been consistently scoring above 80% and earning more XP per mission. Your efficiency is improving — keep the momentum going." |
| `confidence` | REAL | Confidence in this insight, from 0.0 to 1.0. Computed from pattern confidence, signal quality, and historical accuracy. |
| `severity` | TEXT | One of: `info`, `suggestion`, `warning`, `achievement`. Maps to the severity classification in ARCH-0031 Section 6.3. Determines how the insight is presented in the dashboard (color, icon, priority). |
| `source_pattern_type` | TEXT | The type of pattern that produced this insight. Examples: `accelerated_progress`, `struggle_area`, `disengagement_risk`. Enables queries like "how many insights were produced from struggle_area patterns?" |
| `status` | TEXT | Current status in the insight lifecycle. Values: `active` (newly generated, visible to the Builder), `dismissed` (Builder explicitly dismissed), `accepted` (Builder accepted, may have led to a recommendation), `expired` (automatically expired after TTL without Builder action). |
| `tags` | TEXT | Optional JSON array of tag strings. Tags enable categorization and filtering. Examples: `["math", "momentum"]`, `["retention-risk", "week-3"]`. Tags are free-form and set by the cognitive layer configuration. |
| `data` | TEXT | Optional JSON payload with additional context. May include the signals and patterns that contributed to this insight, the algorithm version, or debug information. |
| `created_at` | TEXT | ISO 8601 UTC timestamp when the insight was generated. |
| `triggered_by_obs_id` | TEXT | Optional. The ID of the observation that ultimately triggered this insight. Enables traceability from an insight back through patterns, signals, and observations to the root observation. |
| `dismissed_at` | TEXT | ISO 8601 UTC timestamp when the Builder dismissed this insight. Only populated if `status = 'dismissed'`. |
| `accepted_at` | TEXT | ISO 8601 UTC timestamp when the Builder accepted this insight. Only populated if `status = 'accepted'`. |
| `expired_at` | TEXT | ISO 8601 UTC timestamp when this insight automatically expired. Only populated if `status = 'expired'`. |
| `metadata` | TEXT | Optional JSON string for system metadata: algorithm version, processing time, confidence calculation breakdown. |
| `created_at_db` | TEXT | Database write timestamp. |

#### Insight Lifecycle

```
                        ┌──→ accepted ──→ recommendation generated
                        │
active ────────────────┼──→ dismissed (Builder explicitly rejects)
                        │
                        └──→ expired (TTL elapsed, default 30 days)
```

An insight is generated in `active` status. The Builder sees active insights in their dashboard. The Builder may accept an insight (which typically triggers recommendation generation), dismiss it (hides it permanently), or ignore it. If the Builder takes no action within the TTL (default: 30 days), the insight automatically transitions to `expired`.

### 4.4 The recommendations Table

The `recommendations` table stores actionable suggestions produced from insights. Each recommendation tells the Builder what they could do next and why.

```sql
CREATE TABLE recommendations (
    id TEXT PRIMARY KEY,
    insight_id TEXT NOT NULL,
    builder_id TEXT NOT NULL,
    session_id TEXT,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    action_type TEXT NOT NULL,
    action_target TEXT,
    confidence REAL NOT NULL,
    rationale TEXT,
    status TEXT NOT NULL DEFAULT 'pending',
    priority INTEGER NOT NULL DEFAULT 0,
    source_insight_type TEXT,
    data TEXT,
    metadata TEXT,
    created_at TEXT NOT NULL,
    decided_at TEXT,
    ttl_days INTEGER NOT NULL DEFAULT 7,
    expired_at TEXT,
    created_at_db TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (insight_id) REFERENCES insights(id) ON DELETE CASCADE
);

CREATE INDEX idx_rec_builder ON recommendations(builder_id);
CREATE INDEX idx_rec_status ON recommendations(status);
CREATE INDEX idx_rec_builder_status ON recommendations(builder_id, status);
CREATE INDEX idx_rec_insight ON recommendations(insight_id);
CREATE INDEX idx_rec_action_type ON recommendations(action_type);
CREATE INDEX idx_rec_priority ON recommendations(priority);
CREATE INDEX idx_rec_builder_type ON recommendations(builder_id, type);
CREATE INDEX idx_rec_builder_created ON recommendations(builder_id, created_at);
CREATE INDEX idx_rec_builder_status_priority ON recommendations(builder_id, status, priority);
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT | ULID primary key. |
| `insight_id` | TEXT | Foreign key to the `insights` table. The insight that produced this recommendation. |
| `builder_id` | TEXT | The Builder to whom this recommendation belongs. |
| `session_id` | TEXT | Optional session ID if the recommendation was generated during an active session. |
| `type` | TEXT | Recommendation type per ARCH-0031 Section 7.2. Examples: `next_challenge`, `review_content`, `practice_skill`, `explore_topic`, `take_break`, `retry_mission`, `celebrate_milestone`, `adjust_pace`, `deepen_competency`. |
| `title` | TEXT | Human-readable short title. Examples: "Try the Next Mission", "Review Variable Concepts", "Time for a Break". |
| `description` | TEXT | Human-readable detailed explanation. Examples: "You're ready for the next challenge in this journey. Your last 5 missions all scored above 80%." |
| `action_type` | TEXT | The type of action being recommended. One of: `navigate` (go to a specific location), `retry` (re-attempt a mission), `explore` (browse a topic or category), `practice` (engage in practice activity), `rest` (stop — no destination). |
| `action_target` | TEXT | The target of the action. For `navigate`: a route like `/missions/variables-201`. For `retry`: a mission ID. For `explore`: a topic path like `/topics/functions`. For `practice`: a practice path like `/practice/variables`. For `rest`: NULL. |
| `confidence` | REAL | Confidence in this recommendation, from 0.0 to 1.0. Derived from the insight confidence, modified by the Builder's historical response to similar recommendations. |
| `rationale` | TEXT | Human-readable explanation of why this recommendation was generated. Shown to the Builder alongside the recommendation. |
| `status` | TEXT | Current status in the recommendation lifecycle. Values: `pending` (awaiting Builder decision), `accepted` (Builder accepted), `dismissed` (Builder rejected), `expired` (TTL elapsed). |
| `priority` | INTEGER | Display priority. Higher values are shown first. Computed from confidence, severity, time sensitivity, and Builder preferences. |
| `source_insight_type` | TEXT | The type of the parent insight. Denormalized for efficient querying without joining the insights table. |
| `data` | TEXT | Optional JSON payload with additional context. |
| `metadata` | TEXT | Optional JSON string for system metadata. |
| `created_at` | TEXT | ISO 8601 UTC timestamp when the recommendation was generated. |
| `decided_at` | TEXT | ISO 8601 UTC timestamp when the Builder made a decision on this recommendation. Only populated if `status` is `accepted` or `dismissed`. |
| `ttl_days` | INTEGER | Time-to-live in days. Default 7. After this many days without a Builder decision, the recommendation auto-expires. |
| `expired_at` | TEXT | ISO 8601 UTC timestamp of expiry. Computed as `created_at + ttl_days`. |
| `created_at_db` | TEXT | Database write timestamp. |

#### Recommendation Lifecycle

```
                         ┌──→ accepted ──→ decision recorded → outcome tracked
                         │
pending ────────────────┼──→ dismissed (Builder explicitly rejects)
                         │
                         └──→ expired (TTL elapsed, default 7 days)
```

A recommendation is generated in `pending` status. The Builder sees pending recommendations in their dashboard, sorted by priority. The Builder may accept (triggers execution of the action and tracking of the outcome), dismiss (hides permanently), or ignore. If ignored, the recommendation automatically expires after the TTL.

### 4.5 The sessions Table

The `sessions` table stores metadata about Builder sessions. A session is a contiguous period of Builder activity. Sessions are the primary grouping mechanism for observations — every observation belongs to exactly one session.

```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    duration_seconds INTEGER,
    event_count INTEGER DEFAULT 0,
    observation_count INTEGER DEFAULT 0,
    focus_seconds INTEGER DEFAULT 0,
    missions_started INTEGER DEFAULT 0,
    missions_completed INTEGER DEFAULT 0,
    xp_gained REAL DEFAULT 0.0,
    competencies_touched INTEGER DEFAULT 0,
    completion_rate REAL,
    focus_score REAL,
    metadata TEXT,
    tags TEXT,
    summary TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_ses_builder ON sessions(builder_id);
CREATE INDEX idx_ses_started ON sessions(builder_id, started_at);
CREATE INDEX idx_ses_ended ON sessions(ended_at);
CREATE INDEX idx_ses_builder_ended ON sessions(builder_id, ended_at);
CREATE INDEX idx_ses_duration ON sessions(duration_seconds);
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT | ULID primary key. |
| `builder_id` | TEXT | The Builder who conducted this session. |
| `started_at` | TEXT | ISO 8601 UTC timestamp when the session started. Set when `session.started` observation is written. |
| `ended_at` | TEXT | ISO 8601 UTC timestamp when the session ended. Set when `session.ended` observation is written. NULL if the session is still active (e.g., the Builder closed the app without ending the session). |
| `duration_seconds` | INTEGER | Total session duration in seconds. Computed as `ended_at - started_at` when the session ends. |
| `event_count` | INTEGER | Total number of Runtime events during this session. Updated incrementally as events are processed. |
| `observation_count` | INTEGER | Total number of observations generated during this session. Includes all sources: runtime, cognitive, builder. |
| `focus_seconds` | INTEGER | Estimated seconds of active focus during the session. Computed by subtracting idle time from total duration. Idle detection is based on time between observations — gaps longer than a configurable threshold (default: 5 minutes) are considered idle. |
| `missions_started` | INTEGER | Number of missions started during this session. |
| `missions_completed` | INTEGER | Number of missions completed during this session. |
| `xp_gained` | REAL | Total XP earned during this session. |
| `competencies_touched` | INTEGER | Number of distinct competencies engaged during this session. |
| `completion_rate` | REAL | Ratio of missions completed to missions started. NULL if no missions were started. |
| `focus_score` | REAL | Ratio of focus seconds to total duration. A value of 0.8 means the Builder was actively focused 80% of the session time. |
| `metadata` | TEXT | Optional JSON string with additional session context. Examples: device type, ASCEND version, UI theme, locale. |
| `tags` | TEXT | Optional JSON array of tags. Examples: `["morning", "weekday"]`, `["deep-focus"]`. |
| `summary` | TEXT | Optional human-readable summary generated at session end. Example: "You completed 3 missions, earned 450 XP, and maintained 85% focus over 45 minutes." Generated by the cognitive layer. |
| `created_at` | TEXT | Database write timestamp. |

#### Session Lifecycle

A session begins when the Builder starts an activity (launches the app, begins a learning session). The cognitive layer writes a `session.started` observation and creates a row in the `sessions` table with `started_at` set and `ended_at` NULL.

Throughout the session, observations are written with the session ID. The `sessions` row accumulates metadata — event count, mission counts, XP gained — via periodic updates. These periodic updates are the only writes to a pre-existing row in the entire schema. They are justified because the session row is aggregated metadata, not a raw observation.

When the session ends (Builder closes the app, explicitly ends the session, or after an inactivity timeout), the cognitive layer writes a `session.ended` observation, finalizes the metadata (`ended_at`, `duration_seconds`), and generates a summary.

Sessions that never receive an `ended_at` (e.g., crash, abrupt shutdown) are considered "open" sessions. On next startup, the cognitive layer checks for open sessions older than a configurable threshold (default: 24 hours) and closes them automatically with `ended_at = last_observation_timestamp`.

### 4.6 The snapshots Table

The `snapshots` table stores compressed state snapshots of the Builder's cognitive state at points in time. Snapshots are the foundation of the replay mechanism.

```sql
CREATE TABLE snapshots (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL,
    session_id TEXT,
    snapshot_type TEXT NOT NULL,
    data TEXT NOT NULL,
    schema_version INTEGER NOT NULL DEFAULT 1,
    timestamp TEXT NOT NULL,
    previous_snapshot_id TEXT,
    observation_id TEXT,
    observation_count INTEGER,
    compressed_size INTEGER,
    original_size INTEGER,
    compression_algorithm TEXT DEFAULT 'gzip',
    checksum TEXT,
    data_format TEXT DEFAULT 'json',
    metadata TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_snap_builder ON snapshots(builder_id);
CREATE INDEX idx_snap_time ON snapshots(builder_id, timestamp);
CREATE INDEX idx_snap_type ON snapshots(snapshot_type);
CREATE INDEX idx_snap_session ON snapshots(session_id);
CREATE INDEX idx_snap_builder_type ON snapshots(builder_id, snapshot_type);
CREATE INDEX idx_snap_builder_time_type ON snapshots(builder_id, timestamp, snapshot_type);
CREATE INDEX idx_snap_prev ON snapshots(previous_snapshot_id);
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | TEXT | ULID primary key. |
| `builder_id` | TEXT | The Builder whose state is captured. |
| `session_id` | TEXT | Optional session ID if the snapshot was captured during a session. |
| `snapshot_type` | TEXT | One of: `full` (complete Builder cognitive state), `delta` (changes since the last snapshot), `metrics` (metric snapshot bundle). |
| `data` | TEXT | The snapshot payload. For JSON format, this is a JSON string. Always compressed (gzip) unless the uncompressed size is below a configurable threshold (default: 1 KB). |
| `schema_version` | INTEGER | Version of the snapshot data schema. Enables forward compatibility across schema changes. |
| `timestamp` | TEXT | ISO 8601 UTC timestamp of the snapshot capture time. |
| `previous_snapshot_id` | TEXT | The ID of the previous snapshot in the chain. For full snapshots, this points to the previous full snapshot. For delta snapshots, this points to the previous snapshot (full or delta) in sequence. NULL for the first snapshot. |
| `observation_id` | TEXT | Optional. The ID of the observation that triggered this snapshot. Enables traceability from snapshot back to the event that caused it. |
| `observation_count` | INTEGER | The total number of observations that had been processed for this Builder at the time of the snapshot. Used by the replay engine to verify completeness. |
| `compressed_size` | INTEGER | Byte size of the `data` field after compression. |
| `original_size` | INTEGER | Byte size of the `data` field before compression. |
| `compression_algorithm` | TEXT | The algorithm used for compression. Default: `gzip`. |
| `checksum` | TEXT | SHA-256 checksum of the `data` field before compression. Used for integrity verification during replay. |
| `data_format` | TEXT | The serialization format. Default: `json`. Future extensions may include `msgpack` or `protobuf`. |
| `metadata` | TEXT | Optional JSON string with additional context: capture trigger, processing time, component versions. |
| `created_at` | TEXT | Database write timestamp. |

#### Snapshot Chain

Snapshots form a chain linked by `previous_snapshot_id`. The chain structure enables efficient storage (deltas are smaller than full snapshots) while supporting full state reconstruction.

```
Full Snapshot (t=100) ←── Delta Snapshot (t=110) ←── Delta Snapshot (t=120) ←── Full Snapshot (t=200)
```

To reconstruct state at t=120:
1. Load the full snapshot at t=100
2. Apply delta from t=110
3. Apply delta from t=120

The chain is anchored by full snapshots. Full snapshots represent complete Builder state. They are captured periodically (every 100 observations or at session end, whichever comes first) and are the entry points for replay. Delta snapshots capture only the changes since the previous snapshot in the chain. They are captured more frequently (every 10 observations) to minimize the number of observations that must be replayed, while avoiding the storage cost of full snapshots on every capture.

If a delta snapshot is lost or corrupted, the chain is not broken beyond repair — the replay engine can fall back to the previous full snapshot and replay all observations from that point, ignoring the corrupted delta. This graceful degradation is a design requirement.

---

## 5. Compression

Compression reduces storage footprint with minimal performance impact. The design uses two complementary strategies: per-field compression for large payloads and per-snapshot compression for state captures.

### 5.1 Observation Data Compression

The `data` field in the `observations` table is stored as a JSON string. For small payloads (under 10 KB), compression is not worth the CPU overhead — the JSON is stored as plain text. For payloads that exceed 10 KB, the data is compressed using zlib at compression level 6 (default level, balancing speed and ratio).

Compressed data is encoded as base64 for storage in the TEXT column. The `compressed` flag is set to 1, and `original_size` records the uncompressed byte count. On read, the application checks the `compressed` flag and decompresses if needed.

The 10 KB threshold was chosen based on empirical analysis of observation payload sizes. Typical observation payloads (mission completed, evidence submitted) are 200–500 bytes of JSON. Only observations with large data payloads — such as state dumps, debug attachments, or content snapshots — exceed 10 KB. In practice, fewer than 1% of observations trigger compression, so the CPU overhead is negligible.

### 5.2 Snapshot Compression

All snapshots are compressed using gzip at compression level 9 (maximum compression, since snapshots are written infrequently and read even less frequently). Gzip was chosen for snapshots because:

- Gzip achieves better compression ratios than zlib at maximum level (typically 10–20% better for JSON data).
- Gzip is widely supported across all platforms and languages.
- The decompression speed is still fast enough for replay (a 1 MB snapshot decompresses in under 10 ms on modern hardware).

Expected compression ratios for snapshot data:

| Data Type | Typical Size | Compressed Size | Ratio |
|-----------|-------------|-----------------|-------|
| Full snapshot (JSON) | 50–100 KB | 8–15 KB | 6:1 to 7:1 |
| Delta snapshot (JSON) | 5–15 KB | 1–3 KB | 5:1 |
| Metric bundle (JSON) | 5–10 KB | 1–2 KB | 5:1 |

### 5.3 Decompression Cache

To avoid repeated decompression of the same snapshot during replay, a memory cache stores decompressed snapshots. The cache is LRU (least recently used) with a maximum of 10 entries. Since replay typically reads snapshots sequentially (from earliest to latest), the cache hit rate is high — each snapshot is decompressed once and then used for replaying the subsequent observations.

### 5.4 Integrity Verification

Checksums ensure data integrity. Before compression, the system computes a SHA-256 checksum of the raw data. The checksum is stored alongside the compressed data. On read, the system decompresses the data, recomputes the checksum, and compares it to the stored value. If the checksums do not match, the data has been corrupted and the system falls back to the nearest uncorrupted snapshot or observation.

Checksum verification is optional and configurable. It is enabled by default for snapshots (which are critical for replay) and disabled by default for observation payloads (which are typically small and low-risk). The Builder can enable observation checksums for maximum integrity at the cost of CPU overhead.

---

## 6. Snapshots

Snapshots are the backbone of the replay mechanism. They provide recovery points that minimize the number of observations that must be replayed to reconstruct state.

### 6.1 Snapshot Types

Two types of snapshots are captured:

**Full Snapshots**

A full snapshot contains the complete cognitive state of the Builder at a point in time. This includes:
- The current Builder profile (level, XP, competencies)
- Active session state
- Active insight and recommendation state
- The last sequence number processed
- A digest of recent metrics (last 100 metric snapshots)
- Configuration and preference state

Full snapshots are captured:
- Every 100 observations (configurable)
- At session end
- On explicit request (API or CLI command)
- Before a schema migration

The 100-observation threshold balances storage cost against replay speed. With 100 observations between full snapshots and an average of 10 observations per day, a full snapshot is captured roughly every 10 days. This means replaying a session requires loading at most one full snapshot and replaying at most 100 observations — a negligible computational cost.

**Delta Snapshots**

A delta snapshot contains only the state that changed since the previous snapshot (full or delta). Delta snapshots are captured every 10 observations (configurable). They are significantly smaller than full snapshots — typically 10–20% of the size.

The delta encoding is simple: the cognitive layer computes the difference between the current state and the state at the last snapshot, serializes only the changed portions, and stores the delta. The delta format is a JSON object with only the changed keys. For example:

```json
{
  "xp": 1250,
  "level": 3,
  "lastMissionId": "variables-201",
  "metrics.focus_score": 0.85
}
```

This delta indicates that only four fields changed since the last snapshot. The replay engine applies this delta to the reconstructed state by updating only the specified keys.

### 6.2 Capture Trigger

Snapshots are captured asynchronously. After each observation is written, the cognitive layer checks whether a snapshot threshold has been reached:

```
IF observation_count % 10 == 0 THEN capture_delta_snapshot()
IF observation_count % 100 == 0 THEN capture_full_snapshot()
```

Snapshot capture runs on a background thread to avoid blocking the observation write path. If a capture is in progress when a new observation arrives, the capture completes first; the new observation is buffered and written after the snapshot is persisted.

### 6.3 Snapshot Retention

Snapshots are retained according to the retention policy in Section 9. When snapshots are pruned, the chain is maintained by updating `previous_snapshot_id` references. Specifically, pruning removes old full snapshots but keeps at least one full snapshot within the retention window. If the oldest retained snapshot is a delta, it is converted to a full snapshot before the preceding snapshot is deleted.

---

## 7. Replay

Replay is the process of reconstructing Builder state at a specific point in time by combining snapshots and observations. It is the definitive mechanism for session reproducibility.

### 7.1 Replay Algorithm

To replay a Builder session or time range, the system executes the following algorithm:

```
1. Determine the target time T (or session ID S)
2. If session ID S:
     a. Find the session start time from the sessions table
     b. Set T = session start time
3. Find the most recent full snapshot at or before T:
     SELECT * FROM snapshots
     WHERE builder_id = B
       AND snapshot_type = 'full'
       AND timestamp <= T
     ORDER BY timestamp DESC
     LIMIT 1
4. If no full snapshot exists:
     a. Start from empty state
     b. Load ALL observations for builder B with timestamp <= T
     c. Apply each observation in sequence_number order
     d. Return reconstructed state
5. If full snapshot exists:
     a. Load and decompress the full snapshot data
     b. Set current_state = snapshot.data
     c. Load all delta snapshots between snapshot.timestamp and T:
          SELECT * FROM snapshots
          WHERE builder_id = B
            AND snapshot_type = 'delta'
            AND timestamp > snapshot.timestamp
            AND timestamp <= T
          ORDER BY timestamp ASC
     d. For each delta snapshot:
          Apply delta to current_state
     e. Load all observations between last_snapshot.timestamp and T:
          SELECT * FROM observations
          WHERE builder_id = B
            AND sequence_number > last_snapshot_sequence
            AND timestamp <= T
          ORDER BY sequence_number ASC
     f. For each observation:
          Apply observation to current_state
     g. Return reconstructed state
```

### 7.2 Determinism Guarantee

Replay is deterministic under the following conditions:

1. **Same observations:** The same set of observations, in the same order, must produce the same state. This is guaranteed by gapless sequence numbers per Builder.
2. **Same snapshot chain:** The same snapshot chain must produce the same starting state. This is guaranteed by checksum-verified snapshot data.
3. **Same pipeline version:** The same cognitive pipeline version must process the observations. If the pipeline is upgraded, replay may produce different results for the same observations. This is expected — the new pipeline is a different version and may extract different signals or detect different patterns.

The system records the cognitive pipeline version in the `metadata` field of each observation (via `metada.observationSchema`). Replay can use this version information to route observations through the correct version of the pipeline if multiple versions are installed.

### 7.3 Replay Use Cases

**Session Reconstruction**

The most common replay use case. Given a session ID, reconstruct the Builder's state at any point during that session. The dashboard uses this to display "what my state was at this moment in the session."

**Pipeline Upgrade Replay**

When the cognitive pipeline is upgraded, the Builder may choose to replay their historical sessions through the new pipeline to generate updated insights. The original observations are preserved (they are immutable), and the new pipeline produces new insights, recommendations, decisions, and outcomes. These are stored alongside the originals, differentiated by pipeline version.

**Debugging**

A developer reproduces a bug by replaying a session locally. The replay engine loads the observations, runs them through the pipeline in debug mode, and outputs intermediate state at each step. The developer can inspect the exact sequence of observations, signals, patterns, insights, and recommendations that led to a bug.

**Audit**

A Builder or administrator replays a session to verify that the cognitive layer behaved correctly. The replay output is compared to the original outputs. Any discrepancy is flagged for investigation.

### 7.4 Replay Performance

Replay performance depends on the number of observations and snapshots in the time range. Typical performance:

| Range | Observations | Snapshots | Time |
|-------|-------------|-----------|------|
| Single session (30 min) | 10–50 | 0–2 | < 10 ms |
| Single day | 50–200 | 2–10 | < 50 ms |
| Single week | 350–1400 | 14–70 | < 500 ms |
| Single month | 1500–6000 | 60–300 | < 5 s |
| Full history (1 year) | 18000–73000 | 720–3650 | < 60 s |

These estimates assume a standard desktop CPU and the default snapshot frequency. Replay time scales linearly with observation count. The snapshot chain optimization reduces replay time by a factor of approximately 100 compared to replaying without snapshots (i.e., processing every observation from the beginning of time).

### 7.5 Replay API

The cognitive layer exposes a replay API through the Runtime:

```
replay(session_id: str) -> BuilderState
replay_time(builder_id: str, timestamp: str) -> BuilderState
replay_range(builder_id: str, from_timestamp: str, to_timestamp: str) -> list[Observation]
```

Each function returns a complete snapshot of the Builder's cognitive state at the requested point, plus a list of all observations in the range for the range query.

---

## 8. Aggregation

Aggregations pre-compute summary data for dashboard performance. Without aggregations, every dashboard query would require scanning thousands of observations and computing statistics in real time — an acceptable but suboptimal approach.

### 8.1 Aggregation Strategy

Two strategies are supported, configurable by deployment:

**Strategy A: Pre-computed Aggregation Table**

A dedicated `aggregations` table stores pre-computed summaries that are updated periodically:

```sql
CREATE TABLE aggregations (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL,
    aggregation_type TEXT NOT NULL,
    period TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    data TEXT NOT NULL,
    computed_at TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_agg_builder ON aggregations(builder_id);
CREATE INDEX idx_agg_type ON aggregations(aggregation_type);
CREATE INDEX idx_agg_period ON aggregations(builder_id, period, period_start);
```

| Field | Description |
|-------|-------------|
| `aggregation_type` | The type of aggregation. Values: `daily_event_counts`, `hourly_activity`, `weekly_metric_averages`, `monthly_trends`, `top_insight_types`, `recommendation_success_rate`. |
| `period` | The time period granularity: `hourly`, `daily`, `weekly`, `monthly`. |
| `period_start` | ISO 8601 start of the period. |
| `period_end` | ISO 8601 end of the period. |
| `data` | JSON payload with the aggregated data. Structure depends on `aggregation_type`. |

Aggregations are computed on a schedule:
- Hourly aggregations: computed every hour
- Daily aggregations: computed at midnight
- Weekly aggregations: computed at end of week (Sunday 23:59)
- Monthly aggregations: computed at end of month

The computation queries the raw observations and metric snapshots, computes the aggregations, and writes them to the table. If a computation fails, it is retried on the next cycle. If a computation succeeds but the period is not yet complete (e.g., computing a daily aggregation at 2 PM), the existing partial aggregation is replaced with the new partial aggregation.

**Strategy B: On-the-Fly Computation**

For deployments that prefer simplicity over performance, aggregations are computed on-the-fly from the `observations` and `metric_snapshots` tables. The computation caches results in memory for a configurable TTL (default: 5 minutes). This strategy requires no additional tables but adds query latency for dashboard views.

Strategy B is the default for local-first deployments where query volume is low (one Builder). Strategy A is recommended for multi-Builder deployments or when the dashboard is accessed frequently.

### 8.2 Aggregation Types

**Daily Event Counts**

For each day, the count of observations grouped by type. Enables the dashboard to show "You had 15 events yesterday: 10 missions, 3 evidence submissions, 2 insights."

Computation: `SELECT type, COUNT(*) FROM observations WHERE builder_id = ? AND date(timestamp) = ? GROUP BY type`

**Hourly Activity Heatmap**

For each hour of the day, the count of observations. Enables the dashboard to show "Your most productive hours are 10 AM and 3 PM."

Computation: `SELECT strftime('%H', timestamp) AS hour, COUNT(*) FROM observations WHERE builder_id = ? GROUP BY hour`

**Weekly Metric Averages**

For each week, the average value of each metric. Enables trend charts showing "Your focus score has been stable at 0.72 for the last 4 weeks."

Computation: `SELECT metric_name, AVG(value) FROM metric_snapshots WHERE builder_id = ? AND timestamp >= week_start AND timestamp < week_end GROUP BY metric_name`

**Monthly Trend Data**

For each month, the aggregate of key metrics and observation counts. Enables long-term trend analysis.

Computation: Similar to weekly averages but grouped by month.

### 8.3 Aggregation Lifecycle

Aggregations are invalidated when:
- New observations are written for a past period (unusual in an append-only system, but possible with delayed or synced observations)
- The retention window shifts and data is pruned
- The Builder deletes observations

Invalidation marks the affected aggregation rows as `stale`. On the next computation cycle, stale rows are recomputed. If a Builder deletes observations, all affected aggregations are immediately marked stale and recomputed on the next cycle.

---

## 9. Retention Policy

Retention governs how long data is kept before being eligible for deletion. The retention policy is configurable per Builder, with sensible defaults that balance historical value against storage cost.

### 9.1 Default Retention Windows

| Entity | Default Retention | Justification |
|--------|------------------|---------------|
| Observations | 90 days | Observations are the rawest data. Beyond 90 days, the probability of needing to replay a specific observation diminishes rapidly. The snapshot chain preserves the derived state beyond 90 days even after observations are pruned. |
| Metric snapshots | 180 days | Metric data supports longer trend analysis. 180 days provides half a year of trend data, which is sufficient for most pattern detection algorithms. |
| Insights | 365 days | Insights are the highest-value cognitive artifacts. A Builder may want to review insights from a year ago to see their growth trajectory. |
| Recommendations | 365 days | Recommendations paired with insights provide a complete picture of what was suggested and what was decided. |
| Sessions | 180 days | Session metadata supports analysis of learning habits. 180 days captures seasonal patterns without unbounded growth. |
| Snapshots (full) | 365 days | Full snapshots enable replay of any session within the last year. If a Builder wants to replay a session from 13 months ago, they can do so, but the replay engine will need to process all observations from the beginning (no snapshot shortcut). |
| Snapshots (delta) | 90 days | Delta snapshots are intermediate optimization. Beyond 90 days, only full snapshots are needed — the replay engine can load a full snapshot and replay observations from there. |
| Decisions | 365 days | Decisions record Builder agency. They are cognitive history that the Builder may want to reference. |
| Outcomes | 365 days | Outcomes close the cognitive cycle. They are essential for measuring recommendation effectiveness over time. |
| Aggregations | 90 days | Aggregations are recomputed from source data. They can be regenerated at any time, so retention is primarily a cache management concern. |

### 9.2 Deletion Behavior

Deletion follows a two-phase approach:

**Phase 1: Soft-Delete**

When data reaches its retention limit, it is first soft-deleted. Soft-delete marks the row as deleted (by setting a `deleted_at` field or moving it to a shadow table) but does not remove it from disk. The data remains recoverable for a grace period of 30 days.

Soft-delete enables:
- Undo: The Builder can undo a deletion within the grace period.
- Recovery: If a bug causes premature deletion, the data can be recovered from the shadow table.
- Audit: The deletion log records what was deleted and when.

**Phase 2: Hard-Delete**

After the 30-day grace period, soft-deleted data is hard-deleted. The rows are physically removed from the table, and the database page is freed for reuse. Hard-delete is irreversible.

### 9.3 Export Before Deletion

Before any hard-delete, the system checks whether the Builder has exported the data being deleted. The check is simple:

- The system maintains a log of export operations, recording the `max_timestamp` of exported data per entity type.
- Before deleting data, the system compares the deletion range to the exported range.
- If the Builder has never exported the data, or if the data to be deleted is outside the exported range, the system optionally warns the Builder and offers to export before deleting.
- The export-before-delete feature is configurable. By default, it is enabled with a non-blocking warning. The Builder can disable the warning or change it to a blocking requirement.

### 9.4 Overriding Retention

The Builder can override the default retention for any entity type. Overrides are stored in the configuration file (`~/.ascend/config.toml` or `%APPDATA%\Ascend\config.toml`):

```toml
[storage.retention]
observations = 180       # override: 180 days
insights = 730           # override: 2 years
snapshots_full = 730     # override: 2 years
```

Valid values for retention: any positive integer (days), `0` (immediate hard-delete of data older than 1 day), or `-1` (keep forever — the system will warn about unbounded storage growth but will not delete).

### 9.5 Retention Enforcement

Retention is enforced by the pruning subsystem (Section 10). Pruning runs on a schedule and applies the retention policy to all entities. Pruning respects the soft-delete grace period and export-before-delete check.

---

## 10. Pruning

Pruning is the automated process that enforces the retention policy. It runs on a configurable schedule, identifies expired data, and removes it according to the deletion behavior defined in Section 9.

### 10.1 Pruning Schedule

Pruning runs daily by default. The schedule is configurable:

```toml
[storage.pruning]
schedule = "daily"              # "daily", "weekly", "hourly", or a cron expression
time = "03:00"                  # time of day (local time)
```

The default time of 3:00 AM is chosen because it is typically a period of low activity. If the Builder's device is off at the scheduled time, pruning runs on the next startup.

### 10.2 Pruning Algorithm

```
1. Load retention policy (defaults + Builder overrides)
2. For each entity type with retention >= 0:
     a. Compute cutoff date = now - retention_days
     b. Phase 1: Find all rows older than cutoff that are NOT soft-deleted:
          SELECT COUNT(*) FROM entity
          WHERE builder_id = ?
            AND timestamp < cutoff
            AND deleted_at IS NULL
     c. If count > 0:
          If export_before_delete check passes (or is disabled):
            UPDATE entity SET deleted_at = now()
            WHERE builder_id = ?
              AND timestamp < cutoff
              AND deleted_at IS NULL
     d. Phase 2: Find all rows with deleted_at < now - 30_days:
          DELETE FROM entity
          WHERE deleted_at IS NOT NULL
            AND deleted_at < now - 30_days
3. Log pruning results:
     Entity type, rows soft-deleted, rows hard-deleted, size recovered
```

### 10.3 Pruning Log

Every pruning cycle writes a log entry. The log is stored in the same database in a `pruning_log` table:

```sql
CREATE TABLE pruning_log (
    id TEXT PRIMARY KEY,
    run_at TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    soft_deleted INTEGER NOT NULL DEFAULT 0,
    hard_deleted INTEGER NOT NULL DEFAULT 0,
    size_recovered_bytes INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'completed',
    error TEXT,
    duration_ms INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX idx_prune_time ON pruning_log(run_at);
CREATE INDEX idx_prune_entity ON pruning_log(entity_type);
```

The Builder can inspect the pruning log to understand what data has been removed and when.

### 10.4 Pruning Safeguards

Several safeguards prevent accidental data loss:

- **Export check:** Pruning does not hard-delete data that has not been exported (if export-before-delete is enabled).
- **Minimum retention floor:** Regardless of the Builder's override, no data is deleted within the first 24 hours of creation. This prevents accidental deletion of data that was just written.
- **Consistency check:** Before hard-deleting snapshots, pruning verifies that the snapshot chain remains valid. If deleting a snapshot would break the chain, the snapshot is retained until the next full snapshot is captured.
- **Graceful abort:** If pruning encounters an error (disk full, database locked, export check failure), it logs the error and aborts gracefully. No partial deletions occur — the pruning cycle is atomic per entity type.

### 10.5 Manual Pruning

The Builder can trigger pruning manually via the CLI:

```
ascend cognitive prune
ascend cognitive prune --entity observations --older-than 30
ascend cognitive prune --dry-run
```

The `--dry-run` flag reports what would be deleted without actually deleting anything. The manual prune respects the same safeguards as automated pruning.

---

## 11. Migration

Schema migrations enable the Observation Storage schema to evolve over time without data loss.

### 11.1 Schema Versioning

The schema version is stored in a metadata table:

```sql
CREATE TABLE schema_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

INSERT INTO schema_metadata (key, value) VALUES ('schema_version', '1');
INSERT INTO schema_metadata (key, value) VALUES ('app_version', '1.0.0');
INSERT INTO schema_metadata (key, value) VALUES ('created_at', datetime('now'));
```

On startup, the application reads `schema_version`. If the version is less than the current version expected by the application, migration scripts are applied in order.

### 11.2 Migration Scripts

Migration scripts are stored in `infrastructure/migrations/cognitive/`. Each script is named with a version prefix:

```
001_initial_schema.sql
002_add_tags_to_insights.sql
003_add_compression_flag.sql
004_add_pruning_log.sql
```

Scripts are SQL files that contain:
- ALTER TABLE statements (adding columns, creating indexes)
- CREATE TABLE statements (new tables)
- UPDATE statements (data migration)
- INSERT statements (updating schema_metadata version)

Migrations are forward-only. There is no downgrade path. If a migration fails, the application logs the error and stops — the database is left in its pre-migration state. The administrator must resolve the issue (typically a migration script bug) and restart the application.

### 11.3 Migration on Startup

The migration process runs on every application startup:

```
1. Read schema_version from schema_metadata
2. If schema_version == current_version:
     Skip migration, proceed to normal startup
3. If schema_version < current_version:
     For each migration script from schema_version+1 to current_version:
       a. Begin transaction
       b. Execute migration script
       c. Update schema_version in schema_metadata
       d. Commit transaction
       e. Log migration success
4. If schema_version > current_version:
     Log warning: "Database schema version X is newer than application version Y"
     Proceed with normal startup (backward compatible)
```

### 11.4 Migration Safety

Migrations are designed to be safe for the following reasons:

- **Atomic:** Each migration runs in a single transaction. If it fails, the database is unchanged.
- **Idempotent (where possible):** CREATE TABLE IF NOT EXISTS and CREATE INDEX IF NOT EXISTS are preferred over bare CREATE statements. ALTER TABLE ADD COLUMN is idempotent — adding a column that already exists is a no-op.
- **Backward compatible:** New columns have DEFAULT values so that old rows are valid without updates. New tables are optional — the application works without them (features that depend on new tables check for their existence).
- **Tested:** Every migration script is tested against a copy of the production database schema before deployment.

### 11.5 Data Migration

Some schema changes require data migration — for example, moving data from an old column to a new column, or recomputing a stored value. Data migration steps are included in the migration scripts as UPDATE statements. For large databases, data migration may be slow. The application shows a progress indicator during startup if data migration is anticipated to take more than 5 seconds.

---

## 12. Storage Budget

The storage budget estimates the disk footprint of Observation Storage per Builder over time. All estimates assume default retention windows and average usage of 10 observations per day.

### 12.1 Per-Builder Estimates

| Entity | 90 Days | 180 Days | 365 Days |
|--------|---------|----------|----------|
| Observations (900 rows) | 500 KB | 1 MB | 2 MB |
| Observations (compressed) | 100 KB | 200 KB | 400 KB |
| Metric snapshots (180 rows) | 50 KB | 100 KB | 200 KB |
| Insights (30 rows) | 30 KB | 60 KB | 120 KB |
| Recommendations (60 rows) | 40 KB | 80 KB | 160 KB |
| Sessions (90 rows) | 50 KB | 100 KB | 200 KB |
| Snapshots (full: ~10 / 90d) | 150 KB | 300 KB | 600 KB |
| Snapshots (delta: ~90 / 90d) | 90 KB | 180 KB | 360 KB |
| Aggregations | 30 KB | 60 KB | 120 KB |
| Indexes overhead | 100 KB | 200 KB | 400 KB |

**Total (uncompressed):** ~1.1 MB / 90 days, ~2.1 MB / 180 days, ~4.2 MB / 365 days

**Total (compressed):** ~750 KB / 90 days, ~1.4 MB / 180 days, ~2.8 MB / 365 days

### 12.2 Worst-Case Estimates

A power user generating 100 observations per day (10x the average):

| Period | Uncompressed | Compressed |
|--------|-------------|------------|
| 90 days | ~11 MB | ~7.5 MB |
| 365 days | ~44 MB | ~28 MB |

### 12.3 Database File Overhead

SQLite adds overhead beyond the raw data:
- WAL file: typically 1–4 MB (capped at a configurable size)
- Index pages: additional 20–30% of data size
- Free pages: variable, pruned by `PRAGMA auto_vacuum = INCREMENTAL`

Estimated total database file size for an average Builder after 1 year: 5–10 MB (compressed, including overhead).

### 12.4 Long-Term Growth

With default 90–365 day retention, the database reaches a steady state where pruning removes data at approximately the same rate as new data is written. Steady-state database size:

| Usage Level | Steady-State Size |
|-------------|-------------------|
| Average (10 obs/day) | 3–5 MB |
| Moderate (30 obs/day) | 10–15 MB |
| Power user (100 obs/day) | 30–50 MB |

At steady state, storage does not grow unboundedly. The retention policy ensures that old data is pruned at the same rate as new data is added, keeping the database file at a predictable, manageable size.

---

## 13. Data Sovereignty

Consistent with DOC-0009 Architectural Invariants (I8: Data belongs to the user), Observation Storage is designed for full Builder sovereignty.

### 13.1 Export Format

The export format is JSON Lines (one JSON object per line). Each line represents one entity. The first line is a header:

```jsonl
{"export_version": "1.0", "created_at": "2026-07-21T00:00:00Z", "builder_id": "bld-42", "entity_count": 1234}
{"entity": "observation", "id": "01F8Z...", "type": "mission.completed", ...}
{"entity": "metric_snapshot", "id": "01F8Z...", "metric_name": "focus_score", ...}
```

The Builder can export using the CLI:

```
ascend cognitive export --format jsonl --output ~/ascend-export-2026-07-21.jsonl
ascend cognitive export --entity observations --older-than 90 --format jsonl
ascend cognitive export --all --format jsonl --output ~/ascend-full-export.jsonl
```

### 13.2 Import

The Builder can import an export file into another ASCEND instance:

```
ascend cognitive import --file ~/ascend-export-2026-07-21.jsonl
```

Import is idempotent — duplicate IDs are skipped with a warning. Import restores all entities to the new database.

### 13.3 Deletion

The Builder can delete their data:

```
ascend cognitive delete --all                    # Delete all cognitive data
ascend cognitive delete --entity observations     # Delete only observations
ascend cognitive delete --older-than 30          # Delete data older than 30 days
```

Deletion respects the soft-delete and hard-delete lifecycle (Section 9.2). After soft-delete, the Builder can undo within 30 days.

### 13.4 Anonymization

For Builders who wish to contribute aggregate data (with explicit opt-in), observations can be anonymized before export. Anonymization replaces `builder_id` with a random hash, strips `session_id`, and removes any PII from the `data` JSON payload. The anonymized export contains no personally identifiable information.

---

## 14. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — complete Observation Storage architecture |
