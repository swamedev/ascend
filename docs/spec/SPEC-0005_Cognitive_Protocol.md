# SPEC-0005 — ASCEND Cognitive Protocol (ACP) v1.0

**Status:** Draft  
**Version:** 0.1.0  
**License:** MIT  

---

## 1. Purpose

ACP defines the protocol that governs all communication between the Cognitive Layer and the Runtime. The protocol ensures that:

- The Runtime remains completely sovereign — no external component can mutate its state
- The Cognitive Layer is a read-only observer that never writes to Runtime data stores
- Any AI model can be plugged in or out without changing a single line of Runtime code
- All communication is typed, structured, and auditable via a canonical message envelope
- The system functions correctly with zero AI models installed

ACP is derived from Architectural Invariants I5 (AI never alters business rules), I6 (core works without internet), and I9 (layers communicate inward only). It is the protocol counterpart to SPEC-0004 (AAP), which governs agent-to-Runtime communication for assessment, while ACP governs Cognitive-Layer-to-Runtime communication for observation, query, and insight.

---

## 2. Core Principle

```
Cognitive Layer → [OBSERVES] → Runtime
Cognitive Layer → [REQUESTS] → Runtime (read-only queries)
Cognitive Layer → [RECOMMENDS] → Experience Layer (never writes to Runtime)

Runtime → [PUBLISHES] → Events (consumed by Cognitive Layer)
Runtime → [RESPONDS] → Queries (served to Cognitive Layer)
```

The Cognitive Layer has three and only three relationships with the rest of the system:

1. **Observation** — It consumes domain events published by the Runtime and converts them into internal Observations.
2. **Query** — It requests read-only snapshots of Runtime state through a restricted adapter interface.
3. **Insight** — It publishes derived insights, recommendations, and alerts to the Experience Layer, which may choose to display or act on them. It never writes back to the Runtime.

The Runtime has two and only two outward-facing responsibilities toward the Cognitive Layer:

1. **Publish** — Emit domain events to the event bus for any component subscribed to them.
2. **Respond** — Serve read-only queries through the Query Interface.

---

## 3. Communication Channels

ACP defines three canonical channels. Every message on every channel uses the same envelope format (see Section 4).

### Channel 1 — Event Stream (Runtime → Cognitive)

| Property | Value |
|---|---|
| Direction | Runtime → Cognitive Layer |
| Pattern | Publish / Subscribe |
| Delivery | Async, fire-and-forget |
| Acknowledgement | Required (cognitive layer acknowledges receipt) |
| Retry | None (Runtime does not retry) |
| Payload | ASCEND Domain Event (per domain event schema) |

The Runtime publishes domain events to an internal event bus. The Cognitive Layer subscribes to event types it cares about, receives them via callback, and converts each event into an internal Observation. Events are fire-and-forget from the Runtime's perspective — once published, the Runtime does not track delivery. The Cognitive Layer is responsible for replay and gap detection on restart.

### Channel 2 — Query Interface (Cognitive → Runtime)

| Property | Value |
|---|---|
| Direction | Cognitive Layer → Runtime |
| Pattern | Request / Response |
| Delivery | Synchronous (blocking) |
| Rate Limit | Configurable per builder (default: 60 req/min) |
| Mutations | Forbidden — all queries are read-only |

The Cognitive Layer queries Runtime state through a restricted set of adapter methods. Only getter methods are exposed — no create, update, or delete operations. The Query Interface is a strict subset of the Runtime Adapter. Rate limiting prevents thundering herd scenarios.

### Channel 3 — Insight Stream (Cognitive → Experience)

| Property | Value |
|---|---|
| Direction | Cognitive Layer → Experience Layer |
| Pattern | Push |
| Delivery | Async with optional acknowledgment |
| Validation | Experience Layer validates before acting on any insight |

The Cognitive Layer publishes Insights (observations with meaning), Recommendations (actionable suggestions), and Alerts (critical conditions) to the Experience Layer. The Experience Layer is free to display, ignore, or act on these messages. Insights are advisory only — the Experience Layer always validates before applying any change to the system.

---

## 4. Message Format

Every message across every channel uses the canonical ASCEND Cognitive Protocol envelope:

```typescript
interface CognitiveMessage {
  protocol: 'ascend/cognitive/v1'
  channel: 'event' | 'query' | 'query_response' | 'insight' | 'subscription'
  id: string
  timestamp: string    // ISO 8601
  source: string       // component identifier (e.g., 'cognitive.engine', 'runtime.core')
  payload: unknown     // typed per message type (see sections 5-7)
  trace: {
    correlationId: string
    causationId?: string  // which message caused this one
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `protocol` | string | yes | Always `ascend/cognitive/v1` |
| `channel` | string | yes | One of the five channel identifiers |
| `id` | string | yes | Unique message ID (UUID v4) |
| `timestamp` | string | yes | ISO 8601 UTC timestamp |
| `source` | string | yes | Component identifier in dot notation |
| `payload` | unknown | yes | Type-specific payload |
| `trace.correlationId` | string | yes | Links related messages across channels |
| `trace.causationId` | string | no | Identifies the message that caused this one |

---

## 5. Event Subscription

The Cognitive Layer subscribes to Runtime events declaratively. Subscription messages use the same canonical envelope.

### 5.1 Subscription Message

```typescript
interface EventSubscription {
  protocol: 'ascend/cognitive/v1'
  channel: 'subscription'
  id: string
  timestamp: string
  source: string
  payload: {
    subscribeTo: DomainEventType[]
    builderId?: string   // optional filter — subscribe only for one builder
    callback: string     // handler identifier or channel name
  }
  trace: {
    correlationId: string
  }
}

type DomainEventType = 
  | 'mission_started' | 'mission_completed' | 'mission_failed'
  | 'evidence_submitted' | 'evidence_assessed'
  | 'competency_unlocked' | 'competency_updated'
  | 'achievement_earned'
  | 'journey_started' | 'journey_completed'
  | 'builder_created' | 'builder_updated'
  | 'package_loaded' | 'package_unloaded'
```

### 5.2 Subscription Lifecycle

1. The Cognitive Layer sends an `EventSubscription` message to the Runtime.
2. The Runtime registers the subscription and begins delivering matching events.
3. The Runtime delivers events via callback — for each event, it calls the handler identified by `callback`.
4. The Cognitive Layer acknowledges receipt after processing.
5. The Runtime does not retry delivery. If the Cognitive Layer is down, events are lost.
6. On restart, the Cognitive Layer replays missed events by querying the Event Store (if available) or by requesting a state snapshot via the Query Interface.

### 5.3 Unsubscription

To unsubscribe, the Cognitive Layer sends a subscription message with `subscribeTo: []`. The Runtime removes all subscriptions for that source.

---

## 6. Query Protocol

The Query Interface provides read-only access to Runtime state. Every query and its response use the canonical message envelope.

### 6.1 Query Message

```typescript
interface CognitiveQuery {
  protocol: 'ascend/cognitive/v1'
  channel: 'query'
  id: string
  timestamp: string
  source: string
  payload: {
    type: QueryType
    params: Record<string, unknown>
  }
  trace: {
    correlationId: string
  }
}

type QueryType =
  | 'get_builder'
  | 'get_progress'
  | 'get_competencies'
  | 'get_achievements'
  | 'get_evidence'
  | 'get_journeys'
  | 'get_mission'
  | 'get_activity_log'
```

### 6.2 Query Parameter Constraints

| Query Type | Required Params | Optional Params | Returns |
|---|---|---|---|
| `get_builder` | `builderId: string` | — | Builder profile and state |
| `get_progress` | `builderId: string` | `packageId?: string` | Progress summary |
| `get_competencies` | `builderId: string` | `status?: string` | List of competencies |
| `get_achievements` | `builderId: string` | — | List of earned achievements |
| `get_evidence` | `builderId: string` | `missionId?: string` | Evidence records |
| `get_journeys` | `builderId: string` | `status?: string` | Journey summaries |
| `get_mission` | `missionId: string` | — | Full mission details |
| `get_activity_log` | `builderId: string` | `limit?: number`, `since?: string` | Recent activity entries |

### 6.3 Response Message

```typescript
interface CognitiveQueryResponse {
  protocol: 'ascend/cognitive/v1'
  channel: 'query_response'
  id: string
  timestamp: string
  source: string
  payload: {
    queryId: string       // correlates to the original query ID
    status: 'success' | 'error'
    data: unknown
    error?: {
      code: string
      message: string
    }
  }
  trace: {
    correlationId: string
    causationId: string   // the original query ID
  }
}
```

### 6.4 Error Codes

| Code | Meaning |
|---|---|
| `BUILDER_NOT_FOUND` | The requested builder does not exist |
| `INVALID_PARAMS` | Required parameters are missing or malformed |
| `RATE_LIMITED` | Query rate limit exceeded |
| `INTERNAL_ERROR` | Unexpected Runtime error |

### 6.5 Rate Limiting

The Runtime enforces rate limiting per source per builder:

| Default Limit | Burst | Window |
|---|---|---|
| 60 queries | 10 | 60 seconds |

A `RATE_LIMITED` response includes a `Retry-After` header (in seconds) in the error metadata.

---

## 7. Insight Publication

The Cognitive Layer publishes derived insights to the Experience Layer. Insights are advisory — the Experience Layer is the sole authority on whether to display or act on them.

### 7.1 Insight Message

```typescript
interface InsightPublication {
  protocol: 'ascend/cognitive/v1'
  channel: 'insight'
  id: string
  timestamp: string
  source: string
  payload: {
    type: 'insight' | 'recommendation' | 'alert'
    payload: Insight | Recommendation | Alert
    target: 'dashboard' | 'mentor' | 'notification'
    priority: 'low' | 'medium' | 'high'
    ttl?: number   // seconds until stale; omit for permanent
  }
  trace: {
    correlationId: string
    causationId?: string   // the event or query that generated this insight
  }
}
```

### 7.2 Payload Types

#### Insight

```typescript
interface Insight {
  id: string
  title: string
  description: string
  category: 'achievement' | 'momentum' | 'gap' | 'pattern' | 'milestone'
  confidence: number      // 0.0 to 1.0
  evidence: {
    observationIds: string[]
    metric: string
    value: number | string
  }
  generatedBy: string     // model or rule identifier
}
```

#### Recommendation

```typescript
interface Recommendation {
  id: string
  title: string
  description: string
  action: string              // e.g., "start_mission", "review_evidence", "retry"
  targetId?: string           // e.g., mission ID, competency ID
  expectedImpact: string      // e.g., "unlock_competency", "increase_score"
  confidence: number          // 0.0 to 1.0
  generatedBy: string
}
```

#### Alert

```typescript
interface Alert {
  id: string
  title: string
  description: string
  severity: 'info' | 'warning' | 'critical'
  condition: string           // what triggered this alert
  expiresAt?: string          // ISO 8601
  generatedBy: string
}
```

### 7.3 Publication Behavior

| Aspect | Behavior |
|---|---|
| Delivery | Push via event bus or direct channel |
| Acknowledgement | Optional — Experience Layer may acknowledge |
| Validation | Experience Layer MUST validate before acting |
| Staleness | If `ttl` is set and expired, the Experience Layer MUST discard the insight |
| Persistence | Insights are ephemeral unless the Experience Layer persists them |

---

## 8. Model Adapter Interface

Models connect to the Cognitive Layer through a standard adapter interface. This is the only point where model-specific code lives. The Cognitive Layer itself is model-agnostic — it delegates to adapters.

```typescript
interface ModelAdapter {
  name: string
  version: string
  capabilities: ModelCapability[]

  analyze(
    observations: Observation[],
    context: AnalysisContext
  ): Promise<Insight[]>

  recommend(
    insight: Insight,
    builder: BuilderState
  ): Promise<Recommendation | null>

  health(): Promise<ModelHealth>
}

type ModelCapability =
  | 'pattern_detection'
  | 'insight_generation'
  | 'recommendation'
  | 'natural_language'
  | 'goal_prediction'
  | 'knowledge_gap_analysis'
  | 'strategy_generation'

interface AnalysisContext {
  builderId: string
  timeRange?: { start: string; end: string }
  focusArea?: string
  limit?: number
}

interface ModelHealth {
  available: boolean
  latency: number          // milliseconds
  errorRate: number        // 0.0 to 1.0
  lastSuccess: string      // ISO 8601
  version: string
}
```

### 8.1 Adapter Registration

Adapters register with the Cognitive Engine at startup:

```typescript
cognitiveEngine.registerAdapter('openai-gpt4', new OpenAIAdapter(config))
cognitiveEngine.registerAdapter('rule-based', new RuleBasedAdapter())
```

Multiple adapters MAY be registered simultaneously. The Cognitive Engine selects the best adapter based on capability requirements and availability.

### 8.2 Adapter Contract

- `analyze()` receives a batch of Observations and returns Insights. It MUST never mutate any input.
- `recommend()` receives a single Insight and the current BuilderState, and returns an optional Recommendation. It MUST never mutate state.
- `health()` returns the model's current availability and performance metrics.
- All methods MAY throw. The Cognitive Engine catches exceptions and falls back gracefully.

### 8.3 No Model Capability Assumptions

The Cognitive Engine MUST NOT assume any specific capability exists. Before delegating to an adapter, it checks `adapter.capabilities`. If no registered adapter supports the required capability, the engine falls back to rule-based analysis (see Section 9).

---

## 9. No-Model Mode

The Cognitive Protocol is designed to function correctly with zero AI models installed. When no model adapter is registered, or when all registered adapters are unhealthy, the Cognitive Engine operates in No-Model Mode:

### 9.1 Fallback Behavior

| Component | Default Behavior |
|---|---|
| Pattern Detection | Rule-based heuristics: threshold crossing, frequency analysis, recency weighting |
| Insight Generation | Template-driven: milestone reached, streak detected, stagnation warning |
| Recommendation | Deterministic rules: if competency gap detected → recommend next mission in sequence |
| Confidence Scoring | Based on statistical measures only: count, recency, consistency of observations |
| Insight Stream | Still flows — all insights are published with `generatedBy: 'rule-based'` and lower confidence |

### 9.2 Rule-Based Adapter

The Cognitive Engine includes a built-in rule-based adapter that is always available:

```typescript
class RuleBasedAdapter implements ModelAdapter {
  name = 'rule-based'
  version = '1.0.0'
  capabilities = ['pattern_detection', 'insight_generation', 'recommendation']

  async analyze(observations: Observation[], context: AnalysisContext): Promise<Insight[]> {
    // Apply threshold-based rules
    // Detect streaks, stagnation, milestones
    // Return template-driven insights with statistical confidence
  }

  async recommend(insight: Insight, builder: BuilderState): Promise<Recommendation | null> {
    // Apply deterministic decision trees
    // Example: if competency X is at 60% and mission Y covers it → recommend mission Y
  }

  async health(): Promise<ModelHealth> {
    return { available: true, latency: 0, errorRate: 0, lastSuccess: new Date().toISOString(), version: '1.0.0' }
  }
}
```

### 9.3 Quality Implications

| Metric | With AI Model | No-Model Mode |
|---|---|---|
| Insight Diversity | High — can detect subtle patterns | Low — only detects predefined patterns |
| Confidence Calibration | Learned from data | Statistical only (count, recency) |
| Recommendation Quality | Contextual and adaptive | Deterministic and rule-bound |
| Natural Language | Available | Not available |

The architecture does not break. Data quality is lower but the system remains fully functional.

---

## 10. Audit Trail

Every message across all three channels MUST be logged with the following metadata. The audit log is immutable append-only.

### 10.1 Log Entry Format

```typescript
interface AuditEntry {
  messageId: string
  timestamp: string          // ISO 8601
  source: string
  target: string
  channel: 'event' | 'query' | 'query_response' | 'insight' | 'subscription'
  payloadType: string        // e.g., 'mission_completed', 'get_progress', 'recommendation'
  payloadSizeBytes: number
  processingResult: 'accepted' | 'rejected' | 'error' | 'timeout'
  latencyMs: number
  error?: string             // error message if processingResult is 'error'
  trace: {
    correlationId: string
    causationId?: string
  }
}
```

### 10.2 Audit Rules

1. Every sent and received message produces an audit entry.
2. Payload content is NOT logged for large payloads (> 10 KB). Only `payloadType` and `payloadSizeBytes` are recorded.
3. Audit logs are local-first and belong to the user (per I8).
4. Audit logs MUST NOT contain personally identifiable information beyond builder IDs.
5. Audit entries are retained for a minimum of 30 days (configurable).

### 10.3 Audit Consumers

- **Developer**: Debugging and integration testing
- **Builder**: Transparency — see what the system knows about them
- **Governance**: Compliance with the protocol

---

## 11. Security

### 11.1 Channel Security

| Channel | Authentication | Authorization | Mutations |
|---|---|---|---|
| Event Stream | Cognitive Layer must identify itself at subscription time | Subscribe only to permitted event types | None (read-only) |
| Query Interface | Per-request authentication token | Read-only access to permitted data scopes | Forbidden by construction |
| Insight Stream | Source identity verified | Experience Layer validates before acting | Advisory only |

### 11.2 Read-Only by Construction

The Query Interface is enforced as read-only at the type system level:

```typescript
// The Runtime Adapter exposes two interfaces:
interface RuntimeAdapter {
  // Read-only — exposed to Query Interface
  queries: ReadOnlyQueries
  
  // Read-write — NOT exposed to Cognitive Layer
  commands: ReadWriteCommands
}

interface ReadOnlyQueries {
  getBuilder(id: string): Builder
  getProgress(builderId: string): Progress
  getCompetencies(builderId: string): Competency[]
  // ... all other getters
}
```

The Cognitive Layer receives only the `queries` reference. The `commands` reference is never passed to it.

### 11.3 Authentication

- The Event Stream requires the Cognitive Layer to present a valid component identifier at subscription time.
- The Query Interface requires a bearer token on each request.
- The Insight Stream does not require authentication (it is push-only to the Experience Layer, which validates internally).

### 11.4 Prohibited Operations

The Cognitive Layer MUST NEVER:

- Write to any Runtime data store directly
- Call command methods on the Runtime Adapter
- Modify runtime state through reflection or metaprogramming
- Bypass the Query Interface to access Runtime internals
- Execute mutations in response to events (observe only)

Violations are detected by the Audit Layer and reported as security events.

### 11.5 Sandboxing

If the Cognitive Layer runs in a separate process or container:

- It MUST have network access only to the Event Bus and Query Interface
- It MUST NOT have filesystem access to Runtime data directories
- It MUST NOT have database credentials

---

## 12. Performance Requirements

| Metric | Target | Degradation Threshold |
|---|---|---|
| Event delivery latency (p99) | < 50 ms | < 200 ms |
| Query response time (p99) | < 100 ms | < 500 ms |
| Insight publication latency | < 200 ms | < 1 s |
| Audit log write latency | < 10 ms | < 50 ms |
| Maximum concurrent subscriptions per source | 10 | N/A |
| Maximum query rate per source | 60 req/min | N/A |

---

## 13. Versioning and Compatibility

| Protocol Version | Runtime Versions | Notes |
|---|---|---|
| `ascend/cognitive/v1` | >= 1.0 | Current version |

Breaking changes to the message envelope require a new protocol version (e.g., `ascend/cognitive/v2`). Additive changes (new query types, new event types) are backward-compatible and do not require a version bump.

The Cognitive Engine MUST support at least one previous protocol version for a grace period of one MAJOR Runtime release.

---

## 14. References

| Document | Relation |
|---|---|
| DOC-0009 — Architectural Invariants | I5, I6, I9 directly inform this protocol |
| ARCH-0003 — Core Engine Specification | Core Engine as the substrate for cognitive observation |
| SPEC-0001 — APS v1 | Package format that the Cognitive Layer may reason about |
| SPEC-0002 — AEP v1 | Execution protocol for content the Cognitive Layer observes |
| SPEC-0003 — ARP v1 | Registry protocol; Cognitive Layer may query registry state |
| SPEC-0004 — AAP v1 | Agent protocol for assessment (complementary to ACP) |
