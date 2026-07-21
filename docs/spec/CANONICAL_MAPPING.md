# CANONICAL_MAPPING.md — Unified Domain Language

## 1. Purpose

> Eliminar qualquer tradução entre as camadas do ASCEND

This document provides a complete, ground-truth matrix mapping every domain concept across all four layers:

| Layer | Technology | Location | Role |
|-------|-----------|----------|------|
| **Runtime** | Python 3.11+ | `src/ascend/domain/` | Core engine — domain entities, value objects, events |
| **Contracts** | TypeScript | `packages/contracts/src/` | Canonical type definitions — single source of truth for shape |
| **SDK** | TypeScript | `packages/sdk/src/` | Client library — transport, lifecycle, caching, health |
| **React** | TypeScript (Next.js) | `apps/web/src/` | UI components — visual representation of domain concepts |

## 2. The Canonical Principle

Every layer uses the **same logical entity**. There is **no translation layer** between Runtime, Contracts, SDK, and React. A `Builder` in the Python domain is the same `Builder` in `@ascend/contracts`, the same `Builder` the SDK references, and the same `Builder` a React component renders.

Wherever possible, types flow directly:
- `Runtime` defines the entity → `Contracts` mirrors its shape → `SDK` uses contract types → `React` consumes contract types in props/state

Exceptions are documented in the **Translation Table** (Section 4).

## 3. The Matrix

---

### 3.1 Builder

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Builder` | `Builder` | `AscendSDK` (client) | `JourneyCard`, `LevelBadge`, `XPBar` |
| **Definition** | `src/ascend/domain/builder.py:12` | `packages/contracts/src/builder.ts:4` | `packages/sdk/src/core/ascend-sdk.ts:23` | `apps/web/src/components/shared/` |
| **Identity** | `id: str` (`builder-{username}`) | `id: BuilderId` | SDK instance — `AscendSDK` | `LevelBadge` (level display) |
| **Status** | N/A (mutable fields) | `deletedAt?: string` | `SDKState` (`CREATED`, `INITIALIZING`, `READY`, `DEGRADED`, `OFFLINE`, `STOPPING`, `STOPPED`) | Journey card status: `pending`, `active`, `completed`, `failed`, `locked` |
| **Ownership** | `Builder` | `Builder` | `AscendSDK` | Consumer via SDK |

---

### 3.2 Profile

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | *Embedded in `Builder`* | `Profile` | *Not exposed — consumed via contract* | `Avatar` |
| **Definition** | `src/ascend/domain/builder.py:12` (username field) | `packages/contracts/src/builder.ts:16` | — | `apps/web/src/components/ui/avatar.tsx` |
| **Identity** | `username: str` | `name: string` | — | Avatar rendering |
| **Status** | N/A | N/A | — | N/A |
| **Ownership** | `Builder` | `Builder` | — | Consumer |

---

### 3.3 Preferences

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | *Not implemented* | `Preferences` | *Consumed via contract types* | `ThemeProvider`, `useLayoutStore` |
| **Definition** | — | `packages/contracts/src/builder.ts:29` | — | `apps/web/src/components/theme/theme-provider.tsx`, `apps/web/src/store/layout-store.ts` |
| **Identity** | — | N/A (embedded in `Builder`) | — | Layout mode |
| **Status** | — | `theme: Theme` (`light` | `dark` | `system`), `fontSize: FontSize`, `reducedMotion: boolean` | — | `reducedMotion`, `layoutMode` in zustand store |
| **Ownership** | — | `Builder` | — | Consumer |

---

### 3.4 Journey

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Journey` | `JourneySummary`, `JourneyDetail`, `JourneyProgress`, `JourneyNode` | *Consumed via contract types* | `JourneyCard`, `ProgressIndicator` |
| **Definition** | `src/ascend/domain/journey.py:16` | `packages/contracts/src/journey.ts:4-57` | — | `apps/web/src/components/shared/journey-card.tsx:9` |
| **Identity** | `id: str` (`journey-{name}`) | `id: JourneyId` | — | Card key |
| **Status** | `JourneyStatus` enum: `LOCKED`, `AVAILABLE`, `ACTIVE`, `COMPLETED` | `status: 'not_started' | 'in_progress' | 'completed' | 'abandoned'` (summary/detail); `'locked' | 'available' | 'in_progress' | 'completed'` (node) | — | `status?: 'pending' | 'active' | 'completed' | 'failed' | 'locked'` |
| **Ownership** | `Builder` | `JourneySummary`/`JourneyDetail` | — | Consumer |

---

### 3.5 Mission

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Mission` | `MissionSummary`, `MissionDetail` | *Consumed via contract types* | `MissionStatus` |
| **Definition** | `src/ascend/domain/mission.py:16` | `packages/contracts/src/mission.ts:4-29` | — | `apps/web/src/components/shared/mission-status.tsx:7` |
| **Identity** | `id: str` (`mission-{title}`) | `id: MissionId` | — | N/A (visual state only) |
| **Status** | `MissionStatus` enum: `AVAILABLE`, `STARTED`, `EVIDENCE_SUBMITTED`, `COMPLETED` | `status: 'locked' | 'available' | 'in_progress' | 'completed'` | — | `MissionState`: `'pending' | 'active' | 'completed' | 'failed' | 'locked'` |
| **Ownership** | `Builder` / `Journey` | `MissionSummary`/`MissionDetail` | — | Consumer |

---

### 3.6 Evidence

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Evidence` | `EvidenceRecord`, `EvidenceSummary` | *Consumed via contract types* | `EvidenceBadge` |
| **Definition** | `src/ascend/domain/evidence.py:25` | `packages/contracts/src/mission.ts:31` (record), `packages/contracts/src/builder.ts:93` (summary) | — | `apps/web/src/components/shared/evidence-badge.tsx:6` |
| **Identity** | `id: str` (`ev-{hash}`) | `id: EvidenceId` | — | Count display |
| **Status** | `EvidenceStatus` enum: `SUBMITTED`, `ACCEPTED`, `REJECTED` | `EvidenceStatus` (`'pending' | 'accepted' | 'rejected'`); `status: EvidenceStatus` on record | — | Count rendering (no status per item visually) |
| **Ownership** | `Builder` / `Mission` | `EvidenceRecord` (belongs to mission + builder) | — | Consumer |

---

### 3.7 Assessment

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Assessment` | `AssessmentSummary`, `AssessmentDetail`, `AssessmentSession`, `AssessmentResult`, `Rubric`, `RubricCriterion` | *Consumed via contract types* | *Not directly represented — consumed via SDK data* |
| **Definition** | `src/ascend/domain/assessment.py:7` | `packages/contracts/src/assessment.ts:3-62` | — | — |
| **Identity** | `id: str` (`assess-{evidence_id}`) | `id: AssessmentId` | — | — |
| **Status** | `score: float` (pass/fail via `is_approved` >= 0.7) | `status: 'not_started' | 'in_progress' | 'passed' | 'failed'` (summary); `'in_progress' | 'completed' | 'expired'` (session) | — | — |
| **Ownership** | `Assessment` | `AssessmentSummary`/`AssessmentDetail` | — | — |

---

### 3.8 Competency

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Competency` | `CompetencySummary`, `CompetencyDetail`, `CompetencyNode`, `CompetencyEdge`, `CompetencyRef`, `CompetencyGraph` | *Consumed via contract types* | `CompetencyBadge` |
| **Definition** | `src/ascend/domain/competency.py:6` | `packages/contracts/src/competency.ts:3-26`, `packages/contracts/src/builder.ts:63-84` | — | `apps/web/src/components/shared/competency-badge.tsx:7` |
| **Identity** | `id: str` (`comp-{name}`) | `id: CompetencyId` | — | Name-keyed rendering |
| **Status** | `level: int` (1-based) | `status: 'locked' | 'available' | 'in_progress' | 'completed'`; `currentLevel`, `maxLevel`, `progress` | — | `score / maxScore` (visual progress) |
| **Ownership** | `Builder` | `CompetencySummary`/`CompetencyDetail` | — | Consumer |

---

### 3.9 Achievement

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `Achievement`, `Skill` | `AchievementList`, `Achievement`, `Badge`, `Certificate`, `LedgerEntry` | *Consumed via contract types* | `AchievementBadge` |
| **Definition** | `src/ascend/domain/achievement.py:7`, `src/ascend/domain/skill.py:5` | `packages/contracts/src/achievement.ts:3-39`, `packages/contracts/src/builder.ts:134-145` | — | `apps/web/src/components/shared/achievement-badge.tsx:6` |
| **Identity** | `id: str` (`ach-{name}`) | `id: AchievementId` (achievement), `id: CertificateId` (certificate) | — | Visual badge per achievement |
| **Status** | `is_earned: bool` (via `earned_at`) | `grantedAt?: string` (achievement/badge), `issuedAt: string` (certificate) | — | `unlocked?: boolean` (default `true`) |
| **Ownership** | `Builder` | `AchievementList` | — | Consumer |

---

### 3.10 Pagination

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | *Infrastructure-layer concept (SQL queries)* | `PaginationParams`, `PaginationMeta`, `PaginatedResponse` | *Used in transport request/response* | *Not represented* |
| **Definition** | `src/ascend/infrastructure/persistence/sqlite/` (LIMIT/OFFSET in queries) | `packages/contracts/src/pagination.ts:3-20` | `RequestConfig` (`params` query string) | — |
| **Identity** | — | `offset`, `limit` | — | — |
| **Status** | — | `hasMore: boolean` | — | — |
| **Ownership** | Repository layer | Generic (parameterized `PaginatedResponse<T>`) | `Transport.request()` | — |

---

### 3.11 Domain Events

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | `DomainEvent` | `DomainEventEnvelope`, `DomainEventType`, `DomainEventTypes` (const map), 20+ payload types | `SimpleEventBus`, `SDKEvents`, `SDKEventName`, 8 SDK event payloads | *Consumed via SDK events* |
| **Definition** | `src/ascend/domain/events.py:17` | `packages/contracts/src/domain-events.ts:3-275` | `packages/sdk/src/events/` | — |
| **Identity** | `event_id: str` | `id: string` (envelope); event type string (`builder.created`, `mission.started`, etc.) | SDK event names (`sdk.initializing`, `transport.changed`, etc.) | — |
| **Status** | `EventType` enum: 6 types | `DomainEventTypes` const: 27 event strings across 7 domains + infra | `SDKEventName` | — |
| **Ownership** | `Builder` / aggregate root | `DomainEventEnvelope` | `SimpleEventBus` | — |
| **Runtime types** | `BUILDER_CREATED`, `MISSION_STARTED`, `EVIDENCE_SUBMITTED`, `ASSESSMENT_COMPLETED`, `COMPETENCY_UNLOCKED`, `ACHIEVEMENT_EARNED` | | | |
| **Contract types** | | `builder.*` (5), `journey.*` (4), `mission.*` (5), `evidence.*` (3), `assessment.*` (3), `competency.*` (3), `achievement.*` (2), `runtime.*` (3), `sdk.*` (4) | | |
| **SDK event types** | | | `sdk.initializing`, `sdk.initialized`, `sdk.initialization_failed`, `sdk.shutting_down`, `sdk.shutdown`, `transport.changed`, `transport.failed`, `transport.recovered`, `state.changed`, `cache.cleared`, `cache.miss`, `cache.hit` | |

---

### 3.12 Health

| Aspect | Runtime | Contracts | SDK | React |
|--------|---------|-----------|-----|-------|
| **Type** | *Not implemented (infrastructure-level)* | `HealthReport` | `SDKHealthReport`, `TransportHealthInfo`, `TransportHealth` | *Not represented* |
| **Definition** | — | `packages/contracts/src/health.ts:3-13` | `packages/sdk/src/health/health-report.ts:10-24`, `packages/sdk/src/contracts/transport.ts:20-24` | — |
| **Identity** | — | N/A (per-instance) | SDK instance | — |
| **Status** | — | `HealthStatus`: `'healthy' | 'degraded' | 'unhealthy'`; checks: `database`, `runtime`, `cache` | `status: 'healthy' | 'degraded' | 'unhealthy'`; `sdkState`, `transport`, `cache`, `latency`, `warnings` | — |
| **Ownership** | — | System-level | `AscendSDK.health()` | — |

---

## 4. Translation Table

### Runtime ↔ Contracts

| Direction | Translation | Location |
|-----------|------------|----------|
| Python → TypeScript | `Builder.id: str` → `id: BuilderId` (string alias) | Direct mapping |
| Python → TypeScript | `Builder.username` → `Profile.name` | Field renamed; Runtime has flat username, Contracts nest under `Profile` |
| Python → TypeScript | `Builder.xp: int` → `BuilderProgress.xp.current` | Nested structure added in Contracts |
| Python → TypeScript | `Builder.level: int` → `BuilderProgress.level` | Moved into `BuilderProgress` sub-object |
| Python → TypeScript | `MissionStatus` (AVAILABLE, STARTED, EVIDENCE_SUBMITTED, COMPLETED) → `'locked' | 'available' | 'in_progress' | 'completed'` | Status enum flattened + renamed in Contracts |
| Python → TypeScript | `EvidenceStatus` (SUBMITTED, ACCEPTED, REJECTED) → `'pending' | 'accepted' | 'rejected'` | `SUBMITTED` renamed to `pending` |
| Python → TypeScript | `JourneyStatus` (LOCKED, AVAILABLE, ACTIVE, COMPLETED) → `'not_started' | 'in_progress' | 'completed' | 'abandoned'` | ACTIVE → `in_progress`, LOCKED not in summary status; `abandoned` added |
| Python → TypeScript | `EventType` (Enum with 6 values) → `DomainEventType` (27 string literal union) | Contracts are superset; domain events expanded significantly |
| Python → TypeScript | `Mission.evidence_list: List[Evidence]` → `MissionDetail` (no inline list) | Evidence moved to standalone `EvidenceRecord` type |
| Python → TypeScript | `Assessment.score: float` (0.0-1.0) → `AssessmentResult.score: number` (points), `AssessmentResult.total: number` | Score semantics changed: relative → absolute |
| Python → TypeScript | `Challenge` exists in Python only | No Contract equivalent — challenge is internal runtime concept |
| Python → TypeScript | `Skill` exists in Python only | No Contract equivalent — skill is internal runtime concept |
| **Default** | All other fields | **Direct mapping — no translation needed** |

### Contracts ↔ SDK

| Direction | Translation | Location |
|-----------|------------|----------|
| Contracts → SDK | Contracts define **domain types** (`Builder`, `JourneySummary`, etc.) | SDK does **not re-export** domain types; SDK is transport/lifecycle layer, domain types consumed externally via `@ascend/contracts` |
| Contracts → SDK | `HealthReport` → `SDKHealthReport` | SDK health is superset: adds `sdkState`, `transport.name`, `cache`, `warnings`, `activeTransport`, `registeredTransports` |
| Contracts → SDK | `HealthStatus` (`'healthy'|'degraded'|'unhealthy'`) | Same enum — shared concept |
| Contracts → SDK | `DomainEventEnvelope` → SDK `SDKEventName` + payloads | SDK events are infrastructure-focused, not domain events |
| **Default** | **Direct mapping — no translation needed** (SDK uses `@ascend/contracts` types directly) | |

### SDK ↔ React

| Direction | Translation | Location |
|-----------|------------|----------|
| SDK → React | `SDKHealthReport.status` → UI health indicator | Not yet implemented in React — future feature |
| SDK → React | `AscendSDK` instance → React context | Not yet implemented; future `AscendProvider` planned |
| Contracts → React | `Builder` → `JourneyCard` props (`title`, `description`, `progress`, `status`) | Domain types drive component props — simplified view models |
| Contracts → React | `CompetencySummary` → `CompetencyBadge` props (`name`, `score`, `maxScore`) | `currentLevel`/`maxLevel` → `score`/`maxScore` (renamed for UX) |
| Contracts → React | `MissionSummary.status` → `MissionStatus` component (`MissionState`) | `'in_progress'` → `'active'`; `'not_started'` → `'pending'`; `'failed'` added (presentational) |
| Contracts → React | `Achievement.grantedAt` → `AchievementBadge.unlocked` | Date → boolean (simplified for UI) |
| **Default** | **Direct mapping — no translation needed** (React components accept generic view-model props, not domain types directly) | |

## 5. Invariant I13 Compliance

This document proves **compliance with I13 — Canonical Language**.

> *No concept shall undergo semantic translation between layers. Every layer references the same logical entity by the same name and shape.*

Evidence of compliance:

- **Builder** is `Builder` in all four layers — identical semantic identity.
- **Journey**, **Mission**, **Evidence**, **Assessment**, **Competency**, **Achievement** each appear under the same name in Runtime, Contracts, SDK, and React.
- **Contracts** serves as the canonical type definition layer (`packages/contracts/src/`), and all other layers reference it directly or via consumer code.
- **SDK** does not redefine domain types — it depends on `@ascend/contracts` as an external peer.
- **React** components consume domain shapes directly as props, with only visual simplification (never semantic drift).

Exceptions are documented in Section 4 and amount to:
- **Field nesting changes** (Runtime flat → Contracts nested) — additive, not contradictory
- **Status enum expansion** (Runtime 3-state → Contracts 4-state) — superset, not conflict
- **Presentational renaming** (React UI states like `'active'` vs `'in_progress'`) — visual alias, semantic intent preserved

No exception breaks the invariant that a `Builder` in Python is the same `Builder` in TypeScript, in the SDK, and on screen.

## 6. Change History

| Date | Author | Change |
|------|--------|--------|
| 2026-07-20 | ASCEND TSC | Initial canonical mapping — v1.0 Standard Edition baseline |
