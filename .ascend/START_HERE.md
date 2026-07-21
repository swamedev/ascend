# START HERE — ASCEND Engineering Governance System (AEGS)

| Field | Value |
|-------|-------|
| **ID** | AEGS-000 |
| **Name** | Developer Onboarding and Governance |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000, DOC-0003, DOC-0007, DOC-0009 |
| **Referenced by** | All AEGS protocol documents |

---

## 1. Purpose

This document is the **mandatory starting point** for anyone — human or AI — who intends to modify the ASCEND project.

If you have not read every required document listed below, you are **NOT authorized** to modify ASCEND.

---

## 2. ⚜️ ASCEND Developer Boot Flow

```
START HERE
    │
    ▼
DOC-0000 — North Star
    │
    ▼
DOC-0003 — First Principles
    │
    ▼
DOC-0009 — Architectural Invariants
    │
    ▼
docs/adr/ — Architecture Decision Records
    │
    ▼
.ascend/DEVELOPMENT_PROTOCOL.md
    │
    ▼
docs/COMMIT_PLAYBOOK.md
    │
    ▼
.ascend/WORKFLOW_ENFORCEMENT.md
    │
    ▼
.ascend/AI_DEVELOPMENT_PROTOCOL.md  (if AI)
.ascend/HUMAN_DEVELOPMENT_PROTOCOL.md  (if Human)
    │
    ▼
git status (must be clean)
    │
    ▼
ascend doctor --workflow (must pass)
    │
    ▼
Choose Issue / Feature
    │
    ▼
Implementation
    │
    ▼
Testing
    │
    ▼
Documentation
    │
    ▼
ascend doctor (green)
    │
    ▼
git diff --stat
    │
    ▼
git diff
    │
    ▼
pytest
    │
    ▼
npm run lint && npm run build (if web)
    │
    ▼
ascend doctor
    │
    ▼
Commit (per COMMIT_PLAYBOOK)
    │
    ▼
git status (must be clean)
    │
    ▼
Pull Request
    │
    ▼
Code Review (per CODE_REVIEW_PROTOCOL)
    │
    ▼
Merge
```

---

## 3. Mandatory Reading Order

Every developer **must** read these documents **before** writing any code:

| Order | Document | Why |
|-------|----------|-----|
| 1 | `foundation/DOC-0000_North_Star.md` | The mission of ASCEND |
| 2 | `foundation/DOC-0003_First_Principles.md` | The 7 immutable principles |
| 3 | `foundation/DOC-0007_Engineering_Philosophy.md` | How we engineer |
| 4 | `foundation/DOC-0009_Architectural_Invariants.md` | Rules that cannot be broken |
| 5 | `docs/adr/*` | Why past decisions were made |
| 6 | `.ascend/DEVELOPMENT_PROTOCOL.md` | How to develop |
| 7 | `docs/COMMIT_PLAYBOOK.md` | How to commit |
| 8 | `.ascend/AI_DEVELOPMENT_PROTOCOL.md` | AI-specific rules |
| 9 | `.ascend/HUMAN_DEVELOPMENT_PROTOCOL.md` | Human-specific rules |
| 10 | `.ascend/WORKFLOW_ENFORCEMENT.md` | Workflow rules and enforcement |
| 11 | `docs/COMMIT_PLAYBOOK.md` | Commit playbook and size rules |
| 12 | `docs/RECOVERY_PROTOCOL.md` | Recovery from dirty state |
| 13 | `docs/AI_CHECKLIST.md` | Pre-coding checklist for AI agents |
| 14 | `docs/rfc/RFC_TEMPLATE.md` | RFC process for all architecture changes |

---

## 4. Development Lifecycle

```
Planning → Issue → Branch → Implementation → Tests
    → Documentation → Doctor → Commit → PR → Review → Merge
```

Each phase has explicit gates. No phase can be skipped.

---

## 5. Golden Rules

| Rule | Statement |
|------|-----------|
| **GR-1** | Architecture before code |
| **GR-2** | Simplicity before sophistication |
| **GR-3** | Evidence before claims |
| **GR-4** | Tests before merge |
| **GR-5** | Documentation before release |
| **GR-6** | One commit, one purpose |

---

## 6. Project Philosophy

> *"Toda competência reivindicada deve ser uma competência comprovada."*

This applies not only to Builders but to the code itself. Every claim in a commit, PR, or document must be backed by evidence: tests, docs, or working code.

---

## 7. Engineering Principles

| Principle | Statement |
|-----------|-----------|
| **Engine First** | The Core Engine is agnostic to domain |
| **Content as Data** | Content is never code |
| **AI as Layer** | AI enhances, never sustains |
| **Evidence Driven** | Features must produce observable value |
| **Local First** | User data belongs to the user |
| **v1 Frozen** | v1 architecture requires TSC approval to change |
| **API Independence** | No interface knows the Runtime directly — only the Application Layer |
| **Runtime Frozen** | Runtime is frozen — no changes without TSC approval. All development happens *around* it, never inside it |
| **Platform SDK** | All platforms (Web, Desktop, Mobile, CLI) share the same SDK — the ASCEND Platform SDK |

---

## 8. Experience Layer Quality Gate

> *No UI implementation may begin without an approved wireframe and a corresponding architecture document.*

**Rule:**
- Every screen must be documented in `docs/ui/wireframes/WF-NNNN_*.md`
- Every screen must trace to an architecture document (ARCH-NNNN)
- Wireframes must be approved before implementation begins
- No "emergent screens" — if a screen doesn't exist in the wireframes, it cannot be built

This prevents scope creep and ensures every interface decision is intentional.

---

## 9. Builder First Principle

Every change must answer:

> *"Does this improve the Builder's learning experience?"*

If the answer is not a clear "yes", the change does not belong in ASCEND.

---

## 10. Clean Architecture Reminder

```
┌────────────────────────────────────────────────┐
│            Experience Layer (UI)                │
│                SDK / API / CLI                  │
├────────────────────────────────────────────────┤
│            Application Layer (Use Cases)        │
├────────────────────────────────────────────────┤
│            Domain Layer (Core Engine)           │
├────────────────────────────────────────────────┤
│            Infrastructure Layer (DB, FS, Net)  │
└────────────────────────────────────────────────┘
```

> **Runtime** wraps the Domain Layer — it orchestrates domain entities, manages state machines, and executes pipelines. From the outside, the Runtime is accessed through the Application Layer only.

**Rules:**
- Domain never imports Infrastructure
- Layers communicate inward only
- No interface knows the Runtime directly — only the Application Layer
- Repositories are contracts (Protocols), not implementations
- IA cannot alter business rules

---

## 11. Before Coding Checklist

- [ ] I have read the required documents
- [ ] I understand the feature/issue
- [ ] I have searched existing code for similar patterns
- [ ] I have identified which layer(s) will change
- [ ] I have checked for existing ADRs
- [ ] I have planned my implementation

---

## 12. After Coding Checklist

- [ ] Code compiles
- [ ] All tests pass
- [ ] New tests cover the change
- [ ] Documentation is updated
- [ ] ADR is created (if architecture changed)
- [ ] No debug code, TODOs, commented code, or dead code
- [ ] Commit message follows COMMIT_PROTOCOL
- [ ] `ascend doctor` is green

---

## 13. Definition of Done

A task is done only when:

- [ ] Code implements the feature/fix completely
- [ ] All tests pass (existing + new)
- [ ] Documentation reflects the change
- [ ] ADR recorded (if architecture changed)
- [ ] No technical debt introduced unnecessarily
- [ ] `ascend doctor` passes
- [ ] Commit follows AEGS commit rules
- [ ] PR has been reviewed and approved

---

## 14. Mandatory Commit Rule

Every commit **must** follow the format defined in `COMMIT_PROTOCOL.md`.

Forbidden messages: `update`, `changes`, `fix`, `teste`, `ajustes`, `novo`, `aaaa`, `commit`, `version`, `v2`, `misc`, or any non-descriptive variant.

---

## 15. Pull Request Rule

Every PR must:
- Reference the issue it resolves
- Describe the change and its impact
- List which documents were updated
- Pass all CI checks
- Receive at least one approval

---

## 16. AI Rule

AI agents must run the **AI Boot Sequence** (`AI_BOOT_SEQUENCE.md`) before every task.

AI agents must **never**:
- Break Clean Architecture
- Modify architectural invariants
- Remove tests or documentation
- Create unnecessary coupling
- Duplicate code
- Alter protocols without an ADR

---

## 17. Human Rule

Human developers must follow `HUMAN_DEVELOPMENT_PROTOCOL.md` for every contribution.

---

**If you have not read every required document, you are NOT authorized to modify ASCEND.**

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
