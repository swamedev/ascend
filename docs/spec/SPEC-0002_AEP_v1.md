# SPEC-0002 — ASCEND Execution Protocol (AEP) v1.0

**Status:** Stable  
**Version:** 1.0.0  
**License:** MIT  

---

## 1. Abstract

AEP defines the contract between any executable content and the ASCEND Runtime Kernel.
While APS describes *what* to learn, AEP describes *how* to execute it.
Any content format implementing the AEP contract can run on the Runtime.

---

## 2. Scope

This specification covers:

- Execution lifecycle
- RuntimeExecutable protocol
- Runtime Models
- RuntimeContext
- ExecutionReport
- Hooks
- State Machine
- Error handling

It does NOT cover:

- Package format (see SPEC-0001 APS)
- Registry interactions (see SPEC-0003 ARP)
- Agent interactions (see SPEC-0004 AAP)

---

## 3. Core Contract

### 3.1 RuntimeExecutable Protocol

Any executable content MUST implement this protocol:

```python
class RuntimeExecutable(Protocol):
    def accept(self, visitor: RuntimeVisitor) -> None: ...
```

The Runtime communicates with executables exclusively through this protocol.
No YAML, file I/O, or infrastructure leaks into the Kernel.

### 3.2 RuntimeVisitor Protocol

```python
class RuntimeVisitor(Protocol):
    def visit_package(self, pkg: RuntimePackage): ...
    def visit_journey(self, journey: RuntimeJourney): ...
    def visit_mission(self, mission: RuntimeMission): ...
    def visit_challenge(self, challenge: RuntimeChallenge): ...
```

---

## 4. Execution Lifecycle

Every execution follows this deterministic pipeline:

```
Package
    ↓
Journey
    ↓
Mission
    ↓
Challenge
    ↓
Evidence
    ↓
Assessment
    ↓
Competency Update
    ↓
Achievement Check
    ↓
Progress Update
    ↓
Events
```

### 4.1 Stage Definitions

| Stage | Input | Output | Side Effects |
|---|---|---|---|
| Load | Path | RuntimePackage | None |
| Journey | RuntimeJourney | JourneyResult | Hooks, Events |
| Mission | RuntimeMission | MissionResult | Hooks, Events |
| Challenge | RuntimeChallenge | description | None |
| Evidence | str | submitted | Events |
| Assessment | Evidence + Rubric | AssessmentResult | Hooks, Events |
| Competency | AssessmentResult | CompetencyUpdate | Events |
| Achievement | CompetencyUpdate | AchievementEarned | Events |

---

## 5. Runtime Models

The Kernel works exclusively with these models (defined in `runtime/models.py`):

| Model | Description |
|---|---|
| `RuntimePackage` | Loaded package with all content |
| `RuntimeJourney` | A journey containing missions |
| `RuntimeMission` | A mission with challenge and assessment config |
| `RuntimeChallenge` | The challenge to be completed |
| `RuntimeCompetency` | Competency definition from package |
| `RuntimeRubric` | Assessment rubric with weighted criteria |
| `RuntimeAchievement` | Achievement definition from package |

---

## 6. RuntimeContext

The RuntimeContext carries all execution state and dependencies:

```python
@dataclass
class RuntimeContext:
    builder: Builder              # Current user/builder
    package: RuntimePackage       # Current package
    clock: Clock                  # Time provider
    event_collector: DomainEventCollector  # Event collector (not publisher)
    hooks: RuntimeHooks           # Extension hooks
    evidence_input: dict[str, str]  # Pre-provided evidence per mission
```

The RuntimeContext MUST be the ONLY way components access shared state.
No globals, no singletons, no implicit dependencies.

---

## 7. ExecutionReport

Every `run()` call returns an `ExecutionReport`:

```python
@dataclass
class ExecutionReport:
    success: bool
    package_id: str
    builder_username: str
    duration: float
    journeys_completed: int
    missions_completed: int
    total_xp: int
    competencies_unlocked: list[str]
    achievements_earned: list[str]
    journey_results: list[JourneyResult]
    warnings: list[str]
    errors: list[str]
```

### 7.1 Nested Results

```python
@dataclass
class JourneyResult:
    journey_id: str
    started: bool
    completed: bool
    mission_results: list[MissionResult]

@dataclass
class MissionResult:
    mission_id: str
    started: bool
    completed: bool
    evidence_submitted: bool
    assessment_result: AssessmentResult | None
    competency_updates: list[CompetencyUpdate]

@dataclass
class AssessmentResult:
    mission_id: str
    rubric_id: str
    scores: dict[str, int]
    total_score: int
    max_score: int
    percentage: float
    passed: bool
    evidence_text: str

@dataclass
class CompetencyUpdate:
    competency_id: str
    unlocked: bool
    xp_gained: int
    previous_xp: int
    new_xp: int
    previous_level: int
    new_level: int
    achievements_unlocked: list[str]
```

---

## 8. Hooks

The Runtime provides extension points via hooks:

| Hook | Trigger | Purpose |
|---|---|---|
| `before_journey` | Before journey execution | Setup, logging, metrics |
| `after_journey` | After journey execution | Cleanup, reporting |
| `before_mission` | Before mission execution | Validation, pre-checks |
| `after_mission` | After mission execution | Post-processing |
| `before_assessment` | Before assessment runs | Pre-evaluation setup |
| `after_assessment` | After assessment completes | Post-evaluation logging |

Hooks MUST be synchronous and MUST NOT throw exceptions.
If a hook fails, the Runtime SHOULD log the error and continue.

---

## 9. State Machine

Every mission follows this state machine:

```
AVAILABLE
    │
    ▼
STARTED
    │
    ▼
IN_PROGRESS
    │
    ▼
EVIDENCE_SUBMITTED
    │
    ▼
UNDER_REVIEW
    │
    ▼
COMPLETED
```

### 9.1 Valid Transitions

| From | To | Condition |
|---|---|---|
| AVAILABLE | STARTED | Prerequisites met |
| STARTED | IN_PROGRESS | Challenge opened |
| IN_PROGRESS | EVIDENCE_SUBMITTED | Evidence collected |
| EVIDENCE_SUBMITTED | UNDER_REVIEW | Assessment started |
| UNDER_REVIEW | COMPLETED | Assessment passed |

Invalid transitions MUST raise a clear error.

---

## 10. Error Handling

The Runtime MUST NOT throw exceptions for control flow.
All execution errors MUST be captured in `ExecutionReport.errors`.

```python
report = runtime.run(...)
if not report.success:
    for error in report.errors:
        log(error)
```

---

## 11. Synchronous Guarantee

The Kernel is strictly synchronous. Async execution MUST be added by
infrastructure layers above the Kernel, never inside it.

---

## 12. Implementation

The reference implementation is `ascend.runtime.kernel.RuntimeKernel`.
Any compliant implementation MUST pass the AEP test suite (`tests/test_runtime.py`).
