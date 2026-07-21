# SDK-0002 — ASCEND Frontend SDK Clients

**Status:** Draft  
**Version:** 1.0.0  
**Obsoletes:** None  
**License:** MIT  

---

## 1. Abstract

SDK-0002 defines the **client interfaces** of the ASCEND Frontend SDK: `BuilderClient`, `JourneyClient`, `MissionClient`, `AssessmentClient`, `AchievementClient`, and `ProfileClient`. Every feature consumes domain data exclusively through these clients. No feature imports a transport, calls an API, or knows the data source.

---

## 2. Scope

This specification covers:

- All 6 client interfaces
- Method signatures and return types
- Error conditions per method
- Cache policies per endpoint
- Event emissions per mutation

It does **not** cover:

- Transport implementation (see SDK-0003)
- Mock Engine (see SDK-0004)
- Core SDK lifecycle (see SDK-0001)

---

## 3. Common Patterns

### 3.1 Return Type

Every client method returns a `Result<T>` — never a raw promise:

```typescript
type Result<T> = {
  data: T
  source: 'cache' | 'network' | 'mock'
  timestamp: number
}
```

### 3.2 Error Handling

Methods throw typed errors (never raw `Error`):

| Error | When |
|-------|------|
| `ValidationError` | Invalid arguments |
| `NetworkError` | Transport failure |
| `AuthenticationError` | Unauthenticated |
| `OfflineError` | Operation unavailable offline |

### 3.3 Cache Policy

Each method declares its cache policy:

```typescript
type CachePolicy = {
  ttl: number                    // ms
  staleWhileRevalidate: boolean
  invalidateOnMutate: string[]   // related cache keys
}
```

### 3.4 Events

Mutations publish events to the EventBus. The event name follows the pattern `{Resource}{Action}` (e.g., `MissionCompleted`).

---

## 4. BuilderClient

```typescript
interface BuilderClient {
  // ─── Profile ─────────────────────────────────────

  getProfile(): Promise<Result<BuilderProfile>>
  updateProfile(data: Partial<BuilderProfile>): Promise<Result<BuilderProfile>>

  // ─── XP & Level ──────────────────────────────────

  getXP(): Promise<Result<XPBalance>>
  getLevel(): Promise<Result<LevelInfo>>

  // ─── Timeline ────────────────────────────────────

  getTimeline(params?: TimelineParams): Promise<Result<TimelineEvent[]>>

  // ─── Stats ───────────────────────────────────────

  getStats(): Promise<Result<BuilderStats>>
}
```

### 4.1 Types

```typescript
interface BuilderProfile {
  id: string
  name: string
  avatar?: string
  bio?: string
  joinedAt: string              // ISO date
  level: number
  xp: XPBalance
  streak: Streak
}

interface XPBalance {
  current: number
  total: number
  nextLevel: number
  progress: number              // 0-1
}

interface LevelInfo {
  level: number
  title: string
  xpRequired: number
  unlocked: string[]            // achievement ids
}

interface Streak {
  current: number
  longest: number
  lastActivity: string          // ISO date
}

interface BuilderStats {
  missionsCompleted: number
  evidenceSubmitted: number
  achievementsUnlocked: number
  currentJourney?: string
  activeDays: number
}

interface TimelineParams {
  limit?: number
  offset?: number
  type?: 'xp' | 'achievement' | 'mission' | 'assessment'
}
```

### 4.2 Cache Policy

| Method | TTL | Stale-While-Revalidate | Invalidate On |
|--------|-----|----------------------|---------------|
| `getProfile` | 60000 | yes | `updateProfile` |
| `getXP` | 30000 | yes | `updateProfile` |
| `getLevel` | 60000 | yes | — |
| `getTimeline` | 30000 | no | — |
| `getStats` | 60000 | yes | `updateProfile` |

### 4.3 Events

| Mutation | Event |
|----------|-------|
| `updateProfile` | `BuilderUpdated` |

---

## 5. JourneyClient

```typescript
interface JourneyClient {
  // ─── CRUD ────────────────────────────────────────

  list(params?: JourneyListParams): Promise<Result<JourneySummary[]>>
  get(id: string): Promise<Result<JourneyDetail>>
  start(id: string): Promise<Result<JourneyDetail>>
  abandon(id: string): Promise<Result<void>>

  // ─── Progress ────────────────────────────────────

  getProgress(id: string): Promise<Result<JourneyProgress>>
  getTree(id: string): Promise<Result<JourneyNode[]>>
}
```

### 5.1 Types

```typescript
interface JourneySummary {
  id: string
  title: string
  description: string
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  progress: number              // 0-1
  prerequisites?: string[]
  tags?: string[]
}

interface JourneyDetail extends JourneySummary {
  missions: MissionSummary[]
  competencies: CompetencyRef[]
  estimatedHours: number
  startedAt?: string
  completedAt?: string
}

interface JourneyProgress {
  journeyId: string
  totalMissions: number
  completedMissions: number
  totalXP: number
  earnedXP: number
  lastActivity: string
}

interface JourneyNode {
  id: string
  type: 'mission' | 'gate' | 'milestone'
  status: 'locked' | 'available' | 'completed'
  children: JourneyNode[]
}

interface JourneyListParams {
  status?: 'available' | 'in_progress' | 'completed'
  tag?: string
  search?: string
}
```

### 5.2 Cache Policy

| Method | TTL | SWR | Invalidate On |
|--------|-----|-----|---------------|
| `list` | 60000 | yes | `start`, `abandon` |
| `get` | 60000 | yes | `start`, `abandon` |
| `getProgress` | 30000 | yes | `start` |
| `getTree` | 120000 | no | `start` |

### 5.3 Events

| Mutation | Event |
|----------|-------|
| `start` | `JourneyStarted` |
| `abandon` | `JourneyAbandoned` |
| — | `JourneyCompleted` (from mission completion) |

---

## 6. MissionClient

```typescript
interface MissionClient {
  // ─── CRUD ────────────────────────────────────────

  list(params?: MissionListParams): Promise<Result<MissionSummary[]>>
  get(id: string): Promise<Result<MissionDetail>>

  // ─── Evidence ────────────────────────────────────

  submitEvidence(missionId: string, evidence: EvidenceInput): Promise<Result<EvidenceRecord>>
  getEvidence(missionId: string): Promise<Result<EvidenceRecord[]>>

  // ─── Feedback ────────────────────────────────────

  getFeedback(missionId: string): Promise<Result<Feedback[]>>

  // ─── Status ──────────────────────────────────────

  complete(missionId: string): Promise<Result<MissionResult>>
}
```

### 6.1 Types

```typescript
interface MissionSummary {
  id: string
  title: string
  description: string
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  xpReward: number
  journeyId?: string
}

interface MissionDetail extends MissionSummary {
  instructions: string
  criteria: Criterion[]
  resources: Resource[]
  evidenceRequired: boolean
  startedAt?: string
  completedAt?: string
  feedback?: Feedback[]
}

interface EvidenceInput {
  type: 'text' | 'file' | 'link' | 'image'
  content: string
  description?: string
}

interface EvidenceRecord {
  id: string
  missionId: string
  type: string
  content: string
  status: 'pending' | 'accepted' | 'rejected'
  submittedAt: string
  reviewedAt?: string
  feedback?: string
}

interface Feedback {
  id: string
  type: 'auto' | 'mentor' | 'peer'
  message: string
  createdAt: string
}

interface MissionResult {
  missionId: string
  xpEarned: number
  achievementsUnlocked: string[]
  competenciesAdvanced: CompetencyRef[]
}

interface MissionListParams {
  journeyId?: string
  status?: 'available' | 'in_progress' | 'completed'
  difficulty?: string
}

interface Criterion {
  id: string
  description: string
  required: boolean
}

interface Resource {
  title: string
  url: string
  type: 'article' | 'video' | 'tool'
}
```

### 6.2 Cache Policy

| Method | TTL | SVR | Invalidate On |
|--------|-----|-----|---------------|
| `list` | 30000 | yes | `submitEvidence`, `complete` |
| `get` | 60000 | yes | `submitEvidence`, `complete` |
| `getEvidence` | 15000 | yes | `submitEvidence` |
| `getFeedback` | 30000 | yes | `submitEvidence` |

### 6.3 Events

| Mutation | Event |
|----------|-------|
| `submitEvidence` | `EvidenceSubmitted` |
| `complete` | `MissionCompleted` |

---

## 7. AssessmentClient

```typescript
interface AssessmentClient {
  // ─── Assessments ─────────────────────────────────

  list(params?: AssessmentListParams): Promise<Result<AssessmentSummary[]>>
  get(id: string): Promise<Result<AssessmentDetail>>
  start(id: string): Promise<Result<AssessmentSession>>

  // ─── Responses ───────────────────────────────────

  submitResponse(sessionId: string, answers: Answer[]): Promise<Result<AssessmentResult>>

  // ─── Rubrics ─────────────────────────────────────

  getRubric(assessmentId: string): Promise<Result<Rubric>>
}
```

### 7.1 Types

```typescript
interface AssessmentSummary {
  id: string
  title: string
  type: 'quiz' | 'practical' | 'project'
  duration?: number             // minutes
  passingScore: number
  status: 'available' | 'in_progress' | 'passed' | 'failed'
}

interface AssessmentDetail extends AssessmentSummary {
  instructions: string
  questionCount: number
  rubricId: string
}

interface AssessmentSession {
  id: string
  assessmentId: string
  startedAt: string
  timeRemaining?: number
  questions: Question[]
}

interface Question {
  id: string
  type: 'multiple_choice' | 'essay' | 'coding' | 'upload'
  prompt: string
  options?: string[]
  maxScore: number
}

interface Answer {
  questionId: string
  value: string | string[]
}

interface AssessmentResult {
  sessionId: string
  score: number
  total: number
  passed: boolean
  feedback: Feedback[]
}

interface Rubric {
  id: string
  criteria: RubricCriterion[]
}

interface AssessmentListParams {
  status?: 'available' | 'passed' | 'failed'
}
```

### 7.2 Cache Policy

| Method | TTL | SWR | Invalidate On |
|--------|-----|-----|---------------|
| `list` | 60000 | yes | — |
| `get` | 60000 | yes | — |
| `getRubric` | 300000 | no | — |

### 7.3 Events

| Mutation | Event |
|----------|-------|
| `submitResponse` | `AssessmentCompleted` |

---

## 8. AchievementClient

```typescript
interface AchievementClient {
  // ─── Badges ──────────────────────────────────────

  getBadges(): Promise<Result<Badge[]>>

  // ─── Certificates ────────────────────────────────

  getCertificates(): Promise<Result<Certificate[]>>
  downloadCertificate(id: string): Promise<Result<Blob>>

  // ─── Progress ────────────────────────────────────

  getProgress(): Promise<Result<AchievementProgress>>
}
```

### 8.1 Types

```typescript
interface Badge {
  id: string
  name: string
  description: string
  icon: string
  unlocked: boolean
  unlockedAt?: string
  category: 'journey' | 'mission' | 'streak' | 'special'
}

interface Certificate {
  id: string
  title: string
  description: string
  issuedAt: string
  expiresAt?: string
  issuer: string
  competencies: CompetencyRef[]
}

interface AchievementProgress {
  totalBadges: number
  unlockedBadges: number
  totalCertificates: number
  earnedCertificates: number
  nextMilestone?: {
    name: string
    progress: number           // 0-1
  }
}
```

### 8.2 Cache Policy

| Method | TTL | SWR | Invalidate On |
|--------|-----|-----|---------------|
| `getBadges` | 120000 | yes | — |
| `getCertificates` | 120000 | yes | — |
| `getProgress` | 60000 | yes | — |

### 8.3 Events

No direct mutations. Events are emitted by other clients (e.g., `MissionCompleted` may trigger badge unlock, but the AchievementClient only reads).

---

## 9. ProfileClient

```typescript
interface ProfileClient {
  // ─── Settings ────────────────────────────────────

  getSettings(): Promise<Result<UserSettings>>
  updateSettings(settings: Partial<UserSettings>): Promise<Result<UserSettings>>

  // ─── Preferences ─────────────────────────────────

  getPreferences(): Promise<Result<UserPreferences>>
  updatePreferences(prefs: Partial<UserPreferences>): Promise<Result<UserPreferences>>

  // ─── Account ─────────────────────────────────────

  deleteAccount(reason?: string): Promise<Result<void>>
}
```

### 9.1 Types

```typescript
interface UserSettings {
  profile: {
    name: string
    email: string
    avatar?: string
    bio?: string
  }
  notifications: {
    email: boolean
    push: boolean
    digest: 'daily' | 'weekly' | 'never'
  }
  privacy: {
    profileVisibility: 'public' | 'builders' | 'private'
    showXP: boolean
    showStreak: boolean
  }
}

interface UserPreferences {
  theme: 'light' | 'dark' | 'system'
  language: string
  reducedMotion: boolean
  sidebarCollapsed: boolean
  fontSize: 'small' | 'medium' | 'large'
}
```

### 9.2 Cache Policy

| Method | TTL | SWR | Invalidate On |
|--------|-----|-----|---------------|
| `getSettings` | 300000 | yes | `updateSettings` |
| `getPreferences` | 300000 | yes | `updatePreferences` |

### 9.3 Events

| Mutation | Event |
|----------|-------|
| `updateSettings` | `SettingsUpdated` |
| `updatePreferences` | `PreferencesUpdated` |
| `deleteAccount` | `AccountDeleted` |

---

## 10. Registration

All clients are created and exposed by `AscendSDK` during initialization. No client is ever instantiated directly.

```typescript
class AscendSDK {
  constructor(config: SDKConfig) {
    const transport = createTransport(config)
    const cache = new CacheStore(config.cache)
    const events = new EventBus(config.events)

    this.builder = new BuilderClient(transport, cache, events)
    this.journey = new JourneyClient(transport, cache, events)
    this.mission = new MissionClient(transport, cache, events)
    this.assessment = new AssessmentClient(transport, cache, events)
    this.achievement = new AchievementClient(transport, cache, events)
    this.profile = new ProfileClient(transport, cache, events)
  }
}
```

---

## 11. Client Rules

| Rule | Description |
|------|-------------|
| **C1** | Clients never import transport-specific code |
| **C2** | Clients never call `fetch`, `axios`, or any HTTP library |
| **C3** | Every mutation publishes exactly one event |
| **C4** | Read methods check cache before transport |
| **C5** | Write methods invalidate related cache entries |
| **C6** | All dates are ISO 8601 strings |
| **C7** | All IDs are UUID v4 |

---

## 12. Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO TITAN |
