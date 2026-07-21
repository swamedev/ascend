# ARCH-0027 — Builder Identity Model

| Field | Value |
|-------|-------|
| **ID** | ARCH-0027 |
| **Name** | Builder Identity Model |
| **Version** | 2.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | ARCH-0002, ARCH-0005, ARCH-0017, ARCH-0024 |
| **Principle** | Data belongs to the user |

---

## 1. Purpose

Define the formal identity model of a **Builder** — the central actor in the ASCEND platform.

A Builder is not a user account. A Builder is a **portable learning identity** — a self-sovereign, offline-capable, verifiable record of competency development. The Builder owns themselves. The platform is merely a custodian.

> **Guiding Principle:** O Builder é dono da própria identidade. Nunca o servidor.

---

## 2. Builder Identity

A Builder is a **portable learning identity**. It exists independently of any server. It can be exported, imported, backed up, and restored. The platform enables the identity — it does not own it.

```
                     ┌──────────────────────────────────────────┐
                     │           BUILDER IDENTITY                │
                     ├──────────────────────────────────────────┤
                     │                                          │
                     │  ┌──────────┐      ┌──────────────────┐  │
                     │  │ Profile  │      │   Preferences    │  │
                     │  │ (public) │      │    (private)     │  │
                     │  └──────────┘      └──────────────────┘  │
                     │                                          │
                     │  ┌────────────────────────────────────┐  │
                     │  │        Learning Identity            │  │
                     │  │  ┌────────────┐ ┌──────────────┐   │  │
                     │  │  │ Competency │ │ Achievement  │   │  │
                     │  │  │   Graph    │ │   Ledger     │   │  │
                     │  │  └────────────┘ └──────────────┘   │  │
                     │  │  ┌────────────┐ ┌──────────────┐   │  │
                     │  │  │ Evidence   │ │ Assessment   │   │  │
                     │  │  │ Portfolio  │ │   History    │   │  │
                     │  │  └────────────┘ └──────────────┘   │  │
                     │  │  ┌─────────────────────────────┐   │  │
                     │  │  │       Learning Path          │   │  │
                     │  │  └─────────────────────────────┘   │  │
                     │  └────────────────────────────────────┘  │
                     │                                          │
                     │  ┌────────────────────────────────────┐  │
                     │  │       Activity & Progress           │  │
                     │  │  Timeline │  XP │ Streak │ Stats   │  │
                     │  └────────────────────────────────────┘  │
                     │                                          │
                     │  ┌────────────────────────────────────┐  │
                     │  │       Offline Identity              │  │
                     │  │  Local-first  │  Mutation Queue    │  │
                     │  │  Sync Engine  │  Recovery Bundle   │  │
                     │  └────────────────────────────────────┘  │
                     └──────────────────────────────────────────┘
```

---

## 3. Core Types

### 3.1 Builder

```typescript
interface Builder {
  id: BuilderId                    // UUID v4, immutable
  profile: Profile
  preferences: Preferences
  identity: LearningIdentity
  ledger: AchievementLedger
  progress: BuilderProgress
  createdAt: string                // ISO 8601
  updatedAt: string
  deletedAt?: string
}

type BuilderId = string            // UUID v4
```

### 3.2 Profile

```typescript
interface Profile {
  name: string
  avatar?: string
  bio?: string
  email?: string                   // verified, optional
  socialLinks?: SocialLink[]
}

interface SocialLink {
  platform: 'github' | 'linkedin' | 'twitter' | 'website'
  url: string
}
```

### 3.3 Preferences

```typescript
interface Preferences {
  theme: 'light' | 'dark' | 'system'
  language: string                 // ISO 639-1, default 'en'
  reducedMotion: boolean
  fontSize: 'small' | 'medium' | 'large'
  notifications: NotificationPreferences
  privacy: PrivacySettings
}

interface NotificationPreferences {
  email: boolean
  push: boolean
  digest: 'daily' | 'weekly' | 'never'
  mentions: boolean
  achievements: boolean
  milestoneAlerts: boolean
  streakWarnings: boolean
}

interface PrivacySettings {
  profileVisibility: 'public' | 'builders' | 'private'
  showXP: boolean
  showStreak: boolean
  showCompetencies: boolean
  showAchievements: boolean
  showLearningPath: boolean
  showActivityTimeline: boolean
  allowDataCollection: boolean     // anonymized platform analytics
}
```

---

## 4. Learning Identity

The Learning Identity is the **cognitive core** of the Builder. It represents what they know, what they've proven, and their growth trajectory. This data is fully portable and survivable independent of any platform instance.

```typescript
interface LearningIdentity {
  builderId: BuilderId
  competencies: CompetencyGraph
  evidence: EvidencePortfolio
  assessments: AssessmentHistory
  learningPath: LearningPath
  exportedAt?: string              // last export timestamp
  lastVerifiedAt?: string          // last integrity check
}

interface CompetencyGraph {
  nodes: CompetencyNode[]
  edges: CompetencyEdge[]
  lastUpdated: string
}

interface CompetencyNode {
  id: string
  name: string
  category: string
  currentLevel: number             // 0..maxLevel
  maxLevel: number
  progress: number                 // 0.0 – 1.0
  unlockedAt?: string
  evidenceIds: string[]            // links to evidence
  metadata?: Record<string, unknown>
}

interface CompetencyEdge {
  source: string                   // parent competency id
  target: string                   // child competency id
  relationship: 'prerequisite' | 'extends' | 'alternative' | 'replaces'
}

interface EvidencePortfolio {
  totalCount: number
  acceptedCount: number
  pendingCount: number
  rejectedCount: number
  items: EvidenceSummary[]
}

interface EvidenceSummary {
  id: string
  missionId: string
  type: string
  status: 'pending' | 'accepted' | 'rejected'
  submittedAt: string
  competencies: string[]
  reviewedAt?: string
  reviewerNotes?: string
}

interface AssessmentHistory {
  totalTaken: number
  passed: number
  failed: number
  averageScore: number
  recentResults: AssessmentResult[]
}

interface AssessmentResult {
  assessmentId: string
  title: string
  score: number
  total: number
  passed: boolean
  completedAt: string
  competenciesTested: string[]
}

interface LearningPath {
  completedJourneys: string[]
  inProgressJourneys: string[]
  availableJourneys: string[]
  suggestedNext: string[]
  recommendedBy: 'engine' | 'mentor' | 'self'
}
```

---

## 5. Achievement Ledger

The Achievement Ledger is an **append-only, immutable record** of every achievement granted to a Builder. It functions as a verifiable credential store and is the canonical source of truth for what a Builder has earned.

```typescript
interface AchievementLedger {
  builderId: BuilderId
  entries: LedgerEntry[]
  totalAchievements: number
  totalCertificates: number
  lastUpdated: string
}

interface LedgerEntry {
  id: string                       // UUID v4, globally unique
  type: 'achievement' | 'certificate' | 'badge' | 'milestone'
  ref: string                      // achievement/certificate id
  title: string
  description: string
  grantedAt: string                // ISO 8601
  source: 'journey' | 'mission' | 'streak' | 'special' | 'assessment'
  expiresAt?: string
  metadata?: Record<string, unknown>
  verifiable: boolean              // can be cryptographically verified
  signature?: string               // future: cryptographic signature
  revocationToken?: string         // future: self-sovereign revocation
}
```

---

## 6. Builder Progress

Progress is derivable from events (event sourcing), tracked in real-time, and survivable across device migrations.

```typescript
interface BuilderProgress {
  builderId: BuilderId
  level: number
  xp: XPMetrics
  streak: StreakMetrics
  timeline: TimelineEntry[]
  journeyHistory: JourneyHistoryEntry[]
  missionHistory: MissionHistoryEntry[]
  stats: BuilderStats
}

interface XPMetrics {
  current: number
  total: number                    // lifetime XP
  nextLevelAt: number
  history: XPEvent[]
}

interface XPEvent {
  amount: number
  source: string                   // source category
  sourceId: string                 // specific mission/assessment id
  description: string
  timestamp: string
}

interface StreakMetrics {
  current: number
  longest: number
  lastActivity: string
  frozen: boolean
  freezeAvailable: number
  freezeUsed: number
}

interface TimelineEntry {
  id: string
  type: 'xp_gained' | 'achievement' | 'milestone' | 'assessment' | 'journey_complete' | 'mission_complete' | 'level_up'
  title: string
  description: string
  timestamp: string
  icon?: string
  metadata?: Record<string, unknown>
}
```

### 6.1 Journey History

```typescript
interface JourneyHistoryEntry {
  journeyId: string
  journeyName: string
  status: 'not_started' | 'in_progress' | 'completed' | 'abandoned'
  startedAt?: string
  completedAt?: string
  progress: number                 // 0.0 – 1.0
  missionsCompleted: number
  missionsTotal: number
  competenciesGained: string[]
}
```

### 6.2 Mission History

```typescript
interface MissionHistoryEntry {
  missionId: string
  missionName: string
  journeyId: string
  status: 'locked' | 'available' | 'in_progress' | 'completed' | 'failed'
  startedAt?: string
  completedAt?: string
  attempts: number
  evidenceSubmitted: number
  evidenceAccepted: number
  xpEarned: number
}
```

### 6.3 Activity Timeline

The activity timeline is a unified, chronological feed of everything the Builder has done:

```
┌─────────────────────────────────────┐
│         ACTIVITY TIMELINE           │
├─────────────────────────────────────┤
│ Today                               │
│  ├─ 14:32  XP +50  "Data Structures"│
│  ├─ 12:00  Badge  "Early Bird"      │
│  └─ 09:15  Assessment  "Python 101" │
│ Yesterday                           │
│  ├─ 18:45  Mission  "Sorting" ✅    │
│  └─ 10:30  Journey  "Algorithms" 🚀 │
│ This Week                           │
│  └─ ...                             │
└─────────────────────────────────────┘
```

```typescript
interface ActivityTimeline {
  entries: TimelineEntry[]
  filters: {
    types: string[]                  // filter by type
    dateRange: [string, string]     // ISO 8601 range
    sources: string[]                // filter by source
  }
}

interface BuilderStats {
  missionsCompleted: number
  evidenceSubmitted: number
  evidenceAccepted: number
  acceptanceRate: number             // evidenceAccepted / evidenceSubmitted
  achievementsUnlocked: number
  competenciesUnlocked: number
  journeysCompleted: number
  assessmentsPassed: number
  assessmentsFailed: number
  activeDays: number
  currentStreak: number
  longestStreak: number
  totalXp: number
  joinDate: string
  lastActiveDate: string
}
```

---

## 7. Data Sovereignty

### 7.1 Privacy Principles

| Principle | Description |
|-----------|-------------|
| **Local-first** | All data is stored locally by default. Server is a sync target, not a source of truth. |
| **User-owned** | The Builder owns their data. The platform is a custodian with no ownership rights. |
| **Portable** | Full export/import capability. Export contains everything needed to rebuild identity. |
| **Transparent** | Clear what data is stored, why, and who has access. |
| **Minimal** | Only collect data necessary for the learning mission. |
| **Deletable** | Builder can delete their identity at any time. No vendor lock-in. |
| **Verifiable** | Builder can cryptographically verify their own identity bundle. |

### 7.2 Export Format

```typescript
interface BuilderExport {
  version: string                  // export schema version
  exportedAt: string               // ISO 8601
  builder: Builder
  identity: LearningIdentity
  ledger: AchievementLedger
  progress: BuilderProgress
  events: DomainEvent[]            // all domain events for replay
  recovery: RecoveryBundle         // self-contained recovery data
  metadata: {
    format: 'ascend-identity-v2'
    totalSize: number
    eventCount: number
    includes: string[]
    checksum: string               // sha256 of entire payload
    builderSignature?: string      // future: cryptographic signature
  }
}
```

Export is a single compressed archive (`.ascend` extension) containing:
- `identity.json` — full identity payload
- `events.ndjson` — newline-delimited domain events
- `recovery.key` — recovery verification key
- `MANIFEST.json` — metadata and checksums

### 7.3 Import Validation

Import must validate:

1. Schema version compatibility (semver range)
2. Checksum integrity (sha256 of full payload)
3. BuilderId conflict resolution (merge vs replace vs create new)
4. Duplicate event detection by event id
5. Event ordering and gap detection
6. Cross-reference integrity (evidence refs → ledger entries)

```typescript
interface ImportResult {
  success: boolean
  builderId: BuilderId
  importedAt: string
  conflicts: ConflictResolution[]
  stats: {
    eventsImported: number
    eventsSkipped: number
    achievementsImported: number
    evidenceImported: number
  }
  errors: ImportError[]
}
```

---

## 8. Privacy Zones

```
            ┌─────────────────────────────────────────────┐
            │              PUBLIC ZONE                     │
            │  Name, Avatar, Level, Badges                │
            │  Public achievements (opt-in showcase)      │
            │  Readable by: anyone (including anonymous)  │
            └─────────────────────────────────────────────┘
                            │
            ┌─────────────────────────────────────────────┐
            │           BUILDERS ZONE                      │
            │  Journey progress, Competencies              │
            │  Learning path, XP tier                     │
            │  Readable by: authenticated builders         │
            └─────────────────────────────────────────────┘
                            │
            ┌─────────────────────────────────────────────┐
            │           PRIVATE ZONE                       │
            │  Evidence content, Assessment results       │
            │  Preferences, Email, Full activity feed     │
            │  Readable by: self (and platform for ops)   │
            └─────────────────────────────────────────────┘
                            │
            ┌─────────────────────────────────────────────┐
            │           LOCAL ZONE                         │
            │  Offline mutation queue, Sync state         │
            │  Local backups, Pending exports             │
            │  NEVER leaves the device without consent    │
            └─────────────────────────────────────────────┘
```

Privacy cascade: `PUBLIC ⊃ BUILDERS ⊃ PRIVATE ⊃ LOCAL`

Every Privacy Zone is enforced both online and offline. Offline data is encrypted at rest on the device.

---

## 9. Offline Identity

The Builder Identity is **fully functional offline**. The platform is a sync target, not a dependency.

### 9.1 Local-First Architecture

```
                    ┌──────────────────────────┐
                    │     BUILDER DEVICE         │
                    │                            │
                    │  ┌──────────────────────┐  │
                    │  │   Identity Store      │  │
                    │  │  (SQLite / IndexedDB)  │  │
                    │  └──────────────────────┘  │
                    │          │                 │
                    │  ┌──────────────────────┐  │
                    │  │   Mutation Queue      │  │
                    │  │  (offline changes)     │  │
                    │  └──────────────────────┘  │
                    │          │                 │
                    │  ┌──────────────────────┐  │
                    │  │    Sync Engine        │  │
                    │  │  (when online)        │  │
                    │  └──────────────────────┘  │
                    └──────────┬───────────────┘
                               │ sync
                    ┌──────────▼───────────────┐
                    │     ASCEND PLATFORM        │
                    │  (sync target, not owner)  │
                    └──────────────────────────┘
```

### 9.2 Offline Capabilities

- **100% offline identity** — all identity data is available locally
- **Offline mutations queued** — changes are stored in a local mutation queue
- **Sync on reconnect** — when online, sync engine replays mutations
- **Conflict resolution** — last-writer-wins with manual override option

```typescript
interface OfflineIdentity {
  builderId: BuilderId
  localStore: IdentityStore
  mutationQueue: MutationEntry[]
  syncEngine: SyncEngine

  isAvailable(): boolean           // always true — local-first
  hasPendingChanges(): boolean
  pendingChangeCount(): number
}

interface IdentityStore {
  version: string
  storageType: 'sqlite' | 'indexeddb' | 'filesystem'
  encrypted: boolean
  lastLocalBackup: string
  integrityCheck: string          // checksum of store
}

interface MutationEntry {
  id: string
  type: string
  payload: Record<string, unknown>
  createdAt: string
  retryCount: number
  status: 'pending' | 'synced' | 'conflict' | 'failed'
}

interface SyncEngine {
  lastSyncAt?: string
  syncStrategy: 'push-then-pull' | 'pull-then-push' | 'two-way'
  conflictStrategy: 'lww' | 'manual'
  pendingChanges: number
  state: 'idle' | 'syncing' | 'conflict' | 'error'
}
```

### 9.3 Offline Identity Rules

- Identity is always available — no network required
- All mutations are stored locally first
- Sync is best-effort; identity never depends on it
- Offline identity is identical to online identity in structure and capability
- Platform is notified of changes via sync; it never polls the device

---

## 10. Recovery

A Builder can recover their full identity independently of the platform.

### 10.1 Export-Based Recovery

The primary recovery mechanism is the **identity export bundle** (`.ascend` file). This single file contains everything needed to reconstruct the Builder's identity:

- Full identity payload
- All domain events
- Recovery verification key
- Checksum for integrity verification

```typescript
interface RecoveryBundle {
  version: string
  builderId: BuilderId
  recoveryKey: string              // 256-bit key, user-provided or generated
  recoveryType: 'export' | 'local-backup' | 'cloud'
  createdAt: string
  encrypted: boolean
  integrityHash: string
}
```

### 10.2 Local Backup

```typescript
interface LocalBackup {
  version: string
  builderId: BuilderId
  backupPath: string
  frequency: 'manual' | 'daily' | 'weekly'
  lastBackupAt: string
  includes: ('identity' | 'events' | 'preferences')[]
  encrypted: boolean
  size: number
}
```

### 10.3 Cloud Recovery (Future)

Future versions may support cloud recovery, but it is **never required**:

- Builder opts in to cloud backup
- End-to-end encrypted before upload
- Platform cannot read identity data
- Recovery can be triggered from any device
- Cloud recovery never replaces export-based recovery

### 10.4 Identity Verification Flow

```
1. Builder requests recovery
2. System generates recovery token (or uses existing export)
3. Builder proves ownership:
   a. Via recovery key (from export)
   b. Via email verification (if available)
   c. Via cryptographic signature (future)
4. Identity bundle is decrypted and loaded
5. Integrity check runs against checksum
6. Identity is reconstructed from events
7. Builder confirms identity is correct
8. New recovery bundle is generated
```

```typescript
interface IdentityRecovery {
  step: 'initiated' | 'verifying' | 'decrypting' | 'validating' | 'reconstructing' | 'confirmed'
  recoverySource: 'export' | 'local-backup' | 'cloud' | 'fresh'
  verificationMethod: 'recovery-key' | 'email' | 'crypto-signature'
  startedAt: string
  completedAt?: string
  result?: 'success' | 'partial' | 'failed'
  errors?: RecoveryError[]
}
```

Recovery never requires platform intervention (Rule B10).

---

## 11. Ownership

### 11.1 Formal Ownership Model

```
                    ┌──────────────────────────────────────┐
                    │         DATA OWNERSHIP                │
                    ├──────────────────────────────────────┤
                    │                                      │
                    │  ┌──────────────────────────────┐    │
                    │  │      BUILDER (OWNER)          │    │
                    │  │  ─ Full ownership rights      │    │
                    │  │  ─ Complete data portability  │    │
                    │  │  ─ Deletion rights            │    │
                    │  │  ─ No vendor lock-in          │    │
                    │  └──────────────────────────────┘    │
                    │              │                        │
                    │  ┌──────────────────────────────┐    │
                    │  │   PLATFORM (CUSTODIAN)        │    │
                    │  │  ─ Stores on behalf of user  │    │
                    │  │  ─ No ownership rights       │    │
                    │  │  ─ Must honor deletion       │    │
                    │  │  ─ Must enable export        │    │
                    │  └──────────────────────────────┘    │
                    │                                      │
                    │  ┌──────────────────────────────┐    │
                    │  │     THIRD PARTIES              │    │
                    │  │  ─ Zero access by default     │    │
                    │  │  ─ Access only with consent   │    │
                    │  │  ─ Revocable at any time      │    │
                    │  └──────────────────────────────┘    │
                    └──────────────────────────────────────┘
```

### 11.2 Ownership Principles

| Principle | Description |
|-----------|-------------|
| **Full Ownership** | The Builder owns all data — profile, identity, ledger, preferences, progress |
| **Platform as Custodian** | The platform stores and processes data only on behalf of the Builder |
| **Data Portability** | Full export/import at any time, no restrictions |
| **Deletion Rights** | Builder can delete their identity at any time. Platform must honor within 30 days |
| **No Vendor Lock-in** | Identity is portable. Builder can leave the platform at any time with all their data |
| **Revocable Consent** | Any third-party access granted can be revoked by the Builder at any time |
| **Zero Default Access** | No third party has access by default. All access requires explicit consent |

### 11.3 Ownership Implementation

```typescript
interface OwnershipModel {
  owner: BuilderId
  custodian: string                // platform identifier
  rights: OwnershipRight[]
  consentGrants: ConsentGrant[]
  dataPortability: {
    exportAvailable: boolean
    lastExportAt?: string
    formats: ('ascend' | 'json' | 'openbadges')[]
  }
  deletionRequest?: {
    requestedAt: string
    confirmedAt?: string
    processedAt?: string
    status: 'pending' | 'confirmed' | 'processing' | 'completed'
  }
}

type OwnershipRight =
  | 'read'
  | 'export'
  | 'modify'
  | 'delete'
  | 'grant_access'
  | 'revoke_access'

interface ConsentGrant {
  grantee: string                  // third party identifier
  scope: string[]                  // what data is shared
  grantedAt: string
  expiresAt?: string
  revokedAt?: string
}
```

---

## 12. Builder Identity Rules

| Rule | Description |
|------|-------------|
| **B1** | BuilderId is immutable and globally unique |
| **B2** | Profile is the only public-facing identity |
| **B3** | Learning Identity is always exportable and portable |
| **B4** | Achievement Ledger is append-only and immutable |
| **B5** | Progress is derivable from events (event sourcing principle) |
| **B6** | Preferences never leave the device without explicit consent |
| **B7** | Privacy settings cascade: PUBLIC ⊃ BUILDERS ⊃ PRIVATE ⊃ LOCAL |
| **B8** | Deletion is logical (soft-delete), never physical (GDPR exception applies) |
| **B9** | Offline identity is structurally identical to online identity — same types, same capabilities, same data |
| **B10** | Recovery never requires platform intervention. A Builder can always recover independently from their export bundle |
| **B11** | Export contains everything needed to rebuild identity — no server-side data is necessary for reconstruction |
| **B12** | Ownership is explicit: Builder owns, platform custodies, third parties access only with revocable consent |

---

## 13. Future: Cloud Sync

Cloud sync is an optional enhancement that never compromises local-first sovereignty.

```typescript
interface CloudSyncConfig {
  enabled: boolean
  provider: 'ascend-cloud' | 'self-hosted' | 'custom-s3' | 'webdav'
  syncInterval: number            // ms
  conflictStrategy: 'lww' | 'manual'
  lastSyncAt?: string
  pendingChanges: number
  encryption: {
    inTransit: boolean            // always true (TLS)
    atRest: boolean               // always true (AES-256-GCM)
    keyDerivation: 'pbkdf2' | 'argon2'
  }
}
```

### Sync Rules

| Rule | Description |
|------|-------------|
| **S1** | Local is always the source of truth |
| **S2** | Conflicts are resolved by last-writer-wins or manual override |
| **S3** | Never delete remotely — only merge |
| **S4** | Full end-to-end encryption in transit and at rest |
| **S5** | Sync is opt-in, never required |
| **S6** | Offline mutations are queued and pushed on reconnect |
| **S7** | Platform never polls device — device pushes changes when online |

---

## 14. Definition of Done

ARCH-0027 is approved when:

- [x] Builder identity structure documented (Core Types)
- [x] Profile type defined with social links
- [x] Preferences type defined with notification and privacy settings
- [x] Learning Identity documented (Competency Graph, Evidence Portfolio, Assessment History, Learning Path)
- [x] Achievement Ledger defined as immutable, append-only record
- [x] Builder Progress types (XP, Streak, Timeline, Journey History, Mission History, Stats)
- [x] Activity Timeline documented with visual
- [x] Data sovereignty principles documented
- [x] Export/Import format specified with validation rules
- [x] Privacy zones diagrammed (4 zones including Local Zone)
- [x] Offline Identity architecture documented (9.1 — 9.3)
- [x] Recovery mechanism documented (10.1 — 10.4)
- [x] Ownership model formally defined (11.1 — 11.3)
- [x] 12 Builder Identity rules defined (B1—B12)
- [x] Cloud Sync strategy outlined with encryption requirements
- [ ] Reviewed by Architecture Board
- [ ] Final approval by Chief Architect

---

## 15. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 2.0 | 2026-07-20 | Chief Architect | Identity rewritten as portable learning identity. Added Offline Identity (§9), Recovery (§10), Ownership Model (§11), rules B9—B12. Enhanced all types, diagrams, and privacy zones. |
| 1.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO APOLLO |
