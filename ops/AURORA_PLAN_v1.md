# ⚜️ OPERAÇÃO AURORA — Product Hardening

| Field | Value |
|-------|-------|
| **Document** | AURORA_PLAN_v1.md |
| **Operation** | OPERAÇÃO AURORA |
| **Phase** | E — Product Stabilization |
| **Status** | Active |
| **Date** | 2026-07-20 |
| **Chief Architect** | R.V. |

---

> *"Não adicione mais nada até que o núcleo seja impecável."*

---

## Strategy

```
ORION (diagnóstico)    →    AURORA (execução)    →    v1.1 Stable
       🔍                        🔧                    🚀
```

ORION identificou o que está quebrado. AURORA vai consertar.

---

## Sprint AURORA-1 — Backend Hardening

**Goal:** Remove all critical and major findings from the backend audit.

### Tasks

| # | Task | File(s) | Impact |
|---|------|---------|--------|
| A1.1 | Extract `complete_mission` logic into `CompleteMissionUseCase` | `api/routers/mission.py` → `application/use_cases/complete_mission.py` | 🔴 Critical |
| A1.2 | Remove traceback from error responses; log server-side | `adapter/error_mapper.py` | 🔴 Critical |
| A1.3 | Route `DELETE /builders/{id}` through adapter | `api/routers/builder.py`, `adapter/runtime_adapter.py` | 🔴 Critical |
| A1.4 | Fix encapsulation: routers use only public adapter methods | `api/routers/*.py`, `adapter/runtime_adapter.py` | 🔴 Critical |
| A1.5 | Add `journey_id` FK to missions; fix N+1 queries | `infrastructure/`, `adapter/runtime_adapter.py` | 🔴 Critical |
| A1.6 | Replace `print()` with `logging` module in middleware | `api/middleware/logger.py` | 🟠 Major |
| A1.7 | Consolidate `_code_to_status` into shared `api/errors.py` | All routers + new `api/errors.py` | 🟠 Major |
| A1.8 | Fix auth: separate login/register, proper token scheme | `api/routers/auth.py` | 🟠 Major |
| A1.9 | Add pagination to all list endpoints | All routers + adapter | 🟠 Major |
| A1.10 | Add `GET /builders` list endpoint | `api/routers/builder.py` | 🟡 Minor |
| A1.11 | Fix timestamps in mappers (use actual domain timestamps) | `adapter/mapper.py` | 🟡 Minor |
| A1.12 | Remove dead schemas from `schemas/builder.py` | `api/schemas/builder.py` | 🟡 Minor |
| A1.13 | Add structured logging (correlation ID through error_mapper) | `adapter/error_mapper.py` | 🟠 Major |
| A1.14 | Default DB path from environment variable | `api/app.py` | 🟠 Major |

### Definition of Done

- [ ] Zero direct access to `adapter._*` private members from routers
- [ ] `complete_mission` router is < 10 lines (validate → delegate → respond)
- [ ] All error responses are ASCEND_ERROR envelope; no tracebacks
- [ ] Auth has separate login/register with non-forgeable tokens
- [ ] N+1 queries eliminated from `list_journeys` and `get_journey`
- [ ] All list endpoints accept `?limit=&offset=`
- [ ] `print()` replaced with `logging.getLogger(__name__)`
- [ ] `_code_to_status` defined once in `api/errors.py`
- [ ] All 168+ tests still passing

---

## Sprint AURORA-2 — Frontend Hardening

**Goal:** 100% accessible component library, clean architecture, zero `any`.

### Tasks

| # | Task | File(s) | Impact |
|---|------|---------|--------|
| A2.1 | Type API client with response interfaces | `lib/api.ts` | 🔴 Critical |
| A2.2 | Replace URL result-passing with Zustand store | `missions/[missionId]/page.tsx`, `result/page.tsx` | 🔴 Critical |
| A2.3 | Export `useAuthStore` from barrel | `store/index.ts` | 🔴 Critical |
| A2.4 | Extract `useAuthGuard()` hook | All pages → `hooks/use-auth-guard.ts` | 🟠 Major |
| A2.5 | Fix `aria-label={title}` rendering `"undefined"` | `modal.tsx`, `drawer.tsx` | 🔴 Critical |
| A2.6 | Add focus traps to Modal + Drawer (Radix Dialog) | `modal.tsx`, `drawer.tsx` | 🔴 Critical |
| A2.7 | Add `aria-live` to Toast; migrate to Radix Toast | `toast.tsx` | 🔴 Critical |
| A2.8 | Add `aria-describedby` to Tooltip; migrate to Radix Tooltip | `tooltip.tsx` | 🟠 Major |
| A2.9 | Replace hardcoded colors with CSS variables (6+ components) | `alert.tsx`, `badge.tsx`, `state-components.tsx`, etc. | 🟠 Major |
| A2.10 | Add reduced-motion to Skeleton, XPBar, AscensionRing | `skeleton.tsx`, `xp-bar.tsx`, `ascension-ring.tsx` | 🟠 Major |
| A2.11 | Fix Avatar `Next/Image` hardcoded size + add `onError` | `avatar.tsx` | 🟠 Major |
| A2.12 | Fix Textarea missing `aria-describedby` for error | `textarea.tsx` | 🟠 Major |
| A2.13 | Fix `api.seedJourneys()` inside `queryFn` | `journeys/page.tsx` | 🟠 Major |
| A2.14 | Add explicit React Query config (gcTime, refetchOnWindowFocus) | `providers/query-provider.tsx` | 🟠 Major |
| A2.15 | Remove magic numbers — named constants | `dashboard`, `result`, `journeys` pages | 🟡 Minor |
| A2.16 | Fix dead `scorePercent` formula | `result/page.tsx` | 🟡 Minor |
| A2.17 | Add home page CTA ("Experimentar agora") | `app/page.tsx` | 🟠 Major |
| A2.18 | Migrate variant maps to `cva()` throughout UI library | All `ui/*.tsx` | 🟡 Minor |

### Definition of Done

- [ ] `lib/api.ts` has typed return values for every endpoint
- [ ] Result data flows through Zustand, not URL params
- [ ] Zero `aria-label="undefined"` in any component
- [ ] Modal + Drawer trap focus correctly
- [ ] Toast announces to screen readers
- [ ] Tooltip linked to trigger via `aria-describedby`
- [ ] All accent colors use CSS variables (zero hardcoded `text-green-500`, etc.)
- [ ] Skeleton, XPBar, AscensionRing respect `prefers-reduced-motion`
- [ ] Avatar renders at correct size with fallback on image error
- [ ] Home page has a "Get Started" button
- [ ] TypeScript compiles with zero errors

---

## Sprint AURORA-3 — Demo Builder

**Goal:** TTFC < 2 minutes. No account required.

**Flow:**

```
Home Page (/)
  │
  ├── Hero: "ASCEND — Competency Development Framework"
  ├── Subtitle: "Aprenda fazendo. Comprove com evidências."
  ├── Button: "⭐ Experimentar Agora"
  │
  ├── Cria Builder temporário via POST /api/demo/builders
  │   └── Stores demoId em sessionStorage
  │   └── Redireciona para /demo/journey
  │
Demo Journey (/demo/journey)
  │
  ├── Card: "Python Foundations"
  │   ├── "6 missões · ~20 minutos"
  │   └── Button: "Começar Primeira Missão"
  │
Demo Mission (/demo/mission/{id})
  │
  ├── Briefing curto (3-5 linhas)
  ├── "O que você precisa fazer:"
  ├── Textarea grande
  ├── Button: "Enviar Evidência"
  │
Demo Result (/demo/result)
  │
  ├── "🎉 Missão Concluída!"
  ├── "Você desbloqueou: [Competency]"
  ├── XP ganho
  ├── "Quer salvar seu progresso?"
  ├── Button: "Criar Conta Gratuita" → /auth
  └── Button: "Continuar Explorando" → /demo/journey
```

### Tasks

| # | Task | File(s) | Impact |
|---|------|---------|--------|
| A3.1 | Add `POST /demo/builders` backend endpoint | `api/routers/demo.py` | 🔴 Critical |
| A3.2 | Create `store/demo-store.ts` | Frontend | 🔴 Critical |
| A3.3 | Create `/demo/journey` page | Frontend | 🔴 Critical |
| A3.4 | Create `/demo/mission/[id]` page | Frontend | 🔴 Critical |
| A3.5 | Create `/demo/result` page | Frontend | 🔴 Critical |
| A3.6 | Update home page with "Experimentar Agora" hero | `app/page.tsx` | 🔴 Critical |
| A3.7 | Implement demo Builder cleanup (TTL/cron) | Backend | 🟡 Minor |

### Key Metrics

| Metric | Target |
|--------|--------|
| TTFC (Demo) | < 2 minutes |
| Clicks to first mission | 2 ("Experimentar Agora" → "Começar Primeira Missão") |
| Fields to fill | 0 |

---

## Sprint AURORA-4 — Playtest

**Goal:** Observe 10 real users; identify all friction points; fix before v1.1.

### Protocol

```
1. Preparação
   ├── Build de preview (npm run build)
   ├── Ambiente limpo (sem dados prévios)
   ├── Gravador de tela (opcional)
   └── Roteiro de observação (checklist abaixo)

2. Instrução única ao participante
   "Este é um produto de aprendizado. Explore e use como achar melhor.
    Não vou responder perguntas durante o teste.
    Quando terminar, me diga o que achou."

3. Observação (sem interromper)
   ├── Onde ele clica primeiro?
   ├── Quanto tempo até entender o propósito?
   ├── Onde ele trava?
   ├── O que ele tenta fazer que não existe?
   ├── Ele consegue completar uma missão?
   └── Ele expressa frustração? Onde?

4. Pós-teste (5 min)
   ├── "O que você entendeu que o produto faz?"
   ├── "O que te frustrou?"
   ├── "O que você mais gostou?"
   └── "Você usaria de novo? Por quê?"

5. Correção
   ├── Consolidar observações
   ├── Priorizar por frequência
   ├── Fixar top 5 problemas
   └── Repetir
```

### Observation Checklist

| Observation | Notes |
|-------------|-------|
| Time to first click | |
| Time to understand purpose | |
| Clicks on non-interactive elements | |
| Where they hesitate (> 3s) | |
| Where they backtrack | |
| Attempted unavailable features | |
| Facial expressions (frustration/delight) | |
| Verbal comments | |
| Did they complete a mission? | |
| Would they return? | |

### Criteria for v1.1 Release

- [ ] 8/10 participants complete a mission without help
- [ ] 7/10 say they would use it again
- [ ] Zero participants give up in frustration
- [ ] Average TTFC < 5 min (real, not demo)
- [ ] All AURORA-1, AURORA-2, AURORA-3 tasks complete

---

## Release Cadence

```
AURORA-1 (Backend) ──────┐
                          │
AURORA-2 (Frontend) ──────┤
                          ├──► RC1 ──► Playtest ──► Fix ──► RC2 ──► v1.1 Stable
                          │
AURORA-3 (Demo) ──────────┘
```

Each sprint is estimated at 3-4 days of work. Total: ~12-16 days to v1.1 Stable.

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
