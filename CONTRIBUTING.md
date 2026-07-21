# Contributing to ASCEND

Thank you for your interest in contributing to ASCEND.

**Before contributing, you MUST read:**
👉 [**START HERE — ASCEND Engineering Governance System (AEGS)**](.ascend/START_HERE.md)

The AEGS defines mandatory reading order, development protocols, commit rules, and code review standards. Compliance is required for all contributions. If you have not read every required document, you are NOT authorized to modify ASCEND.

This document provides guidelines for contributors.

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment.
All contributors must adhere to the [Contributor Covenant](https://www.contributor-covenant.org/).

---

## How to Contribute

### 0. Read the AEGS

Before any contribution:
1. Read `.ascend/START_HERE.md` — mandatory onboarding
2. Read the full **ASCEND Engineering Governance System (AEGS)** in `.ascend/`
3. Follow the commit protocol (AEGS-002) for all commits
4. Follow the code review protocol (AEGS-005) for all PRs

---

### 1. Report Issues

Open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)

### 2. Submit Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Submit a Pull Request

### 3. Write Specifications

Specifications follow the RFC process:

1. Draft a SPEC document under `docs/spec/`
2. Use the format: `SPEC-NNNN_Title_v1.md`
3. Submit for review by the Technical Steering Committee

### 4. Create Packages

Packages follow the APS format (see SPEC-0001).
Submit packages via the Registry (see SPEC-0003).

---

## Development Setup

```bash
git clone https://github.com/ascend/ascend-runtime
cd ascend-runtime
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e ".[dev]"
pytest
```

---

## Standards

- Python 3.11+
- Pure Python, no external dependencies for core layers
- Type hints required for all public APIs
- Tests required for all contributions
- Documentation required for new features

---

## Governance

See [GOVERNANCE.md](GOVERNANCE.md) for details on project governance.
