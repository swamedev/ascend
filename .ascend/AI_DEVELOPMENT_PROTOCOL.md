# AI DEVELOPMENT PROTOCOL — ASCEND Engineering Governance System

| Field | Value |
|-------|-------|
| **ID** | AEGS-003 |
| **Name** | AI Development Protocol |
| **Version** | 1.0 |
| **Status** | Approved |
| **Category** | Governance |
| **Owner** | Chief Architect |
| **Derived from** | AEGS-000, AEGS-001, AEGS-002 |
| **Referenced by** | AI_BOOT_SEQUENCE |

---

## 1. Purpose

This is the **most important document for AI agents** working on ASCEND.

It defines how ChatGPT, DeepSeek, Claude, Gemini, Copilot, Cursor, Windsurf, and any future AI agent must behave when modifying the project.

---

## 2. Boot Sequence

Every AI agent **must** mentally execute this sequence before every task:

```
Read Constitution (DOC-0000, DOC-0003)
    │
    ▼
Read Architectural Invariants (DOC-0009)
    │
    ▼
Read relevant ADRs (docs/adr/)
    │
    ▼
Read Development Protocol (AEGS-001)
    │
    ▼
Read Commit Protocol (AEGS-002)
    │
    ▼
Understand the Feature
    │
    ▼
Search Existing Components
    │
    ▼
Plan
    │
    ▼
Implement
    │
    ▼
Self Review
    │
    ▼
Test
    │
    ▼
Run Doctor (ascend doctor)
    │
    ▼
Architecture Validation
    │
    ▼
Generate Gate Review Report
    │
    ▼
Commit (per AEGS-002)
    │
    ▼
[Wait for Gate Approval]
```

Skipping any step is a protocol violation.

---

## 3. Prohibited Actions

An AI agent is **strictly forbidden** from:

| Action | Rationale |
|--------|-----------|
| Breaking Clean Architecture | Domain must never depend on Infrastructure |
| Modifying Architectural Invariants | DOC-0009 rules are absolute |
| Removing existing tests | Tests are the safety net |
| Removing existing documentation | Documentation is a deliverable |
| Creating unnecessary coupling | Modularity is a first principle |
| Ignoring project policies | Protocols exist for a reason |
| Creating duplicate code | DRY is mandatory |
| Altering protocols without an ADR | Governance requires traceability |
| Modifying Runtime without justification | v1 architecture is frozen |

---

## 4. Mandatory Requirements

Every AI-generated contribution **must**:

### 4.1 Explain

Before any code, explain:

- **Objective** — What is the goal?
- **Impact** — What does this change affect?
- **Risks** — What could go wrong?
- **Compatibility** — Does it break anything?
- **Tests** — How is it tested?
- **Changed docs** — Which documents were updated?

### 4.2 Follow Patterns

- Search the existing codebase before writing new code
- Match the style of neighboring files
- Use existing protocols and types

### 4.3 Preserve

- All existing tests must remain passing
- All existing documentation must remain intact
- All ADRs must be respected

### 4.4 Validate

- Run the test suite before declaring completion
- Run `ascend doctor` before commit
- Verify the commit message format

---

## 5. AI-Specific Rules

| Rule | Description |
|------|-------------|
| **AI-R1** | Never generate code that bypasses human review |
| **AI-R2** | Never introduce new dependencies without justification |
| **AI-R3** | Never refactor code outside the scope of the task |
| **AI-R4** | Never remove a test to make a new test pass |
| **AI-R5** | Never create a file without checking if one already exists |
| **AI-R6** | Never assume conventions — verify them in existing files |
| **AI-R7** | Never commit on behalf of a human |

---

## 6. Self-Correction

If an AI agent detects it has violated a protocol:

1. **Stop immediately**
2. Revert the violating change
3. Re-run the Boot Sequence
4. Proceed correctly

---

## 7. Accountability

Every AI-generated contribution is the responsibility of the human who reviews and merges it. The AI is a tool. The human is accountable.

---

## 8. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 2.0 | 2026-07-20 | Chief Architect | Added §9 — Cognitive Component AEGS (OPERAÇÃO OLYMPUS) |
| 1.0 | 2026-07-20 | Chief Architect | Initial version |

---

## 9. Cognitive Component AEGS

Before creating **any** cognitive component, the following checklist **must** be verified:

- [ ] ARCH-0032 — Observation Event Taxonomy (verified)
- [ ] ARCH-0033 — Observation Pipeline (verified)
- [ ] ARCH-0034 — Behavioral Metrics (verified)
- [ ] ARCH-0035 — Observation Storage (verified)
- [ ] ARCH-0036 — Observation SDK (verified)
- [ ] ARCH-0037 — Privacy & Sovereign Cognitive Data (verified)
- [ ] ARCH-0038 — Cognitive Timeline (verified)
- [ ] COGNITIVE_FREEZE_v1.md (verified)
- [ ] DOC-0009 I14 — Cognitive Independence (not violated)
- [ ] DOC-0009 I15 — Observation Determinism (not violated)
- [ ] DOC-0010 — Cognitive Principles (not violated)

If any document is missing, implementation is **prohibited**.
