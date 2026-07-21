# CODE REVIEW PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-005 |
| **Name** | Code Review Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-000, AEGS-001, DOC-0009 |
| **Referenced by** | AEGS-004 |

---

## 1. Purpose

Define the mandatory code review checklist and scoring system for all ASCEND contributions.

---

## 2. Review Requirements

| Aspect | Requirement |
|--------|-------------|
| **Minimum reviewers** | 1 for patches, 2 for features, 3 for architecture changes |
| **Review scope** | Code, tests, documentation, commit message |
| **Blocking issues** | Must be resolved before merge |
| **Non-blocking** | Suggestions that improve but don't block |
| **Response time** | Within 48 hours (target) |

---

## 3. Review Checklist

Every review must answer these ten questions:

### Q1 — Architecture Respected?

```
□ Change follows Clean Architecture
□ Domain layer is independent
□ No layer-skipping dependencies
□ Architectural Invariants (DOC-0009) are preserved
```

**If no:** Block the PR.

### Q2 — Builder Benefits?

```
□ Change answers "Does this improve the Builder's experience?"
□ The feature produces observable value
□ No feature-creep or scope expansion
```

**If no:** Reject or request redesign.

### Q3 — Tests Added?

```
□ New tests cover the change
□ Edge cases are tested
□ All existing tests still pass
□ Tests are readable and maintainable
□ No test removal without justification
```

**If no:** Request tests before approval.

### Q4 — Documentation Updated?

```
□ README updated if applicable
□ ADR created if architecture changed
□ API docs updated if interface changed
□ UI docs updated if UI changed
□ Governance docs updated if protocol changed
```

**If no:** Request documentation before approval.

### Q5 — Performance Impacted?

```
□ No N+1 queries introduced
□ No unnecessary computation in hot paths
□ No memory leaks or unbounded growth
□ Performance regression < 5% (measured if critical)
```

**If yes (negative):** Block or request optimization.

### Q6 — Security Impacted?

```
□ No secrets exposed
□ Input validation in place
□ No injection vulnerabilities
□ No unsafe deserialization
□ Authentication/authorization considered
```

**If yes (negative):** Block immediately.

### Q7 — Breaking Changes?

```
□ Public API changed
□ Database schema changed
□ Configuration format changed
□ Behavior changed for existing users
```

**If yes:** Ensure migration guide exists.

### Q8 — Technical Debt?

```
□ Code is clean and idiomatic
□ No unnecessary complexity
□ No duplicate code
□ No dead code or commented code
□ Naming is clear and consistent
```

**If yes (significant):** Request refactoring.

### Q9 — Future Maintenance?

```
□ Code is readable by another engineer
□ Error messages are clear
□ Logging is appropriate
□ Configuration is externalized
□ Change is reversible if needed
```

**If no:** Request improvements.

### Q10 — Commit Message Compliant?

```
□ Follows AEGS-002 format
□ Type, scope, and description present
□ References issue number
□ No forbidden words
```

**If no:** Request correction.

---

## 4. Final Score

| Score | Meaning | Action |
|-------|---------|--------|
| **0-3** | Fails critical checks | Blocked, must be reworked |
| **4-6** | Minor issues found | Approved with changes requested |
| **7-9** | Good quality | Approved with suggestions |
| **10** | Excellent | Approved without reservation |

Any score below 7 requires re-review after changes.

---

## 5. Review Types

| Type | Description | Action |
|------|-------------|--------|
| **Approve** | Change is ready to merge | Merge when CI passes |
| **Request Changes** | Issues must be addressed | Re-review required |
| **Comment** | Suggestions, non-blocking | Author decides |

---

## 6. Speed of Review

| PR Size | Target Review Time |
|---------|-------------------|
| < 50 lines | 4 hours |
| 50-200 lines | 24 hours |
| 200-500 lines | 48 hours |
| > 500 lines | Consider splitting |

---

## 7. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
