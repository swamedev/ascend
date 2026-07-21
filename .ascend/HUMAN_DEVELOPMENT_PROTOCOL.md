# HUMAN DEVELOPMENT PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-004 |
| **Name** | Human Development Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-000, AEGS-001, AEGS-002 |
| **Referenced by** | CODE_REVIEW_PROTOCOL |

---

## 1. Purpose

Define the complete development workflow for human contributors to the ASCEND project.

---

## 2. Full Workflow

```
Planning
    │
    ▼
Issue Creation
    │
    ▼
Branch Creation
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
Self-Review
    │
    ▼
Commit
    │
    ▼
Pull Request
    │
    ▼
Code Review
    │
    ▼
Approval
    │
    ▼
Merge
```

---

## 3. Phase Details

### 3.1 Planning

Before writing any code:
- Understand the problem completely
- Search for existing solutions or discussions
- Check ADRs for relevant decisions
- Determine which layers will change
- Estimate effort and identify risks

### 3.2 Issue Creation

Every change must be linked to an issue. The issue must contain:
- **Description** — What needs to change and why
- **Acceptance criteria** — How to verify the change
- **Dependencies** — What must happen first
- **Labels** — Type, priority, layer

### 3.3 Branch Creation

Use the branch naming convention from AEGS-001:
```
feat/short-description
fix/short-description
docs/short-description
refactor/short-description
test/short-description
```

### 3.4 Implementation

- Follow AEGS-001 conventions
- Write tests alongside code (TDD preferred)
- Keep changes focused on the issue scope
- Do not introduce unrelated changes

### 3.5 Testing

- All existing tests must pass
- New tests must cover the change
- Run the full test suite before commit
- Test edge cases, not just the happy path

### 3.6 Documentation

- Update existing documentation that the change affects
- Create new documentation for new features
- Update ADR if the architecture changed

### 3.7 Self-Review

Before committing, verify the After Coding Checklist from AEGS-000:
- [ ] Code compiles
- [ ] All tests pass
- [ ] New tests cover the change
- [ ] Documentation updated
- [ ] ADR created if needed
- [ ] No debug code, TODOs, commented code, or dead code
- [ ] Commit message follows AEGS-002

### 3.8 Commit

Follow AEGS-002 (COMMIT_PROTOCOL) exactly.

### 3.9 Pull Request

- Title follows commit message format
- Description explains what, why, and impact
- References the issue
- Lists changed documents
- Requests specific reviewers

### 3.10 Code Review

See AEGS-005 (CODE_REVIEW_PROTOCOL) for the review checklist.

### 3.11 Merge

- Squash commits if appropriate
- Use merge commit for feature branches
- Delete the branch after merge

---

## 4. Responsibilities

| Role | Responsibility |
|------|----------------|
| **Author** | Produce correct, tested, documented code |
| **Reviewer** | Verify correctness, completeness, and compliance |
| **Committer** | Ensure clean commit history |
| **Mergers** | Verify CI passes before merging |

---

## 5. Communication

- Use issues for feature requests and bug reports
- Use PR comments for code discussion
- Use ADRs for architectural decisions
- Use GitHub Discussions for open-ended topics

---

## 6. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
