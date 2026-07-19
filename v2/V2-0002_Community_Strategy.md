# V2-0002 — Community Strategy

**Status:** Draft  
**Version:** 0.1  
**Date:** 2026-07-19  
**Author:** Founder

---

## 1. Community Model

ASCEND is an open competency ecosystem. Its community must reflect the same principles: open, evidence-based, meritocratic.

### Structure

```
                    ┌─────────────────┐
                    │  TSC (Technical  │
                    │  Steering Comm.) │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     Package Authors    Spec Reviewers    Tool Contributors
            │                │                │
            ▼                ▼                ▼
       Content             Quality         Platform
```

### Roles

| Role | Responsibility |
|------|---------------|
| TSC Member | Governance, spec approval, conflict resolution |
| Package Author | Creates and maintains ASCEND packages |
| Spec Reviewer | Reviews RFCs and specification changes |
| Contributor | Code, tests, documentation, tools |
| Community Member | Discussions, bug reports, ideas |

## 2. Communication Channels

| Channel | Purpose |
|---------|---------|
| GitHub Issues | Bug reports, feature requests, RFCs |
| GitHub Discussions | Q&A, ideas, community support |
| (Future) Discourse/Forum | Long-form discussions, package announcements |
| (Future) Monthly Sync | Video call for contributors |

## 3. Contribution Pathways

### For Package Authors
1. Read the APS specification (SPEC-0001)
2. Study a reference package (e.g., `linux-foundations`)
3. Create a package using `ascend package create`
4. Submit to community registry (when available)

### For Spec Contributors
1. Open an RFC issue using the RFC template
2. Discuss and iterate
3. Submit PR with spec changes
4. TSC reviews and votes

### For Code Contributors
1. Find a `good first issue` label
2. Read CONTRIBUTING.md
3. Submit PR with tests (must pass all 163 existing tests)
4. Maintain zero-dependency discipline

## 4. Community Health

- **Code of Conduct:** Standard contributor covenant
- **Inclusive language:** All documentation and specs use neutral terminology
- **Recognition:** Contributors listed in release notes
- **Governance disputes:** Escalated to TSC, final decision by Founder

## 5. Immediate Actions

1. Prepare GitHub repository for public access
2. Create issue/PR templates
3. Write CONTRIBUTING.md v2 (already exists — verify and update)
4. Define `good first issue` backlog
5. Recruit 3 initial spec reviewers from personal network
