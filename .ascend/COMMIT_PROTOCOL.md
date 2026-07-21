# COMMIT PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-002 |
| **Name** | Commit Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-000 |
| **Referenced by** | AEGS-003, AEGS-004 |

---

## 1. Purpose

Define the mandatory commit policy for all ASCEND contributions. One change = one commit = one purpose.

---

## 2. Commit Philosophy

> *A commit is a logical unit of work. It tells a story. It is not a save point.*

**Rules:**
- One commit = one atomic change
- A commit must compile and pass tests independently
- A commit message must explain *what* and *why*, not *how*

---

## 3. Commit Template

```
<type>(<scope>): <brief description>

<body> (optional — explain why, not what)

<footer> (optional — references, breaking changes)
```

---

## 4. Types

| Type | Usage | Example |
|------|-------|---------|
| `feat` | New feature | `feat(ui): add dashboard shell` |
| `fix` | Bug fix | `fix(runtime): enforce mission state transition` |
| `refactor` | Code change with no behavior change | `refactor(api): extract runtime service` |
| `test` | Adding or modifying tests | `test(runtime): add state engine tests` |
| `docs` | Documentation only | `docs(ui): add wireframe specification` |
| `perf` | Performance improvement | `perf(infra): optimize evidence query` |
| `style` | Formatting, linting only | `style(domain): fix type hints` |
| `chore` | Build, CI, tooling | `chore(ci): update pytest config` |
| `revert` | Revert a previous commit | `revert(ui): undo dashboard shell` |

---

## 5. Scopes

| Scope | Area |
|-------|------|
| `domain` | Core domain entities, events |
| `application` | Use cases, services |
| `infra` | Infrastructure, repositories |
| `engine` | Core engine components |
| `runtime` | Runtime kernel |
| `api` | API layer |
| `cli` | CLI interface |
| `ui` | Frontend |
| `sdk` | SDK packages |
| `policy` | Governance, protocols |
| `docs` | Documentation |
| `test` | Tests |

---

## 6. Examples

```
feat(ui): add dashboard shell with continue mission card

Implement the main dashboard layout with sidebar, header,
and the continue mission component. Includes loading,
empty, and error states.

Closes #142
```

```
fix(runtime): enforce competency validation before level up

Competency engine was allowing level-up without checking
whether all prerequisite skills were validated. This fix
adds the missing validation step in the progress pipeline.

Fixes #89
```

```
refactor(api): extract runtime service from CLI module

CLI was directly instantiating Runtime, creating coupling.
Extracted RuntimeService use case to mediate between
CLI and Runtime kernel.

No behavior change.
```

```
docs(ui): add mission workspace wireframe specification

Complete wireframe for WF-0003 including Focus Mode,
four-panel layout, and all states.
```

```
test(runtime): add state engine transition tests

Cover all 12 transitions of the mission state machine.
Includes edge cases for invalid transitions.
```

---

## 7. Forbidden Commits

These commit messages are **strictly forbidden**:

| Forbidden | Reason |
|-----------|--------|
| `update` | Does not describe what or why |
| `changes` | Does not describe what or why |
| `fix` | Too vague, no scope |
| `teste` | Non-English, no scope |
| `ajustes` | Non-English, no scope |
| `novo` | Non-English, no scope |
| `aaaa` | Meaningless |
| `commit` | Meaningless |
| `version` | Does not describe what or why |
| `v2` | Does not describe what or why |
| `misc` | Does not describe what or why |
| `wip` | Work in progress does not belong in main branch |
| `.` | Single character is meaningless |

Any commit with a forbidden message will be rejected.

---

## 8. Pre-Commit Checklist

Before every commit, verify:

- [ ] Code compiles without errors
- [ ] All tests pass (`pytest`)
- [ ] `ascend doctor` reports green
- [ ] Documentation is updated (if applicable)
- [ ] ADR is created or updated (if architecture changed)
- [ ] No debug code (`print()`, `breakpoint()`, `console.log()`)
- [ ] No `TODO`, `FIXME`, `HACK`, `XXX` comments
- [ ] No commented-out code blocks
- [ ] No dead code (unused imports, functions, variables)
- [ ] Commit message follows AEGS-002 format

---

## 9. Tag Policy

| Tag | Frequency | Example |
|-----|-----------|---------|
| `v<major>.<minor>.<patch>` | Per release | `v0.1.0` |
| `v<major>.<minor>.<patch>-alpha.<N>` | Alpha | `v1.0.0-alpha.1` |
| `v<major>.<minor>.<patch>-beta.<N>` | Beta | `v1.0.0-beta.1` |
| `v<major>.<minor>.<patch>-rc.<N>` | Release Candidate | `v1.0.0-rc.1` |

---

## 10. Versioning

ASCEND follows **Semantic Versioning 2.0**:

| Increment | When |
|-----------|------|
| **MAJOR** | Breaking API change |
| **MINOR** | New feature, backward compatible |
| **PATCH** | Bug fix, backward compatible |

---

## 11. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
