# ARCH-0020 — UI Contracts

| Field | Value |
|-------|-------|
| **ID** | ARCH-0020 |
| **Name** | UI Contracts |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | ARCH-0011, ARCH-0019, WF-0001 through WF-0010 |
| **Referenced by** | Frontend Implementation |

---

## 1. Purpose

Define the exact data contract for every screen in ASCEND.

Each screen declares: "I need exactly this data, nothing more, nothing less."

This prevents over-fetching, under-fetching, and coupling between UI and backend.

---

## 2. Contract Philosophy

| Rule | Statement |
|------|-----------|
| **C1** | Each screen has one contract — no surprises |
| **C2** | The contract is the API response type — no transformation layer needed |
| **C3** | Contracts are shared between SDK and API — single source of truth |
| **C4** | No screen imports Runtime types — only contract types |
| **C5** | Contracts evolve via additive fields — never remove without version bump |

---

## 3. Dashboard Contract

**File:** `@ascend/types/contracts/dashboard.ts`

**Used by:** WF-0001 — Dashboard

```typescript
interface DashboardContract {
  // Active mission (priority 1)
  activeMission: {
    id: string
    title: string
    description: string
    journeyName: string
    progress: number  // 0-100
    difficulty: 'beginner' | 'medium' | 'hard'
    estimatedMinutes: number
  } | null  // null if no active mission

  // Quick stats (priority 2)
  stats: {
    totalMissions: number
    completedMissions: number
    earnedCompetencies: number
    unlockedAchievements: number
  }

  // Streak (priority 3)
  streak: {
    currentDays: number
    longestDays: number
    milestone: number | null  // e.g. 7, 14, 30
  }

  // Level / XP (priority 3)
  progression: {
    level: number
    title: string
    xpCurrent: number
    xpMax: number
  }

  // Next achievement (priority 3)
  nextAchievement: {
    id: string
    name: string
    progress: number  // 0-100
  } | null

  // Activity feed (priority 4)
  recentActivity: Array<{
    id: string
    type: 'mission_complete' | 'achievement' | 'level_up' | 'evidence_reviewed'
    description: string
    timestamp: string  // ISO 8601
    xpEarned?: number
  }>

  // Mentor suggestion (priority 5)
  mentorSuggestion: {
    text: string
    type: 'tip' | 'insight' | 'encouragement'
    actionUrl?: string
  } | null
}
```

---

## 4. Journey Explorer Contract

**File:** `@ascend/types/contracts/journeys.ts`

**Used by:** WF-0002 — Journey Explorer

```typescript
interface JourneySummary {
  id: string
  name: string
  icon: string
  description: string
  totalMissions: number
  completedMissions: number
  competencyCount: number
  progress: number  // 0-100
  difficulty: 'beginner' | 'medium' | 'hard'
  totalXp: number
  estimatedHours: number
  prerequisites: string[]
  status: 'locked' | 'available' | 'active' | 'completed'
  tags: string[]
}

interface JourneyListContract {
  journeys: JourneySummary[]
  filters: {
    status: string[]
    difficulty: string[]
    tags: string[]
  }
}

interface JourneyDetailContract {
  journey: JourneySummary & {
    competencies: Array<{
      id: string
      name: string
      level: number
      maxLevel: number
      progress: number
      status: 'locked' | 'available' | 'in_progress' | 'dominated'
    }>
    missions: Array<{
      id: string
      title: string
      order: number
      difficulty: string
      estimatedMinutes: number
      xpReward: number
      status: 'locked' | 'available' | 'active' | 'completed'
      prerequisites: string[]
    }>
  }
}
```

---

## 5. Mission Workspace Contract

**File:** `@ascend/types/contracts/missions.ts`

**Used by:** WF-0003 — Mission Workspace

```typescript
interface MissionDetailContract {
  id: string
  title: string
  journeyId: string
  journeyName: string

  // Core
  objective: string
  description: string
  difficulty: 'beginner' | 'medium' | 'hard'
  estimatedMinutes: number
  xpReward: number

  // Status
  status: 'available' | 'active' | 'submitted' | 'reviewed' | 'completed'
  progress: number  // 0-100, only meaningful for active

  // Rubric
  rubric: Array<{
    id: string
    criterion: string
    weight: number  // 0-100
    score?: number  // null if not yet reviewed
  }>

  // Resources
  resources: Array<{
    type: 'document' | 'video' | 'link'
    title: string
    url: string
  }>

  // Evidence (if submitted)
  evidence?: {
    id: string
    files: Array<{ name: string; url: string; size: number }>
    description: string
    submittedAt: string
    status: 'pending' | 'approved' | 'rejected'
  }

  // Feedback (if reviewed)
  feedback?: {
    score: number
    totalScore: number
    comments: string
    rubricScores: Array<{
      criterionId: string
      score: number
      comment?: string
    }>
    reviewer: 'ai' | 'human'
    reviewedAt: string
  }
}

interface StartMissionResponse {
  mission: MissionDetailContract
  message: string
}

interface SubmitEvidenceResponse {
  evidenceId: string
  status: 'pending'
  message: string
}
```

---

## 6. Competency Tree Contract

**File:** `@ascend/types/contracts/competencies.ts`

**Used by:** WF-0004 — Competency Tree

```typescript
interface CompetencyNode {
  id: string
  name: string
  icon: string
  description: string
  level: number   // 0-5
  maxLevel: number
  progress: number  // 0-100
  xpEarned: number
  missionsCompleted: number
  totalMissions: number
  status: 'locked' | 'available' | 'in_progress' | 'dominated'
  prerequisites: string[]  // competency IDs
  children: CompetencyNode[]
}

interface CompetencyTreeContract {
  root: CompetencyNode
}

interface CompetencyDetailContract {
  competency: CompetencyNode & {
    missions: Array<{
      id: string
      title: string
      status: string
      xpReward: number
    }>
    evidence: Array<{
      id: string
      title: string
      status: string
      submittedAt: string
    }>
  }
}
```

---

## 7. Builder Profile Contract

**File:** `@ascend/types/contracts/builder.ts`

**Used by:** WF-0005 — Builder Profile

```typescript
interface BuilderProfileContract {
  // Identity
  id: string
  name: string
  avatar: string | null
  bio: string | null
  title: string
  level: number
  joinDate: string

  // Progression
  progression: {
    xpCurrent: number
    xpMax: number
    xpTotal: number
    level: number
    title: string
  }

  // Stats
  stats: {
    totalMissions: number
    completedCompetencies: number
    earnedAchievements: number
    streakDays: number
    totalStudyHours: number
    learningVelocity: number  // XP/week
    velocityTrend: number     // percentage vs last month
  }

  // XP History (for chart)
  xpHistory: Array<{
    date: string
    xpEarned: number
    cumulativeXp: number
  }>

  // Competencies (summary for ring)
  competencies: Array<{
    id: string
    name: string
    icon: string
    level: number
    progress: number
  }>

  // Timeline
  recentEvents: Array<{
    id: string
    type: string
    description: string
    timestamp: string
  }>
}
```

---

## 8. Evidence Center Contract

**File:** `@ascend/types/contracts/evidence.ts`

**Used by:** WF-0006 — Evidence Center

```typescript
interface EvidenceItem {
  id: string
  missionTitle: string
  journeyName: string
  description: string
  status: 'pending' | 'under_review' | 'approved' | 'rejected'
  score: number | null
  totalScore: number | null
  files: Array<{
    name: string
    url: string
    size: number
    type: string
  }>
  submittedAt: string
  reviewedAt: string | null
  feedback: string | null
}

interface EvidenceListContract {
  evidence: EvidenceItem[]
  meta: PaginationMeta
}

interface EvidenceDetailContract {
  evidence: EvidenceItem & {
    rubric: Array<{
      criterion: string
      weight: number
      score?: number
      comment?: string
    }>
    canResubmit: boolean
  }
}
```

---

## 9. Achievement Gallery Contract

**File:** `@ascend/types/contracts/achievements.ts`

**Used by:** WF-0007 — Achievement Gallery

```typescript
interface Badge {
  id: string
  name: string
  description: string
  icon: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary' | 'mythic'
  status: 'earned' | 'locked' | 'hidden'
  earnedAt: string | null
  progress: number | null  // 0-100 if in progress
}

interface Certificate {
  id: string
  title: string
  competencyName: string
  level: string
  issuedAt: string
  verificationUrl: string
}

interface AchievementGalleryContract {
  badges: Badge[]
  certificates: Certificate[]
  levelHistory: Array<{
    level: number
    title: string
    reachedAt: string
    xpRequired: number
  }>
  stats: {
    totalBadges: number
    earnedBadges: number
    totalCertificates: number
    currentLevel: number
    maxLevel: number
  }
}
```

---

## 10. AI Mentor Contract

**File:** `@ascend/types/contracts/mentor.ts`

**Used by:** WF-0008 — AI Mentor

```typescript
interface MentorSuggestion {
  id: string
  text: string
  type: 'tip' | 'insight' | 'encouragement' | 'intervention'
  context: string | null
  actionLabel: string | null
  actionUrl: string | null
}

interface MentorMessage {
  id: string
  role: 'mentor' | 'builder'
  content: string
  timestamp: string
}

interface MentorAskResponse {
  message: MentorMessage
  suggestions: MentorSuggestion[]
}

interface MentorPanelContract {
  status: 'online' | 'thinking' | 'offline'
  currentSuggestion: MentorSuggestion | null
  quickActions: Array<{
    id: string
    label: string
    icon: string
    action: string
  }>
  context: {
    currentMission: string | null
    currentJourney: string | null
    progress: number | null
  }
}
```

---

## 11. Analytics Contract

**File:** `@ascend/types/contracts/analytics.ts`

```typescript
interface AnalyticsSummaryContract {
  weeklyReport: {
    missionsCompleted: number
    xpEarned: number
    competenciesAdvanced: number
    badgesEarned: number
    activeDays: number
    averageSessionMinutes: number
  }
  xpHistory: Array<{
    date: string
    xpEarned: number
  }>
  velocity: {
    currentWeek: number
    previousWeek: number
    trend: number  // percentage
    average: number
  }
}
```

---

## 12. Shared Types

```typescript
// Shared across all contracts
interface PaginationMeta {
  page: number
  perPage: number
  total: number
  totalPages: number
  hasNext: boolean
  hasPrev: boolean
}

type Difficulty = 'beginner' | 'medium' | 'hard'
type MissionStatus = 'locked' | 'available' | 'active' | 'submitted' | 'reviewed' | 'completed'
type CompetencyStatus = 'locked' | 'available' | 'in_progress' | 'dominated'
type EvidenceStatus = 'pending' | 'under_review' | 'approved' | 'rejected'
type BadgeStatus = 'earned' | 'locked' | 'hidden'
```

---

## 13. Contract Location

```
packages/
└── types/
    └── contracts/
        ├── dashboard.ts
        ├── journeys.ts
        ├── missions.ts
        ├── competencies.ts
        ├── builder.ts
        ├── evidence.ts
        ├── achievements.ts
        ├── mentor.ts
        └── analytics.ts
```

All contracts live in `@ascend/types/contracts/`. They are used by:
- **SDK** — to type API responses
- **API** — to type API responses (single source of truth)
- **Frontend** — to type component props and hook returns
- **Tests** — to type test fixtures

---

## 14. Definition of Done

ARCH-0020 aprovado quando:

- [ ] Contract philosophy defined (5 rules)
- [ ] Dashboard contract complete
- [ ] Journey Explorer contracts complete (list + detail)
- [ ] Mission Workspace contract complete
- [ ] Competency Tree contracts complete (tree + detail)
- [ ] Builder Profile contract complete
- [ ] Evidence Center contracts complete (list + detail)
- [ ] Achievement Gallery contract complete
- [ ] AI Mentor contracts complete
- [ ] Analytics contract complete
- [ ] Shared types defined
- [ ] Contract location and usage documented

---

## 15. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
