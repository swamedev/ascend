# COMMIT PLAYBOOK — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-009 |
| **Name** | Commit Playbook |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-008 WORKFLOW_ENFORCEMENT |
| **Supersedes** | AEGS-002 COMMIT_PROTOCOL |

---

> *"Small commits. Always."*

---

## 1. When to Commit

A commit is required when any of these conditions are met:

| Condition | Example |
|-----------|---------|
| ✓ Finished an architecture document | `docs(architecture): add ARCH-0042` |
| ✓ Finished a component | `feat(cognitive): implement normalizer` |
| ✓ Finished an API endpoint | `feat(api): add builder progress endpoint` |
| ✓ Finished a test file | `test(cognitive): add normalizer tests` |
| ✓ Finished documentation | `docs(spec): update SDK lifecycle` |
| ✓ Finished a layer | `feat(cognitive): complete signal extractor` |
| ✓ Reached 10 files changed | `chore: checkpoint at 10 files` |
| ✓ Reached 500 lines changed | `chore: checkpoint at 500 lines` |
| ✓ Fixed a bug | `fix(api): handle null builder in progress` |
| ✓ Refactored code | `refactor(infra): extract connection pool` |
| ✓ Updated governance | `docs(governance): update workflow rules` |

**Never** say "vou terminar mais uma coisa..." before committing.

---

## 2. Commit Size Rules

| Metric | Limit | Action |
|--------|-------|--------|
| Files changed | ≤ 10 | Commit required at limit |
| Lines changed | ≤ 500 | Commit required at limit |
| Files changed | > 10 ∧ > 500 | **Blocked** — must split |

If both limits are exceeded, split into multiple logical commits before proceeding.

---

## 3. Pre-Commit Validation Gate

Before every commit, execute these steps **in order**:

```
STEP 1:  git diff --stat           # Review what files changed
STEP 2:  git diff                  # Review the actual changes
STEP 3:  python -m pytest tests\   # All tests must pass
STEP 4:  cd apps\web && npm run lint && cd ..\..  # Lint (if web changed)
STEP 5:  cd apps\web && npm run build && cd ..\.. # Build (if web changed)
STEP 6:  python -m ascend doctor   # Architecture checks
STEP 7:  git add <files>
STEP 8:  git commit -m "<message>"
```

No commit may skip any step. If any step fails, fix the issue and restart from STEP 3.

---

## 4. Commit Message Format

```
<type>(<scope>): <description>

[optional body]
```

### Types

| Type | When |
|------|------|
| `feat` | New feature or component |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `test` | Tests only |
| `refactor` | Code change with no behavior change |
| `chore` | Build, config, tooling |
| `style` | Formatting, linting |
| `perf` | Performance improvement |

### Scope Examples

| Scope | Applies to |
|-------|------------|
| `cognitive` | Cognitive layer |
| `api` | REST API |
| `sdk` | Platform SDK |
| `web` | Frontend web app |
| `infra` | Infrastructure |
| `domain` | Domain layer |
| `cli` | CLI |
| `contracts` | @ascend/contracts |
| `errors` | @ascend/errors |
| `architecture` | Architecture docs |
| `spec` | Specification docs |
| `ui` | UI/UX docs |
| `governance` | AEGS docs |
| `project` | Project config |

### Examples

```
feat(cognitive): add signal extraction rules
docs(governance): add workflow enforcement
fix(api): handle null builder in progress endpoint
test(cognitive): add extractor determinism tests
chore(project): update pyproject.toml metadata
```

### Forbidden Messages

| Forbidden | Reason |
|-----------|--------|
| `update` | Vague |
| `changes` | Vague |
| `fix` | No scope, no detail |
| `teste` | Portuguese, vague |
| `ajustes` | Portuguese, vague |
| `novo` | Portuguese, vague |
| `aaaa` | Placeholder |
| `commit` | Meaningless |
| `version` | Vague |
| `v2` | Vague |
| `misc` | Too broad |
| `wip` | Not a finished unit |

---

## 5. Post-Commit Checklist

- [ ] `git status` shows `working tree clean`
- [ ] `git log --oneline -1` shows the expected message
- [ ] Tests still pass (run `pytest` to confirm)

---

## 6. Commit Bundling

When multiple files form a single logical change, they should be committed together:

```
# Logical unit: "add signal extractor"
git add src/ascend/cognitive/extractor.py
git add src/ascend/cognitive/__init__.py
git add tests/test_extractor.py
git commit -m "feat(cognitive): add signal extractor with extraction rules"
```

Never bundle unrelated changes in the same commit.

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO HERMES II |
