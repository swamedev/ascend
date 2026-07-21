# ASCEND — Product Milestones

| Field | Value |
|-------|-------|
| **Version** | 2.0 |
| **Status** | Approved |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000 North Star, ROADMAP_2035 |

---

> *"Software was never the destination. It was the vehicle."*

---

## Overview

This document defines the eight macro-milestones of ASCEND's product evolution. Each milestone represents a major capability level — not a version number.

```
A — Foundation                ✅ (COMPLETE)
B — Experience                ✅ (COMPLETE)
C — Platform                  ✅ (COMPLETE)
D — First Builder Journey     ✅ (COMPLETE)
E — Product Stabilization     🔄 (ACTIVE)
F — Intelligence              ⬜ (NEXT)
G — Ecosystem                 ⬜
H — Sovereign Learning Network  🌌 (VISION)
```

---

## A — Foundation ✅

**Status:** Complete (v1.0 Standard Edition)

**Theme:** *Make it work.*

### What was delivered

| Area | Deliverables |
|------|--------------|
| **Core Engine** | Mission, Evidence, Progress, Competency, Assessment engines |
| **Domain** | 10 entities, 6 domain events, domain protocols |
| **Application** | 5 use cases, DTOs, services |
| **Infrastructure** | SQLite repos, event store, migrations, Unit of Work |
| **Package Engine** | Parser, Validator (13 rules), Loader, 4 reference packages |
| **Runtime** | 7 components, hooks, execution report |
| **API + CLI** | Runtime class, `ascend` CLI (run, validate, init, doctor) |
| **Governance** | AEGS, Foundation docs, Architecture docs, ADRs, SPECs |

### Key metrics
- 168 tests, all passing
- 4 reference packages published
- Architecture frozen (v1)

---

## B — Experience ✅

**Status:** Complete

**Theme:** *Make it beautiful.*

### What was delivered

| Area | Deliverables |
|------|--------------|
| **Experience Architecture** | ARCH-0011, ARCH-0013, ARCH-0014 |
| **Design System** | UI-0001 (colors, typography, tokens, motion) |
| **Builder Journey** | UI-0002 (emotional design, 7 stages) |
| **Information Architecture** | UI-0003 (11 sections, navigation, command palette) |
| **Component Library** | UI-0004 (45 components in 6 categories) |
| **Wireframes** | WF-0001 through WF-0010 (10 screens) |
| **Product Behavior** | ARCH-0013 (daily, weekly, monthly, long-term loops) |
| **Ascension Ring** | ARCH-0014 (signature component specification) |

---

## C — Platform ✅

**Status:** Complete

**Theme:** *Make it multi-layer.*

### What was delivered

| Area | Deliverables |
|------|--------------|
| **Runtime Adapter** | Python package (5 files, 25 methods, 12/12 tests) |
| **FastAPI API** | 9 files, middleware (correlation, logger, error handler) |
| **REST Endpoints** | Builder CRUD, health, version, journeys, missions, auth |
| **OpenAPI** | Auto-generated docs at `/docs`, `/redoc` |
| **Schema Layer** | Pydantic v2 models (27 Builder schemas) |
| **Error Envelope** | ASCEND_ERROR — consistent error response format |
| **API Tests** | 13/13 integration tests passing |

---

## D — First Builder Journey ✅

**Status:** Complete

**Theme:** *Make it flow.*

### What was delivered

| Area | Deliverables |
|------|--------------|
| **Auth Page** | Login / create builder with stub auth |
| **Dashboard** | Builder stats, XP, progress, competencies, achievements |
| **Journey Explorer** | Journey listing, detail panel, mission start |
| **Mission Workspace** | 3-phase flow: briefing → focus mode → submit → complete |
| **Assessment Result** | Celebration page with score, XP, level-up, achievements |
| **API Client** | Fetch-based client with all endpoints |
| **React Query** | Provider with configurable defaults |
| **Zustand Stores** | Auth, layout, result — persisted and ephemeral |

### Key metrics
- 5 pages, 4 stores, 27+ UI components
- Full vertical slice: auth → journey → mission → evidence → assessment → competency → achievement
- TypeScript compiles clean (zero errors)

---

## E — Product Stabilization 🔄

**Status:** Active (current)

**Theme:** *Make it solid.*

*See full plan: `ops/STABILIZATION_PLAN_v1.md`*

### Objective

Transform the MVP into a solid product. Not building features — refining what already exists.

### Key areas

| Area | Focus |
|------|-------|
| **Backend** | Remove business logic from routers, fix N+1 queries, seal adapter encapsulation, kill traceback leakage |
| **Frontend** | Type API client, fix URL result-passing, consolidate auth guard, remove magic numbers |
| **Components** | Fix accessibility (focus traps, aria-label, live regions), adopt Radix primitives, respect reduced motion |
| **UX** | Demo Builder, TTFC < 5 min, fix friction points |
| **Architecture** | Eliminate duplication, consolidate error handling, standardize patterns |

### Key metric: Time To First Competency (TTFC)

| Level | Target | Current (est.) |
|-------|--------|----------------|
| 🟢 Excelente | < 5 min | — |
| 🟡 Aceitável | 5-10 min | 5-8 min |
| 🔴 Ruim | > 10 min | — |

### Opening

- [ ] Demo Builder (experiência completa sem cadastro)
- [ ] TTFC < 5 minutos consistente
- [ ] Backend architecture: business logic extraída de routers, adapter selado
- [ ] Frontend architecture: API tipada, barrel completo, auth guard centralizado
- [ ] Component library: Radix UI adotado, acessibilidade WCAG AA, `cva()` em uso
- [ ] Todos os estados (loading, error, empty, disabled) cobertos consistentemente
- [ ] Zero `any` types no pipeline de dados

---

## F — Intelligence ⬜

**Status:** Planned

**Theme:** *Make it smart.*

**Trigger:** TTFC < 5 min consistente; NPS > 50; Builder Journey validado.

| Capability | Description |
|-----------|-------------|
| **Mentor Agent** | Production-ready AI Mentor |
| **Reviewer Agent** | Automated evidence review |
| **Career Agent** | Career path recommendations |
| **Teacher Agent** | Dynamic content generation |
| **Interviewer Agent** | Competency validation through questioning |
| **Personalization** | Adaptive difficulty and pacing |

---

## G — Ecosystem ⬜

**Status:** Planned

**Theme:** *Make it open.*

**Trigger:** 10+ community packages published; Builder Journey validated.

| Capability | Description |
|-----------|-------------|
| **Package Registry** | Public registry for community packages |
| **Marketplace** | Discover, install, rate packages |
| **Community** | Leaderboards, forums, mentorship |
| **API Ecosystem** | Public API for tool builders |
| **Integrations** | GitHub, GitLab, LMS platforms |
| **SDK** | JavaScript, Python SDKs for embedding |

---

## H — Sovereign Learning Network 🌌

**Status:** Vision

**Theme:** *Make it borderless.*

This is the long-term vision.

> *A network where knowledge, competencies, and progress belong to the Builder — not to any single platform.*

| Capability | Description |
|-----------|-------------|
| **Portable Identity** | Builder profile and credentials across platforms |
| **Decentralized Evidence** | Verifiable credentials (W3C VC standard) |
| **Cross-Platform** | Competency recognized by other learning systems |
| **Peer Network** | Direct Builder-to-Builder knowledge exchange |
| **Open Protocol** | Anyone can build an ASCEND-compatible interface |
| **Self-Sovereign** | Builder owns all data, all progress, all evidence |

---

## Progress Tracking

| Milestone | Status | Start | Target | % Complete |
|-----------|--------|-------|--------|------------|
| **A — Foundation** | ✅ Complete | 2026-Q1 | 2026-Q2 | 100% |
| **B — Experience** | ✅ Complete | 2026-Q2 | 2026-Q3 | 100% |
| **C — Platform** | ✅ Complete | 2026-Q3 | 2026-Q3 | 100% |
| **D — First Builder Journey** | ✅ Complete | 2026-Q3 | 2026-Q3 | 100% |
| **E — Product Stabilization** | 🔄 Active | 2026-Q3 | 2026-Q3 | ~5% |
| **F — Intelligence** | ⬜ Planned | 2026-Q4 | 2027-Q1 | 0% |
| **G — Ecosystem** | ⬜ Planned | 2027-Q1 | 2027-Q3 | 0% |
| **H — Sovereign Network** | 🌌 Vision | 2027-Q3 | — | 0% |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
| 2.0 | 2026-07-20 | Chief Architect | Added D (First Builder Journey), E (Product Stabilization), shifted F→F/G/H; B and C marked Complete |
