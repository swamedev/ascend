# ASCEND Governance

**Version:** 1.0.0  
**Status:** Approved  

---

## Roles

### Chief Architect

The Chief Architect is the guardian of the architecture, specifications, and
Architecture Decision Records (ADRs). Responsibilities:

- Approve or reject RFCs
- Maintain architectural integrity
- Ensure alignment with First Principles
- Appoint and remove Technical Steering Committee members

### Chief Philosophy Officer (CPO)

The CPO is the guardian of the mission, First Principles, and invariants.
Responsibilities:

- Ensure all decisions align with the project's North Star
- Protect the project from scope creep
- Maintain the Manifesto and Identity Architecture
- Resolve philosophical disputes

### Technical Steering Committee (TSC)

The TSC is a group responsible for approving significant changes to
specifications and core components. Responsibilities:

- Vote on RFC approvals
- Review major architectural changes
- Mediate technical disputes
- Approve new maintainers

Current TSC members:

- Chief Architect (chair)
- 2-4 invited members from the community

---

## Decision-Making Process

### RFC Process

1. **Draft** — Author writes the RFC
2. **Review** — TSC reviews and provides feedback
3. **Vote** — TSC votes: Approve, Reject, or Request Changes
4. **Merge** — Approved RFCs are merged and become active

### ADR Process

Architecture Decision Records document significant decisions:

1. Create `adr/NNNN-title.md`
2. Describe context, decision, and consequences
3. Chief Architect approves

---

## Versioning

- Runtime: SemVer 2.0
- Specifications: MAJOR.MINOR per release cycle
- Packages: SemVer 2.0

---

## ASCEND Engineering Governance System (AEGS)

The **ASCEND Engineering Governance System (AEGS)** is the official governance framework for all development activity.

📍 **Location:** `.ascend/`

| Document | ID | Purpose |
|----------|----|---------|
| START_HERE | AEGS-000 | Mandatory onboarding and reading order |
| DEVELOPMENT_PROTOCOL | AEGS-001 | Development conventions and policies |
| COMMIT_PROTOCOL | AEGS-002 | Commit message format and rules |
| AI_DEVELOPMENT_PROTOCOL | AEGS-003 | Rules for AI agents |
| HUMAN_DEVELOPMENT_PROTOCOL | AEGS-004 | Workflow for human contributors |
| CODE_REVIEW_PROTOCOL | AEGS-005 | Code review checklist and scoring |
| RELEASE_PROTOCOL | AEGS-006 | Release lifecycle and process |
| AI_BOOT_SEQUENCE | AEGS-007 | AI startup sequence |

Every contributor must read AEGS-000 before making any change.

---

## License

All code and specifications are licensed under MIT unless otherwise noted.

---
## Phase 2 Doctrine: The Feature Freeze Rule

Conforme deliberação do Chief Architect e do Chief Product Officer na transição para a v1.0.0:

> **NENHUMA nova funcionalidade (IA, GUI, Plugins, Network) será adicionada ao núcleo do ASCEND até que um grupo inicial de 10 a 20 *Early Adopters* tenha completado o pacote de referência (`cyber-foundations`) e fornecido feedback estruturado.**

A prioridade absoluta da engenharia passa a ser:
1. Developer Experience (DX) e Onboarding.
2. Correção de bugs reportados por usuários reais.
3. Documentação orientada ao usuário final.
