# AI CHECKLIST — Mandatory Pre-Coding Checklist for AI Agents

| Field | Value |
|-------|-------|
| **ID** | AEGS-011 |
| **Name** | AI Checklist |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |

---

> **Toda IA começa lendo este documento.**

---

## 1. Pre-Coding Checklist

Every AI agent must complete this checklist **before writing any code**:

```
□ 1. Read START_HERE (.ascend/START_HERE.md)
□ 2. Read WORKFLOW_ENFORCEMENT (.ascend/WORKFLOW_ENFORCEMENT.md)
□ 3. Read AI_BOOT_SEQUENCE (.ascend/AI_BOOT_SEQUENCE.md)
□ 4. Execute: git status (must be clean)
□ 5. Confirm: Working on the correct branch
□ 6. Confirm: All existing tests pass (python -m pytest tests\)
□ 7. Confirm: Architecture is frozen (if applicable)
□ 8. Confirm: RFC exists for this change (if needed)
□ 9. Confirm: Feature is isolated (one feature per commit)
□ 10. Read COMMIT_PLAYBOOK (docs/COMMIT_PLAYBOOK.md)
□ 11. Read RECOVERY_PROTOCOL (docs/RECOVERY_PROTOCOL.md)
```

**Without completing this checklist, the AI is NOT authorized to modify ASCEND.**

---

## 2. Pre-Commit Checklist

Before every commit:

```
□ 1. git diff --stat          # Review changed files
□ 2. git diff                 # Review changes in detail
□ 3. python -m pytest tests\  # All tests pass
□ 4. cd apps\web && npm run lint && cd ..\..   # Lint clean (if web)
□ 5. cd apps\web && npm run build && cd ..\..  # Build green (if web)
□ 6. python -m ascend doctor  # Architecture checks
□ 7. git add <files>
□ 8. git commit -m "<message>" # Per COMMIT_PLAYBOOK format
```

---

## 3. Post-Task Checklist

After every task:

```
□ 1. python -m pytest tests\          # All tests still pass
□ 2. python -m ascend doctor           # Doctor green
□ 3. git status                        # Working tree clean
□ 4. git push origin <branch>          # If feature branch complete
```

---

## 4. Constitutional Rules (Never Break)

| Rule | Statement |
|------|-----------|
| **CR-1** | You NEVER start coding if `git status` is dirty |
| **CR-2** | You NEVER finish coding without a commit |
| **CR-3** | You NEVER leave the repository dirty |
| **CR-4** | You NEVER commit without running tests first |
| **CR-5** | You NEVER exceed 10 files or 500 lines per commit |
| **CR-6** | You NEVER create a commit with a forbidden message |

---

## 5. Self-Correction

If you detect a violation of any rule in this document:

1. **Stop immediately**
2. Read RECOVERY_PROTOCOL.md
3. Recover the working tree
4. Re-run the Pre-Coding Checklist
5. Proceed correctly

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-21 | Chief Architect | Initial version — OPERAÇÃO HERMES II |
