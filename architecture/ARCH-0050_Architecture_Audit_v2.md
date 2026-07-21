# ARCH-0050 — Architecture Audit v2.x

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0050 |
| **Nome** | Architecture Audit v2.x |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Governance |
| **Operação** | HADES |
| **Data** | 2026-07-21 |

---

## Part I — Current State

### Documentation Inventory

| Category | Count | Range |
|----------|-------|-------|
| ARCH docs | 48 | ARCH-0001 to ARCH-0047 |
| SPEC docs | 6 | SPEC-0001 to SPEC-0006 |
| Foundation docs | 13 | DOC-0000 to DOC-0012 (incl. I18) |
| Source modules | 10 packages | domain, application, infrastructure, package_engine, runtime, cli, api, shared, cognitive, adapter |

### Architectural Layers (clean separation)

| Layer | Package | Description |
|-------|---------|-------------|
| Domain | `domain/` | 10 entities, 6 domain events |
| Application | `application/` | 5 use cases, 4 services, DTOs, interfaces |
| Infrastructure | `infrastructure/` | SQLite repos, event store, migrations, UoW |
| Package Engine | `package_engine/` | Parser, Validator (13 rules), Loader |
| Runtime Kernel | `runtime/` | Kernel, Hooks, Orchestrator, Runners, Report, Assessment, Adapters |
| Cognitive Pipeline | `cognitive/` | Collector→Normalizer→Extractor→Detector→Insight→Recommendation→Timeline |
| API | `api/` | 8 routers (auth, builder, mission, journey, health, cognitive, demo, version) |
| CLI | `cli/` | `ascend` CLI (run, validate, init, doctor) |
| Shared | `shared/` | IDs, Result, Clock, types, value_objects |
| Adapter | `adapter/` | Mapper, ErrorMapper, EventAdapter, RuntimeAdapter |

### Test Health

- **Total tests**: 395 (all passing, deterministic)
- **Coverage areas**: domain (43), application (19), infrastructure (23), package_engine (37), runtime (28), API+CLI (13), cognitive pipeline (46-340 across stages)
- **No flaky tests observed**

### Configuration State

- `.ascend/AI_BOOT_SEQUENCE.md` — aligns with I1–I18
- `.opencode/settings.json` — configured
- `pyproject.toml` — project metadata, dependencies pinned
- `pytest.ini` — test configuration
- `.gitignore`, `.dockerignore` — standard exclusions

---

## Part II — Architectural Debt

### Critical Issues

| ID | Severity | Description |
|----|----------|-------------|
| D-01 | HIGH | **ARCH-0008 ID collision**: `ARCH-0008_Competency_Lifecycle.md` and `ARCH-0008_Persistence_Architecture.md` share ARCH-0008 |
| D-02 | HIGH | **Missing ARCH-0007**: gap in ARCH sequence (0001-0006 → 0008) |
| D-03 | HIGH | **SPEC-0002 ID collision**: `SPEC-0002_AEP_v1.md` (official) and `SPEC-0002_Package_Validation.md` (later addition) |
| D-04 | HIGH | **SPEC-0003 ID collision**: `SPEC-0003_ARP_v1.md` (official) and `SPEC-0003_Registry_Protocol.md` (later addition) |
| D-05 | MEDIUM | **docs/charter.md duplication**: duplicates `foundation/DOC-0001_Project_Charter.md` (242 lines) |

### Documentation Issues

| ID | Severity | Description |
|----|----------|-------------|
| D-06 | LOW | **ARCH-0022 vs ARCH-0023**: Frontend Structure and Layout Architecture — distinct but adjacent; considered clean |
| D-07 | LOW | **runtime/assessment vs cognitive/**: AssessmentPipeline scores evidence against rubrics; cognitive pipeline processes learning analytics — distinct domains, no overlap |

### Source Code Issues

| ID | Severity | Description |
|----|----------|-------------|
| D-08 | LOW | **doctor.py**: 593 lines, contains 3 concerns (workflow, release, architecture) — candidate for splitting |
| D-09 | LOW | **No standalone integration tests**: all 395 tests are unit-level; no cross-layer integration suite |
| D-10 | MEDIUM | **No Evidence router**: `evidence` is a core domain entity but has no dedicated API router (served through mission/journey) |
| D-11 | LOW | **cognitive.py router**: 119 lines, 6 endpoints — clean, reasonable size |

### Architectural Boundary Clarity

| Boundary | Assessment |
|----------|------------|
| `runtime/` vs `package_engine/` | Clean: package_engine parses/validates/loads; runtime executes |
| `runtime/` vs `cognitive/` | Clean: runtime runs missions; cognitive analyzes learning data |
| `adapter/` vs `runtime/adapters/` | Clean: `adapter/` is generic domain-DTO mapping; `runtime/adapters/` converts packages |

---

## Part III — Simplifications

### S-01: Renumber ARCH-0008 duplicate

- `ARCH-0008_Persistence_Architecture.md` → reassign to **ARCH-0007**
- Update internal references in the file
- `Persistence_Architecture` was written after `Competency_Lifecycle` and lacks the original ID — reassign

### S-02: Renumber SPEC-0002 duplicate

- `SPEC-0002_Package_Validation.md` → reassign to **SPEC-0007** (next available; SPEC-0005 = Cognitive Protocol, SPEC-0006 = Cognitive Pipeline Contracts)
- SPEC-0002_AEP_v1 retains SPEC-0002

### S-03: Renumber SPEC-0003 duplicate

- `SPEC-0003_Registry_Protocol.md` → reassign to **SPEC-0008**
- SPEC-0003_ARP_v1 retains SPEC-0003

### S-04: Remove docs/charter.md

- Delete `docs/charter.md` (duplicate of `foundation/DOC-0001_Project_Charter.md`)

### S-05: Add I19 — Evidence API Invariant

Evidence must have a dedicated API surface. Add invariant to DOC-0009.

### S-06: Standalone Integration Test Suite

Create `tests/integration/` with cross-layer tests: API → Use Case → Repository → SQLite.

---

## Part IV — Freezes (v2.x Stabilization)

After applying Simplifications S-01 through S-06, the following are **frozen** for v2.x:

### Frozen Documents

| Document | Freeze Note |
|----------|-------------|
| All ARCH docs (ARCH-0001 to ARCH-0050) | No structural changes without TSC approval |
| All SPEC docs (SPEC-0001 to SPEC-0009) | After renumbering, no spec changes |
| All Foundation docs (DOC-0000 to DOC-0012) | Including I18 + I19 |
| `.ascend/AI_BOOT_SEQUENCE.md` | Must align with invariants |

### Frozen Architectural Boundaries

| Boundary | Freeze Rule |
|----------|-------------|
| Domain Model (10 entities) | No new entities without TSC |
| Cognitive Pipeline (7 stages) | Pipeline is final; new rules can be added within stages |
| Package Engine (parse/validate/load) | No new pipeline stages |
| Runtime Kernel (7 components) | No new components without TSC |
| API (read-only cognitive) | No mutations on cognitive data in v2.x |

### What CAN change in v2.x

- New detection/insight/recommendation rules within existing pipeline stages
- New ERA G features under `src/ascend/g/` prefix
- Observability, Plugin System, Event Replay as extensions
- AI Adapter Layer (G6) as interfaces only

---

## Part V — Roadmap v3.0

### Phase 1: Corrections (this session)

| Step | Action |
|------|--------|
| 1 | Rename ARCH-0008_Persistence_Architecture → ARCH-0007 (update file, internal refs) |
| 2 | Rename SPEC-0002_Package_Validation → SPEC-0007 |
| 3 | Rename SPEC-0006_Cognitive_Query → SPEC-0008 |
| 4 | Rename SPEC-0003_Registry_Protocol → SPEC-0009 |
| 5 | Delete docs/charter.md |
| 6 | Add I19 to DOC-0009 |
| 7 | Git tag `v2.1.0-audit` |

### Phase 2: ERA G — Platform Maturity

| Step | Code | Description |
|------|------|-------------|
| 8 | G1 | Observability (metrics, logging, tracing SDK) |
| 9 | G2 | Plugin System (hook-based plugin loader) |
| 10 | G3 | Event Replay (event stream replay from event store) |
| 11 | G4 | Sandbox Runtime (isolated package execution) |
| 12 | G5 | Marketplace Foundation (package index, registry client) |
| 13 | G6 | AI Adapter Layer (interfaces: LLM, Embedding, Vision, Speech, Reasoning) |
| 14 | G7 | Sovereign Runtime (offline-first, self-hosted execution environment) |

### Phase 3: Freeze

| Step | Action |
|------|--------|
| 15 | Git tag `v2.2.0-platform` |
| 16 | Declare v2 architecture frozen |

---

## Appendix A — Complete Document Register

| ID | File | Status |
|----|------|--------|
| ARCH-0001 | System Architecture Overview | ✅ |
| ARCH-0002 | Domain Model | ✅ |
| ARCH-0003 | Core Engine Specification | ✅ |
| ARCH-0004 | Agent Architecture | ✅ |
| ARCH-0005 | Data Model | ✅ |
| ARCH-0006 | MVP Technical Specification | ✅ |
| ARCH-0007 | **Persistence Architecture** (was ARCH-0008) | 🔄 |
| ARCH-0008 | Competency Lifecycle | ✅ |
| ARCH-0009 | Runtime State Machine | ✅ |
| ARCH-0010 | Policy Engine | ✅ |
| ARCH-0011 | Experience Layer | ✅ |
| ARCH-0012 | Developer Governance System | ✅ |
| ARCH-0013 | Product Behavior Architecture | ✅ |
| ARCH-0014 | Ascension Ring Specification | ✅ |
| ARCH-0015 | API Architecture | ✅ |
| ARCH-0016 | Frontend SDK | ✅ |
| ARCH-0017 | Authentication Model | ✅ |
| ARCH-0018 | Frontend State | ✅ |
| ARCH-0019 | Frontend Data Flow | ✅ |
| ARCH-0020 | UI Contracts | ✅ |
| ARCH-0021 | Error Handling | ✅ |
| ARCH-0022 | Frontend Structure | ✅ |
| ARCH-0023 | Layout Architecture | ✅ |
| ARCH-0024 | Frontend SDK Architecture | ✅ |
| ARCH-0025 | SDK Lifecycle | ✅ |
| ARCH-0026 | Domain Event Catalog | ✅ |
| ARCH-0027 | Builder Identity Model | ✅ |
| ARCH-0028 | API Resource Model | ✅ |
| ARCH-0029 | Dependency Graph | ✅ |
| ARCH-0030 | Cognitive Architecture | ✅ |
| ARCH-0031 | Observation Model | ✅ |
| ARCH-0032 | Observation Event Taxonomy | ✅ |
| ARCH-0033 | Observation Pipeline | ✅ |
| ARCH-0034 | Behavioral Metrics | ✅ |
| ARCH-0035 | Observation Storage | ✅ |
| ARCH-0036 | Observation SDK | ✅ |
| ARCH-0037 | Privacy Sovereign Cognitive Data | ✅ |
| ARCH-0038 | Cognitive Timeline | ✅ |
| ARCH-0039 | Observation Normalization | ✅ |
| ARCH-0040 | Signal Extraction Architecture | ✅ |
| ARCH-0041 | Timeline and Replay | ✅ |
| ARCH-0042 | Engineering Workflow Architecture | ✅ |
| ARCH-0043 | Cognitive Processing Pipeline | ✅ |
| ARCH-0044 | Signal Model | ✅ |
| ARCH-0045 | Pattern Detection Architecture | ✅ |
| ARCH-0046 | Insight Engine Architecture | ✅ |
| ARCH-0047 | Recommendation Engine Architecture | ✅ |
| ARCH-0050 | Architecture Audit v2.x **(this document)** | ✅ |

## Appendix B — Renumbering Table

| Old ID | New ID | File |
|--------|--------|------|
| ARCH-0008 (Persistence) | ARCH-0007 | `ARCH-0007_Persistence_Architecture.md` |
| SPEC-0002 (Package Validation) | SPEC-0007 | `SPEC-0007_Package_Validation.md` |
| SPEC-0003 (Registry Protocol) | SPEC-0008 | `SPEC-0008_Registry_Protocol.md` |
