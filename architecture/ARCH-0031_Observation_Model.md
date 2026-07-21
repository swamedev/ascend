# ARCH-0031 — Observation Model

| Field | Value |
|-------|-------|
| **ID** | ARCH-0031 |
| **Name** | Observation Model |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, DOC-0009 Architectural Invariants, ARCH-0003 Core Engine Specification |
| **Principle** | No competency without evidence — no evidence without observation |

---

## 1. Why Observation Matters

The Runtime produces events and state. It is a deterministic engine — it executes missions, validates evidence, computes XP, and transitions builders through their journeys. But it does not **interpret**. It does not ask *why* a builder is stuck, *what* pattern their progress reveals, or *when* to intervene.

That is the role of the Cognitive Layer.

Observation is the **input** to all cognitive functions. Every insight, every recommendation, every decision traceable by the builder must be rooted in an observed fact. Without a formal observation model, insights are arbitrary, untraceable, and impossible to audit.

> **Core Philosophy:** AI does not think. It observes. Then infers. Every inference must be grounded in an observation — raw, timestamped, and immutable after capture.

The Observation Model provides:
- **Traceability** — every insight links back to one or more observations
- **Auditability** — the builder can examine exactly what was observed and why
- **Decoupling** — the Cognitive Layer never depends on Runtime internals; it only consumes events and state
- **Determinism** — observations are first-class data, not ephemeral log lines
- **No-AI Viability** — the entire pipeline works with zero ML/AI dependencies

---

## 2. The Cognitive Cycle

The Cognitive Cycle defines how raw Runtime events and state transform into actionable recommendations and measurable outcomes. Each step in the cycle is a formal, implementable stage.

```
Runtime Event / State Snapshot
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  1. OBSERVATION                                             │
│     Raw capture of what happened                            │
│     e.g., "Mission 'variables-101' completed with score 85" │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SIGNAL                                                  │
│     Structured data point extracted from observation        │
│     e.g., xp_gained = 150, completion_rate = 0.85           │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  3. PATTERN                                                 │
│     Meaningful relationship between signals                 │
│     e.g., "completion_rate > 0.8 for last 5 missions"       │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  4. INSIGHT                                                 │
│     Interpreted pattern with confidence                     │
│     e.g., "Builder is in a momentum phase — keep going"     │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  5. RECOMMENDATION                                          │
│     Actionable suggestion based on insight                  │
│     e.g., "Try the next mission while momentum is high"     │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  6. DECISION                                                │
│     Builder chooses to accept, ignore, or modify             │
│     e.g., Builder clicks "Accept" — navigates to mission    │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│  7. OUTCOME                                                 │
│     Result of the decision, observed in the next cycle      │
│     e.g., Mission completed successfully → positive outcome │
└─────────────────────────────────────────────────────────────┘
    │
    └──→ feeds back into OBSERVATION (cycles continue)
```

Each stage produces a typed, persisted record. The cycle is continuous and asynchronous — new observations may enter while previous cycles are still being processed.

---

## 3. Observation Definition

An **Observation** is the atomic unit of raw data in the Cognitive Layer. It is a timestamped record of something that happened — a domain event emitted by the Runtime, a snapshot of builder state, a cognitive event produced by the layer itself, or an explicit action taken by the builder.

### 3.1 Interface

```typescript
interface Observation {
  id: string
  type: ObservationType
  source: 'runtime' | 'cognitive' | 'builder'
  timestamp: string  // ISO 8601
  data: Record<string, unknown>
  context: {
    builderId: string
    sessionId?: string
    missionId?: string
    journeyId?: string
  }
  metadata: {
    observationSchema: string  // version
    collector: string          // which collector produced this
  }
}
```

### 3.2 ObservationType

`ObservationType` is a union string type categorized by domain origin:

**Mission lifecycle:**
- `mission.started` — builder began a mission
- `mission.completed` — builder finished a mission
- `mission.failed` — builder failed or abandoned a mission

**Evidence lifecycle:**
- `evidence.submitted` — builder submitted evidence for a competency
- `evidence.accepted` — evidence was validated and accepted
- `evidence.rejected` — evidence failed validation

**Competency lifecycle:**
- `competency.unlocked` — a new competency was unlocked
- `competency.leveled_up` — an existing competency advanced in level

**Achievement lifecycle:**
- `achievement.earned` — builder earned an achievement

**Builder lifecycle:**
- `builder.leveled_up` — builder overall level increased

**Session lifecycle:**
- `session.started` — a learning session began
- `session.ended` — a learning session ended

**Journey lifecycle:**
- `journey.started` — builder embarked on a journey
- `journey.completed` — builder completed a journey

**Assessment lifecycle:**
- `assessment.passed` — builder passed an assessment
- `assessment.failed` — builder failed an assessment

### 3.3 Rules

| Rule | Description |
|------|-------------|
| `id` | UUID v4, generated at observation time, immutable |
| `type` | Must match `^[a-z]+\.[a-z_]+$` |
| `timestamp` | Must be ISO 8601 UTC, set at capture time |
| `context.builderId` | Always required — every observation belongs to a builder |
| `metadata.observationSchema` | Semantic version of the observation schema used |
| `metadata.collector` | Name of the collector component that produced this observation |

---

## 4. Signal Definition

A **Signal** is a structured, quantified data point extracted from one or more observations. Signals bridge the gap between raw events and meaningful patterns. While an observation says *what happened*, a signal says *what measurable fact we can derive*.

### 4.1 Interface

```typescript
interface Signal {
  id: string
  observationId: string
  type: SignalType
  value: number | string | boolean
  confidence: number  // 0.0 to 1.0
  extractedAt: string  // ISO 8601
}
```

### 4.2 SignalType

Signal types are organized by the dimension they measure:

**Progress signals:**
- `xp_gained` — amount of XP earned in a single event
- `xp_total` — cumulative XP
- `mission_count` — number of missions completed
- `completion_rate` — ratio of completed to started missions
- `time_spent` — time spent on task (seconds)

**Quality signals:**
- `evidence_quality` — quality score of submitted evidence (0.0–1.0)
- `error_rate` — frequency of errors or failed attempts
- `streak_length` — current streak length in days
- `topics_covered` — number of distinct topics engaged

**Engagement signals:**
- `session_duration` — duration of a learning session
- `session_frequency` — sessions per time period
- `time_of_day` — when builder is most active
- `day_of_week` — which days builder engages

**Competency signals:**
- `competency_count` — number of unlocked competencies
- `competency_depth` — average competency level
- `level_progression_rate` — speed of level advancement

### 4.3 Extraction Rules

- A signal MUST reference exactly one observation via `observationId`
- Multiple signals may be extracted from a single observation
- `confidence` MUST be between 0.0 and 1.0 (inclusive)
- In deterministic (No-AI) mode, confidence is typically 1.0 for direct extractions and scored for inferred values

---

## 5. Pattern Definition

A **Pattern** is a meaningful relationship between two or more signals observed over time. Patterns represent recurring phenomena in the builder's learning behavior.

### 5.1 Interface

```typescript
interface Pattern {
  id: string
  type: PatternType
  signals: string[]  // signal IDs
  confidence: number  // 0.0 to 1.0
  firstObserved: string  // ISO 8601
  lastObserved: string   // ISO 8601
  occurrenceCount: number
}
```

### 5.2 PatternType

- `learning_plateau` — builder's progress has flattened; completion rate flat, time spent increasing without corresponding XP gain
- `accelerated_progress` — completion rate and XP gain are both trending upward faster than historical average
- `topic_affinity` — builder consistently engages with a specific topic category
- `struggle_area` — repeated failures, low evidence quality, or high error rate on a specific topic
- `consistent_performer` — steady, predictable progress with low variance
- `burst_then_pause` — intense activity followed by inactivity; suggests burnout or scheduling pattern
- `deep_diver` — builder spends significantly more time per mission than average, suggesting thorough engagement
- `rapid_advancer` — builder moves through levels faster than the 90th percentile
- `recovery_pattern` — after a failure, builder retries and succeeds; shows resilience
- `disengagement_risk` — session frequency dropping, streak broken, time since last session increasing

### 5.3 Detection Rules

- A pattern MUST reference at least two signal IDs in `signals`
- `firstObserved` is set when the pattern is first detected and never updated
- `lastObserved` is updated each time the pattern criteria are met again
- `occurrenceCount` is incremented each time the pattern criteria are satisfied
- In No-AI mode, patterns are detected via heuristic rules (threshold comparisons, sliding window statistics)

---

## 6. Insight Definition

An **Insight** is the interpreted meaning of a pattern — a human-readable conclusion about the builder's learning state. While a pattern says *this behavior is recurring*, an insight says *this is what it means for the builder*.

### 6.1 Interface

```typescript
interface Insight {
  id: string
  type: InsightType
  patternId: string
  title: string
  description: string
  confidence: number  // 0.0 to 1.0
  severity: 'info' | 'suggestion' | 'warning' | 'achievement'
  createdAt: string   // ISO 8601
  dismissedAt?: string
  acceptedAt?: string
}
```

### 6.2 InsightType

- `knowledge_gap` — builder is struggling with a specific concept or skill
- `strength_identified` — builder demonstrates above-average proficiency in an area
- `momentum` — builder is in a positive progress flow; now is a good time to increase challenge
- `stagnation_risk` — progress has stalled; intervention may be needed
- `burnout_risk` — patterns indicate overwork or unsustainable pace
- `goal_proximity` — builder is close to achieving a milestone or competency
- `topic_mastery` — builder has demonstrated sufficient proficiency to move on
- `learning_style` — builder consistently performs better with certain mission types
- `consistency_praise` — builder has maintained a streak or regular practice habit
- `resilience_noted` — builder failed and persisted; demonstrates growth mindset

### 6.3 Severity Mapping

| Severity | Meaning | Example |
|----------|---------|---------|
| `info` | Neutral observation, no action needed | "You've covered 5 topics this week" |
| `suggestion` | Gentle recommendation | "Consider reviewing variables before the next mission" |
| `warning` | Potential negative outcome ahead | "Your session frequency has dropped 40% — you may lose your streak" |
| `achievement` | Positive milestone reached | "You've unlocked your 10th competency!" |

---

## 7. Recommendation Definition

A **Recommendation** is an actionable suggestion produced from an insight. It tells the builder *what they could do next* and *why*.

### 7.1 Interface

```typescript
interface Recommendation {
  id: string
  insightId: string
  type: RecommendationType
  title: string
  description: string
  action: {
    type: 'navigate' | 'retry' | 'explore' | 'practice' | 'rest'
    target?: string  // route, mission ID, etc.
  }
  confidence: number  // 0.0 to 1.0
  rationale: string  // human-readable explanation
  createdAt: string   // ISO 8601
  status: 'pending' | 'accepted' | 'dismissed' | 'expired'
}
```

### 7.2 RecommendationType

- `next_challenge` — suggest a new mission to maintain momentum
- `review_content` — suggest revisiting previous content to fill knowledge gaps
- `practice_skill` — suggest targeted practice for a struggling area
- `explore_topic` — suggest branching into a new or related topic
- `take_break` — suggest resting to avoid burnout
- `retry_mission` — suggest retrying a failed mission with new strategies
- `celebrate_milestone` — acknowledge an achievement
- `adjust_pace` — suggest slowing down or speeding up
- `deepen_competency` — suggest advancing an existing competency to the next level

### 7.3 Action Types

| Action Type | Meaning | Example Target |
|-------------|---------|----------------|
| `navigate` | Go to a specific location in the app | `/missions/advanced-variables` |
| `retry` | Retry a previously attempted mission | Mission ID of a failed mission |
| `explore` | Browse a topic or category | `/topics/functions` |
| `practice` | Engage in a practice or review activity | `/practice/variables` |
| `rest` | No destination — suggests stopping | empty target |

### 7.4 Status Lifecycle

```
pending ──→ accepted
    │            │
    ├──→ dismissed
    │
    └──→ expired (automatic after TTL, default 7 days)
```

---

## 8. Decision Definition

A **Decision** records the builder's explicit response to a recommendation. This closes the loop between the Cognitive Layer and the builder's agency.

### 8.1 Interface

```typescript
interface Decision {
  id: string
  recommendationId: string
  choice: 'accept' | 'dismiss' | 'modify' | 'snooze'
  modifiedAction?: {
    type: 'navigate' | 'retry' | 'explore' | 'practice' | 'rest'
    target?: string
  }
  decidedAt: string  // ISO 8601
}
```

### 8.2 Choice Meanings

| Choice | Meaning |
|--------|---------|
| `accept` | Builder followed the recommendation as-is |
| `dismiss` | Builder explicitly rejected the recommendation |
| `modify` | Builder accepted but changed the action (e.g., chose a different mission) |
| `snooze` | Builder postponed the decision (recommendation will re-appear later) |

When `choice` is `modify`, the `modifiedAction` field MUST contain the builder's customized action. When `choice` is any other value, `modifiedAction` MUST be omitted.

---

## 9. Outcome Definition

An **Outcome** records what actually happened after a decision was made. It is the final feedback signal in the cognitive cycle, connecting a decision back to real-world results.

### 9.1 Interface

```typescript
interface Outcome {
  id: string
  decisionId: string
  result: 'positive' | 'neutral' | 'negative'
  observedAt: string  // ISO 8601
  followUpInsightId?: string
}
```

### 9.2 Result Meanings

| Result | Meaning | Example |
|--------|---------|---------|
| `positive` | The decision led to a desirable outcome | Accepted next challenge → completed mission successfully |
| `neutral` | The decision had no measurable effect | Accepted suggestion to explore → builder browsed but did not engage |
| `negative` | The decision led to an undesirable outcome | Ignored burnout warning → builder's streak broke the next day |

### 9.3 Feedback Loop

When an outcome produces a `followUpInsightId`, the cycle continues — the outcome itself becomes an observation, feeding back into the Cognitive Layer for continuous refinement.

```
Observation → Signal → Pattern → Insight → Recommendation → Decision → Outcome
                                                                              │
                                                                              └──→ Observation (next cycle)
```

---

## 10. Observation Sources

Observations enter the system from four distinct sources:

### 10.1 Runtime Events

Domain events published by the ASCEND Runtime. These are the primary source of observations. Each domain event maps to one or more `ObservationType` values.

**Examples:**
- `MissionCompleted` domain event → `Observation { type: 'mission.completed', source: 'runtime' }`
- `EvidenceAccepted` domain event → `Observation { type: 'evidence.accepted', source: 'runtime' }`

### 10.2 State Snapshots

Periodic captures of the Builder's current state. Unlike events (which record deltas), snapshots record the full state at a point in time. Snapshots are useful for detecting changes in state that do not correspond to a single event.

**Examples:**
- Daily snapshot of competency graph → signals about competency depth
- Weekly snapshot of XP total → signals about progress rate

### 10.3 Builder Actions

Explicit actions taken by the builder that may not produce domain events. These are typically UI-level interactions.

**Examples:**
- Navigation patterns (which pages the builder visits)
- Time-on-task per mission section
- Click patterns (what the builder interacts with)
- Pause/resume actions

### 10.4 Cognitive Events

Events produced by the Cognitive Layer itself. These enable self-reflection and recursive improvement of the cognitive system.

**Examples:**
- `Observation` of an insight being dismissed → `observation.type: 'insight.dismissed'`
- `Observation` of a pattern fading → `observation.type: 'pattern.expired'`
- Cycle timing metrics (how long each stage took)

---

## 11. Observation Storage & Lifecycle

### 11.1 Storage Model

All observations, signals, patterns, insights, recommendations, decisions, and outcomes are stored locally. The storage backend is the same SQLite database used by the Runtime.

| Entity | Table | Retention |
|--------|-------|-----------|
| Observation | `cognitive_observations` | Configurable (default 90 days) |
| Signal | `cognitive_signals` | Configurable (default 90 days) |
| Pattern | `cognitive_patterns` | Configurable (default 90 days) |
| Insight | `cognitive_insights` | Indefinite (builder-facing) |
| Recommendation | `cognitive_recommendations` | Indefinite (builder-facing) |
| Decision | `cognitive_decisions` | Indefinite (builder-facing) |
| Outcome | `cognitive_outcomes` | Indefinite (builder-facing) |

### 11.2 Retention Policy

- Observations, signals, and patterns are subject to a configurable retention window (default: 90 days)
- After the retention window expires, old records may be archived or purged
- Insights, recommendations, decisions, and outcomes are retained indefinitely — they form the builder's cognitive history
- The builder can adjust retention settings at any time

### 11.3 Data Sovereignty

Consistent with DOC-0009 (Architectural Invariants — I8: Data belongs to the user):

- **Exportable:** The builder can export all observations, signals, patterns, insights, recommendations, decisions, and outcomes in a portable format (JSON)
- **Deletable:** The builder can delete any or all cognitive data at any time
- **Anonymizable:** Observations can be stripped of PII (builder ID, session ID) for optional aggregate analysis
- **Local-first:** All data lives on the builder's machine. No upload occurs without explicit consent.

### 11.4 Privacy Guarantees

| Guarantee | Implementation |
|-----------|---------------|
| No mandatory telemetry | Cognitive data never leaves the device unless builder exports |
| Builder-owned | All records reference `builderId` but can be fully deleted |
| Transparent | Builder can inspect every observation and derived artifact |

---

## 12. Complete Cycle Example

This section walks through a full cognitive cycle from Runtime event to Outcome.

### Step 0: Runtime Produces Event

The builder completes mission `variables-101` with a score of 85 and earns 150 XP. The Runtime publishes a `MissionCompleted` domain event.

### Step 1: Observation

The Observation Collector subscribes to Runtime events and captures:

```json
{
  "id": "obs-001",
  "type": "mission.completed",
  "source": "runtime",
  "timestamp": "2026-07-21T14:30:00Z",
  "data": {
    "missionId": "variables-101",
    "score": 85,
    "xpEarned": 150,
    "duration": 1800
  },
  "context": {
    "builderId": "bld-42",
    "sessionId": "ses-17",
    "missionId": "variables-101",
    "journeyId": "jny-05"
  },
  "metadata": {
    "observationSchema": "1.0",
    "collector": "runtime-event-collector"
  }
}
```

### Step 2: Signal Extraction

The Signal Extractor processes the observation and produces structured signals:

```json
[
  {
    "id": "sig-001",
    "observationId": "obs-001",
    "type": "xp_gained",
    "value": 150,
    "confidence": 1.0,
    "extractedAt": "2026-07-21T14:30:01Z"
  },
  {
    "id": "sig-002",
    "observationId": "obs-001",
    "type": "completion_rate",
    "value": 0.85,
    "confidence": 1.0,
    "extractedAt": "2026-07-21T14:30:01Z"
  },
  {
    "id": "sig-003",
    "observationId": "obs-001",
    "type": "time_spent",
    "value": 1800,
    "confidence": 1.0,
    "extractedAt": "2026-07-21T14:30:01Z"
  }
]
```

### Step 3: Pattern Detection

The Pattern Detector analyzes current and historical signals. It finds that:
- The last 5 missions all had completion_rate > 0.8
- XP gained per mission has increased 20% over the builder's average
- Time spent per mission has decreased (builder is getting faster)

It detects a pattern:

```json
{
  "id": "pat-001",
  "type": "accelerated_progress",
  "signals": ["sig-001", "sig-002", "sig-003"],
  "confidence": 0.72,
  "firstObserved": "2026-07-21T14:30:02Z",
  "lastObserved": "2026-07-21T14:30:02Z",
  "occurrenceCount": 1
}
```

Confidence is 0.72 (not 1.0) because the pattern heuristic requires at least 5 data points to reach maximum confidence — the detector is using a sliding window with a confidence ramp.

### Step 4: Insight Generation

The Insight Generator interprets the pattern and produces a human-readable insight:

```json
{
  "id": "ins-001",
  "type": "momentum",
  "patternId": "pat-001",
  "title": "Strong Progress",
  "description": "You've been consistently scoring above 80% and earning more XP per mission. Your efficiency is improving — keep the momentum going.",
  "confidence": 0.72,
  "severity": "achievement",
  "createdAt": "2026-07-21T14:30:03Z"
}
```

### Step 5: Recommendation Building

The Recommendation Builder uses the insight to produce an actionable suggestion:

```json
{
  "id": "rec-001",
  "insightId": "ins-001",
  "type": "next_challenge",
  "title": "Take the Next Mission",
  "description": "You're ready for the next challenge in this journey.",
  "action": {
    "type": "navigate",
    "target": "/missions/variables-201"
  },
  "confidence": 0.68,
  "rationale": "You are progressing faster than average. Consider taking the next mission while your momentum is high. Your last 5 missions all scored above 80%.",
  "createdAt": "2026-07-21T14:30:04Z",
  "status": "pending"
}
```

### Step 6: Decision

The builder sees the recommendation in their dashboard and clicks "Accept" (which navigates them to the mission page):

```json
{
  "id": "dec-001",
  "recommendationId": "rec-001",
  "choice": "accept",
  "decidedAt": "2026-07-21T14:31:00Z"
}
```

The builder navigates to `/missions/variables-201` and begins the mission.

### Step 7: Outcome

Later, the builder completes `variables-201` (also with a good score). The next cognitive cycle processes this as a new observation. Meanwhile, the previous cycle's outcome is recorded:

```json
{
  "id": "out-001",
  "decisionId": "dec-001",
  "result": "positive",
  "observedAt": "2026-07-21T15:15:00Z"
}
```

The builder's decision to accept the recommendation led to a positive outcome. This outcome itself feeds into the next cognitive cycle — the system learns that recommendations of type `next_challenge` have a high success rate for this builder when the `momentum` pattern is active.

---

## 13. No-AI Mode

Every component in this model can operate with **zero ML/AI dependencies**. This is not an afterthought — it is a design requirement (consistent with I5 and I6 of DOC-0009).

| Component | No-AI Implementation |
|-----------|---------------------|
| **Observation Collector** | Event subscriber + state poller. Pure data capture. No ML. |
| **Signal Extractor** | Deterministic mapping functions: `(observation) => Signal[]`. Switch on `observation.type`, extract known fields, apply simple transformations. No ML. |
| **Pattern Detector** | Heuristic rules with configurable thresholds. Sliding window statistics, frequency counters, moving averages. Example: "if completion_rate > 0.8 for last N missions, pattern = accelerated_progress". No ML. |
| **Insight Generator** | Decision tree with rule sets per `PatternType`. Each pattern maps to one or more insights with template-based title/description. Confidence derived from pattern confidence × signal count × occurrence count. No ML. |
| **Recommendation Builder** | Rule engine mapping `InsightType × severity × builder preferences` to recommendations. Simple priority scoring: `score = confidence × (1 + recurrenceWeight)`. No ML. |

### 13.1 Confidence Without AI

Confidence values in No-AI mode are computed using simple statistics:

- **Direct extractions** (e.g., `xp_gained` from `mission.completed`): confidence = 1.0
- **Computed signals** (e.g., moving average of XP): confidence = `min(1.0, dataPointCount / minimumRequiredCount)`
- **Pattern detection**: confidence = `avgSignalConfidence × occurrenceWeight × coverageRatio`
- **Insights**: confidence = `patternConfidence × decayFactor(age)`
- **Recommendations**: confidence = `insightConfidence × acceptanceHistoryWeight`

### 13.2 When AI Is Available

If an AI provider is configured, it can replace or augment any stage:
- Use an LLM to generate richer insight descriptions
- Use a classifier to detect subtle patterns
- Use a recommender system for personalized recommendations

But the system NEVER depends on AI. If the AI provider is unavailable, the pipeline degrades gracefully to No-AI mode. The builder sees the same types of insights — they may be less nuanced, but they are never absent.

### 13.3 Architectural Invariant Compliance

| Invariant | How ARCH-0031 Complies |
|-----------|----------------------|
| **I2 — Competência só existe quando há evidência** | Observations are the evidence for cognitive artifacts. Every insight traces to observations of real evidence events. |
| **I5 — IA nunca altera regras de negócio** | AI is a replaceable layer. Rules in sections 4–7 define deterministic behavior. AI augments, never overrides. |
| **I6 — Núcleo deve funcionar sem internet** | No-AI mode requires zero network. All storage is local SQLite. |
| **I8 — Dados pertencem ao usuário** | Observations are local, exportable, deletable, anonymizable. |
| **I9 — Camadas comunicam-se apenas para dentro** | Cognitive Layer observes Runtime via events/state — never the reverse. |

---

## 14. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — formal definition of the Observation Model |
