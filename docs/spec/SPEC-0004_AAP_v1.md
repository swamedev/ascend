# SPEC-0004 — ASCEND Agent Protocol (AAP) v1.0

**Status:** Draft  
**Version:** 0.1.0  
**License:** MIT  

---

## 1. Abstract

AAP defines how an external agent (AI, human reviewer, automated system)
communicates with the ASCEND Runtime to perform assessments, submit evidence,
provide feedback, and propose competency updates.

---

## 2. Scope

This specification covers:

- Agent ↔ Runtime communication contract
- Assessment submission from agents
- Evidence submission from agents
- Feedback protocol
- Agent registration and discovery

It does NOT cover:

- Package format (see SPEC-0001 APS)
- Execution semantics (see SPEC-0002 AEP)
- Registry interactions (see SPEC-0003 ARP)

---

## 3. Agent Contract

### 3.1 Agent Protocol

```python
class Agent(Protocol):
    async def assess(
        self, evidence: str, rubric: Rubric, context: AgentContext
    ) -> AssessmentResult: ...

    async def provide_feedback(
        self, result: AssessmentResult, context: AgentContext
    ) -> Feedback: ...

    async def propose_competency(
        self, builder: Builder, context: AgentContext
    ) -> CompetencyProposal: ...
```

### 3.2 AgentContext

```python
@dataclass
class AgentContext:
    agent_id: str
    builder_id: str
    mission_id: str
    package_id: str
    runtime_version: str
    metadata: dict  # Extensible
```

---

## 4. Agent Types

| Type | Description | Sync/Async |
|---|---|---|
| `human` | Human reviewer via CLI or UI | Sync |
| `ai` | LLM-based assessment | Async |
| `auto` | Automated rule-based assessment | Sync |
| `hybrid` | Combination of multiple agents | Async |
| `peer` | Peer review from another builder | Sync |

---

## 5. Assessment Flow

```
Runtime
    │
    1. Submits evidence to Agent
    │
    2. Agent evaluates evidence against rubric
    │
    3. Agent returns AssessmentResult
    │
    4. Runtime applies result to CompetencyEngine
    │
    5. Runtime records agent_id in assessment metadata
```

### 5.1 Assessment Request

```python
@dataclass
class AssessmentRequest:
    evidence: str
    rubric: Rubric
    mission_id: str
    builder_id: str
    context: AgentContext
```

### 5.2 Assessment Response

```python
@dataclass
class AssessmentResponse:
    result: AssessmentResult
    confidence: float  # 0.0 to 1.0
    feedback: str | None
    agent_id: str
    duration_ms: int
```

---

## 6. Evidence Submission

Agents MAY submit evidence on behalf of a builder:

```python
async def submit_evidence(
    self, evidence: str, evidence_type: str, builder_id: str, context: AgentContext
) -> EvidenceReceipt: ...
```

This enables scenarios such as:

- AI generating evidence from a simulation
- Peer reviewers submitting evidence
- Automated test runners submitting results

---

## 7. Feedback Protocol

```python
@dataclass
class Feedback:
    mission_id: str
    criteria_scores: dict[str, int]
    comments: str
    suggestions: list[str]
    agent_id: str
    timestamp: datetime
```

Feedback MUST NOT modify builder state directly. The Runtime applies feedback.

---

## 8. Agent Registration

Agents register with the Runtime:

```python
runtime.register_agent("ai-reviewer", AIAssessmentAgent())
```

Registration is OPTIONAL. If no agent is registered for assessment,
the Runtime uses its built-in AssessmentPipeline.

---

## 9. Execution Strategy

The Agent Protocol enables multiple execution strategies:

| Strategy | Description |
|---|---|
| `LocalExecutionStrategy` | Built-in assessment, no external agent |
| `AIExecutionStrategy` | AI agent performs assessment |
| `TeamExecutionStrategy` | Multiple reviewers, consensus-based |
| `ClassroomExecutionStrategy` | Instructor reviews all submissions |
| `EnterpriseExecutionStrategy` | Compliance-driven assessment pipeline |

The Kernel remains unchanged; strategies are a layer above.

---

## 10. Security

- Agents MUST authenticate with the Runtime via tokens
- Agents MUST NOT access builder data outside their scope
- All assessment results MUST be signed by the agent
- The Runtime MAY reject assessments from untrusted agents
