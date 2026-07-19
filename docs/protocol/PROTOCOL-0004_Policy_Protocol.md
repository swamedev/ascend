# PROTOCOL-0004 — Policy Protocol

| Campo | Valor |
|-------|-------|
| **ID** | PROTOCOL-0004 |
| **Nome** | Policy Protocol |
| **Versão** | 1.0 |
| **Status** | Stable |
| **Categoria** | Protocol |
| **Owner** | Chief Architect |
| **Derivado de** | Constituição, ARCH-0010, PROTOCOL-0001, PROTOCOL-0003 |
| **Linguagem** | Independente |

---

## 1. Propósito

Este protocolo formaliza o **sistema de políticas de autorização** do ASCEND.

Ele define:
- O que é uma Policy
- O que é um PolicyDecision
- O que é uma PolicyEvaluation
- O que é um PolicyContext
- O que é uma PolicyViolation
- A interface conceitual
- O fluxo de decisão
- A resolução de conflitos

---

## 2. Definições

### 2.1 Policy

Uma **Policy** é uma função pura que responde a uma pergunta de autorização.

```
Policy: (Context) → PolicyDecision
```

Características:
- **Pura**: mesmo input → mesmo output
- **Stateless**: não mantém estado entre chamadas
- **Específica**: uma policy responde a uma única pergunta
- **Componível**: policies podem ser compostas para decisões complexas
- **Rastreável**: toda decisão produz um trace

### 2.2 PolicyDecision

```python
@dataclass
class PolicyDecision:
    result: PolicyResult       # ALLOW | DENY
    reason: str                # Explicação legível
    failed_invariant: str | None  # Invariante violado (se DENY)
    severity: PolicySeverity   # CRITICAL | HIGH | MEDIUM | LOW | INFO
    trace_id: str              # Correlação com a execução
    policy_name: str           # Nome da policy que decidiu
    evaluated_at: datetime     # Timestamp da decisão
    context_snapshot: dict     # Estado relevante no momento da decisão
```

### PolicyResult

| Resultado | Significado |
|-----------|-------------|
| **ALLOW** | A ação é permitida |
| **DENY** | A ação é proibida |

### PolicySeverity

| Severidade | Quando usar | Impacto |
|------------|-------------|---------|
| CRITICAL | Violação de invariante arquitetural (I1–I10) | Bloqueia execução |
| HIGH | Violação de invariante de ciclo de vida (CL1–CL7) | Bloqueia transição |
| MEDIUM | Violação de regra de negócio não-invariante | Bloqueia ação |
| LOW | Violação de recomendação ou warning | Permite com aviso |
| INFO | Decisão informacional, sem bloqueio | Log apenas |

### 2.3 PolicyEvaluation

Uma **PolicyEvaluation** é o processo de avaliar uma policy contra um contexto.

```json
{
    "evaluation_id": "eval:x1y2z3",
    "policy_name": "can_start_mission",
    "context": {
        "builder_id": "builder:alex",
        "mission_id": "mission:linux-001",
        "mission_status": "AVAILABLE",
        "prerequisites": ["mission:linux-000"],
        "completed_missions": ["mission:linux-000"]
    },
    "decision": {
        "result": "ALLOW",
        "reason": "Pré-requisitos cumpridos",
        "failed_invariant": null,
        "severity": "INFO",
        "trace_id": "pol:a1b2c3d4",
        "policy_name": "can_start_mission",
        "evaluated_at": "2026-07-19T10:30:00Z",
        "context_snapshot": { ... }
    },
    "duration_ms": 2
}
```

### 2.4 PolicyContext

O **PolicyContext** é o conjunto de informações necessárias para avaliar uma policy.

```json
{
    "builder": { "id": "builder:alex", "level": 3, "xp": 1250 },
    "mission": { "id": "mission:linux-001", "status": "AVAILABLE", "prerequisites": ["mission:linux-000"] },
    "evidence": { "id": "ev:a1b2c3", "text": "...", "type": "code" },
    "runtime": { "current_state": "EXECUTING", "trace_id": "trace:exec-2026-001" },
    "package": { "id": "pkg:cyber-foundations", "version": "1.0.0" }
}
```

### 2.5 PolicyViolation

Uma **PolicyViolation** ocorre quando uma policy retorna DENY.

```json
{
    "violation_id": "viol:x1y2z3",
    "policy_name": "can_start_mission",
    "decision": {
        "result": "DENY",
        "reason": "Pré-requisitos não cumpridos: linux-001, linux-002",
        "failed_invariant": "CL-005",
        "severity": "HIGH",
        "trace_id": "pol:a1b2c3d4",
        "policy_name": "can_start_mission",
        "evaluated_at": "2026-07-19T10:30:00Z",
        "context_snapshot": { ... }
    },
    "action": "BLOCKED",
    "remediation": "Complete as missões: linux-001, linux-002"
}
```

---

## 3. Interface Conceitual

### 3.1 Policy Engine Interface

```python
class PolicyEngine(Protocol):
    def evaluate(self, policy_name: str, **context) -> PolicyDecision: ...
    def evaluate_all(self, **context) -> list[PolicyDecision]: ...
    def register(self, name: str, policy: Callable[..., PolicyDecision]) -> None: ...
    def unregister(self, name: str) -> None: ...
    def list_policies(self) -> list[str]: ...
```

### 3.2 Policy Function Signature

```python
Policy = Callable[..., PolicyDecision]
```

Onde `...` representa os argumentos contextuais necessários para a policy específica.

### 3.3 Policy Registry Interface

```python
class PolicyRegistry(Protocol):
    def register(self, name: str, policy: Callable[..., PolicyDecision]) -> None: ...
    def evaluate(self, name: str, **context) -> PolicyDecision: ...
    def evaluate_all(self, **context) -> list[PolicyDecision]: ...
    def list_policies(self) -> list[str]: ...
    def remove(self, name: str) -> None: ...
```

---

## 4. Fluxo de Decisão

### 4.1 Fluxo Completo

```
1. Runtime solicita ação (ex: start_mission)
2. Runtime monta PolicyContext
3. Runtime chama PolicyEngine.evaluate("can_start_mission", context)
4. PolicyEngine localiza a policy registrada
5. PolicyEngine executa a policy function
6. Policy function avalia regras contra o contexto
7. Policy function retorna PolicyDecision
8. PolicyEngine retorna PolicyDecision para o Runtime
9. Runtime verifica o resultado:
     a. Se ALLOW → executa a transição via State Engine
     b. Se DENY → bloqueia a ação, retorna erro
```

### 4.2 Fluxo com Múltiplas Policies

```
1. Runtime solicita ação complexa (ex: completar missão)
2. Runtime chama PolicyEngine.evaluate_all(context)
3. PolicyEngine executa todas as policies relevantes:
     a. can_submit_evidence
     b. can_assess
     c. can_unlock_competency
     d. can_grant_achievement
4. PolicyEngine coleta todos os PolicyDecisions
5. PolicyEngine aplica resolução de conflitos:
     a. Se alguma DENY com CRITICAL → bloqueia tudo
     b. Se alguma DENY com HIGH → bloqueia a ação específica
     c. Se todas ALLOW → prossegue
6. PolicyEngine retorna lista consolidada
```

---

## 5. Resolução de Conflitos

### 5.1 Hierarquia de Prioridade

```
1. SECURITY   (sempre vence — invariantes arquiteturais)
2. INTEGRITY  (invariantes de ciclo de vida)
3. BUSINESS   (regras de negócio)
4. CONVENIENCE (experiência do usuário)
```

### 5.2 Regras de Resolução

| Condição | Resultado |
|----------|-----------|
| Qualquer policy SECURITY retorna DENY | **DENY** (bloqueia tudo) |
| Qualquer policy INTEGRITY retorna DENY | **DENY** (bloqueia a ação) |
| BUSINESS retorna DENY, SECURITY/INTEGRITY ALLOW | **DENY** (bloqueia a ação) |
| CONVENIENCE retorna DENY, demais ALLOW | **ALLOW** (apenas warning) |
| Todas retornam ALLOW | **ALLOW** |

### 5.3 Exceções

| Exceção | Regra | Justificativa |
|---------|-------|---------------|
| Admin override | SECURITY pode ALLOW quando INTEGRITY DENY | Apenas para administradores |
| Force flag | Parâmetro `force=True` bypassa BUSINESS | Apenas em modo de desenvolvimento |
| Dry run | Parâmetro `dry_run=True` não bloqueia | Apenas para simulação |

---

## 6. Compliance com a Constituição

| Elemento | Constituição | ARCH | Invariante |
|----------|-------------|------|------------|
| PolicyDecision | — | ARCH-0010 | — |
| PolicyContext | — | ARCH-0010 | — |
| PolicyViolation | — | ARCH-0010 | — |
| Hierarquia Security > Integrity > Business > Convenience | — | ARCH-0010 | — |
| Resolução de conflitos | — | ARCH-0010 | — |
| Interface PolicyRegistry | — | ARCH-0010 | — |

---

## 7. Declaração Final

> **PROTOCOL-0004 é a especificação formal do sistema de políticas do ASCEND.**
>
> Toda ação no sistema passa por uma policy.
> Toda policy retorna um PolicyDecision.
> Toda decisão é rastreável, justificável e invariante.
>
> O Policy Protocol garante que o ASCEND nunca age sem antes perguntar:
>
> *"Esta ação é permitida?"*
