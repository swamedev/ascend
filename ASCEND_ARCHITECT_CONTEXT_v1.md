# ASCEND Constitution v1.0

> Documento Mestre de Arquitetura — Toda IA deve receber este documento antes de trabalhar no projeto.

---

## Sumário

1. [North Star](#1-north-star)
2. [First Principles](#2-first-principles)
3. [Engineering Philosophy](#3-engineering-philosophy)
4. [Architectural Invariants (Imutáveis)](#4-architectural-invariants-imutaveis)
5. [System Architecture](#5-system-architecture)
6. [Domain Model](#6-domain-model)
7. [Application Layer](#7-application-layer)
8. [Package Engine](#8-package-engine)
9. [Runtime Kernel](#9-runtime-kernel)
10. [API & CLI](#10-api--cli)
11. [Infrastructure](#11-infrastructure)
12. [Specifications (Protocolos)](#12-specifications-protocolos)
13. [Roadmap 2026–2035](#13-roadmap-2026-2035)
14. [O Que Pode e O Que Não Pode Mudar](#14-o-que-pode-e-o-que-nao-pode-mudar)
15. [Decisões Congeladas](#15-decisoes-congeladas)

---

## 1. North Star

> **Toda competência reivindicada deve ser uma competência comprovada.**

### Definição de Competência

Uma competência é a **capacidade demonstrável** de aplicar conhecimento para produzir resultados dentro de um contexto definido. Possui quatro dimensões:

| Dimensão | Descrição |
|----------|-----------|
| **Conhecimento** | A pessoa entende os fundamentos |
| **Aplicação** | A pessoa consegue executar |
| **Evidência** | A pessoa consegue demonstrar o resultado |
| **Reflexão** | A pessoa consegue explicar suas decisões |

### Pergunta de Validação Universal

> *"Esta decisão aumenta nossa capacidade de transformar conhecimento em competência comprovável?"*

| Resposta | Ação |
|----------|------|
| **Sim** | Alinhado com a North Star |
| **Não** | Deve ser reconsiderado |

### O Que Nunca Mudará

**Podem mudar:** tecnologias, linguagens, interfaces, modelos de IA, metodologias, ferramentas, estruturas organizacionais.

**Não podem mudar:** a busca por competência real, a necessidade de evidência, o compromisso com transparência, a valorização da prática.

---

## 2. First Principles

### As Sete Leis Fundamentais

| # | Princípio | Essência |
|---|-----------|----------|
| 1 | **Competência exige evidência** | Demonstre, não declare |
| 2 | **Construção supera consumo** | Crie, não consuma |
| 3 | **IA amplifica humanos; não substitui** | Aumente, não substitua |
| 4 | **Autonomia é o objetivo final** | Liberte, não prenda |
| 5 | **Complexidade precisa ser justificada** | Simplifique, não acumule |
| 6 | **Conhecimento aberto gera evolução coletiva** | Compartilhe, não restrinja |
| 7 | **Verdade técnica supera aparência** | Prove, não aparente |

### Implicações Diretas

- **P1**: Toda jornada deve produzir evidências observáveis (projetos, desafios, documentação)
- **P2**: Missões sempre respondem "O que você consegue criar ou resolver depois disso?"
- **P3**: Agentes de IA questionam, orientam, revisam — nunca fazem o trabalho inteiro
- **P4**: Dificuldade aumenta progressivamente; suporte diminui conforme competência aumenta
- **P5**: Complexidade adicionada apenas quando cria valor real
- **P6**: Comunidade não é funcionalidade — é parte da arquitetura
- **P7**: Projeto incompleto mas bem documentado vale mais que lista de cursos

---

## 3. Engineering Philosophy

### 3.1 Arquitetura antes de código
Entender o *porquê* antes de escrever o *como*.

### 3.2 Simplicidade antes de sofisticação
A solução mais simples que resolve o problema é a solução correta.

### 3.3 Modularidade como princípio
Cada componente: responsabilidade clara, baixo acoplamento, substituível.

### 3.4 Dados separados de comportamento
Engine executa. Packages definem conhecimento. Separação fundamental: lógica de avaliação ≠ conteúdo avaliado.

### 3.5 AI-Native, não AI-Dependent
A plataforma funciona sem IA. IA melhora, não sustenta.

### 3.6 Open Source First
Código legível, documentado, contribuível.

### 3.7 Evidence Driven Development
Toda funcionalidade produz valor observável.

### Arquitetura Conceitual

```
              FOUNDATION
                   │
                   ▼
        Competency Framework
                   │
                   ▼
               ENGINE
        ┌──────────┼──────────┐
        │          │          │
       AI      Missions   Evidence
        │          │          │
     Agents    Packages   Portfolio
```

### Camadas

| Camada | Responsabilidade |
|--------|-----------------|
| **Foundation** | Princípios, identidade, filosofia — não muda com frequência |
| **Competency Framework** | Modelo de competências, taxonomia, níveis — evolui por versão |
| **Engine** | Motor de avaliação, orquestração, progressão — código vivo |
| **AI / Agents** | Mentor, Avaliador, Gerador — inteligência acoplável |
| **Missions / Packages** | Conteúdo estruturado, desafios, cenários — contribuição aberta |
| **Evidence / Portfolio** | Artefatos produzidos pelo Builder — propriedade do usuário |

---

## 4. Architectural Invariants (Imutáveis)

Estas regras **jamais** podem ser quebradas. Qualquer PR que violar um invariante deve ser marcado como `blocked: architectural-invariant` e notificar o Chief Architect.

### I1 — Domain nunca depende de Infrastructure
`ascend.domain` não pode importar nada de `ascend.infrastructure`, `ascend.application`, SQLite, PostgreSQL, Redis, Kafka ou qualquer framework externo.

### I2 — Competência só existe quando há evidência
Nenhum método no domínio permite desbloquear competência sem evidência submetida e aceita.

### I3 — Todo comportamento relevante gera um evento
Mutações de estado no domínio (criação, transição, conclusão) devem produzir um `DomainEvent`.

### I4 — Conteúdo é dado, nunca código
Pacotes, missões, desafios e avaliações são dados (YAML). O motor interpreta — nunca compila ou importa — conteúdo.

### I5 — IA nunca altera regras de negócio
Agentes de IA podem orientar, avaliar, explicar, recomendar. **Não podem** alterar regras de validação, modificar estados críticos ou decidir aprovações sem supervisão configurável.

### I6 — O núcleo deve funcionar sem internet
`ascend.domain` e `ascend.application` operam offline. Recursos de rede (IA, sincronização) são opcionais e substituíveis.

### I7 — Toda funcionalidade deve ser testável sem interface gráfica
Qualquer comportamento precisa ser exercitável via teste unitário, teste de integração ou CLI.

### I8 — Dados pertencem ao usuário
Local-first. Sem telemetria obrigatória. Sem lock-in de nuvem.

### I9 — Camadas comunicam-se apenas para dentro
```
Presentation → Application → Domain → Infrastructure
```
Nenhuma camada pode pular a anterior ou depender de uma camada externa.

### I10 — Repositórios são contratos, não implementações
Application conhece apenas interfaces (Protocol). Implementação concreta (SQLite, PostgreSQL, memória) é injetada.

---

## 5. System Architecture

### Stack Tecnológica

| Componente | Tecnologia |
|------------|-----------|
| Linguagem | Python 3.12+ |
| Persistência | SQLite (local-first) |
| Testes | pytest + pytest-cov |
| CLI | argparse (stdlib) |
| Serialização | YAML (PyYAML) |
| Tipagem | Protocol, dataclasses, NewType |
| IA | Camada substituível (AAP) |

### Estrutura de Diretórios

```
src/ascend/
├── __init__.py              # Runtime como entry point público
├── api/
│   └── runtime.py           # Runtime class (facade pública)
├── application/
│   ├── commands/            # Command objects (CQRS-style)
│   ├── dto/                 # Data Transfer Objects
│   ├── interfaces/          # Protocols (repositories, event bus)
│   ├── services/            # Use cases
│   └── exceptions.py
├── cli/
│   └── main.py              # CLI argparse (ascend run, validate, init, doctor)
├── domain/
│   ├── builder.py           # Agregado raiz
│   ├── competency.py        # Competência
│   ├── skill.py             # Habilidade
│   ├── journey.py           # Jornada (sequência de missões)
│   ├── mission.py           # Missão com state machine
│   ├── challenge.py         # Desafio
│   ├── evidence.py          # Evidência
│   ├── assessment.py        # Avaliação
│   ├── achievement.py       # Conquista
│   └── events.py            # Domain Events (6 tipos)
├── infrastructure/
│   ├── uow.py               # Unit of Work
│   ├── config/settings.py   # Configurações
│   ├── events/memory_event_bus.py
│   └── persistence/sqlite/  # Repositórios, migrations, event store
├── package_engine/
│   ├── models.py            # APS Package models
│   ├── parser.py            # YAML → Package models
│   ├── validator.py         # 13 regras de validação
│   └── loader.py            # Loader (parse + validate)
├── runtime/
│   ├── kernel.py            # RuntimeKernel (entry point do motor)
│   ├── context.py           # RuntimeContext (estado compartilhado)
│   ├── models.py            # Runtime models (Package, Journey, Mission, etc.)
│   ├── orchestrator.py      # Orquestrador de execução
│   ├── report.py            # ExecutionReport, MissionResult, etc.
│   ├── hooks.py             # RuntimeHooks (Protocol) + NoopHooks
│   ├── adapters/
│   │   └── package_converter.py  # APS → Runtime models
│   ├── assessment/
│   │   └── pipeline.py      # AssessmentPipeline (scoring)
│   ├── competency/
│   │   └── engine.py        # CompetencyEngine (XP, level, achievements)
│   ├── events/
│   │   └── collector.py     # DomainEventCollector
│   └── runners/
│       ├── challenge_runner.py  # Abre desafio, coleta evidência
│       ├── mission_runner.py   # Executa missão completa
│       └── journey_runner.py   # Executa jornada (sequência de missões)
├── shared/
│   ├── clock.py             # Clock (ABC) + SystemClock
│   ├── ids.py               # generate_id()
│   ├── result.py            # Result[T, E] (Ok/Err pattern)
│   ├── types.py             # NewTypes (BuilderId, MissionId, etc.)
│   └── value_objects.py     # XP, Level (value objects imutáveis)
```

---

## 6. Domain Model

### Entidades

| Entidade | Atributos Principais | Comportamento |
|----------|---------------------|---------------|
| **Builder** | username, id, level, xp, competencies, achievements, missions, evidence_list, events | start_mission, submit_evidence, add_competency, earn_achievement, gain_xp |
| **Competency** | name, description, level, criteria, id | increase_level, check_completion |
| **Skill** | name, description, weight, id | — |
| **Journey** | name, objective, missions, status, id | — |
| **Mission** | title, objective, difficulty, xp_reward, prerequisites, status, evidence_list | start, submit, complete |
| **Challenge** | description, requirements, validation_rules, id | — |
| **Evidence** | artifact, type, builder_id, mission_id, status | submit, accept, reject |
| **Assessment** | evidence_id, score, feedback, reviewer | is_approved (score >= 0.7) |
| **Achievement** | name, description, criteria, badge | earn, is_earned |
| **Skill** | name, description, weight | — |

### Domain Events (6 tipos)

| Evento | Trigger | Payload |
|--------|---------|---------|
| `BuilderCreated` | Builder instanciado | builder_id, username |
| `MissionStarted` | Mission.start() | mission_id, builder_id |
| `EvidenceSubmitted` | Evidence.submit() | evidence_id, mission_id, builder_id |
| `AssessmentCompleted` | Assessment concluída | assessment_id, evidence_id, score |
| `CompetencyUnlocked` | Competência desbloqueada | competency_id, builder_id, level |
| `AchievementEarned` | Achievement conquistado | achievement_id, builder_id |

### State Machine (Missão)

```
AVAILABLE → STARTED → IN_PROGRESS → EVIDENCE_SUBMITTED → UNDER_REVIEW → COMPLETED
```

### Regras de Domínio

- XP não pode ser negativo
- Missão só pode ser iniciada se AVAILABLE
- Evidência só pode ser submetida se missão STARTED
- Missão só completa se EVIDENCE_SUBMITTED
- Builder ganha level a cada 500 XP
- Assessment aprovado se score >= 0.7
- Competência desbloqueada se percentage >= mastery_threshold

---

## 7. Application Layer

### Padrão: CQRS-style com Services + Commands + DTOs

**Commands:**
- `CreateBuilder(username)` → cria Builder, salva, publica eventos
- `StartMission(builder_id, mission_id)` → inicia missão
- `SubmitEvidence(builder_id, mission_id, artifact, evidence_type)` → submete evidência
- `CompleteAssessment(evidence_id, score, feedback, reviewer)` → completa avaliação
- `UnlockCompetency(builder_id, name, description, level, criteria)` → desbloqueia competência

**Services:**
- `BuilderService` — create, get, gain_xp
- `MissionService` — start_mission, submit_evidence, get_mission
- `CompetencyService` — unlock_competency

**Interfaces (Protocols):**
- `BuilderRepository`, `MissionRepository`, `EvidenceRepository`, `CompetencyRepository`, `JourneyRepository`
- `EventBus` — publish(events)

**DTOs:**
- `BuilderDTO` — id, username, level, xp, competency_count, achievement_count, active_mission_count
- `MissionDTO` — id, title, objective, difficulty, xp_reward, status
- `EvidenceDTO` — id, artifact, type, status, builder_id, submitted_at

---

## 8. Package Engine

### Pipeline: Parse → Validate → Load

**Parser** (`package_engine/parser.py`): Lê YAML do disco e converte para modelos APS (`Package`, `Journey`, `Mission`, `CompetencyDef`, `AchievementDef`, `Rubric`).

**Validator** (`package_engine/validator.py`): 13 regras de validação:

| # | Regra | Descrição |
|---|-------|-----------|
| 1 | `missing-id` | Package ID é obrigatório |
| 2 | `missing-version` | Version é obrigatório |
| 3 | `no-content` | Warning se sem journeys ou competencies |
| 4 | `journey-no-id` | Journey sem ID |
| 5 | `journey-unlock-not-found` | Unlock reference a journey inexistente |
| 6 | `competency-not-found` | Competency referenciada não definida |
| 7 | `mission-no-id` | Mission sem ID |
| 8 | `duplicate-mission-id` | Mission ID duplicado na mesma journey |
| 9 | `rubric-not-found` | Rubric referenciada não definida (warning) |
| 10 | `rubric-weights` | Pesos da rubric não somam 100 (warning) |
| 11 | `negative-xp` | XP negativo |
| 12 | `prerequisite-not-found` | Prerequisite não encontrado na journey |
| 13 | `no-content` | Warning se sem conteúdo |

### Loader Pipeline

```
PackageLoader.load(path)
  → PackageParser.parse_package(package.yaml)
  → PackageParser.parse_competencies(competencies.yaml)
  → PackageParser.parse_achievements(achievements.yaml)
  → PackageParser.parse_rubrics(rubrics.yaml)
  → PackageParser.parse_journey(journey.yaml)  [para cada journey]
    → PackageParser.parse_mission(mission.yaml)  [para cada mission]
  → PackageValidator.validate(pkg)  [13 regras]
  → return (Package, ValidationResult)
```

---

## 9. Runtime Kernel

### Arquitetura do Runtime

```
Runtime (API Facade)
  └── RuntimeKernel
        ├── PackageLoader (package_engine)
        ├── PackageConverter (APS → Runtime models)
        ├── RuntimeOrchestrator
        │     ├── JourneyRunner
        │     │     └── MissionRunner
        │     │           ├── ChallengeRunner
        │     │           ├── AssessmentPipeline
        │     │           └── CompetencyEngine
        │     └── DomainEventCollector
        └── RuntimeContext (estado compartilhado)
```

### RuntimeKernel.run()

1. Carrega pacote via `PackageLoader.load(path)`
2. Valida pacote (13 regras)
3. Converte APS → Runtime models via `PackageConverter`
4. Cria `RuntimeContext` com builder, package, clock, hooks, evidence
5. Executa `RuntimeOrchestrator.run(context)`
6. Retorna `ExecutionReport`

### RuntimeContext

Único container de estado compartilhado. Sem globais, sem singletons, sem dependências implícitas.

```python
@dataclass
class RuntimeContext:
    builder: Builder
    package: RuntimePackage
    clock: Clock
    event_collector: DomainEventCollector
    hooks: RuntimeHooks
    evidence_input: dict[str, str]
```

### ExecutionReport

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

### Hooks (Extension Points)

| Hook | Trigger | Propósito |
|------|---------|-----------|
| `before_journey` | Antes da journey | Setup, logging |
| `after_journey` | Após journey | Cleanup, reporting |
| `before_mission` | Antes da missão | Validação |
| `after_mission` | Após missão | Pós-processamento |
| `before_assessment` | Antes da avaliação | Pré-avaliação |
| `after_assessment` | Após avaliação | Pós-avaliação |

Hooks são síncronos, não lançam exceções. Se falham, Runtime loga e continua.

### AssessmentPipeline

Pipeline de avaliação built-in (substituível por agentes AAP):
- Se sem rubric: aprovado automaticamente (100%)
- Se com rubric: scoring por word overlap + length score
- Baseline mínimo: 60%
- Suporta normalização de acentos (português)

### CompetencyEngine

- XP gained = mission.xp se aprovado, 0 se não
- Level = (XP // 500) + 1
- Competências desbloqueadas se percentage >= mastery_threshold
- Achievements verificados por critérios textuais

---

## 9. API & CLI

### Runtime (Facade Pública)

```python
class Runtime:
    def run(self, package, builder, evidence=None) -> ExecutionReport
```

Aceita:
- `package`: path string ou Path
- `builder`: username string ou Builder object
- `evidence`: dict[str, str], path de arquivo, ou texto direto

### CLI (argparse)

| Comando | Descrição |
|---------|-----------|
| `ascend run [path] --builder <name> --evidence <text>` | Executa pacote |
| `ascend package validate [path]` | Valida pacote |
| `ascend package create <name>` | Cria pacote |
| `ascend init <name>` | Inicializa pacote |
| `ascend doctor` | Diagnóstico do sistema |
| `ascend progress` | Progresso do builder (placeholder) |
| `ascend --version` | Versão |

---

## 11. Infrastructure

### SQLite Persistence

- **ConnectionManager**: Gerencia conexão SQLite (thread-safe com Lock)
- **MigrationEngine**: Aplica schema (11 tabelas: builders, competencies, builder_competencies, missions, builder_missions, evidence, assessments, achievements, builder_achievements, events, journeys, schema_version)
- **UnitOfWork**: Context manager com commit/rollback
- **Repositórios**: SQLiteBuilderRepository, SQLiteMissionRepository, SQLiteEvidenceRepository, SQliteEventStore
- **Event Bus**: MemoryEventBus (in-memory pub/sub)

### Settings

```python
@dataclass
class Settings:
    db_path: str = ":memory:"
    debug: bool = False
    capabilities: dict = {
        "persistence": True,
        "event_store": True,
        "ai_runtime": False,
        "plugin_sdk": False,
    }
```

---

## 12. Specifications (Protocolos)

### SPEC-0001 — APS (Package Specification) v1.0

Define o formato padrão para pacotes de competência. Um pacote é uma unidade autossuficiente, versionada e validada de conteúdo de aprendizado.

**Estrutura de diretórios:**
```
<package-id>/
    package.yaml              # Obrigatório
    competencies/competencies.yaml  # Opcional
    achievements/achievements.yaml  # Opcional
    assessments/rubrics.yaml       # Opcional
    journeys/<id>/
        journey.yaml          # Obrigatório
        missions/<id>/
            mission.yaml      # Obrigatório
    README.md                 # Opcional
```

**package.yaml:**
```yaml
metadata:
  id: string        # kebab-case, 1-64 chars
  version: semver   # MAJOR.MINOR.PATCH
  title: string
  description: string
  author: string
  license: string   # SPDX
spec:
  runtime: string   # ex: ">=1.0"
  language: string  # BCP 47
  estimated_hours: int
  dependencies: [string]
capabilities: [string]  # evidence, ai, plugin, async
```

### SPEC-0002 — AEP (Execution Protocol)

Define o contrato entre conteúdo executável e o Runtime Kernel.

**Pipeline de execução:**
```
Package → Journey → Mission → Challenge → Evidence → Assessment → Competency Update → Achievement Check → Progress Update → Events
```

**RuntimeExecutable Protocol:**
```python
class RuntimeExecutable(Protocol):
    def accept(self, visitor: RuntimeVisitor) -> None: ...
```

**RuntimeVisitor Protocol:**
```python
class RuntimeVisitor(Protocol):
    def visit_package(self, pkg: RuntimePackage): ...
    def visit_journey(self, journey: RuntimeJourney): ...
    def visit_mission(self, mission: RuntimeMission): ...
    def visit_challenge(self, challenge: RuntimeChallenge): ...
```

**State Machine (Missão):**
```
AVAILABLE → STARTED → IN_PROGRESS → EVIDENCE_SUBMITTED → UNDER_REVIEW → COMPLETED
```

**Synchronous Guarantee:** O Kernel é estritamente síncrono. Async é adicionado por camadas de infraestrutura acima.

### SPEC-0003 — ARP (Registry Protocol) — Draft v0.1.0

Define como pacotes são publicados, descobertos, instalados e verificados.

**Endpoints:**
- `GET /packages` — Listar/search
- `GET /packages/{id}` — Metadados
- `GET /packages/{id}/versions` — Listar versões
- `GET /packages/{id}/versions/{version}/download` — Download
- `PUT /packages/{id}/versions/{version}` — Publicar
- `GET /search?q={query}` — Busca

**Publish Flow:** Criar → Assinar (PGP) → Upload → Validar → 201 Created

**Install Flow:** Resolver → Download → Verificar checksum + PGP → Extrair → Resolver dependências

### SPEC-0004 — AAP (Agent Protocol) — Draft v0.1.0

Define comunicação entre agente externo (AI, humano, automático) e o Runtime.

**Agent Protocol:**
```python
class Agent(Protocol):
    async def assess(self, evidence, rubric, context) -> AssessmentResult
    async def provide_feedback(self, result, context) -> Feedback
    async def propose_competency(self, builder, context) -> CompetencyProposal
```

**Tipos de Agente:** human, ai, auto, hybrid, peer

**Estratégias de Execução:**
- `LocalExecutionStrategy` — built-in, sem agente externo
- `AIExecutionStrategy` — AI agent
- `TeamExecutionStrategy` — Múltiplos revisores, consenso
- `ClassroomExecutionStrategy` — Instrutor revisa
- `EnterpriseExecutionStrategy` — Compliance-driven

---

## 13. Roadmap 2026–2035

| Ano | Tema | Marco |
|-----|------|-------|
| 2026 | Foundation | Runtime v1.0, APS, AEP, CLI, 4 pacotes, Open Source |
| 2027 | Registry & SDK | ARP, Registry, SDK Python, 20 pacotes |
| 2028 | Developer Experience | VS Code, JetBrains, REST API, 100+ pacotes |
| 2029 | Intelligence Layer | AAP, AI Reviewer, Mentor, Interviewer |
| 2030 | Enterprise | LMS, SCORM, SSO, Audit |
| 2031 | Global Community | 10k+ pacotes, traduções, conferência |
| 2032 | Ecosystem Maturity | Studio v1.0, editor visual, analytics |
| 2033 | Interoperability | WebAssembly, Mobile SDK, IoT |
| 2034 | Self-Sustaining | Marketplace, certificação, enterprise tiers |
| 2035 | Open Standard | ISO/IEC, adoção governamental, 1M+ builders |

### Princípios do Roadmap
1. **Spec first, code second** — Toda feature começa como especificação
2. **Backward compatibility** — Breaking changes exigem MAJOR version bump
3. **Content over features** — Grandes pacotes importam mais que grandes ferramentas
4. **Community before company** — Ecossistema sobrevive a qualquer organização
5. **Ten-year thinking** — Toda decisão defensável em 2035

---

## 14. O Que Pode e O Que Não Pode Mudar

### PODE MUDAR
- Tecnologias, linguagens, interfaces
- Modelos de IA, metodologias, ferramentas
- Estruturas organizacionais
- Implementação de repositórios (SQLite → PostgreSQL)
- Estratégias de execução (local, AI, team, classroom)
- Interface CLI (argparse → typer/click)
- Detalhes do AssessmentPipeline (scoring algorithm)

### NÃO PODE MUDAR
- North Star: "Toda competência reivindicada deve ser comprovada"
- Os 7 First Principles
- Os 10 Architectural Invariants (I1–I10)
- Domain nunca depende de Infrastructure (I1)
- Conteúdo é dado, nunca código (I4)
- IA nunca altera regras de negócio (I5)
- Núcleo funciona offline (I6)
- Dados pertencem ao usuário (I8)
- Camadas comunicam-se apenas para dentro (I9)
- Repositórios são contratos, não implementações (I10)
- Engine é agnóstica a domínio
- AI é camada substituível, não o core
- v1 architecture está congelada — sem mudanças sem aprovação do TSC

---

## 15. Decisões Congeladas (v1)

Estas decisões não podem ser revertidas sem aprovação do Technical Steering Committee:

1. **Engine First** — Engine é agnóstica a domínio
2. **Content as Data** — Pacotes independentes, Engine apenas interpreta
3. **AI as Layer** — IA é camada substituível
4. **Evidence Driven** — Evidência é a unidade mais importante
5. **CLI-First MVP** — Python + SQLite + argparse
6. **Local First** — Dados pertencem ao usuário
7. **v1 Frozen** — Arquitetura da v1 não será modificada
8. **Spec first, code second** — Toda feature começa como especificação
9. **Engine agnóstica a domínio** — Engine não sabe o que está executando, apenas como executar
10. **Content as Data** — Pacotes são YAML, nunca Python executável

---

## Apêndice: Convenções de Código

### Naming
- Classes: PascalCase
- Funções/métodos: snake_case
- Constantes: UPPER_SNAKE_CASE
- Arquivos: snake_case.py
- IDs: kebab-case

### Padrões Arquiteturais
- **Domain**: dataclasses puras, sem dependências externas
- **Application**: Services + Commands + DTOs + Protocols
- **Infrastructure**: Implementações concretas (SQLite, EventBus)
- **Runtime**: Kernel + Orchestrator + Runners (Visitor Pattern)
- **Package Engine**: Parser → Validator → Loader (Pipeline)

### Testes
- pytest com pytest-cov
- Testes unitários para domain (sem banco, sem IA)
- Testes de integração para infrastructure
- Testes de runtime com pacotes de referência
- Cobertura mínima: 80%

---

*Documento gerado em 2026-07-19. v1.0.*
*Próxima revisão: quando houver mudança arquitetural significativa.*
