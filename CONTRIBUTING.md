# Contributing to ASCEND

## Philosophy

Before contributing, read:

1. `CONTEXT.md` — project identity and current state
2. `foundation/DOC-0003_First_Principles.md` — the 7 laws of the ecosystem
3. `docs/build/BUILD-0001_Implementation_Roadmap.md` — execution plan

## Workflow

```
Read
    ↓
Understand
    ↓
Question
    ↓
Propose
    ↓
Implement
```

Never: `Code → Explain later`

## Commit Messages

```
type(scope): description
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## Code Standards

- Python 3.12+
- Type hints required
- Tests required for all new code
- No infrastructure imports in domain layer
