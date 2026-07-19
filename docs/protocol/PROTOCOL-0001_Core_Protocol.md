# PROTOCOL-0001 — Core Protocol

| Campo | Valor |
|-------|-------|
| **ID** | PROTOCOL-0001 |
| **Nome** | Core Protocol |
| **Versão** | 1.0 |
| **Status** | Stable |
| **Categoria** | Protocol |
| **Owner** | Chief Architect |
| **Derivado de** | Constituição, DOC-0006 Lexicon, ARCH-0001, ARCH-0002, ARCH-0008 |
| **Linguagem** | Independente |

---

## 1. Propósito

Este protocolo define o **vocabulário oficial**, as **entidades fundamentais**, os **identificadores**, as **relações**, as **regras universais** e o **ciclo de vida** do ASCEND.

Ele é a fonte de verdade para qualquer implementação — Python, Rust, TypeScript ou qualquer outra linguagem.

---

## 2. Vocabulário Oficial

### 2.1 Termos Proibidos

| Termo | Substituir por | Motivo |
|-------|---------------|--------|
| Aluno | Builder | Modelo passivo vs. ativo |
| Estudante | Builder | Mesmo motivo |
| Curso | Package | Curso implica consumo; package implica prática |
| Aula | Mission | Aula é passiva; missão é ativa |
| Prova | Assessment | Prova mede memorização; assessment mede capacidade |
| Certificado | Competency Record | Certificado é papel; competency record é evidência |
| Professor | Mentor | Professor ensina; mentor guia |
| Nota | Score | Nota é numérica; score é multi-dimensional |
| Matéria | Competency Domain | Matéria é conteúdo; competency domain é capacidade |
| Turma | Cohort | Turma é escolar; cohort é profissional |

### 2.2 Termos Oficiais

| Termo | Definição | Exemplo |
|-------|-----------|---------|
| **Builder** | Pessoa que desenvolve e demonstra competências | `builder:alex` |
| **Competency** | Capacidade demonstrável de aplicar conhecimento | `comp:linux-admin` |
| **Skill** | Elemento atômico que compõe uma competência | `skill:user-management` |
| **Journey** | Trajetória organizada para desenvolver competências | `journey:linux-foundations` |
| **Mission** | Unidade atômica de execução com desafio e evidência | `mission:linux-001` |
| **Challenge** | Problema ou tarefa que o builder deve resolver | Descrito em YAML |
| **Evidence** | Artefato produzido pelo builder como prova | Código, relatório, projeto |
| **Assessment** | Processo de avaliação da evidência contra critérios | Score, feedback |
| **Rubric** | Conjunto de critérios ponderados para avaliação | `rubric:linux-basics` |
| **Achievement** | Conquista especial por critérios específicos | `ach:linux-builder` |
| **Package** | Unidade autossuficiente de conteúdo (APS) | `pkg:cyber-foundations` |
| **Runtime** | Motor que orquestra a execução de packages | `RuntimeKernel` |
| **Engine** | Núcleo lógico que processa o ciclo de competência | `CompetencyEngine` |
| **Agent** | Entidade inteligente especializada (IA ou humana) | `agent:reviewer` |
| **XP** | Pontos de experiência (progressão no sistema) | `xp:1250` |
| **Level** | Indicador de progressão global do builder | `level:3` |
| **Mastery Threshold** | Percentual mínimo para desbloquear competência | `threshold:0.7` |

### 2.3 Prefixos de Identificação

| Entidade | Prefixo | Exemplo |
|----------|---------|---------|
| Builder | `builder:` | `builder:alex-1234` |
| Competency | `comp:` | `comp:linux-admin` |
| Skill | `skill:` | `skill:user-management` |
| Journey | `journey:` | `journey:linux-foundations` |
| Mission | `mission:` | `mission:linux-001` |
| Evidence | `ev:` | `ev:a1b2c3d4` |
| Assessment | `ass:` | `ass:e5f6g7h8` |
| Achievement | `ach:` | `ach:linux-builder` |
| Package | `pkg:` | `pkg:cyber-foundations` |
| Agent | `agent:` | `agent:reviewer-v1` |
| Event | `evt:` | `evt:mission-started-001` |
| Runtime Event | `revt:` | `revt:package-loaded-001` |
| Policy Decision | `pol:` | `pol:a1b2c3d4` |
| Trace | `trace:` | `trace:exec-2026-001` |

---

## 3. Entidades Oficiais

### 3.1 Builder

```
Builder {
    id:          BuilderId        (prefixo: "builder:")
    username:    string           (3-32 chars, alfanumérico)
    level:       Level            (int >= 1)
    xp:          XP               (int >= 0)
    competencies: list<CompetencyId>
    achievements: list<AchievementId>
    missions:    list<MissionStatus>
    evidence:    list<EvidenceId>
    created_at:  Timestamp
}
```

### 3.2 Competency

```
Competency {
    id:          CompetencyId     (prefixo: "comp:")
    name:        string
    description: string
    domain:      string
    level:       int              (1-5)
    criteria:    list<string>
    skills:      list<SkillId>
    mastery_threshold: float      (0.0 - 1.0, default: 0.7)
}
```

### 3.3 Skill

```
Skill {
    id:          SkillId          (prefixo: "skill:")
    name:        string
    description: string
    weight:      float            (0.0 - 1.0, soma = 1.0 por competency)
}
```

### 3.4 Journey

```
Journey {
    id:          JourneyId        (prefixo: "journey:")
    name:        string
    objective:   string
    missions:    list<MissionId>  (ordenada)
    competencies: list<CompetencyId>
    prerequisites: list<JourneyId>
    status:      JourneyStatus
}
```

### 3.5 Mission

```
Mission {
    id:          MissionId        (prefixo: "mission:")
    title:       string
    objective:   string
    difficulty:  Difficulty       (beginner, intermediate, advanced, expert)
    xp_reward:   int              (> 0)
    prerequisites: list<MissionId>
    evidence_required: bool
    challenge:   Challenge
    rubric_id:   RubricId | nil
    status:      MissionStatus
}
```

### 3.6 Challenge

```
Challenge {
    description: string
    requirements: list<string>
    validation_rules: list<string> | nil
}
```

### 3.7 Evidence

```
Evidence {
    id:          EvidenceId       (prefixo: "ev:")
    builder_id:  BuilderId
    mission_id:  MissionId
    type:        EvidenceType     (code, document, project, report, presentation, analysis, experiment)
    artifact:    string           (texto ou path)
    status:      EvidenceStatus
    submitted_at: Timestamp
}
```

### 3.8 Assessment

```
Assessment {
    id:          AssessmentId     (prefixo: "ass:")
    evidence_id: EvidenceId
    reviewer:    ReviewerType     (builtin, ai, human, hybrid)
    score:       float            (0.0 - 1.0)
    percentage:  float            (0.0 - 100.0)
    passed:      bool             (score >= threshold)
    feedback:    string
    rubric_id:   RubricId | nil
    created_at:  Timestamp
}
```

### 3.9 Rubric

```
Rubric {
    id:          RubricId         (prefixo: "rubric:")
    name:        string
    criteria:    list<RubricCriterion>
}

RubricCriterion {
    name:        string
    weight:      int              (soma = 100)
    description: string
}
```

### 3.10 Achievement

```
Achievement {
    id:          AchievementId    (prefixo: "ach:")
    name:        string
    description: string
    criteria:    string           (expressão textual avaliada)
    badge:       string | nil
}
```

### 3.11 Package

```
Package {
    id:          PackageId        (prefixo: "pkg:")
    version:     SemVer
    title:       string
    description: string
    author:      string
    license:     string           (SPDX)
    runtime:     string           (ex: ">=1.0")
    language:    string           (BCP 47)
    estimated_hours: int
    dependencies: list<PackageId>
    capabilities: list<Capability>
    journeys:    list<Journey>
    competencies: list<CompetencyDef>
    achievements: list<AchievementDef>
    rubrics:     list<Rubric>
}
```

---

## 4. Identificadores

### 4.1 Regras de Formação

| Regra | Descrição | Exemplo Válido | Exemplo Inválido |
|-------|-----------|----------------|-------------------|
| Prefixo obrigatório | Toda entidade tem prefixo | `builder:alex` | `alex` |
| kebab-case | IDs em kebab-case | `comp:linux-admin` | `comp:linux_admin` |
| 1-64 caracteres | Limite de tamanho | `mission:linux-user-administration-basics` | (64+ chars) |
| Sem espaços | IDs sem espaços | `journey:linux-foundations` | `journey:linux foundations` |
| Sem caracteres especiais | Apenas a-z, 0-9, hífen | `skill:user-management` | `skill:user_management!` |

### 4.2 Geração de IDs

- **Entidades de domínio** (Builder, Competency, etc.): definidos em YAML (kebab-case)
- **Entidades de runtime** (Evidence, Assessment, Event): gerados por hash (prefixo + uuid4 truncado)
- **Trace IDs**: `trace:{execution_id}-{timestamp}`

---

## 5. Relações

### 5.1 Diagrama de Relações

```
Package 1 ──── N Journey
Journey 1 ──── N Mission
Mission 1 ──── 1 Challenge
Mission 1 ──── 0..1 Rubric
Builder N ──── N Journey
Builder 1 ──── N Evidence
Builder 1 ──── N Competency
Builder 1 ──── N Achievement
Evidence 1 ──── 1 Assessment
Evidence N ──── 1 Mission
Competency 1 ──── N Skill
Competency N ──── N Builder
Achievement N ──── N Builder
Package 1 ──── N CompetencyDef
Package 1 ──── N AchievementDef
Package 1 ──── N Rubric
```

### 5.2 Cardinalidades

| Origem | Destino | Cardinalidade | Descrição |
|--------|---------|---------------|-----------|
| Package | Journey | 1:N | Um pacote contém N jornadas |
| Journey | Mission | 1:N | Uma jornada contém N missões |
| Mission | Challenge | 1:1 | Cada missão tem exatamente um desafio |
| Mission | Rubric | 1:0..1 | Missão pode ter ou não uma rubrica |
| Builder | Journey | N:N | Builder participa de N jornadas |
| Builder | Evidence | 1:N | Builder produz N evidências |
| Builder | Competency | N:N | Builder possui N competências |
| Builder | Achievement | N:N | Builder conquista N achievements |
| Evidence | Assessment | 1:1 | Cada evidência gera um assessment |
| Evidence | Mission | N:1 | N evidências por missão |
| Competency | Skill | 1:N | Competência composta por N skills |
| Package | CompetencyDef | 1:N | Pacote define N competências |
| Package | AchievementDef | 1:N | Pacote define N achievements |
| Package | Rubric | 1:N | Pacote define N rubricas |

---

## 6. Regras Universais

### 6.1 Regras de Identidade

| # | Regra | Descrição |
|---|-------|-----------|
| U1 | Toda entidade tem um ID único | Nenhuma entidade existe sem identificador |
| U2 | IDs são imutáveis | Uma vez atribuído, o ID nunca muda |
| U3 | Prefixo define o tipo | O prefixo do ID determina a entidade |
| U4 | IDs são legíveis por humanos | Preferir kebab-case descritivo sobre UUIDs |

### 6.2 Regras de Estado

| # | Regra | Descrição |
|---|-------|-----------|
| U5 | Toda entidade mutável tem estado | Entidades que mudam no tempo têm um campo `status` |
| U6 | Estado não regride | Nenhuma transição retorna a estado anterior |
| U7 | Estados terminais são finais | COMPLETED, FAILED, CANCELLED não mudam |
| U8 | Toda transição gera evento | Toda mudança de estado produz um DomainEvent |

### 6.3 Regras de Evidência

| # | Regra | Descrição |
|---|-------|-----------|
| U9 | Evidência precede competência | Nenhuma competência sem evidência avaliada |
| U10 | Evidência é imutável | Uma vez registrada, evidência não é alterada |
| U11 | Evidência pertence ao builder | O builder é dono da evidência |
| U12 | Evidência é rastreável | Toda evidência tem origem, data e contexto |

### 6.4 Regras de Execução

| # | Regra | Descrição |
|---|-------|-----------|
| U13 | Runtime é síncrono | Kernel executa em uma thread, sem async |
| U14 | Runtime é determinístico | Mesmo input → mesmo output (sem IA) |
| U15 | Conteúdo é dado | Packages são YAML, nunca código executável |
| U16 | IA é opcional | Sistema funciona sem agentes de IA |

### 6.5 Regras de Dados

| # | Regra | Descrição |
|---|-------|-----------|
| U17 | Dados são locais | Banco SQLite no dispositivo do usuário |
| U18 | Sem telemetria obrigatória | Nenhum dado enviado sem consentimento |
| U19 | Repositórios são contratos | Application conhece interfaces, não implementações |
| U20 | Camadas comunicam-se para dentro | Presentation → Application → Domain → Infrastructure |

---

## 7. Ciclo de Vida das Entidades

### 7.1 Builder Lifecycle

```
CREATED → ACTIVE → INACTIVE → ARCHIVED
```

| Transição | Gatilho | Evento |
|-----------|---------|--------|
| CREATED → ACTIVE | Primeira missão iniciada | BuilderActivated |
| ACTIVE → INACTIVE | Inatividade por N dias | BuilderDeactivated |
| INACTIVE → ACTIVE | Nova missão iniciada | BuilderReactivated |
| ACTIVE → ARCHIVED | Solicitação do builder | BuilderArchived |

### 7.2 Mission Lifecycle (Domain)

Conforme ARCH-0008:

```
NOT_STARTED → AVAILABLE → IN_PROGRESS → EVIDENCE_PENDING → ASSESSING → COMPLETED
                                                                              ↓
                                                                     COMPETENCY_UNLOCKED → ACHIEVEMENT_GRANTED
```

### 7.3 Evidence Lifecycle

```
CREATED → SUBMITTED → VALIDATED → ASSESSED → ARCHIVED
                         ↓
                     REJECTED → RESUBMITTED
```

### 7.4 Assessment Lifecycle

```
PENDING → IN_PROGRESS → COMPLETED
                  ↓
              FAILED → RETRY
```

### 7.5 Competency Lifecycle

```
LOCKED → AVAILABLE → IN_PROGRESS → UNLOCKED → MASTERED
```

### 7.6 Achievement Lifecycle

```
NOT_EARNED → EARNED → REVOKED
```

### 7.7 Package Lifecycle

```
DRAFT → VALIDATED → PUBLISHED → DEPRECATED → RETIRED
```

### 7.8 Runtime Lifecycle

Conforme ARCH-0009:

```
IDLE → LOADING → VALIDATING → CONVERTING → READY → EXECUTING → REPORTING → COMPLETED
                                                              ↓
                                                          FAILED / CANCELLED
```

---

## 8. Compliance com a Constituição

| Regra Universal | Constituição | First Principle | Invariante |
|----------------|-------------|----------------|------------|
| U1 | DOC-0004 | — | — |
| U2 | DOC-0004 | — | — |
| U3 | DOC-0006 | — | — |
| U4 | DOC-0006 | — | — |
| U5 | ARCH-0003 | Lei 2 (State Driven) | — |
| U6 | ARCH-0008 | — | CL-006 |
| U7 | ARCH-0009 | — | — |
| U8 | ARCH-0008 | Lei 3 (Event Driven) | I-003 |
| U9 | North Star | P1 | I-002 |
| U10 | — | P7 | — |
| U11 | — | — | I-008 |
| U12 | — | — | I-003 |
| U13 | SPEC-0002 (AEP) | — | — |
| U14 | ARCH-0009 | — | — |
| U15 | ADR-002 | — | I-004 |
| U16 | ADR-003 | P3 | I-005 |
| U17 | ADR-004 | — | I-006, I-008 |
| U18 | ADR-004 | — | I-008 |
| U19 | — | — | I-010 |
| U20 | — | — | I-009 |

---

## 9. Declaração Final

> **PROTOCOL-0001 é a fonte de verdade terminológica do ASCEND.**
>
> Nenhuma implementação, documentação ou comunicação pode usar termos que contradizem este protocolo.
>
> Se uma palavra não está aqui, ela não faz parte do vocabulário oficial do ASCEND.
>
> Se uma relação não está aqui, ela não existe no modelo de domínio.
>
> Se uma regra não está aqui, ela não é universal.
