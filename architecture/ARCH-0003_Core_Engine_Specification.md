# ARCH-0003 — Core Engine Specification

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0003 |
| **Nome** | Core Engine Specification |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0007 Engineering Philosophy, ARCH-0001 System Architecture Overview, ARCH-0002 Domain Model |
| **Será utilizado por** | ARCH-0005 Data Model, ARCH-0006 MVP Technical Specification, Implementation Phase |

---

## 1. Core Engine Definition

A **Core Engine** é o núcleo lógico do ASCEND.

Ela é responsável por transformar:

```
intenção
    ↓
jornada
    ↓
missões
    ↓
ações
    ↓
evidências
    ↓
competências comprovadas
```

A Engine **NÃO** é:

- uma plataforma de cursos
- um LMS
- um chatbot
- um gerenciador de vídeos
- um sistema de certificados

A Engine **É**:

> Um sistema operacional para desenvolvimento e comprovação de competências.

---

## 2. Core Engine Philosophy

A Engine segue **cinco leis**:

### Lei 1 — Evidence First

A evidência é o centro do sistema.

Não existe:

> Missão concluída

sem:

> Evidência analisada

### Lei 2 — State Driven

Tudo possui estado.

**Exemplo (Mission):**

```
LOCKED
    ↓
AVAILABLE
    ↓
ACTIVE
    ↓
SUBMITTED
    ↓
REVIEWED
    ↓
COMPLETED
```

### Lei 3 — Event Driven

Mudanças importantes geram eventos.

**Exemplo:**

```
EvidenceSubmitted
    ↓
ReviewRequested
    ↓
CompetencyUpdated
    ↓
AchievementUnlocked
```

### Lei 4 — Human Centric

A máquina acompanha.  
O humano evolui.

### Lei 5 — Provider Independent

A Engine não depende de:

- IA específica
- banco específico
- interface específica

---

## 3. Core Engine Components

### Component 1 — Mission Engine

**Responsabilidade:** Gerenciar objetivos e desafios.

- **Entrada:** Mission Package
- **Saída:** Active Mission
- **Funções:**
  - `createMission()`
  - `startMission()`
  - `trackProgress()`
  - `completeMission()`

---

### Component 2 — Evidence Engine

**O componente mais importante.**

**Responsável por:**
- receber evidências
- validar formato
- enviar para revisão
- armazenar histórico

**Fluxo:**

```
Builder
    ↓
Artifact
    ↓
Evidence Record
    ↓
Review
    ↓
Validation
```

---

### Component 3 — Competency Engine

**Responsável por evolução.**

**Modelo:**

```
Skill
    ↓
Competency
    ↓
Mastery Level
```

**Exemplo (Linux):**

```
Level 1: Executa comandos básicos
Level 2: Administra usuários
Level 3: Protege sistema
Level 4: Projeta arquitetura
```

---

### Component 4 — Progress Engine

**Responsável por:**
- XP
- níveis
- progresso
- conquistas

**Modelo:**

```
Progress:
  XP
  Level
  Completed Missions
  Competencies
  Achievements
```

---

### Component 5 — Assessment Engine

**Responsável pela avaliação.**

Não responde: *"Passou ou falhou?"*

Responde: *"Qual nível de competência foi demonstrado?"*

**Modelo:**

```
Assessment:
  criteria:
    - Technical Accuracy
    - Practical Execution
    - Explanation Quality
    - Problem Solving
  score:
  feedback:
```

---

### Component 6 — Package Engine

**Permite expansão infinita.**

**Exemplo:**

```
packages/
  cyber-security/
  software-engineering/
  cloud/
  ai/
```

Cada pacote possui:

- skills
- missions
- projects
- assessments
- resources

---

### Component 7 — Agent Interface Layer

A Engine conversa com agentes através de uma interface padrão.

**Exemplo:**

```python
Agent.review(evidence)
```

A Engine não sabe:

- qual modelo
- qual fornecedor
- qual prompt

---

## 4. Internal Architecture

```
                 CORE ENGINE
                     |
                    API
                     |
 ┌──────────────────────────────────┐
 │                                  │
 │        Domain Services           │
 │                                  │
 │ Mission │ Evidence │ Progress    │
 │                                  │
 └──────────────────────────────────┘
                     |
              Domain Events
                     |
             Persistence Layer
```

---

## 5. Engine State Machine

### Builder Lifecycle

```
CREATED
    ↓
EXPLORING
    ↓
BUILDING
    ↓
VALIDATING
    ↓
COMPETENT
    ↓
MENTORING
```

### Mission Lifecycle

```
LOCKED
    ↓
AVAILABLE
    ↓
ACTIVE
    ↓
EVIDENCE_PENDING
    ↓
UNDER_REVIEW
    ↓
COMPLETED
```

### Evidence Lifecycle

```
CREATED
    ↓
SUBMITTED
    ↓
REVIEWING
    ↓
ACCEPTED
    ↓
ARCHIVED
```

---

## 6. XP System

**Importante:** XP não mede valor humano.  
XP mede progresso dentro do sistema.

**Modelo inicial:**

```
Mission Complete:       +100
Quality Evidence:        +50
Peer Review:             +75
Open Source Contribution: +200
```

---

## 7. Achievement System

Conquistas são marcos.

**Exemplo:**

```yaml
Achievement:
  id: linux-builder
  condition: Complete 10 Linux missions
  reward: Badge
```

---

## 8. Rules Engine

Algumas regras são imutáveis:

```
IF competency evidence < required
THEN competency cannot advance
```

```
IF mission has no measurable outcome
THEN mission invalid
```

---

## 9. MVP Core Engine

A primeira versão **NÃO** terá tudo.

**MVP:**
- Builder
- Mission
- Evidence
- Progress
- Simple Review

**Não teremos inicialmente:**
- marketplace
- comunidade
- mobile
- ranking global
- certificação

---

## 10. Tecnologia Inicial Recomendada

Para o MVP:

| Camada | Tecnologia | Motivo |
|--------|-----------|--------|
| **Linguagem** | Python | excelente para IA, protótipo rápido, comunidade enorme |
| **Interface** | CLI | mínimo viável |
| **Persistência** | SQLite | zero configuração, embarcado |

**Estrutura:**

```
ascend/
├── engine/
├── domain/
├── missions/
├── evidence/
├── agents/
├── cli/
├── tests/
└── docs/
```

---

## Definition of Done

ARCH-0003 aprovado quando:

- [x] Engine possui responsabilidades claras
- [x] IA está desacoplada
- [x] Conteúdo está separado
- [x] Evidência é o centro
- [x] MVP pode ser implementado sem decisões arquiteturais abertas

---

## Status

**ARCH-0003 — Core Engine Specification**

- Estado: 🟡 Draft técnico
- Resultado: Núcleo lógico definido — 7 componentes, 5 leis, máquinas de estado, XP, achievements, regras imutáveis.
- Próximo: ARCH-0004 — Agent Architecture
