# PROTO-0004 — ASCEND Execution Protocol (AEP)

**Status:** Draft  
**Version:** 0.1.0  
**Scope:** Runtime Kernel

---

## 1. Purpose

AEP defines the contract between any executable content and the ASCEND Runtime Kernel.
APS describes *what* to learn; AEP describes *how* to execute it.

---

## 2. Core Contract

Any executable MUST implement the `RuntimeExecutable` protocol:

```python
class RuntimeExecutable(Protocol):
    def accept(self, visitor: RuntimeVisitor) -> None: ...
```

The Runtime communicates with executables exclusively through this protocol.
No YAML, no file I/O, no infrastructure leaks into the Kernel.

---

## 3. Execution Lifecycle

```
Package → Journey → Mission → Challenge
  → Evidence → Assessment → Competency → Achievement
```

Each stage is defined in AEP as:

| Stage | Input | Output |
|---|---|---|
| Package | RuntimePackage | Ready |
| Journey | RuntimeJourney | JourneyResult |
| Mission | RuntimeMission | MissionResult |
| Challenge | RuntimeChallenge | ChallengeOpened |
| Evidence | str | EvidenceSubmitted |
| Assessment | Evidence + Rubric | AssessmentResult |
| Competency | AssessmentResult | CompetencyUpdate |
| Achievement | CompetencyUpdate | AchievementEarned |

---

## 4. Runtime Models

The Kernel works exclusively with these models (defined in `runtime/models.py`):

- `RuntimePackage`
- `RuntimeJourney`
- `RuntimeMission`
- `RuntimeChallenge`
- `RuntimeCompetency`
- `RuntimeRubric`
- `RuntimeAchievement`

---

## 5. Extension Points

| Hook | Trigger |
|---|---|
| `before_journey` | Before journey starts |
| `after_journey` | After journey completes |
| `before_mission` | Before mission starts |
| `after_mission` | After mission completes |
| `before_assessment` | Before assessment runs |
| `after_assessment` | After assessment completes |

---

## 6. Future Implementations

Any content format implementing `RuntimeExecutable` can run on the Kernel:

- APS Packages (current)
- Corporate Packages
- University Packages
- AI-Generated Journeys
- Simulation Packages

---

## 7. Synchronous Guarantee

The Kernel is strictly synchronous. Async execution MUST be added by
infrastructure layers above the Kernel, never inside it.
