# ⚜️ APOLLO FREEZE v1.0

| Field | Value |
|-------|-------|
| **ID** | APOLLO-FREEZE-001 |
| **Name** | Apollo Freeze v1.0 — Unified Domain Language |
| **Date** | 2026-07-20 |
| **Author** | Chief Architect |
| **Status** | **LOCKED** |

## 1. Declaration

Starting from this date, the canonical domain language of ASCEND is frozen. No breaking changes to the contracts, errors, events, identity model, or resource model may be made without an approved RFC.

## 2. What is Frozen

- **@ascend/contracts** — all canonical types (Builder, Journey, Mission, Evidence, Assessment, Competency, Achievement, events, pagination, API envelope, export)
- **@ascend/errors** — all error classes and envelope (AscendError, ValidationError, NetworkError, AuthenticationError, ConflictError, OfflineError, PolicyError, DomainError, RuntimeError, UIError)
- **Domain Event Catalog** — ARCH-0026 (all event types, envelopes, payloads, guarantees, rules E1–E10)
- **Builder Identity Model** — ARCH-0027 (Builder, Profile, Preferences, LearningIdentity, AchievementLedger, BuilderProgress, data sovereignty, privacy zones, offline identity, recovery, ownership)
- **API Resource Model** — ARCH-0028 (all 9 resources, lifecycle, state machines, endpoints, response/error envelopes, pagination, rules R1–R9)
- **Dependency Graph** — ARCH-0029 (all packages, allowed/forbidden/circular dependencies, 4 Mermaid diagrams)
- **Canonical Mapping** — CANONICAL_MAPPING.md (12-concept matrix: Runtime ↔ Contracts ↔ SDK ↔ React)
- **Architectural Invariants I1–I13** — DOC-0009

## 3. What is NOT Frozen

Things that can still change freely:
- Implementation details
- UI components
- Tests
- Documentation
- SDK internals (as long as public API matches contracts)
- Runtime implementation

## 4. The RFC Process

For breaking changes:
1. Write RFC document
2. Submit to Chief Architect
3. TSC review
4. Vote
5. If approved, update freeze document

## 5. Signatories

| Name | Role | Date | Signature |
|------|------|------|-----------|
|      |      |      |           |
|      |      |      |           |
|      |      |      |           |

## 6. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial freeze declaration — OPERAÇÃO APOLLO II complete |
