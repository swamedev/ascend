# ⚜️ OPERAÇÃO ORION — Product Stabilization Plan

| Field | Value |
|-------|-------|
| **Document** | STABILIZATION_PLAN_v1.md |
| **Operation** | OPERAÇÃO ORION |
| **Phase** | Product Stabilization |
| **Status** | Approved |
| **Date** | 2026-07-20 |
| **Chief Architect** | R.V. |
| **Derived from** | MILESTONES.md, Vertical Slice Audit |

---

> *"Software was never the destination. It was the vehicle."*
>
> Antes de acelerar, precisamos ter certeza de que o veículo não desmonta.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Scope: Vertical Slice Audited](#2-scope-vertical-slice-audited)
3. [Technical Review](#3-technical-review)
4. [UX Review](#4-ux-review)
5. [Visual Review](#5-visual-review)
6. [Architectural Review](#6-architectural-review)
7. [New Metric: Time To First Competency (TTFC)](#7-new-metric-time-to-first-competency-ttfc)
8. [Demo Builder](#8-demo-builder)
9. [JWT, Marketplace, Multiplayer, IA — Postponed](#9-jwt-marketplace-multiplayer-ia--postponed)
10. [Architecture Freeze](#10-architecture-freeze)
11. [Stabilization Roadmap](#11-stabilization-roadmap)
12. [Change History](#12-change-history)

---

## 1. Executive Summary

### Context

O ASCEND acabou de entregar a primeira **Vertical Slice** completa:

- Backend Python (FastAPI + Runtime Adapter)
- Frontend Next.js 15 (5 páginas, 4 stores, API client, React Query)
- 168 testes passando
- TypeScript compilando sem erros

### Findings

A auditoria revelou um sistema funcional, mas com **três crises sistêmicas** que precisam ser resolvidas antes de qualquer nova funcionalidade:

| Dimensão | Score | Status |
|----------|-------|--------|
| **Backend (Python)** | **4.5/10** | 🔴 Crítico |
| **Frontend Pages** | **~6.5/10** | 🟡 Atenção |
| **Component Library** | **6.1/10** | 🟡 Atenção |
| **Overall** | **5.5/10** | 🔴 Precisa de estabilização |

### Decisão do Chief Architect

1. **Nenhuma nova funcionalidade** será aceita durante a OPERAÇÃO ORION.
2. **JWT, Marketplace, Multiplayer, IA** estão oficialmente adiados.
3. **Toda energia** deve ser direcionada para refinar o que já existe.
4. **A única exceção** é o **Demo Builder**, por ser estratégico para reduzir barreira de entrada.

---

## 2. Scope: Vertical Slice Audited

### Frontend (Next.js 15)

| File | Lines | Score | Key Issue |
|------|-------|-------|-----------|
| `app/auth/page.tsx` | 86 | 7/10 | Barrel export missing; duplicated auth guard |
| `app/dashboard/page.tsx` | 227 | 6/10 | `any` types; 3 queries OR-joined; magic numbers |
| `app/journeys/page.tsx` | 242 | 7/10 | Seed inside `queryFn` causes re-seed on refetch |
| `app/missions/[missionId]/page.tsx` | 254 | **5/10** | Result via URL query param (security + truncation) |
| `app/missions/[missionId]/result/page.tsx` | 280 | 6/10 | Dead code `scorePercent`; potential crashes |
| `app/layout.tsx` | 47 | 9/10 | Dev tool in production |
| `app/page.tsx` | 12 | 6/10 | No CTA, no navigation |
| `lib/api.ts` | 48 | 6/10 | All returns `any`; no timeout |
| `store/auth-store.ts` | 25 | 8/10 | `isAuthenticated` desync risk |
| `store/result-store.ts` | 26 | 9/10 | Clean |
| `store/layout-store.ts` | 97 | 9/10 | Clean |
| `store/index.ts` | 4 | **5/10** | `useAuthStore` not exported |
| `providers/query-provider.tsx` | 11 | 7/10 | Missing explicit `gcTime`, `refetchOnWindowFocus` |

### Backend (Python FastAPI)

| File | Lines | Score | Key Issue |
|------|-------|-------|-----------|
| `api/app.py` | 66 | 6/10 | `:memory:` default loses data; CORS wide open |
| `api/routers/builder.py` | 120 | **4/10** | Raw SQL delete bypassing adapter; inline imports |
| `api/routers/journey.py` | 92 | **3/10** | Business logic + direct `_private` access in router |
| `api/routers/mission.py` | 230 | **2/10** | 110 lines of domain logic in router; N+1 queries |
| `api/routers/auth.py` | 54 | **3/10** | Fake forgeable token; conflates login/register |
| `api/routers/health.py` | 36 | 7/10 | Unsafe dict access on error |
| `api/routers/version.py` | 12 | 10/10 | Clean |
| `api/schemas/builder.py` | 220 | 5/10 | Dead aspirational schemas; out of sync with routers |
| `api/middleware/correlation.py` | 39 | 9/10 | Clean |
| `api/middleware/logger.py` | 34 | **4/10** | Uses `print()` instead of `logging` |
| `api/middleware/error_handler.py` | 29 | 8/10 | Clean |
| `adapter/runtime_adapter.py` | 486 | **4/10** | N+1 queries; no pagination; dynamic type creation |
| `adapter/mapper.py` | 407 | 5/10 | Hardcoded placeholders; fake timestamps |
| `adapter/error_mapper.py` | 140 | **3/10** | Traceback leakage to client; fresh `correlationId` |
| `adapter/event_adapter.py` | 102 | 7/10 | Hardcoded defaults |

### Component Library

| Component | Score | Key Issue |
|-----------|-------|-----------|
| `Button` | 7/10 | No `cva()`, no `asChild` |
| `IconButton` | 7/10 | Same as Button |
| `Input` | 7/10 | Error `id` breaks when no `id` prop |
| `Textarea` | 6/10 | Missing `aria-describedby` for error |
| `Badge` | 7/10 | Hardcoded colors on `xp` variant |
| `Avatar` | 6/10 | `Next/Image` hardcoded to 40x40; no `onError` |
| `Alert` | 7/10 | Hardcoded icon colors |
| `Card` | 7/10 | `CardHeader` ignores `className` |
| `Modal` | **4/10** | No focus trap; `aria-label="undefined"` |
| `Drawer` | **4/10** | No focus trap; `aria-label="undefined"` |
| `Toast` | **5/10** | No `aria-live` region; Radix unused |
| `Tooltip` | **5/10** | No `aria-describedby` linkage; Radix unused |
| `AscensionRing` | 7/10 | No reduced-motion; no ARIA progress attrs |
| `XPBar` | 7/10 | Same as AscensionRing |
| `ProgressIndicator` | 7/10 | Same as AscensionRing |
| `Skeleton` | 7/10 | Shimmer ignores reduced-motion |
| `CompetencyBadge` | 8/10 | Clean |
| `LevelBadge` | 8/10 | Clean |
| `JourneyCard` | 7/10 | Dead `group` class |
| `AchievementBadge` | 8/10 | Clean |
| `EmptyState` | 8/10 | Clean |
| `LoadingState` / `ErrorState` / `SuccessState` | 7/10 | Hardcoded colors |

### Cross-Cutting Crises

| # | Crisis | Severity | Files Affected |
|---|--------|----------|----------------|
| 1 | **URL query param for mission result** | 🔴 CRITICAL | `missions/[missionId]/page.tsx`, `result/page.tsx` |
| 2 | **API client returns `any`** | 🔴 CRITICAL | `lib/api.ts` + all 5 pages |
| 3 | **`useAuthStore` not in barrel** | 🔴 CRITICAL | `store/index.ts` + all 5 pages |
| 4 | **Business logic in routers** | 🔴 CRITICAL | `mission.py`, `journey.py`, `builder.py` |
| 5 | **Adapter encapsulation breached** | 🔴 CRITICAL | All routers access `adapter._*` private members |
| 6 | **Traceback leaked to client** | 🔴 CRITICAL | `error_mapper.py` |
| 7 | **Fake forgeable auth token** | 🔴 CRITICAL | `auth.py` |
| 8 | **N+1 queries in hot paths** | 🟠 MAJOR | `runtime_adapter.py` (list_journeys, get_journey) |
| 9 | **Magic numbers everywhere** | 🟠 MAJOR | `dashboard`, `result`, `journeys` pages |
| 10 | **Duplicated auth guard pattern** | 🟠 MAJOR | All 5 client pages |
| 11 | **Radix UI / cva() in deps but unused** | 🟠 MAJOR | `ui/` components |
| 12 | **Hardcoded colors bypass theme** | 🟠 MAJOR | 6+ components |
| 13 | **No pagination on any list endpoint** | 🟡 MINOR | All backend list endpoints |
| 14 | **`print()` instead of `logging`** | 🟡 MINOR | `logger.py` |
| 15 | **Fake timestamps in mappers** | 🟡 MINOR | `mapper.py` |

---

## 3. Technical Review

### 3.1 Backend (Python)

**Score: 4.5/10 — 🔴 Crítico**

| Sub-dimension | Score | Summary |
|---------------|-------|---------|
| Code Quality | 4/10 | Duplicated patterns, inline imports, `print()` logging |
| Architecture | 4/10 | Layered design correct but breached everywhere |
| Performance | 3/10 | N+1 queries in hot paths; no pagination |
| API Design | 5/10 | Consistent error envelope concept, inconsistent application |
| Security | **2/10** | Fake auth, traceback leak, raw SQL delete, CORS `*` |
| Maintainability | 4/10 | Hardcoded config, duplicate functions, dead schemas |

**Top 5 Backend Fixes:**

1. 🔴 Extract `complete_mission` logic from router into a proper use case
2. 🔴 Remove traceback from API responses (log server-side only)
3. 🔴 Route `DELETE /builders/{id}` through adapter instead of raw SQL
4. 🔴 Fix N+1 queries in `list_journeys` / `get_journey` (add `journey_id` FK)
5. 🔴 Replace `print()` with `logging` module in middleware

### 3.2 Frontend Pages & Stores

**Average Score: 6.5/10 — 🟡 Atenção**

| Sub-dimension | Score | Summary |
|---------------|-------|---------|
| Code Quality | 6/10 | `any` types, magic numbers, monolithic pages |
| Performance | 6/10 | Missing React Query tuning; OR-joined loading states |
| UX | 7/10 | Most pages have loading/error/empty states |
| Type Safety | **4/10** | `any` cascades from API client through all pages |
| Architecture | 7/10 | Clean stores; barrel pattern broken (missing export) |

**Top 5 Frontend Fixes:**

1. 🔴 Replace URL result-passing with Zustand store
2. 🔴 Type the API client (define response interfaces per endpoint)
3. 🔴 Export `useAuthStore` from `store/index.ts`
4. 🟠 Extract duplicated auth guard into `useAuthGuard()` hook
5. 🟠 Fix `api.seedJourneys()` inside `queryFn` (move to `useMutation`)

### 3.3 Component Library

**Score: 6.1/10 — 🟡 Atenção**

| Sub-dimension | Score | Summary |
|---------------|-------|---------|
| Visual Quality | 7.5/10 | Good baseline, inconsistent CSS variable usage |
| Code Quality | 7/10 | Consistent `cn()`, but no `cva()` |
| Accessibility | **5/10** | No focus traps, no live regions, `aria-label="undefined"` |
| State Coverage | 7/10 | Solid loading/disabled/error coverage |
| Dark Mode | 7/10 | Good via Tailwind, some hardcoded colors bypass |
| Responsiveness | 6/10 | Works but not tested at breakpoints |
| Reduced Motion | **5/10** | Only 3/7 animated components respect it |
| Architecture | 5/10 | Radix UI unused; no `cva()`; manual variant maps |

**Top 5 Component Fixes:**

1. 🔴 Fix `aria-label={title}` rendering `"undefined"` in Modal + Drawer
2. 🔴 Add focus traps to Modal and Drawer (use Radix Dialog)
3. 🔴 Replace hardcoded colors with CSS variables in 6+ components
4. 🟠 Add `aria-describedby` linkage to Tooltip
5. 🟠 Add `aria-live` region to Toast (use Radix Toast)

### 3.4 Bundle Size & Performance

Not measured programmatically (Lighthouse). High-risk areas identified:

| Area | Risk | Why |
|------|------|-----|
| **React Query `staleTime: 30s`** | Medium | Default is reasonable but `gcTime` not explicitly set |
| **`refetchOnWindowFocus: true`** (default) | Medium | May cause unexpected refetches during development |
| **All list queries unbounded** | High | No pagination means memory grows with data |
| **3 separate useQuery on dashboard** | Medium | OR-joined loading state blocks entire page |
| **framer-motion on every page** | Low | Tree-shaken; first-load JS is the concern |
| **lucide-react icons** | Low | Tree-shaken by default |

### 3.5 Lighthouse Estimate

Based on code analysis (not actual measurement):

| Metric | Estimate | Risk |
|--------|----------|------|
| Performance | 70-85 | Moderate — no obvious blockers |
| Accessibility | **50-65** | 🔴 Critical — focus traps, aria-label, live regions |
| Best Practices | 80-90 | Good |
| SEO | 90-100 | Static content is minimal |

---

## 4. UX Review

### 4.1 Time Metrics (Estimated)

| Metric | Current (Est.) | Target | Gap |
|--------|----------------|--------|-----|
| **Time to Create Builder** | ~15s | < 10s | 🟢 Good |
| **Time to First Mission** | ~60s | < 30s | 🟡 Acceptable |
| **Time to First Competency (TTFC)** | ~5-8 min | < 5 min | 🟡 Near target |
| **Time to First Achievement** | ~5-8 min | < 5 min | 🟡 Near target |
| **Time to Understand Dashboard** | ~10s | < 5s | 🟡 Could improve |

### 4.2 Friction Points Identified

| # | Friction | Severity | Where |
|---|----------|----------|-------|
| 1 | **No "Get Started" on home page** | 🔴 High | `/` shows static text with no CTA |
| 2 | **Auth page has no "continue as guest"** | 🟠 Medium | Forces account creation for evaluation |
| 3 | **No way to go back from Focus Mode** | 🟠 Medium | Phase `submitted` only offers "Complete" |
| 4 | **Result page redirects to dashboard if refreshed** | 🟠 Medium | Result store not persisted |
| 5 | **No transition feedback between pages** | 🟡 Low | All pages hard-transition |
| 6 | **No loading indicator on auth submit** | 🟡 Low | Button stays idle during API call |
| 7 | **Mission Workspace lacks timer/ETA** | 🟡 Low | No indication of mission length |

### 4.3 User Flow: Current State

```
Home (/)
  │
  ├── No CTA → user must know to go to /auth
  │
Auth (/auth)
  │
  ├── Type username → click "Login"
  │   └── Auto-registers if not found
  │
Dashboard (/dashboard) ← auto-redirect after auth
  │
  ├── Shows stats (zero if new)
  ├── "Start Your First Journey" button
  │
Journeys (/journeys)
  │
  ├── Click "Start Journey" on a journey
  │
Mission (/missions/:id)
  │
  ├── Briefing → Start → Focus Mode → Submit → Complete
  │
Result (/missions/:id/result)
  │
  ├── Celebration → "Back to Dashboard" / "Continue Journey"
```

**Gaps:**
- Entry point (home page) is a dead end
- No Demo mode for instant evaluation
- No way to skip auth entirely

### 4.4 TTFC Target: < 5 minutes

**Current estimate:** 5-8 minutes (including account creation)

**Optimization path to < 5 min:**

| Step | Current | Optimized | Saving |
|------|---------|-----------|--------|
| Create account | ~15s | ~0s (Demo mode) | 15s |
| Browse journeys | ~30s | ~15s (pre-selected) | 15s |
| Start mission | ~10s | ~5s | 5s |
| Complete mission (read + evidence) | ~4-7 min | ~3-4 min | 1-3 min |
| Receive competency | ~0s (auto) | ~0s | 0s |
| **Total** | **5-8 min** | **3.5-4.5 min** | **1.5-3.5 min** |

**Demo Mode** is the single highest-impact change for TTFC.

---

## 5. Visual Review

### 5.1 Spacing & Alignment

| Issue | Location | Severity |
|-------|----------|----------|
| Inconsistent page wrapper padding | `dashboard` uses `p-4 md:p-6 lg:p-8`; `journeys` uses `p-6`; `auth` uses `p-4` | 🟡 MEDIUM |
| Skeleton grids use hardcoded padding | `dashboard` line 93: `padding="md"` hardcoded | 🟡 MEDIUM |
| Card padding inconsistently applied | `CardContent` duplicates Card's padding logic | 🟡 MEDIUM |

### 5.2 Color & Contrast

| Issue | Location | Severity |
|-------|----------|----------|
| Hardcoded `text-green-500`, `text-red-500` | `Alert`, `ErrorState`, `SuccessState`, `Toast` | 🔴 HIGH |
| Hardcoded `purple-100`/`purple-700` on xp variant | `Badge` | 🟠 MEDIUM |
| Status dot colors hardcoded (`bg-yellow-400`, etc.) | `MissionStatus` | 🟠 MEDIUM |
| Gradient hardcoded in XPBar | `XPBar` | 🟡 LOW |

### 5.3 Animations

| Issue | Location | Severity |
|-------|----------|----------|
| `Skeleton` shimmer ignores `prefers-reduced-motion` | `Skeleton` | 🟠 MEDIUM |
| `XPBar` / `ProgressIndicator` transition ignores reduced-motion | Both | 🟠 MEDIUM |
| `AscensionRing` transition ignores reduced-motion | AscensionRing | 🟠 MEDIUM |
| No page transition/route animation | All pages | 🟡 LOW |

### 5.4 Dark Mode

| Issue | Severity |
|-------|----------|
| Hardcoded colors (green/red/purple) bypass dark mode entirely | 🔴 HIGH |
| CSS variables for primary surfaces are correct — only accent colors leak | 🟠 MEDIUM |

### 5.5 Responsiveness

| Issue | Location | Severity |
|-------|----------|----------|
| No explicit mobile testing done; layouts use Tailwind responsive prefixes | All pages | 🟡 LOW |
| Dashboard stat grid collapses to 2 columns on mobile | Dashboard | 🟢 GOOD |
| Journey explorer uses 2-column grid | Journeys | 🟢 GOOD |

### 5.6 Accessibility

| Issue | Location | Severity |
|-------|----------|----------|
| `aria-label={title}` renders `"undefined"` when no title | Modal, Drawer | 🔴 CRITICAL |
| No focus trap in Modal | Modal | 🔴 CRITICAL |
| No focus trap in Drawer | Drawer | 🔴 CRITICAL |
| No `aria-live` region for Toast | Toast | 🔴 CRITICAL |
| No `aria-describedby` in Tooltip | Tooltip | 🟠 MAJOR |
| No `role="progressbar"` on XPBar | XPBar | 🟠 MAJOR |
| AscensionRing lacks ARIA progress attributes | AscensionRing | 🟠 MAJOR |
| Avatar no `onError` fallback to initials | Avatar | 🟠 MAJOR |
| Textarea missing `aria-describedby` for error | Textarea | 🟠 MAJOR |
| AchievementBadge no `aria-label` for locked state | AchievementBadge | 🟡 MINOR |

---

## 6. Architectural Review

### 6.1 Duplication Found

| Pattern | Count | Files |
|---------|-------|-------|
| `_code_to_status` function | **4 copies** | `builder.py`, `mission.py`, `auth.py` (x2) |
| Auth guard (useEffect + null return) | **5 copies** | All 5 pages |
| Error-handling if-block pattern | **~10 copies** | Across all routers |
| `competency_node_to_canonical` vs `competency_to_summary` | **90% identical** | `mapper.py` |
| Skeleton grid rendering pattern | **2 copies** | `dashboard`, `journeys` |

### 6.2 Coupling Found

| Coupling | Severity | Description |
|----------|----------|-------------|
| Routers → `adapter._*` private members | 🔴 CRITICAL | 6 routers access private adapter state |
| Result page → URL query params | 🔴 CRITICAL | Result data flows through URL encoding |
| Pages → `lib/api.ts` `any` return type | 🔴 CRITICAL | Type unsafety cascades everywhere |
| Auth → localStorage (Zustand persist) | 🟡 MEDIUM | Middleware can't read auth state |

### 6.3 Large Components

| Component | Lines | Should Split? |
|-----------|-------|---------------|
| `runtime_adapter.py` | 486 | Yes — into use-case-specific adapters |
| `mapper.py` | 407 | Yes — into per-domain mappers |
| `mission.py` router | 230 | Yes — the `complete_mission` function (110 lines) |
| `dashboard/page.tsx` | 227 | Yes — extract StatCard, skeleton, empty state |
| `journeys/page.tsx` | 242 | Yes — extract detail panel, mission list |
| `result/page.tsx` | 280 | Yes — extract reward sections |
| `missions/[missionId]/page.tsx` | 254 | Yes — extract phase components |

### 6.4 Repeated Hooks / Stores / Queries

| Pattern | Occurrences | Recommendation |
|---------|-------------|----------------|
| `useAuthStore` import | 5 ad-hoc | Export from barrel, use `@/store` |
| `useQuery` for builder data | Scattered | Centralize in a `useBuilder` hook |
| `useMutation` patterns | Varied per page | Standardize mutation error handling |
| `useEffect` auth guard | 5 copies | Extract `useAuthGuard()` hook |

### 6.5 Redundant / Dead Code

| Where | What | Status |
|-------|------|--------|
| `schemas/builder.py` | `SocialLinkOut`, `CompetencyEdgeOut`, `LearningPathOut`, etc. | Dead — never returned by any endpoint |
| `schemas/builder.py` | `BuilderUpdate.bio` | Dead — router only updates `display_name` |
| `result/page.tsx:59` | `scorePercent` calculation | Dead — formula cancels out |
| `mapper.py` | `assessment_to_result` | Dead — never called |
| `journey-card.tsx` | `group` class | Dead — no `group-hover` styles |

---

## 7. New Metric: Time To First Competency (TTFC)

### Definition

> **TTFC** = Tempo decorrido entre o momento em que um usuário abre o ASCEND pela primeira vez e o momento em que recebe sua primeira competência.

### Formula

```
TTFC = t_auth + t_journey_select + t_mission_read + t_evidence_submit + t_assessment
```

Onde:
- `t_auth`: tempo para criar/autenticar Builder
- `t_journey_select`: tempo para escolher uma jornada
- `t_mission_read`: tempo para ler o briefing da missão
- `t_evidence_submit`: tempo para produzir e enviar evidência
- `t_assessment`: tempo para avaliação automática (0 — instantânea)

### Target

| Level | TTFC | Condition |
|-------|------|-----------|
| 🟢 Excelente | **< 5 min** | Meta principal |
| 🟡 Aceitável | 5-10 min | Mínimo aceitável |
| 🔴 Ruim | > 10 min | Requer redesign |

### How to Measure

Instrumentar o frontend com eventos de telemetria local (sem backend):

```typescript
// store/telemetry-store.ts
interface TelemetryEvent {
  name: 'builder_created' | 'journey_selected' | 'mission_started'
       | 'evidence_submitted' | 'competency_unlocked'
  timestamp: number
}
```

Armazenar em `localStorage`. O TTFC é calculado como:

```
TTFC = competency_unlocked.timestamp - builder_created.timestamp
```

### Primary Levers to Improve TTFC

1. **Demo Builder** (remove `t_auth`) → -15s
2. **Pre-selected journey** on Demo → -30s
3. **Shorter mission briefing** (content design, not code) → -1-3 min
4. **Evidence template/suggestion** → -1 min
5. **Instant assessment** (already implemented) → 0s

### Secondary Metric: Time To First Achievement (TTFA)

Same principle, but measuring when the first achievement is earned. Should be ≤ TTFC.
If TTFA > TTFC, the first mission should also grant an achievement.

---

## 8. Demo Builder

### Why

A barreira de entrada mais alta hoje é **criação de conta**. O Demo Builder elimina isso:

- Sem cadastro
- Sem login
- Sem senha
- Experiência completa em < 5 minutos
- Dados armazenados localmente (sessionStorage)

### How

```typescript
// store/demo-store.ts
interface DemoStore {
  isDemo: boolean
  demoId: string | null
  startDemo: () => void
  endDemo: () => void
}
```

**Flow:**

```
Home Page (/)
  │
  ├── "Experimentar agora" button
  │   └── Cria Builder temporário via API
  │   └── Salva demoId em sessionStorage
  │   └── Redireciona para /demo/journey
  │
Demo Journey (/demo/journey)
  │
  ├── Pré-seleciona "Python Foundations"
  ├── Inicia primeira missão automaticamente
  │
Demo Mission (/demo/mission/1)
  │
  ├── Briefing reduzido
  ├── Textarea para evidência
  ├── "Enviar e ver resultado"
  │
Demo Result (/demo/result)
  │
  ├── Mostra competência desbloqueada
  ├── "Criar conta para salvar progresso"
  └── "Explorar mais" (convite para criar conta)
```

**Technical concerns:**
- Demo Builder = real Builder na API, mas sem persistência garantida
- Backend precisa de um endpoint `POST /demo/builders` que cria Builder com flag `is_demo: true`
- Cleanup periódico de Builders demo (cron job ou TTL)
- Frontend usa namespace `/demo/*` separado para clareza

### When

Recomendado como a **primeira entrega** da OPERAÇÃO ORION, antes de qualquer refatoração profunda, porque:
1. Impacto direto em TTFC
2. Sem risco de regressão (caminho novo)
3. Valida a hipótese mais importante: "o fluxo funciona sem cadastro"

---

## 9. JWT, Marketplace, Multiplayer, IA — Postponed

### Decisão

| Feature | Decision | Rationale |
|---------|----------|-----------|
| **JWT / Real Auth** | ❌ Postponed | Stub atual é suficiente para validação de experiência |
| **Marketplace** | ❌ Postponed | Sem comunidade, não há o que marketplacar |
| **Multiplayer** | ❌ Postponed | Sem fluxo single-player validado |
| **AI Mentor** | ❌ Postponed | Sem evidência de que o núcleo funciona |
| **Chat / Ranking** | ❌ Postponed | Gamificação prematura |

### Quando cada um fará sentido

| Feature | Trigger |
|---------|---------|
| **JWT** | Múltiplos Builders, persistência remota, contas reais |
| **Marketplace** | 10+ pacotes comunitários publicados |
| **Multiplayer** | Builder Journey validado com NPS > 50 |
| **AI Mentor** | TTFC < 5 min consistente; feedback qualitativo positivo |

### A única pergunta que importa agora

> **Uma pessoa aprende melhor usando o ASCEND do que estudando da forma tradicional?**

Se essa resposta ainda não foi validada, qualquer funcionalidade adicional aumenta a complexidade sem reduzir a incerteza.

---

## 10. Architecture Freeze

### Declaração do Chief Architect

A arquitetura do ASCEND **v1.x está oficialmente congelada**.

A partir de 2026-07-20:

| Regra | Descrição |
|-------|-----------|
| ✅ **Aceito** | Correções de bugs, performance, segurança, acessibilidade, UX |
| ✅ **Aceito** | Refatorações que reduzem duplicação e acoplamento |
| ✅ **Aceito** | Demo Builder (exceção estratégica) |
| ❌ **Rejeitado** | Novas abstrações sem problema concreto identificado |
| ❌ **Rejeitado** | Novas funcionalidades (JWT, IA, Marketplace, etc.) |
| ❌ **Rejeitado** | Mudanças arquiteturais sem RFC |

### Fluxo para mudanças arquiteturais

```
Identificou um problema concreto durante estabilização?
  │
  ├── Sim → Escreve RFC → TSC review → Aprovação → Implementa
  │
  └── Não → Documenta no backlog → Revisita após OPERAÇÃO ORION
```

---

## 11. Stabilization Roadmap

### Sprint ORION-001 — Foundation Fixes (Priority 1)

| # | Task | Area | Effort | Impact |
|---|------|------|--------|--------|
| 1 | Replace URL result-passing with Zustand store | Frontend | S | 🔴 Critical |
| 2 | Type API client with response interfaces | Frontend | M | 🔴 Critical |
| 3 | Export `useAuthStore` from barrel | Frontend | XS | 🔴 Critical |
| 4 | Remove traceback from error responses | Backend | XS | 🔴 Critical |
| 5 | Add `journey_id` FK to missions table; fix N+1 queries | Backend | M | 🔴 Critical |
| 6 | Extract `complete_mission` logic from router to use case | Backend | L | 🔴 Critical |
| 7 | Stop router access to `adapter._*` private members | Backend | M | 🔴 Critical |
| 8 | Extract duplicated auth guard into `useAuthGuard()` hook | Frontend | S | 🟠 Major |
| 9 | Fix `aria-label="undefined"` in Modal + Drawer | Frontend | XS | 🔴 Critical |
| 10 | Add focus traps to Modal + Drawer (Radix Dialog) | Frontend | M | 🔴 Critical |

### Sprint ORION-002 — UX & Quality (Priority 2)

| # | Task | Area | Effort |
|---|------|------|--------|
| 11 | Move `seedJourneys` out of `queryFn` into separate mutation | Frontend | S |
| 12 | Add explicit `gcTime`, `refetchOnWindowFocus` to QueryProvider | Frontend | XS |
| 13 | Replace hardcoded colors with CSS variables in 6+ components | Frontend | S |
| 14 | Add `aria-live` region to Toast; add `aria-describedby` to Tooltip | Frontend | M |
| 15 | Replace `print()` with `logging` in API middleware | Backend | XS |
| 16 | Add pagination to all backend list endpoints | Backend | M |
| 17 | Add `GET /builders` list endpoint | Backend | S |
| 18 | Add `GET /missions` list endpoint with filters | Backend | M |
| 19 | Consolidate `_code_to_status` into shared `api/errors.py` | Backend | S |
| 20 | Fix dead `scorePercent` formula on result page | Frontend | XS |

### Sprint ORION-003 — Demo Builder (Priority 3)

| # | Task | Area | Effort |
|---|------|------|--------|
| 21 | Add `POST /demo/builders` endpoint | Backend | S |
| 22 | Create `store/demo-store.ts` | Frontend | S |
| 23 | Create `/demo/journey`, `/demo/mission/:id`, `/demo/result` pages | Frontend | M |
| 24 | Add "Experimentar agora" CTA to home page | Frontend | S |
| 25 | Implement periodic demo Builder cleanup | Backend | S |

### Sprint ORION-004 — Component Library Overhaul (Priority 4)

| # | Task | Area | Effort |
|---|------|------|--------|
| 26 | Migrate all variant maps to `cva()` | Frontend | M |
| 27 | Migrate Modal/Drawer to Radix Dialog | Frontend | M |
| 28 | Migrate Toast to Radix Toast | Frontend | M |
| 29 | Migrate Tooltip to Radix Tooltip | Frontend | M |
| 30 | Add `prefers-reduced-motion` to Skeleton, XPBar, AscensionRing | Frontend | S |
| 31 | Fix Avatar `Next/Image` hardcoded size + add `onError` | Frontend | S |
| 32 | Remove dead schemas from `schemas/builder.py` | Backend | S |
| 33 | Remove dead code from `mapper.py` | Backend | S |

### Effort Summary

| Sprint | Tasks | Total Effort |
|--------|-------|-------------|
| ORION-001 | 10 | ~4-5 days |
| ORION-002 | 10 | ~4-5 days |
| ORION-003 | 5 | ~3-4 days |
| ORION-004 | 8 | ~4-5 days |
| **Total** | **33** | **~15-19 days** |

---

## 12. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial stabilization plan |
