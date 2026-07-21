# RECOVERY PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-010 |
| **Name** | Recovery Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-008 WORKFLOW_ENFORCEMENT |

---

> *"Processos bons impedem erro humano."*

---

## 1. Purpose

If you encounter a dirty working tree — whether 10 files or 300 — this protocol tells you exactly how to recover.

**Do not guess. Do not improvise. Follow the protocol.**

---

## 2. Initial Assessment

Run this command first:

```
git status
```

Count the uncommitted changes:

| Category | Count |
|----------|-------|
| Modified (tracked) | `git diff --stat` → count files |
| Untracked (new) | `git status` → count untracked entries |

---

## 3. Recovery Scenarios

### Scenario A: ≤ 10 files, ≤ 500 lines

This is within normal limits. Commit directly per COMMIT_PLAYBOOK.

```
git diff --stat
git diff
python -m pytest tests\
git add <files>
git commit -m "<type>(<scope>): <description>"
```

### Scenario B: 11–50 files OR 501–2000 lines

Group changes into logical units. Commit each unit separately.

```
1. Identify logical groups (see Section 4)
2. For each group:
   a. git add <group-files>
   b. git diff --cached --stat    # Verify group is correct
   c. python -m pytest tests\ --selected   # Run relevant tests
   d. git commit -m "<msg>"
3. git status                      # Verify progress
4. Repeat until clean
```

### Scenario C: 51–200 files OR 2001–10000 lines

Use incremental commit strategy with `git add -p` for precision.

```
1. git status > ~/recovery_inventory.txt    # Save full inventory
2. Identify top-level logical domains
3. For each domain:
   a. git add <domain-files>
   b. git diff --cached --stat
   c. python -m pytest tests\
   d. git commit -m "<type>(<scope>): <description>"
4. git status                                # Track progress
5. Repeat until clean
```

### Scenario D: 200+ files (Constitutional Violation)

This triggers I17 — Repository Integrity violation. Full recovery required.

```
1.  git status > ~/recovery_inventory.txt   # Full inventory
2.  python -m pytest tests\                 # Baseline: are tests passing?
3.  Create recovery branch:
    git checkout -b recovery/v1.1
4.  For each domain (see Section 4):
    a. git add <domain-files>
    b. git diff --cached --stat
    c. python -m pytest tests\
    d. npm run lint (if web)
    e. git commit -m "<type>(<scope>): <description>"
5.  git checkout main
6.  git merge recovery/v1.1 --no-ff
7.  git branch -d recovery/v1.1
8.  git status                              # Must be clean
```

---

## 4. Logical Grouping Reference

When splitting a dirty working tree, use these domain groupings:

| Domain | Common files |
|--------|--------------|
| **Governance** | `.ascend/*.md`, `docs/COMMIT_PLAYBOOK.md`, `docs/RECOVERY_PROTOCOL.md`, `docs/AI_CHECKLIST.md` |
| **Architecture** | `architecture/ARCH-*.md` |
| **Foundation** | `foundation/DOC-*.md` |
| **Specs** | `docs/spec/*.md`, `docs/sdk/*` |
| **UI/UX** | `docs/ui/*.md`, `docs/ui/wireframes/*` |
| **Functional Docs** | `docs/features/*`, `docs/experience/*`, `docs/rfc/*` |
| **Ops** | `ops/*.md` |
| **Backend Source** | `src/ascend/adapter/*`, `src/ascend/api/*`, `src/ascend/application/*` |
| **Infrastructure** | `src/ascend/infrastructure/*` |
| **Cognitive** | `src/ascend/cognitive/*`, `tests/test_cognitive.py`, `tests/test_normalizer.py`, `tests/test_extractor.py` |
| **SDK** | `packages/sdk/*` |
| **Contracts** | `packages/contracts/*` |
| **Errors** | `packages/errors/*` |
| **Frontend** | `apps/web/src/app/*`, `apps/web/src/components/*`, `apps/web/src/store/*`, `apps/web/src/hooks/*` |
| **Config** | `.gitignore`, `pyproject.toml`, `apps/web/tailwind.config.ts` |

---

## 5. Git Commands Reference

| Situation | Command |
|-----------|---------|
| Discard unstaged changes in one file | `git restore <file>` |
| Discard all unstaged changes | `git restore .` |
| Unstage a file | `git restore --staged <file>` |
| Save dirty work temporarily | `git stash push -m "message"` |
| List stashes | `git stash list` |
| Restore latest stash | `git stash pop` |
| Restore specific stash | `git stash apply stash@{n}` |
| Delete stash | `git stash drop stash@{n}` |
| View changes not yet staged | `git diff` |
| View staged changes | `git diff --cached` |
| View summary of changes | `git diff --stat` |
| Interactive staging (per hunk) | `git add -p <file>` |
| Create recovery branch | `git checkout -b recovery/name` |
| Merge recovery branch | `git merge recovery/name --no-ff` |
| Remove untracked files (dry-run) | `git clean -n` |
| Remove untracked files | `git clean -fd` |
| Amend last commit (no push) | `git commit --amend` |
| Reset to last commit (keep changes) | `git reset --soft HEAD~1` |
| Reset to last commit (discard changes) | `git reset --hard HEAD~1` |
| View commit log | `git log --oneline -10` |
| View what commit changed | `git show --stat <commit-hash>` |
| Create worktree for parallel work | `git worktree add ../ascend-feature feature-branch` |

---

## 6. Validation After Recovery

After the working tree is clean:

```
1.  python -m pytest tests\          # All tests pass
2.  cd apps\web && npm run lint && npm run build && cd ..\..  # Web OK
3.  python -m ascend doctor           # Doctor green
4.  git status                        # working tree clean
```

---

## 7. Preventing Recurrence

To prevent future dirty-tree scenarios:

1. **Commit after every logical unit** (see COMMIT_PLAYBOOK Section 1)
2. **Run `git status` before and after every session** (Rule 4, Rule 5)
3. **Never exceed 10 files / 500 lines** (Rule 3)
4. **Run `ascend doctor --workflow` before every push**

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO HERMES II |
