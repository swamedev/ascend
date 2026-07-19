# PROTOCOL-0002 — Event Protocol

| Campo | Valor |
|-------|-------|
| **ID** | PROTOCOL-0002 |
| **Nome** | Event Protocol |
| **Versão** | 1.0 |
| **Status** | Stable |
| **Categoria** | Protocol |
| **Owner** | Chief Architect |
| **Derivado de** | Constituição, ARCH-0008, ARCH-0009, PROTOCOL-0001 |
| **Linguagem** | Independente |

---

## 1. Propósito

Este protocolo cataloga **todos os eventos oficiais** do ASCEND.

Cada evento possui: nome, payload, origem, consumidores, persistência, idempotência, versionamento e garantias.

Existem duas categorias de eventos:

| Categoria | Nível | Armazenamento | Consumidores |
|-----------|-------|---------------|--------------|
| **DomainEvent** | Domínio | EventStore (SQLite) | Audit trail, projeções, hooks |
| **RuntimeEvent** | Infraestrutura | Runtime log (memória) | Monitoramento, debugging |

---

## 2. DomainEvents

### 2.1 Catálogo Completo

| # | Evento | Emissor | Payload | Consumidores |
|---|--------|---------|---------|--------------|
| DE-01 | **BuilderCreated** | Application Service | `{ builder_id, username, created_at }` | EventStore, BuilderRepository |
| DE-02 | **BuilderActivated** | Domain | `{ builder_id, activated_at }` | EventStore |
| DE-03 | **BuilderDeactivated** | Domain | `{ builder_id, reason, deactivated_at }` | EventStore |
| DE-04 | **BuilderArchived** | Domain | `{ builder_id, archived_at }` | EventStore |
| DE-05 | **JourneyStarted** | JourneyRunner | `{ journey_id, builder_id, mission_count }` | EventStore, Hooks |
| DE-06 | **JourneyCompleted** | JourneyRunner | `{ journey_id, builder_id, missions_done, missions_total }` | EventStore, Hooks |
| DE-07 | **MissionStarted** | MissionRunner | `{ mission_id, builder_id, journey_id }` | EventStore, Hooks |
| DE-08 | **MissionCompleted** | MissionRunner | `{ mission_id, builder_id, xp_gained, passed }` | EventStore, Hooks |
| DE-09 | **ChallengePresented** | ChallengeRunner | `{ mission_id, challenge_type, description }` | EventStore |
| DE-10 | **EvidenceSubmitted** | ChallengeRunner | `{ evidence_id, mission_id, builder_id, evidence_type }` | EventStore, Hooks |
| DE-11 | **EvidenceValidated** | AssessmentPipeline | `{ evidence_id, valid, reason }` | EventStore |
| DE-12 | **AssessmentStarted** | AssessmentPipeline | `{ mission_id, rubric_id, timestamp }` | EventStore, Hooks |
| DE-13 | **AssessmentCompleted** | AssessmentPipeline | `{ mission_id, score, percentage, passed, rubric_id }` | EventStore, Hooks, CompetencyEngine |
| DE-14 | **CompetencyUnlocked** | CompetencyEngine | `{ competency_id, builder_id, level, score }` | EventStore, Builder |
| DE-15 | **CompetencyLevelIncreased** | CompetencyEngine | `{ competency_id, builder_id, old_level, new_level }` | EventStore |
| DE-16 | **AchievementGranted** | CompetencyEngine | `{ achievement_id, builder_id, competency_id }` | EventStore, Builder |
| DE-17 | **AchievementRevoked** | Governance | `{ achievement_id, builder_id, reason }` | EventStore |
| DE-18 | **LevelAdvanced** | CompetencyEngine | `{ builder_id, old_level, new_level, total_xp }` | EventStore |
| DE-19 | **XPGained** | CompetencyEngine | `{ builder_id, mission_id, xp_gained, total_xp }` | EventStore |
| DE-20 | **MissionCancelled** | Admin/System | `{ mission_id, builder_id, reason }` | EventStore |

### 2.2 Schema do DomainEvent

```json
{
    "event_id": "evt:mission-started-a1b2c3",
    "event_type": "MissionStarted",
    "aggregate_id": "mission:linux-001",
    "aggregate_type": "Mission",
    "payload": {
        "mission_id": "mission:linux-001",
        "builder_id": "builder:alex",
        "journey_id": "journey:linux-foundations"
    },
    "metadata": {
        "version": 1,
        "timestamp": "2026-07-19T10:30:00Z",
        "trace_id": "trace:exec-2026-001",
        "correlation_id": "corr:abc123"
    }
}
```

### 2.3 Schema Formal

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `event_id` | string (prefixo `evt:`) | Sim | Identificador único do evento |
| `event_type` | string | Sim | Nome do evento (PascalCase) |
| `aggregate_id` | string | Sim | ID da entidade afetada |
| `aggregate_type` | string | Sim | Tipo da entidade (Builder, Mission, etc.) |
| `payload` | object | Sim | Dados específicos do evento |
| `metadata.version` | int | Sim | Versão do schema do evento |
| `metadata.timestamp` | datetime | Sim | Momento em que o evento ocorreu |
| `metadata.trace_id` | string | Sim | Correlação com a execução |
| `metadata.correlation_id` | string | Não | Correlação entre eventos relacionados |

---

## 3. RuntimeEvents

### 3.1 Catálogo Completo

| # | Evento | Emissor | Estado Origem | Estado Destino | Payload |
|---|--------|---------|---------------|----------------|---------|
| RE-01 | **RunRequested** | Cliente (CLI/API) | IDLE | LOADING | `{ package_path, builder_id }` |
| RE-02 | **PackageLoaded** | PackageLoader | LOADING | VALIDATING | `{ package_id, version, file_count }` |
| RE-03 | **PackageLoadFailed** | PackageLoader | LOADING | FAILED | `{ error, path }` |
| RE-04 | **PackageValidated** | PackageValidator | VALIDATING | CONVERTING | `{ valid, warning_count }` |
| RE-05 | **PackageInvalid** | PackageValidator | VALIDATING | FAILED | `{ errors: [...] }` |
| RE-06 | **PackageConverted** | PackageConverter | CONVERTING | READY | `{ journey_count, mission_count }` |
| RE-07 | **ExecutionStarted** | Orchestrator | READY | EXECUTING | `{ builder_id, package_id }` |
| RE-08 | **JourneyStarted** | JourneyRunner | EXECUTING | JOURNEY_STARTED | `{ journey_id, mission_count }` |
| RE-09 | **MissionStarted** | MissionRunner | JOURNEY_STARTED | MISSION_STARTED | `{ mission_id, challenge_type }` |
| RE-10 | **ChallengePresented** | ChallengeRunner | MISSION_STARTED | CHALLENGE_PRESENTED | `{ mission_id, description }` |
| RE-11 | **EvidenceCollected** | ChallengeRunner | CHALLENGE_PRESENTED | EVIDENCE_COLLECTED | `{ evidence_id, evidence_type }` |
| RE-12 | **AssessmentStarted** | AssessmentPipeline | EVIDENCE_COLLECTED | ASSESSING | `{ mission_id, rubric_id }` |
| RE-13 | **AssessmentCompleted** | AssessmentPipeline | ASSESSING | MISSION_COMPLETED | `{ score, percentage, passed }` |
| RE-14 | **MissionCompleted** | MissionRunner | MISSION_COMPLETED | JOURNEY_STARTED | `{ mission_id, xp_gained, unlocked }` |
| RE-15 | **JourneyCompleted** | JourneyRunner | JOURNEY_STARTED | EXECUTING | `{ journey_id, missions_done, missions_total }` |
| RE-16 | **ExecutionFinished** | Orchestrator | EXECUTING | REPORTING | `{ journeys_completed, missions_completed }` |
| RE-17 | **ReportGenerated** | Orchestrator | REPORTING | COMPLETED | `{ duration, total_xp, competencies_unlocked }` |
| RE-18 | **ExecutionCancelled** | Cliente/Admin | EXECUTING | CANCELLED | `{ reason }` |
| RE-19 | **RuntimeError** | Qualquer | Qualquer | FAILED | `{ error, location, recoverable }` |

### 3.2 Schema do RuntimeEvent

```json
{
    "event_id": "revt:package-loaded-x1y2z3",
    "event_type": "PackageLoaded",
    "previous_state": "LOADING",
    "current_state": "VALIDATING",
    "payload": {
        "package_id": "pkg:cyber-foundations",
        "version": "1.0.0",
        "file_count": 12
    },
    "metadata": {
        "version": 1,
        "timestamp": "2026-07-19T10:30:00Z",
        "trace_id": "trace:exec-2026-001",
        "duration_ms": 45
    }
}
```

### 3.3 Schema Formal

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `event_id` | string (prefixo `revt:`) | Sim | Identificador único do evento |
| `event_type` | string | Sim | Nome do evento (PascalCase) |
| `previous_state` | string | Sim | Estado anterior do Runtime |
| `current_state` | string | Sim | Estado atual do Runtime |
| `payload` | object | Sim | Dados específicos do evento |
| `metadata.version` | int | Sim | Versão do schema |
| `metadata.timestamp` | datetime | Sim | Momento do evento |
| `metadata.trace_id` | string | Sim | Correlação com a execução |
| `metadata.duration_ms` | int | Não | Duração da transição |

---

## 4. Propriedades dos Eventos

### 4.1 Origem

| Evento | Origem | Categoria |
|--------|--------|-----------|
| BuilderCreated | Application Service | Domain |
| BuilderActivated | Domain | Domain |
| MissionStarted | MissionRunner | Domain |
| EvidenceSubmitted | ChallengeRunner | Domain |
| AssessmentCompleted | AssessmentPipeline | Domain |
| CompetencyUnlocked | CompetencyEngine | Domain |
| AchievementGranted | CompetencyEngine | Domain |
| RunRequested | CLI/API | Runtime |
| PackageLoaded | PackageLoader | Runtime |
| ExecutionStarted | Orchestrator | Runtime |
| RuntimeError | Qualquer | Runtime |

### 4.2 Consumidores

| Consumidor | Eventos que consome | Ação |
|------------|---------------------|------|
| **EventStore** | Todos os DomainEvents | Persiste para audit trail |
| **BuilderRepository** | BuilderCreated, BuilderActivated | Atualiza projeção do builder |
| **CompetencyEngine** | AssessmentCompleted | Processa unlock, XP, level |
| **RuntimeHooks** | JourneyStarted, MissionStarted, AssessmentStarted | Executa hooks configurados |
| **ExecutionReport** | Todos os RuntimeEvents | Constrói relatório final |
| **Policy Engine** | (consultivo) | Avalia autorizações |

### 4.3 Persistência

| Categoria | Local | Formato | Retenção |
|-----------|-------|---------|----------|
| DomainEvent | EventStore (SQLite) | JSON column | Permanente |
| RuntimeEvent | Runtime log (memória) | Objeto em memória | Até o fim da execução |

### 4.4 Idempotência

| Evento | Idempotente | Estratégia |
|--------|-------------|------------|
| BuilderCreated | Sim | `event_id` único, INSERT OR IGNORE |
| MissionStarted | Sim | Verifica se missão já está STARTED |
| EvidenceSubmitted | Sim | `evidence_id` único |
| AssessmentCompleted | Sim | Verifica se assessment já existe |
| CompetencyUnlocked | Sim | Verifica se competência já está UNLOCKED |
| AchievementGranted | Sim | Verifica se achievement já foi concedido |
| RuntimeEvents | Sim | Apenas log, sem efeito colateral |

### 4.5 Versionamento

| Versão do Schema | Mudança | Compatibilidade |
|------------------|---------|-----------------|
| 1 (atual) | Definição inicial | — |
| 2+ | Adição de campos opcionais | Retroativa |
| 2+ | Remoção de campos obrigatórios | **Breaking** (MAJOR) |
| 2+ | Alteração de tipo de campo | **Breaking** (MAJOR) |

Regra: `metadata.version` incrementa quando o schema muda. Consumidores devem rejeitar versões que não conhecem.

### 4.6 Garantias

| Garantia | DomainEvent | RuntimeEvent |
|----------|-------------|--------------|
| **Ordenação causal** | Sim (por aggregate) | Sim (sequencial) |
| **Entrega pelo menos uma vez** | Sim | Sim |
| **Imutabilidade** | Sim (append-only) | Sim (log em memória) |
| **Rastreabilidade** | Sim (trace_id) | Sim (trace_id) |
| **Atomicidade** | Sim (UoW) | Sim (transição atômica) |
| **Replayability** | Sim (EventStore) | Não (apenas memória) |

---

## 5. Ordem Causal dos Eventos

### 5.1 DomainEvents

```
BuilderCreated
    → JourneyStarted
        → MissionStarted
            → ChallengePresented
                → EvidenceSubmitted
                    → EvidenceValidated
                        → AssessmentStarted
                            → AssessmentCompleted
                                → CompetencyUnlocked
                                    → AchievementGranted
                                → XPGained
                                → LevelAdvanced
                            → MissionCompleted
                        → MissionCancelled
                    → (retry)
                → (retry)
        → JourneyCompleted
    → (próxima journey)
```

### 5.2 RuntimeEvents

```
RunRequested
    → PackageLoaded | PackageLoadFailed
        → PackageValidated | PackageInvalid
            → PackageConverted
                → ExecutionStarted
                    → JourneyStarted (por journey)
                        → MissionStarted (por missão)
                            → ChallengePresented
                                → EvidenceCollected
                                    → AssessmentStarted
                                        → AssessmentCompleted
                                            → MissionCompleted
                                    → (retry)
                            → (retry)
                        → (próxima missão)
                    → JourneyCompleted
                    → (próxima journey)
                → ExecutionFinished
                    → ReportGenerated
                → RuntimeError → FAILED
                → ExecutionCancelled → CANCELLED
```

---

## 6. Eventos e Invariantes

| Invariante | Eventos que o protegem |
|------------|----------------------|
| I-002 (Competência exige evidência) | EvidenceSubmitted → AssessmentCompleted → CompetencyUnlocked |
| I-003 (Comportamento gera evento) | Todos os DomainEvents |
| CL-001 (Assessment antes de unlock) | AssessmentCompleted → CompetencyUnlocked |
| CL-002 (Achievement depende de competency) | CompetencyUnlocked → AchievementGranted |
| CL-003 (Assessment exige evidência real) | EvidenceValidated → AssessmentStarted |
| CL-004 (Challenge precede evidence) | ChallengePresented → EvidenceSubmitted |
| CL-005 (Missão exige pré-requisitos) | (verificado antes de MissionStarted) |
| CL-006 (Estado não regride) | Eventos seguem ordem causal estrita |
| CL-007 (Eventos são imutáveis) | EventStore append-only |

---

## 7. Declaração Final

> **PROTOCOL-0002 é o catálogo oficial de eventos do ASCEND.**
>
> Todo comportamento relevante no sistema produz um evento.
>
> Todo evento tem um schema, uma origem, consumidores e garantias.
>
> Nenhum evento pode ser emitido sem estar catalogado aqui.
>
> Nenhum evento pode ser alterado depois de emitido.
>
> A ordem causal dos eventos é a espinha dorsal da rastreabilidade do ASCEND.
