# ASCEND Traceability Matrix

| Campo | Valor |
|-------|-------|
| **ID** | TRACE-MATRIX |
| **Nome** | ASCEND Traceability Matrix |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Governance |
| **Owner** | Chief Architect |

---

## 1. Propósito

Esta matriz mapeia a rastreabilidade entre todos os artefatos do ASCEND:

```
Constituição → Foundation → Architecture → ADR → Protocol → Specification → Runtime → Testes
```

Cada requisito possui um **identificador único** e é rastreável através de todas as camadas.

---

## 2. Matriz de Rastreabilidade

### 2.1 Constituição → Foundation

| ID Constituição | Foundation Doc | Seção |
|----------------|---------------|-------|
| North Star | DOC-0000 | North Star |
| First Principle 1 | DOC-0003 | P1 — Competência exige evidência |
| First Principle 2 | DOC-0003 | P2 — Construção supera consumo |
| First Principle 3 | DOC-0003 | P3 — IA amplifica humanos |
| First Principle 4 | DOC-0003 | P4 — Autonomia é o objetivo |
| First Principle 5 | DOC-0003 | P5 — Complexidade justificada |
| First Principle 6 | DOC-0003 | P6 — Conhecimento aberto |
| First Principle 7 | DOC-0003 | P7 — Verdade técnica |
| I1 | DOC-0007 | Domain não depende de Infrastructure |
| I2 | DOC-0007 | Competência exige evidência |
| I3 | DOC-0007 | Comportamento gera evento |
| I4 | DOC-0007 | Conteúdo é dado, nunca código |
| I5 | DOC-0007 | IA nunca altera regras de negócio |
| I6 | DOC-0007 | Núcleo funciona offline |
| I7 | DOC-0007 | Funcionalidade testável sem GUI |
| I8 | DOC-0007 | Dados pertencem ao usuário |
| I9 | DOC-0007 | Camadas comunicam-se para dentro |
| I10 | DOC-0007 | Repositórios são contratos |

---

## 3. Foundation → Architecture

| Foundation | Architecture | Seção |
|------------|-------------|-------|
| North Star | ARCH-0001 | 1. Architecture Vision |
| North Star | ARCH-0002 | 1. Domain Vision |
| North Star | ARCH-0003 | 1. Core Engine Definition |
| North Star | ARCH-0008 | 1. Propósito |
| P1 (Competência exige evidência) | ARCH-0008 | 2.1 Evidência é o centro |
| P1 | ARCH-0010 | 3.4 Competency Policies |
| P2 (Construção supera consumo) | ARCH-0002 | 1. Domain Vision |
| P3 (IA amplifica humanos) | ARCH-0004 | 2. AI First Principles |
| P3 | ARCH-0010 | 3.3 Assessment Policies (can_auto_assess) |
| P4 (Autonomia) | ARCH-0002 | 3. Entity 1 — Builder |
| P5 (Complexidade justificada) | ARCH-0006 | 2. MVP Scope |
| P6 (Conhecimento aberto) | ARCH-0001 | 7. Extension Model |
| P7 (Verdade técnica) | ARCH-0008 | 2.1 Evidência é o centro |
| I1 (Domain não depende de Infrastructure) | ARCH-0001 | 4. Architectural Invariants |
| I2 (Competência exige evidência) | ARCH-0008 | CL-001 |
| I3 (Comportamento gera evento) | ARCH-0008 | 4. Eventos |
| I4 (Conteúdo é dado) | ARCH-0001 | 3.2 Content as Data |
| I5 (IA não altera regras) | ARCH-0004 | 8. Agent Governance |
| I6 (Núcleo offline) | ARCH-0006 | 4. Technology Stack |
| I7 (Testável sem GUI) | ARCH-0006 | 7. CLI Specification |
| I8 (Dados do usuário) | ADR-004 | Local-First |
| I9 (Camadas para dentro) | ARCH-0001 | 4. Architectural Invariants |
| I10 (Repositórios são contratos) | ARCH-0001 | 4. Architectural Invariants |

---

## 3. Architecture → ADR

| Architecture | ADR | Decisão |
|-------------|-----|---------|
| ARCH-0001 (Engine First) | ADR-001 | Engine agnóstica a domínio |
| ARCH-0001 (Content as Data) | ADR-002 | Conteúdo é YAML, nunca código |
| ARCH-0004 (AI as Layer) | ADR-003 | IA é camada substituível |
| ARCH-0006 (Local-First) | ADR-004 | SQLite, dados do usuário |
| ARCH-0008 (Competency Lifecycle) | ADR-001 | Engine agnóstica |
| ARCH-0009 (Runtime State Machine) | ADR-001 | Engine agnóstica |
| ARCH-0010 (Policy Engine) | ADR-001, ADR-002, ADR-003, ADR-004 | Policies protegem ADRs |

---

## 4. Architecture → Protocol

| Architecture | Protocol | Seção |
|-------------|----------|-------|
| ARCH-0001 (System Architecture) | PROTOCOL-0001 (Core) | 2. Vocabulário, 3. Entidades |
| ARCH-0002 (Domain Model) | PROTOCOL-0001 (Core) | 3. Entidades, 5. Relações |
| ARCH-0003 (Core Engine) | PROTOCOL-0001 (Core) | 6. Regras Universais |
| ARCH-0008 (Competency Lifecycle) | PROTOCOL-0002 (Event) | 2. DomainEvents |
| ARCH-0008 (Competency Lifecycle) | PROTOCOL-0003 (State) | 3.2 Mission State Machine |
| ARCH-0009 (Runtime State Machine) | PROTOCOL-0002 (Event) | 3. RuntimeEvents |
| ARCH-0009 (Runtime State Machine) | PROTOCOL-0003 (State) | 3.7 Runtime State Machine |
| ARCH-0010 (Policy Engine) | PROTOCOL-0004 (Policy) | 2. Definições, 3. Interface |
| ARCH-0001 (System Architecture) | PROTOCOL-0005 (Capability) | 2. Capabilities |

---

## 5. Protocol → Specification

| Protocol | Specification | Seção |
|----------|--------------|-------|
| PROTOCOL-0001 (Core) | SPEC-0001 (APS) | Vocabulário, entidades |
| PROTOCOL-0001 (Core) | SPEC-0002 (AEP) | Pipeline de execução |
| PROTOCOL-0002 (Event) | SPEC-0002 (AEP) | Eventos de domínio |
| PROTOCOL-0003 (State) | SPEC-0002 (AEP) | State machine |
| PROTOCOL-0004 (Policy) | — | (futuro: SPEC-0005) |
| PROTOCOL-0005 (Capability) | SPEC-0001 (APS) | Capabilities em packages |

---

## 6. Specification → Runtime

| Specification | Runtime Component | Arquivo |
|--------------|-------------------|---------|
| SPEC-0001 (APS) | PackageLoader | `package_engine/loader.py` |
| SPEC-0001 (APS) | PackageParser | `package_engine/parser.py` |
| SPEC-0001 (APS) | PackageValidator | `package_engine/validator.py` |
| SPEC-0002 (AEP) | RuntimeKernel | `runtime/kernel.py` |
| SPEC-0002 (AEP) | RuntimeOrchestrator | `runtime/orchestrator.py` |
| SPEC-0002 (AEP) | JourneyRunner | `runtime/runners/journey_runner.py` |
| SPEC-0002 (AEP) | MissionRunner | `runtime/runners/mission_runner.py` |
| SPEC-0002 (AEP) | ChallengeRunner | `runtime/runners/challenge_runner.py` |
| SPEC-0002 (AEP) | AssessmentPipeline | `runtime/assessment/pipeline.py` |
| SPEC-0002 (AEP) | CompetencyEngine | `runtime/competency/engine.py` |
| SPEC-0002 (AEP) | DomainEventCollector | `runtime/events/collector.py` |
| SPEC-0002 (AEP) | PackageConverter | `runtime/adapters/package_converter.py` |
| SPEC-0003 (ARP) | (futuro) | Registry |
| SPEC-0004 (AAP) | (futuro) | Agent Layer |

---

## 7. Runtime → Testes

| Runtime Component | Test File | Cobertura |
|-------------------|-----------|-----------|
| RuntimeKernel | `tests/test_runtime.py` | 85%+ |
| RuntimeOrchestrator | `tests/test_runtime.py` | 85%+ |
| JourneyRunner | `tests/test_runtime.py` | 85%+ |
| MissionRunner | `tests/test_runtime.py` | 85%+ |
| ChallengeRunner | `tests/test_runtime.py` | 85%+ |
| AssessmentPipeline | `tests/test_runtime.py` | 85%+ |
| CompetencyEngine | `tests/test_runtime.py` | 85%+ |
| PackageLoader | `tests/test_package_engine.py` | 90%+ |
| PackageParser | `tests/test_package_engine.py` | 90%+ |
| PackageValidator | `tests/test_package_engine.py` | 90%+ |
| PackageConverter | `tests/test_runtime.py` | 85%+ |
| DomainEventCollector | `tests/test_runtime.py` | 85%+ |
| RuntimeKernel | `tests/test_runtime.py` | 85%+ |
| BuilderRepository | `tests/test_infrastructure.py` | 85%+ |
| EventStore | `tests/test_infrastructure.py` | 85%+ |
| UnitOfWork | `tests/test_infrastructure.py` | 85%+ |
| CLI | `tests/test_api.py` | 70%+ |

---

## 8. Matriz de Cobertura de Requisitos

| ID do Requisito | Fonte | Architecture | Protocol | Runtime | Testado? |
|-----------------|-------|-------------|----------|---------|----------|
| R-001 | North Star | ARCH-0008 | PROTOCOL-0001 | CompetencyEngine | ✅ |
| R-002 | P1 | ARCH-0008 | PROTOCOL-0002 | AssessmentPipeline | ✅ |
| R-003 | P2 | ARCH-0002 | PROTOCOL-0001 | MissionRunner | ✅ |
| R-004 | P3 | ARCH-0004 | PROTOCOL-0005 | (futuro) | ❌ |
| R-005 | P4 | ARCH-0002 | PROTOCOL-0001 | Builder | ✅ |
| R-006 | P5 | ARCH-0006 | — | — | ✅ |
| R-007 | P6 | ARCH-0001 | — | — | ❌ |
| R-008 | P7 | ARCH-0008 | PROTOCOL-0002 | Evidence | ✅ |
| R-009 | I1 | ARCH-0001 | — | Domain | ✅ |
| R-010 | I2 | ARCH-0008 | PROTOCOL-0003 | CompetencyEngine | ✅ |
| R-011 | I3 | ARCH-0008 | PROTOCOL-0002 | EventCollector | ✅ |
| R-012 | I4 | ADR-002 | PROTOCOL-0001 | PackageLoader | ✅ |
| R-013 | I5 | ADR-003 | PROTOCOL-0005 | (futuro) | ❌ |
| R-014 | I6 | ARCH-0006 | — | Runtime | ✅ |
| R-015 | I7 | ARCH-0006 | — | CLI | ✅ |
| R-016 | I8 | ADR-004 | — | SQLite | ✅ |
| R-017 | I9 | ARCH-0001 | — | Layers | ✅ |
| R-018 | I10 | ARCH-0001 | — | Protocols | ✅ |
| R-019 | CL-001 | ARCH-0008 | PROTOCOL-0003 | CompetencyEngine | ✅ |
| R-020 | CL-002 | ARCH-0008 | PROTOCOL-0003 | CompetencyEngine | ✅ |
| R-021 | CL-003 | ARCH-0008 | PROTOCOL-0003 | AssessmentPipeline | ✅ |
| R-022 | CL-004 | ARCH-0008 | PROTOCOL-0003 | ChallengeRunner | ✅ |
| R-023 | CL-005 | ARCH-0008 | PROTOCOL-0003 | JourneyRunner | ✅ |
| R-024 | CL-006 | ARCH-0008 | PROTOCOL-0003 | State Engine | ❌ |
| R-025 | CL-007 | ARCH-0008 | PROTOCOL-0002 | EventStore | ✅ |
| R-026 | ARCH-0009-001 | ARCH-0009 | PROTOCOL-0003 | State Engine | ❌ |

---

## 9. Declaração Final

> **ASCEND_TRACEABILITY_MATRIX é a prova de que o ASCEND é um sistema arquiteturalmente consistente.**
>
> Cada requisito da Constituição está mapeado para:
> - Um documento de Foundation
> - Uma decisão de Architecture
> - Um ADR
> - Um Protocol
> - Uma Specification
> - Um componente do Runtime
> - Testes
>
> Se um requisito não está nesta matriz, ele não é rastreável.
> Se um componente não está nesta matriz, ele não é justificado.
>
> A rastreabilidade é a garantia de que o ASCEND não tem partes órfãs.
