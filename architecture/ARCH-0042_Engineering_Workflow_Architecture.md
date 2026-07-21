# ARCH-0042 — Engineering Workflow Architecture

| Field | Value |
|-------|-------|
| **ID** | ARCH-0042 |
| **Name** | Engineering Workflow Architecture |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0009, AEGS-008, AEGS-009, AEGS-010 |
| **Principle** | Every change must be traceable, validated, and committed in small logical units |

---

## 1. Purpose

This document defines the architecture of the **Engineering Workflow Enforcement** system — the governance layer that ensures all ASCEND development follows a disciplined, repeatable process.

This is not documentation about how to develop. This is the **blueprint** for the system that enforces how development happens.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  ENGINEERING WORKFLOW SYSTEM                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────┐    ┌──────────────────┐                 │
│  │  Workflow       │    │  Doctor Engine    │                 │
│  │  State Machine  │◄───│  (ascend doctor)  │                 │
│  └────────┬───────┘    └──────────────────┘                 │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────────────────────────────┐                 │
│  │  Enforcement Checks                      │                 │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ │                 │
│  │  │ git diff  │ │ pytest   │ │ npm lint │ │                 │
│  │  │ --stat    │ │ runner   │ │ & build  │ │                 │
│  │  └──────────┘ └──────────┘ └──────────┘ │                 │
│  └─────────────────────────────────────────┘                 │
│           │                                                    │
│           ▼                                                    │
│  ┌─────────────────────────────────────────┐                 │
│  │  Governance Documents                    │                 │
│  │  AEGS-008  │  COMMIT_PLAYBOOK  │  RECOV  │                 │
│  └─────────────────────────────────────────┘                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Workflow State Machine

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ PLANNING │────▶│DOCUMENTATION │────▶│IMPLEMENTATION│
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                                             ▼
┌──────────┐     ┌──────────┐     ┌──────────────┐
│  COMMIT  │◀────│  REVIEW  │◀────│    LOCAL      │
│          │     │          │     │  VALIDATION   │
└────┬─────┘     └──────────┘     └──────────────┘
     │
     ▼
┌──────────┐     ┌──────────┐     ┌──────────────┐
│   PUSH   │────▶│   SYNC   │────▶│  NEXT TASK   │
└──────────┘     └──────────┘     └──────────────┘

State Transition Rules:
- No state can be skipped
- No state can be re-entered without completing forward
- Each state has explicit exit criteria (gates)
```

### 3.1 State Gates

| State | Exit Criteria |
|-------|---------------|
| PLANNING | RFC created (if needed), objective defined |
| DOCUMENTATION | Architecture docs updated, ADR created (if needed) |
| IMPLEMENTATION | Code complete, follows Clean Architecture |
| LOCAL VALIDATION | `pytest` green, `lint` green, `build` green, `doctor` green |
| REVIEW | PR submitted, at least one approval |
| COMMIT | Message per COMMIT_PLAYBOOK, working tree clean |
| PUSH | All commits pushed, `git status` clean |
| SYNC | `git fetch`, `git merge` or `git rebase`, no conflicts |
| NEXT TASK | Previous task verified, ready for next cycle |

---

## 4. Doctor Command Architecture

### 4.1 Command Structure

```
ascend doctor           → Architecture health check (existing)
ascend doctor --workflow → Workflow enforcement check (new)
ascend doctor --release  → Release readiness check (new)
```

### 4.2 Doctor Modes

| Mode | Checks |
|------|--------|
| `doctor` (default) | I1–I16 invariants, project structure, runtime health, test health, package health, architecture layers |
| `doctor --workflow` | Working tree clean, files ≤ 10, lines ≤ 500, branch correct, no conflicts, tests pass, lint pass, build pass, docs up to date, ADR present, RFC present |
| `doctor --release` | Working tree clean, branch correct, no conflicts, tests green, build green, lint green, min coverage, docs synced, versions aligned (runtime, sdk, contracts, errors), CHANGELOG/manifesto updated |

### 4.3 Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | One or more checks failed |
| 2 | Warning threshold reached (non-blocking) |

---

## 5. Integration with Existing System

```
┌─────────────────────────────────────────────────────────────┐
│                    EXISTING ASCEND SYSTEM                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CLI Layer                                                    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ascend doctor          → doctor.py (existing)       │    │
│  │  ascend doctor --workflow → doctor.py (new mode)     │    │
│  │  ascend doctor --release  → doctor.py (new mode)     │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Governance Layer (NEW)                                       │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  AEGS-008  WORKFLOW_ENFORCEMENT                       │    │
│  │  AEGS-009  COMMIT_PLAYBOOK                            │    │
│  │  AEGS-010  RECOVERY_PROTOCOL                          │    │
│  │  AEGS-011  AI_CHECKLIST                               │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Foundation Layer (updated)                                  │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  I17 — Repository Integrity (new)                    │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. Enforcement Points

| Point | What Happens |
|-------|-------------|
| Before any AI task | AI reads AI_CHECKLIST.md, runs `git status` |
| Before any commit | Pre-commit gate executes (diff, tests, lint, build, doctor) |
| After any commit | Post-commit verification (`git status`, `git log`) |
| Before any push | `ascend doctor --workflow` must pass |
| Before any release | `ascend doctor --release` must pass |

---

## 7. Failure Modes

| Failure | Behavior |
|---------|----------|
| Working tree dirty | Block task start, suggest RECOVERY_PROTOCOL |
| Tests fail | Block commit, report what failed |
| Lint fails | Block commit, report violations |
| Build fails | Block commit, report build errors |
| Doctor fails | Block commit, report which checks failed |
| >10 files or >500 lines | Block commit, suggest splitting |

No failure can be bypassed. Every failure must be resolved before proceeding.

---

## 8. References

| Reference | Description |
|-----------|-------------|
| AEGS-008 | WORKFLOW_ENFORCEMENT — workflow state machine and rules |
| AEGS-009 | COMMIT_PLAYBOOK — when and how to commit |
| AEGS-010 | RECOVERY_PROTOCOL — recovering from dirty state |
| AEGS-011 | AI_CHECKLIST — pre-coding checklist for AI agents |
| DOC-0009 | Architectural Invariants — I17 Repository Integrity |
| ARCH-0009 | Runtime State Machine — existing state machine pattern |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO HERMES II |
