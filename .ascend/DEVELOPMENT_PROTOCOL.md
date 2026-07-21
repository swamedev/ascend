# DEVELOPMENT PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-001 |
| **Name** | Development Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-000, DOC-0007, DOC-0009 |
| **Referenced by** | AEGS-002, AEGS-003, AEGS-004, AEGS-005 |

---

## 1. Purpose

Define the complete development conventions, folder structure, naming rules, and engineering policies for the ASCEND project.

---

## 2. Folder Conventions

```
ascend/
├── .ascend/              # AEGS governance documents
├── foundation/            # Immutable foundation documents (DOC-*)
├── architecture/          # Architecture documents (ARCH-*)
├── docs/
│   ├── adr/              # Architecture Decision Records
│   ├── build/            # Build & CI specifications
│   ├── protocol/         # External protocols docs
│   ├── spec/             # RFC specifications (SPEC-*)
│   └── ui/               # UI/UX specifications
├── src/
│   ├── ascend/
│   │   ├── domain/       # Core domain entities, events, protocols
│   │   ├── application/  # Use cases, DTOs, services
│   │   ├── infrastructure/ # Persistence, file system, external calls
│   │   ├── engine/       # Core engine components
│   │   ├── cli/          # CLI interface
│   │   └── runtime/      # Runtime kernel (orchestrator)
│   └── ...
├── packages/              # Reference content packages
├── tests/                 # All tests
├── platform/              # Platform-level configuration
├── scripts/               # Utility scripts
├── tools/                 # Developer tools
├── v1/                    # v1 Standard Edition artifacts
├── v2/                    # v2 Adoption artifacts
└── pyproject.toml         # Project configuration
```

---

## 3. Layer Responsibilities

| Layer | Directory | Responsibility | Dependencies |
|-------|-----------|----------------|--------------|
| **Domain** | `src/ascend/domain/` | Entities, value objects, events, protocols | None (pure Python) |
| **Application** | `src/ascend/application/` | Use cases, DTOs, services | Domain only |
| **Infrastructure** | `src/ascend/infrastructure/` | Repositories, file I/O, external adapters | Domain, Application |
| **Engine** | `src/ascend/engine/` | Core engine components | Domain, Application |
| **Runtime** | `src/ascend/runtime/` | Execution orchestrator | Engine, Domain, Application |
| **CLI** | `src/ascend/cli/` | Command-line interface | Runtime |
| **UI** | `apps/web/` | Web application | API |

---

## 4. Naming Conventions

### 4.1 Python

| Element | Convention | Example |
|---------|------------|---------|
| Classes | `PascalCase` | `MissionEngine`, `EvidenceSubmitted` |
| Functions | `snake_case` | `create_mission()`, `validate_evidence()` |
| Variables | `snake_case` | `mission_id`, `evidence_record` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_XP_PER_MISSION`, `DEFAULT_LEVEL` |
| Private | `_leading_underscore` | `_validate_internal()` |
| Protocols | `PascalCase` suffix | `EvidenceRepository` (Protocol) |
| Exceptions | `PascalCase` suffix `Error` | `InvalidEvidenceError` |

### 4.2 Files

| Element | Convention | Example |
|---------|------------|---------|
| Python modules | `snake_case.py` | `mission_engine.py` |
| Test files | `test_` prefix | `test_mission_engine.py` |
| Documentation | `ID_Title.md` | `ARCH-0003_Core_Engine_Spec.md` |
| ADR files | `NNNN-title.md` | `ADR-001_Engine_First_Architecture.md` |

### 4.3 Git Branches

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feat/short-description` | `feat/dashboard-shell` |
| Fix | `fix/short-description` | `fix/evidence-validation` |
| Docs | `docs/short-description` | `docs/wireframe-spec` |
| Refactor | `refactor/short-description` | `refactor/runtime-service` |
| Test | `test/short-description` | `test/runtime-state-engine` |

---

## 5. Type Hints

- All public APIs **must** have type hints
- All private functions **should** have type hints
- Use `Protocol` for interfaces (not `ABC`)
- Use `dataclass` for data containers
- Use `Optional[T]` instead of `T | None` for consistency

```python
from typing import Protocol, Optional
from dataclasses import dataclass

@dataclass
class Evidence:
    id: str
    content: str
    status: str

class EvidenceRepository(Protocol):
    def save(self, evidence: Evidence) -> None: ...
    def find_by_id(self, evidence_id: str) -> Optional[Evidence]: ...
```

---

## 6. Dataclasses

- Use `@dataclass(frozen=True)` for immutable value objects
- Use `@dataclass` for mutable entities
- Implement `__post_init__` for validation

---

## 7. Protocol Usage

- All repositories must be defined as `Protocol` in the domain layer
- Application layer depends on protocols, never on concrete implementations
- Infrastructure provides concrete implementations

```python
# domain/protocols.py
class MissionRepository(Protocol):
    def save(self, mission: Mission) -> None: ...
    def find_by_id(self, mission_id: str) -> Optional[Mission]: ...

# infrastructure/sqlite_mission_repository.py
class SQLiteMissionRepository:
    def save(self, mission: Mission) -> None:
        ...  # SQLite implementation
```

---

## 8. Testing Policy

| Aspect | Policy |
|--------|--------|
| **Coverage** | Every public function must have at least one test |
| **Types** | Unit tests + integration tests |
| **Framework** | pytest |
| **Location** | `tests/` mirroring `src/` structure |
| **Naming** | `test_<module>.py` |
| **Fixture** | Use `conftest.py` for shared fixtures |
| **Quality** | Tests must be readable and maintainable |
| **Speed** | Unit tests < 100ms each, integration < 2s each |
| **No network** | Tests must not depend on external services |

---

## 9. Documentation Policy

| Type | Location | Required For |
|------|----------|--------------|
| Architecture docs | `architecture/` | System changes |
| ADRs | `docs/adr/` | Architecture decisions |
| UI/UX docs | `docs/ui/` | UI changes |
| Specifications | `docs/spec/` | New protocols |
| Protocol docs | `.ascend/` | Governance changes |

Every document must have: version, purpose, scope, and change history.

---

## 10. ADR Policy

An ADR is required when:
- A new architectural decision is made
- A previous decision is reversed or modified
- A new external dependency is introduced
- A layer boundary changes

ADR format:
```markdown
# ADR-NNN — Title

## Status
Proposed | Approved | Superseded

## Context
Why is this decision needed?

## Decision
What was decided?

## Consequences
What does this mean for the project?
```

---

## 11. Runtime Modification Policy

- Runtime modifications require an ADR
- Runtime modifications must not violate Architectural Invariants (DOC-0009)
- All Runtime changes must maintain backward compatibility
- The v1 architecture is frozen — changes require TSC approval

---

## 12. Experience Layer Policy

- UI components must pass the four validation questions (ARCH-0011)
- No business logic in the frontend
- State management must use Zustand for client state, React Query for server state
- All UI components must follow the ASCEND Design System (UI-0001)
- **No Feature may import HTTP libraries directly** — all data access goes through an SDK Client
- **No Feature may import a Transport** — clients are the only interface to data
- **No Component may call `fetch` or `axios`** — SDK Clients are the sole data conduit

---

## 13. Implementation Gate Policy

Every implementation must follow the **Gate Cycle**:

```
Plan
  │
  ▼
Implement
  │
  ▼
Self Review
  │
  ▼
Run Tests
  │
  ▼
Run Doctor
  │
  ▼
Architecture Validation
  │
  ▼
Generate Gate Review Report
  │
  ▼
Receive Gate Approval
  │
  ▼
[Next Gate]
```

| Rule | Description |
|------|-------------|
| **Gate-R1** | É proibido iniciar o próximo Gate sem aprovação do Gate atual |
| **Gate-R2** | Cada Gate deve produzir um relatório de revisão em `ops/reviews/SPR-NNN_GATE-NN_REVIEW.md` |
| **Gate-R3** | O relatório deve conter: objetivo, arquivos criados, commits realizados, desvios do plano, riscos identificados, próximo Gate, checklist AEGS |
| **Gate-R4** | Architecture Review é obrigatória ao final de cada Gate |
| **Gate-R5** | Nenhum Gate pode introduzir Runtime, HTTP calls ou regras de negócio sem autorização explícita |

---

## 14. Security Rules

| Rule | Description |
|------|-------------|
| **No secrets in code** | API keys, tokens, passwords must use environment variables |
| **Input validation** | All user input must be validated |
| **SQL injection** | Use parameterized queries |
| **XSS prevention** | Escape all user content rendered in UI |
| **Least privilege** | Components must have minimum necessary permissions |
| **No eval** | `eval()` and `exec()` are forbidden |

---

## 14. Performance Rules

| Rule | Description |
|------|-------------|
| **N+1 prevention** | Avoid N+1 queries in all database access |
| **Lazy loading** | Import heavy modules only when needed |
| **Caching** | Cache frequent queries where appropriate |
| **No premature optimization** | Profile before optimizing |

---

## 15. Forbidden Practices

| Practice | Reason |
|----------|--------|
| `from x import *` | Namespace pollution |
| Mutable default arguments | Surprising behavior |
| Bare `except:` | Silences unexpected errors |
| `print()` in production code | Use logging instead |
| Global mutable state | Testing and reasoning difficulty |
| Circular imports | Module coupling |
| Magic numbers/strings | Maintainability |
| Deep inheritance (>3 levels) | Complexity |

---

## 16. Refactoring Policy

- Refactoring must not change external behavior
- Tests must pass before and after refactoring
- Large refactoring must be split into incremental commits
- Refactoring that touches multiple layers requires an ADR

---

## 17. Dependency Policy

| Category | Policy |
|----------|--------|
| **Core domain** | Zero external dependencies |
| **Application** | Zero external dependencies |
| **Infrastructure** | Minimal, justified dependencies |
| **Engine** | Zero external dependencies |
| **Runtime** | Minimal, justified dependencies |
| **CLI** | Standard library only |

---

## 18. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
