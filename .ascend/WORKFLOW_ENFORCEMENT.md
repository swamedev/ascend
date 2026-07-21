# WORKFLOW ENFORCEMENT — Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-008 |
| **Name** | Workflow Enforcement |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | DOC-0000, DOC-0003, DOC-0007, DOC-0009, AEGS-000 |
| **Enforced by** | `ascend doctor --workflow` |

---

> *"Ninguém pula etapas."*

---

## 1. Purpose

This document defines the **mandatory engineering workflow** for every contributor — human or AI — who modifies ASCEND.

It is not documentation. It is a **governance system**. It forces good practices instead of relying on developer memory.

---

## 2. Workflow States

Every task passes through exactly these states, in order:

```
┌─────────────────────────────────────────────────────────────┐
│                      WORKFLOW STATE MACHINE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PLANNING                                                     │
│      │                                                        │
│      ▼                                                        │
│  DOCUMENTATION                                                │
│      │                                                        │
│      ▼                                                        │
│  IMPLEMENTATION                                               │
│      │                                                        │
│      ▼                                                        │
│  LOCAL VALIDATION                                             │
│      │                                                        │
│      ▼                                                        │
│  REVIEW                                                       │
│      │                                                        │
│      ▼                                                        │
│  COMMIT                                                       │
│      │                                                        │
│      ▼                                                        │
│  PUSH                                                         │
│      │                                                        │
│      ▼                                                        │
│  SYNC                                                         │
│      │                                                        │
│      ▼                                                        │
│  NEXT TASK                                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

No state can be skipped. No state can be re-entered without completing the cycle.

---

## 3. Task Status

Every task has exactly one status at any time.

| Status | Meaning |
|--------|---------|
| `Planning` | Objective defined, impact assessed, RFC written (if needed) |
| `Documentation` | Architecture docs updated, specs written, ADR created |
| `Implementation` | Code being written |
| `Validation` | Tests pass, lint clean, build green, `doctor` green |
| `Review` | Code review requested and approved |
| `Committed` | Commit completed, message per COMMIT_PLAYBOOK |
| `Merged` | PR merged into target branch |
| `Closed` | Task complete, no further action needed |

Never "half-done". Never "almost ready".

---

## 4. Immutable Rules

### Rule 1 — No Implementation Without Clean State

Nenhuma implementação continua enquanto existir código sem commit.

```python
# ILLEGAL STATE
git status  # returns dirty → STOP
```

### Rule 2 — Clean Tree Before Next Feature

`git status` must return `working tree clean` before starting another feature.

```python
# REQUIRED BEFORE ANY NEW FEATURE
git status
# output: nothing to commit, working tree clean
```

### Rule 3 — Commit Size Limit

Never accumulate more than **10 files changed** OR **500 lines** without commit.

```python
# WARNING THRESHOLD
if files_changed > 10 or lines_changed > 500:
    COMMIT_REQUIRED()
```

### Rule 4 — AI Must Run `git status` Before Starting

Every AI agent must execute `git status` before beginning any task. If the working tree is dirty, the agent must refuse to start and invoke RECOVERY_PROTOCOL.md.

### Rule 5 — AI Must Run `git status` Before Finishing

Every AI agent must execute `git status` before declaring a task complete. If the working tree is dirty, the task is not complete.

### Rule 6 — No 200 Uncommitted Files

Under no circumstances may the working tree contain 200+ uncommitted files. This is a **Constitutional Violation** requiring immediate invocation of RECOVERY_PROTOCOL.md.

### Rule 7 — Small Commits Always

Every commit must be small, focused, and coherent:

- One commit = one logical change
- Never "wip", "fix", "changes", "update"
- Always validate before commit

---

## 5. Pre-Commit Gate

Before EVERY commit, the following must be executed in order:

```
1. git diff --stat           # Review file list
2. git diff                  # Review changes
3. pytest                    # All tests pass
4. npm run lint (if web)     # Lint clean
5. npm run build (if web)    # Build green
6. ascend doctor             # Architecture checks
7. git add <files>
8. git commit -m "..."
```

No commit may skip any step.

---

## 6. Enforcement

The `ascend doctor --workflow` command enforces these rules automatically:

| Check | Rule |
|-------|------|
| Working tree clean | Rules 1, 2, 6 |
| Files changed ≤ 10 | Rule 3 |
| Lines changed ≤ 500 | Rule 3 |
| Branch is correct | Convention |
| No merge conflicts | Convention |
| Tests pass | Pre-commit gate |
| Lint passes | Pre-commit gate |
| Build passes | Pre-commit gate |
| `ascend doctor` passes | Pre-commit gate |
| Docs up to date | Convention |
| ADR present (if arch change) | Convention |
| RFC present (if needed) | Convention |

---

## 7. Violation Protocol

If any rule is violated:

1. **Stop immediately**
2. Read RECOVERY_PROTOCOL.md
3. Recover the working tree
4. Resume from the correct state
5. Document the violation in the commit message

Repeated violations may result in loss of commit privileges.

---

## 8. Relationship to Other AEGS Documents

| Document | Role |
|----------|------|
| AEGS-000 START_HERE | Entry point, boot sequence |
| AEGS-007 AI_BOOT_SEQUENCE | AI-specific startup |
| AEGS-008 WORKFLOW_ENFORCEMENT | This document |
| COMMIT_PLAYBOOK | When and how to commit |
| RECOVERY_PROTOCOL | How to recover from dirty state |
| AI_CHECKLIST | Pre-coding checklist for AI agents |

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO HERMES II |
