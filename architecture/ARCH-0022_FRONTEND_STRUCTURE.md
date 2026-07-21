# ARCH-0022 — Frontend Structure

| Field | Value |
|-------|-------|
| **ID** | ARCH-0022 |
| **Name** | Frontend Structure |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | ARCH-0011, ARCH-0016, ARCH-0018, ARCH-0019, ARCH-0020, ARCH-0021 |
| **Referenced by** | Frontend Implementation |

---

## 1. Purpose

Define the complete folder structure, naming conventions, module boundaries, and code organization for the ASCEND frontend.

---

## 2. Monorepo Structure

```
ascend/
├── apps/
│   └── web/                    # Next.js 15 application
│       ├── app/                # Next.js App Router pages
│       ├── components/         # App-specific components
│       ├── features/           # Feature modules
│       ├── hooks/              # App-specific hooks
│       ├── lib/                # Utility functions
│       ├── store/              # Zustand stores
│       ├── styles/             # Global styles
│       └── services/           # Service configurations
│
├── packages/
│   ├── ui/                    # Shared UI component library
│   │   ├── primitives/        # Base components (Button, Input, Card)
│   │   ├── domain/            # Domain components (MissionCard, etc.)
│   │   ├── composite/         # Composite components (DashboardOverview)
│   │   ├── layout/            # Layout components (AppShell, Sidebar)
│   │   └── feedback/          # Feedback components (Toast, Skeleton)
│   │
│   ├── sdk/                   # ASCEND Platform SDK
│   │   ├── client/            # Main client
│   │   ├── resources/         # Resource modules (missions, journeys)
│   │   ├── auth/              # Auth manager
│   │   ├── cache/             # Cache layer
│   │   ├── offline/           # Offline queue
│   │   ├── errors/            # Error mapping
│   │   └── events/            # SSE subscriber
│   │
│   └── types/                 # Shared TypeScript types
│       ├── contracts/         # UI contracts (ARCH-0020)
│       ├── domain/            # Domain types (shared with API)
│       ├── events/            # SSE event types
│       └── sdk/               # SDK types
│
├── tooling/
│   ├── eslint/                # ESLint configurations
│   ├── typescript/            # TypeScript configs
│   └── jest/                  # Jest configs
│
└── package.json               # Root (workspaces)
```

---

## 3. Feature Module Architecture

Each feature module in `apps/web/features/` is self-contained:

```
features/
├── auth/                      # Authentication feature
│   ├── components/
│   │   ├── login-form.tsx
│   │   ├── register-form.tsx
│   │   └── auth-guard.tsx
│   ├── hooks/
│   │   ├── use-login.ts
│   │   └── use-register.ts
│   ├── store/
│   │   └── session-store.ts
│   └── index.ts               # Public API (barrel)
│
├── dashboard/                 # Dashboard feature
│   ├── components/
│   │   ├── dashboard-shell.tsx
│   │   ├── continue-mission-card.tsx
│   │   ├── stats-grid.tsx
│   │   ├── streak-card.tsx
│   │   ├── activity-feed.tsx
│   │   └── mentor-suggestion.tsx
│   ├── hooks/
│   │   ├── use-dashboard.ts
│   │   └── use-activity-feed.ts
│   └── index.ts
│
├── missions/                  # Missions feature
│   ├── components/
│   │   ├── mission-list.tsx
│   │   ├── mission-card.tsx
│   │   ├── mission-viewer.tsx
│   │   ├── evidence-uploader.tsx
│   │   └── feedback-panel.tsx
│   ├── hooks/
│   │   ├── use-missions.ts
│   │   ├── use-mission-detail.ts
│   │   └── use-submit-evidence.ts
│   └── index.ts
│
├── journeys/                  # Journeys feature
│   ├── components/
│   │   ├── journey-list.tsx
│   │   ├── journey-card.tsx
│   │   ├── journey-detail.tsx
│   │   └── journey-tree.tsx
│   ├── hooks/
│   │   ├── use-journeys.ts
│   │   └── use-journey-detail.ts
│   └── index.ts
│
├── competencies/              # Competencies feature
│   ├── components/
│   │   ├── competency-tree.tsx
│   │   ├── competency-node.tsx
│   │   └── competency-detail.tsx
│   ├── hooks/
│   │   └── use-competency-tree.ts
│   └── index.ts
│
├── achievements/              # Achievements feature
│   ├── components/
│   │   ├── badge-grid.tsx
│   │   ├── badge-card.tsx
│   │   ├── certificate-list.tsx
│   │   └── level-timeline.tsx
│   ├── hooks/
│   │   └── use-achievements.ts
│   └── index.ts
│
├── evidence/                  # Evidence feature
│   ├── components/
│   │   ├── evidence-list.tsx
│   │   ├── evidence-card.tsx
│   │   └── evidence-detail.tsx
│   ├── hooks/
│   │   └── use-evidence.ts
│   └── index.ts
│
├── mentor/                    # AI Mentor feature
│   ├── components/
│   │   ├── mentor-panel.tsx
│   │   ├── mentor-message.tsx
│   │   └── mentor-suggestion.tsx
│   ├── hooks/
│   │   └── use-mentor.ts
│   └── index.ts
│
├── builder/                   # Builder Profile feature
│   ├── components/
│   │   ├── builder-profile.tsx
│   │   ├── xp-chart.tsx
│   │   └── builder-timeline.tsx
│   ├── hooks/
│   │   └── use-builder-profile.ts
│   └── index.ts
│
├── community/                 # Community feature
│   ├── components/
│   │   ├── leaderboard.tsx
│   │   ├── activity-feed.tsx
│   │   └── builder-card.tsx
│   ├── hooks/
│   │   └── use-community.ts
│   └── index.ts
│
├── marketplace/               # Marketplace feature
│   ├── components/
│   │   ├── package-list.tsx
│   │   └── package-card.tsx
│   ├── hooks/
│   │   └── use-marketplace.ts
│   └── index.ts
│
├── settings/                  # Settings feature
│   ├── components/
│   │   ├── profile-settings.tsx
│   │   ├── preference-settings.tsx
│   │   └── account-settings.tsx
│   ├── hooks/
│   │   └── use-settings.ts
│   └── index.ts
│
└── shared/                    # Shared across features
    ├── components/
    │   ├── ascension-ring.tsx
    │   ├── command-palette.tsx
    │   ├── notification-center.tsx
    │   └── onboarding-flow.tsx
    ├── hooks/
    │   ├── use-keyboard-shortcuts.ts
    │   └── use-online-status.ts
    └── utils/
        ├── formatters.ts
        └── validators.ts
```

---

## 4. Naming Conventions

### 4.1 Files

| Element | Convention | Example |
|---------|------------|---------|
| React components | `kebab-case.tsx` | `mission-card.tsx` |
| Hooks | `kebab-case.ts` | `use-missions.ts` |
| Stores | `kebab-case.ts` | `session-store.ts` |
| Types | `kebab-case.ts` | `dashboard-contract.ts` |
| Utils | `kebab-case.ts` | `formatters.ts` |
| Tests | `.test.ts` / `.test.tsx` | `mission-card.test.tsx` |

### 4.2 Components

| Element | Convention | Example |
|---------|------------|---------|
| Component | `PascalCase` | `MissionCard` |
| Props | `{Name}Props` | `MissionCardProps` |
| Default export | Component | `export default MissionCard` |
| Named exports | Utilities | `export { formatXp }` |

### 4.3 Hooks

| Convention | Example |
|------------|---------|
| `use{Resource}` | `useMissions()` |
| `use{Action}` | `useSubmitEvidence()` |
| Returns tuple or object | `const { data, isLoading } = useMissions()` |

### 4.4 Stores

| Store | File | Export |
|-------|------|--------|
| UI state | `ui-store.ts` | `useUIStore` |
| Session state | `session-store.ts` | `useSessionStore` |
| Mission context | `mission-store.ts` | `useMissionStore` |

---

## 5. Import Rules

### 5.1 Barrel Files

Each feature module has an `index.ts` barrel:

```typescript
// features/dashboard/index.ts
export { DashboardShell } from './components/dashboard-shell'
export { ContinueMissionCard } from './components/continue-mission-card'
export { useDashboard } from './hooks/use-dashboard'
```

### 5.2 Alias Paths

| Alias | Path |
|-------|------|
| `@/` | `apps/web/` |
| `@ui/` | `packages/ui/` |
| `@sdk/` | `packages/sdk/` |
| `@types/` | `packages/types/` |

```typescript
// Good
import { Button } from '@ui/primitives/button'
import { useMissions } from '@/features/missions'
import { client } from '@sdk/client'
import type { MissionDetailContract } from '@types/contracts/missions'

// Bad — no relative imports across feature boundaries
import { useMissions } from '../missions/hooks/use-missions'
```

### 5.3 Import Boundaries

| Source can import → | `@ui/` | `@sdk/` | `@types/` | `@/features/` | `@/hooks/` |
|---------------------|--------|---------|-----------|---------------|------------|
| `@ui/` | ✅ | ❌ | ✅ | ❌ | ❌ |
| `@sdk/` | ❌ | ✅ | ✅ | ❌ | ❌ |
| `@types/` | ✅ | ✅ | ✅ | ❌ | ❌ |
| `@/features/` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `@/hooks/` | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 6. Code Splitting

| Strategy | Where | How |
|----------|-------|-----|
| **Route-based** | `apps/web/app/` | Next.js App Router (automatic) |
| **Component-based** | Heavy components | `dynamic(() => import('./heavy-component'))` |
| **Library-based** | Large libs | `const Chart = dynamic(() => import('recharts'))` |

### 6.1 Lazy Loading Targets

| Component | Bundle size (est.) | Strategy |
|-----------|-------------------|----------|
| Competency Tree | 15 KB | Dynamic import on `/competencies` |
| Achievement Gallery | 10 KB | Dynamic import on `/achievements` |
| Mentor Chat | 8 KB | Dynamic import on `/mentor` |
| Marketplace | 12 KB | Dynamic import on `/marketplace` |
| Community | 10 KB | Dynamic import on `/community` |

---

## 7. Testing Structure

```
apps/web/
└── __tests__/
    ├── components/       # Component tests
    ├── hooks/            # Hook tests
    ├── features/         # Feature integration tests
    └── e2e/              # End-to-end tests

packages/
├── sdk/__tests__/
├── ui/__tests__/
└── types/__tests__/
```

---

## 8. Page Structure (Next.js App Router)

```
apps/web/app/
├── layout.tsx                    # Root layout (AppShell)
├── page.tsx                      # Dashboard (/) redirect or render
├── loading.tsx                   # Root loading state
├── error.tsx                     # Root error boundary
│
├── (auth)/
│   ├── login/page.tsx
│   └── register/page.tsx
│
├── (authenticated)/              # Protected routes
│   ├── layout.tsx                # Auth guard + sidebar layout
│   │
│   ├── journeys/
│   │   ├── page.tsx              # Journey list
│   │   └── [slug]/page.tsx       # Journey detail
│   │
│   ├── missions/
│   │   ├── page.tsx              # Mission list
│   │   └── [id]/page.tsx         # Mission workspace
│   │
│   ├── competencies/
│   │   ├── page.tsx              # Competency tree
│   │   └── [id]/page.tsx         # Competency detail
│   │
│   ├── achievements/
│   │   ├── page.tsx              # Achievement gallery
│   │   └── certificates/[id]/page.tsx
│   │
│   ├── evidence/
│   │   ├── page.tsx              # Evidence list
│   │   └── [id]/page.tsx         # Evidence detail
│   │
│   ├── mentor/page.tsx           # AI Mentor
│   ├── profile/page.tsx          # Builder profile
│   │
│   ├── community/
│   │   ├── page.tsx              # Community hub
│   │   ├── leaderboard/page.tsx
│   │   └── builders/[id]/page.tsx
│   │
│   ├── marketplace/
│   │   ├── page.tsx              # Marketplace
│   │   └── packages/[id]/page.tsx
│   │
│   └── settings/
│       ├── page.tsx              # Profile settings
│       ├── preferences/page.tsx
│       └── account/page.tsx
```

---

## 9. Definition of Done

ARCH-0022 aprovado quando:

- [ ] Monorepo structure documented
- [ ] Feature module architecture documented (auth through settings)
- [ ] Shared components/hooks specified
- [ ] File naming conventions defined
- [ ] Component naming conventions defined
- [ ] Hook naming conventions defined
- [ ] Import rules with aliases defined
- [ ] Import boundary table complete
- [ ] Code splitting and lazy loading strategy defined
- [ ] Testing structure documented
- [ ] Page structure (Next.js App Router) complete

---

## 10. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
