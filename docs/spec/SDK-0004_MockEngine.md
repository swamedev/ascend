# SDK-0004 — ASCEND Mock Engine

**Status:** Draft  
**Version:** 1.0.0  
**Obsoletes:** None  
**License:** MIT  

---

## 1. Abstract

SDK-0004 defines the **Mock Engine** — a complete in-memory simulation of the ASCEND domain. The Mock Engine allows the entire frontend to be developed, tested, and demonstrated without any backend, API, or database. It is the primary development tool from now until the REST API is stable.

---

## 2. Scope

This specification covers:

- MockEngine interface and lifecycle
- Seed data presets
- All mock data models (Builder, Journeys, Missions, Competencies, XP, Notifications, Timeline)
- Simulated behavior (latency, failures, state transitions)
- Reset and customization

It does **not** cover:

- Transport contracts (see SDK-0003)
- Client contracts (see SDK-0002)
- Production API behavior

---

## 3. MockEngine Interface

```typescript
class MockEngine {
  // ─── Lifecycle ───────────────────────────────────

  constructor(preset?: SeedPreset, options?: MockEngineOptions)
  initialize(): Promise<void>
  reset(): Promise<void>

  // ─── State ───────────────────────────────────────

  getState(): MockState
  setState(partial: Partial<MockState>): void

  // ─── Seed ────────────────────────────────────────

  loadPreset(preset: SeedPreset): void
  loadSeedFile(path: string): Promise<void>
  customize(patch: MockCustomization): void

  // ─── Simulation ──────────────────────────────────

  advanceTime(ms: number): Promise<void>
  triggerEvent(event: MockEvent): Promise<void>
  simulateFailure(endpoint: string, probability: number): void

  // ─── Inspection ──────────────────────────────────

  getCallHistory(): MockCall[]
  clearCallHistory(): void
  getMetrics(): MockMetrics
}

interface MockEngineOptions {
  latency?: number               // simulated ms per call (default 0)
  failureRate?: number           // 0-1 (default 0)
  seed?: number                  // deterministic seed
}

type SeedPreset = 'empty' | 'demo' | 'comprehensive'

interface MockState {
  builder: MockBuilder
  journeys: Map<string, MockJourney>
  missions: Map<string, MockMission>
  competencies: Map<string, MockCompetency>
  achievements: Map<string, MockAchievement>
  notifications: MockNotification[]
  timeline: MockTimelineEvent[]
}

interface MockCustomization {
  builder?: Partial<MockBuilder>
  journeys?: Partial<MockJourney>[]
  missions?: Partial<MockMission>[]
}

interface MockCall {
  method: string
  path: string
  timestamp: number
  duration: number
  success: boolean
  status: number
}

interface MockMetrics {
  totalCalls: number
  successfulCalls: number
  failedCalls: number
  averageLatency: number
  cacheHits: number
  cacheMisses: number
}
```

---

## 4. Seed Presets

### 4.1 `empty`

| Data | Count | Purpose |
|------|-------|---------|
| Builder | 1 (fresh, level 1) | First-run experience |
| Journeys | 0 | Empty state testing |
| Missions | 0 | Empty state testing |
| XP | 0 | Fresh user |
| Notifications | 0 | Clean state |

Use case: First-time user onboarding, empty states.

### 4.2 `demo`

| Data | Count | Purpose |
|------|-------|---------|
| Builder | 1 (level 3) | Active user |
| Journeys | 2 (1 in progress, 1 available) | Navigation flow |
| Missions | 6 (3 per journey, mixed status) | Mission interaction |
| Competencies | 4 (2 unlocked) | Tree visualization |
| Achievements | 3 (1 unlocked) | Badge gallery |
| XP | 450 | Progress bars |
| Notifications | 3 | Notification center |
| Timeline | 10 events | Activity feed |

Use case: Demo environment, UI walkthroughs.

### 4.3 `comprehensive`

| Data | Count | Purpose |
|------|-------|---------|
| Builder | 1 (level 10) | Power user |
| Journeys | 5 (all statuses) | Full journey management |
| Missions | 20 (mixed statuses) | Complex mission trees |
| Competencies | 12 (6 unlocked) | Deep tree exploration |
| Achievements | 15 (8 unlocked) | Rich gallery |
| XP | 3200 | High-level display |
| Certificates | 3 | Certificate panel |
| Notifications | 8 | Notification overload |
| Timeline | 30 events | Scrolling, pagination |
| Assessment history | 5 results | Assessment display |

Use case: Full-feature demo, performance testing, edge cases.

---

## 5. Data Models

### 5.1 Builder

```typescript
interface MockBuilder {
  id: string
  name: string
  avatar?: string
  bio: string
  level: number
  xp: XPMetrics
  streak: StreakData
  joinedAt: string
  preferences: MockPreferences
}

interface XPMetrics {
  current: number
  total: number
  nextLevelAt: number
  history: XPEvent[]
}

interface XPEvent {
  amount: number
  source: string               // 'mission' | 'achievement' | 'streak'
  timestamp: string
  description: string
}

interface StreakData {
  current: number
  longest: number
  lastActivity: string
  frozen: boolean              // streak freeze active
}

interface MockPreferences {
  theme: 'light' | 'dark' | 'system'
  sidebarCollapsed: boolean
  reducedMotion: boolean
}
```

### 5.2 Journey

```typescript
interface MockJourney {
  id: string
  title: string
  description: string
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  progress: number
  missions: MockMission[]
  prerequisites: string[]
  tags: string[]
  competencies: CompetencyRef[]
  estimatedHours: number
  startedAt?: string
  completedAt?: string
  image?: string
}
```

### 5.3 Mission

```typescript
interface MockMission {
  id: string
  journeyId: string
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  xpReward: number
  evidenceRequired: boolean
  evidence: MockEvidence[]
  feedback: MockFeedback[]
  instructions: string
  criteria: MockCriterion[]
  resources: MockResource[]
  startedAt?: string
  completedAt?: string
}

interface MockEvidence {
  id: string
  type: 'text' | 'file' | 'link' | 'image'
  content: string
  description: string
  status: 'pending' | 'accepted' | 'rejected'
  submittedAt: string
  reviewedAt?: string
  feedback?: string
}

interface MockFeedback {
  id: string
  type: 'auto' | 'mentor' | 'peer'
  message: string
  createdAt: string
}

interface MockCriterion {
  id: string
  description: string
  required: boolean
}

interface MockResource {
  title: string
  url: string
  type: 'article' | 'video' | 'tool'
}
```

### 5.4 Competency

```typescript
interface MockCompetency {
  id: string
  name: string
  description: string
  category: 'technical' | 'behavioral' | 'domain'
  level: number
  maxLevel: number
  progress: number
  unlocked: boolean
  unlockedAt?: string
  children: string[]           // sub-competency ids
  prerequisites: string[]
  evidenceCount: number
}
```

### 5.5 Achievement

```typescript
interface MockAchievement {
  id: string
  name: string
  description: string
  icon: string
  category: 'journey' | 'mission' | 'streak' | 'special'
  unlocked: boolean
  unlockedAt?: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
}

interface MockCertificate {
  id: string
  title: string
  description: string
  issuedAt: string
  competencies: CompetencyRef[]
}

interface CompetencyRef {
  id: string
  name: string
  level: number
}
```

### 5.6 Notification

```typescript
interface MockNotification {
  id: string
  type: 'achievement' | 'xp' | 'mission' | 'feedback' | 'system'
  title: string
  message: string
  read: boolean
  createdAt: string
  actionUrl?: string
  icon?: string
}
```

### 5.7 Timeline

```typescript
interface MockTimelineEvent {
  id: string
  type: 'xp_gained' | 'mission_completed' | 'achievement_unlocked'
        | 'journey_started' | 'journey_completed' | 'level_up'
        | 'evidence_submitted' | 'feedback_received'
  title: string
  description: string
  timestamp: string
  icon: string
  metadata?: Record<string, unknown>
}
```

---

## 6. Simulated Behavior

### 6.1 State Transitions

The Mock Engine simulates valid state transitions:

```
Journey: locked → available → in_progress → completed

Mission: locked → available → in_progress → completed

Evidence: pending → accepted | rejected

Competency: locked → unlocked (level up)
```

### 6.2 Side Effects

When a mission is completed:

```
1. XP is awarded to builder
2. Builder progress toward next level updates
3. Journey progress recalculated
4. Related competencies may advance
5. Achievements may unlock
6. Notification created
7. Timeline event recorded
```

When a journey is completed:

```
1. All missions marked completed
2. Competency levels increased
3. Certificate issued (if applicable)
4. Notification created
5. Timeline event recorded
```

### 6.3 Latency Simulation

```typescript
interface LatencyConfig {
  base: number                  // ms
  variance: number              // ms (added randomly)
  distribution: 'uniform' | 'normal'
}

// Default: { base: 50, variance: 30, distribution: 'normal' }
```

### 6.4 Failure Simulation

```typescript
interface FailureConfig {
  rate: number                  // 0-1
  statuses: number[]            // [500, 503, 408, 429]
  endpoints?: string[]          // specific paths, empty = all
}
```

---

## 7. MockTransport ↔ MockEngine Contract

The MockTransport wraps the MockEngine and maps requests to engine methods:

```typescript
class MockTransport implements Transport {
  private engine: MockEngine

  async request<T>(config: RequestConfig): Promise<TransportResponse<T>> {
    this.simulateLatency()
    this.maybeFail()

    return this.route(config)    // maps path → engine method
  }

  private route<T>(config: RequestConfig): TransportResponse<T> {
    // GET    /builder          → engine.getBuilder()
    // GET    /journeys         → engine.getJourneys()
    // GET    /journeys/:id     → engine.getJourney(id)
    // POST   /missions/:id/evidence → engine.submitEvidence(id, body)
    // ...
  }
}
```

---

## 8. Reset and Lifecycle

```typescript
// Full reset — returns to initial seed state
engine.reset()

// Partial reset — preserves builder, resets progress
engine.reset({ preserveBuilder: true, resetProgress: true })

// Custom seed — load specific scenario
engine.loadPreset('comprehensive')

// Advance simulation — triggers time-based events
engine.advanceTime(3600000)  // 1 hour
```

---

## 9. Mock Engine Rules

| Rule | Description |
|------|-------------|
| **M1** | Mock Engine must work without any network, database, or external dependency |
| **M2** | State transitions must follow domain rules (no invalid states) |
| **M3** | Side effects must be consistent (completing mission awards XP) |
| **M4** | All 3 presets must initialize deterministically |
| **M5** | `reset()` must restore exact initial state |
| **M6** | Failure simulation must not break the engine (always recoverable) |
| **M7** | Call history must be inspectable for test assertions |

---

## 10. Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO TITAN |
