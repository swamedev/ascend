# Project Identity

**Nome:** ASCEND
**Categoria:** Competency Development Framework (CDF)

---

# North Star

> Toda competência reivindicada deve ser uma competência comprovada.

---

# Phase

**v1.0 Standard Edition — RELEASED** (Architecture frozen)
**v2.0 Adoption — ACTIVE**

---

# The Vehicle

> *Software was never the destination. It was the vehicle.*

---

# Completed

## v1.0 Standard Edition (2026-07-19)

### Foundation
- DOC-0000 — North Star
- DOC-0001 — Project Charter
- DOC-0002 — Manifesto
- DOC-0003 — First Principles
- DOC-0004 — Identity Architecture
- DOC-0005 — Brand Architecture
- DOC-0006 — Lexicon
- DOC-0007 — Engineering Philosophy
- DOC-0008 — Project Continuity Protocol

### System Architecture
- ARCH-0001 — System Architecture Overview
- ARCH-0002 — Domain Model
- ARCH-0003 — Core Engine Specification
- ARCH-0004 — Agent Architecture
- ARCH-0005 — Data Model Specification
- ARCH-0006 — MVP Technical Specification

### Implementation
- BUILD-0001 — Implementation Roadmap
- AGENT-0001 — DeepSeek Implementation Profile

### Core Domain (Sprint 1)
- 10 entities, 6 domain events, 43 tests

### Application Layer (Sprint 2)
- 5 use cases, 3 services, DTOs, protocols, 19 tests

### Infrastructure (Sprint 3)
- SQLite repositories, event store, migrations, UoW, 23 tests

### Package Engine (Sprint 4)
- Parser, Validator (13 rules), Loader, 4 ref. packages, 37 tests

### Runtime Kernel (Sprint 5)
- 7 components, hooks, execution report, 28 tests

### API + CLI (Sprint 6)
- `Runtime` class, `ascend` CLI (run, validate, init, doctor), 13 tests

### Specifications (Formal RFCs)
- SPEC-0001 — APS v1.0
- SPEC-0002 — AEP v1.0
- SPEC-0003 — ARP v1.0
- SPEC-0004 — AAP v1.0

### Governance
- CONTRIBUTING.md, GOVERNANCE.md, ROADMAP_2035.md

### Standard Edition Closure
- v1/STANDARD_EDITION.md — formal release declaration

---

# Current Work

**v2 Adoption — Phase 1: Strategy**

| Doc | Status |
|-----|--------|
| V2-0001 Adoption Strategy | Draft |
| V2-0002 Community Strategy | Draft |
| V2-0003 Content Strategy | Draft |
| V2-0004 Institute Strategy | Draft |
| V2-0005 Funding Strategy | Draft |

**Next:** Publish, build community, author ASCEND Book, launch Academy

---

# Rules

1. Preserve approved decisions
2. Do not restart architecture
3. Follow First Principles
4. No competency without evidence
5. AI is a layer, not the core
6. **v1 architecture is frozen** — no changes without TSC approval
7. **Adoption drives v2** — code serves community, not the reverse

---

# Key Architecture Decisions

- **Engine First** — Engine é agnóstica a domínio
- **Content as Data** — Pacotes independentes, Engine apenas interpreta
- **AI as Layer** — IA é camada substituível
- **Evidence Driven** — Evidência é a unidade mais importante
- **CLI-First MVP** — Python + SQLite + argparse
- **Local First** — Dados pertencem ao usuário
- **v1 Frozen** — Arquitetura da v1 não será modificada
