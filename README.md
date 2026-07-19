# ASCEND

Competency Development Framework (CDF)

---

## North Star

> Toda competência reivindicada deve ser uma competência comprovada.

---

## What is ASCEND?

ASCEND is a competency development framework that transforms learning into demonstrable, verifiable competence. It replaces superficial metrics (courses completed, hours watched, certificates earned) with **evidence-driven progression**.

The system doesn't model courses. It models:

```
Builder → Journey → Missions → Challenges → Evidence → Competencies
```

---

## Current Status

| Phase | Status |
|-------|--------|
| Foundation | ✅ Complete |
| System Architecture | ✅ Complete |
| Implementation Plan | ✅ Complete |
| Sprint 0 — Bootstrap | ✅ Complete |
| Sprint 1 — Core Domain | ✅ Complete |
| Sprint 2 — Persistence Layer | ⬜ Pending |

---

## Project Structure

```
ascend/
├── foundation/       # Canonical documents (DOC-0000 to DOC-0008)
├── architecture/     # System architecture (ARCH-0001 to ARCH-0006)
├── docs/             # Build plans, prompts, ADRs
├── src/ascend/       # Python implementation
│   ├── domain/       # Pure domain entities
│   ├── engine/       # Core engine
│   ├── database/     # Persistence layer
│   ├── agents/       # AI agent layer
│   └── cli/          # Command-line interface
├── packages/         # Learning packages
├── tests/            # pytest test suite
└── tools/            # Governance tooling
```

---

## Development

**Requirements:** Python 3.11+

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows
pip install -e ".[dev]"
```

**Run tests:**

```bash
python -m pytest
```

---

## License

MIT
