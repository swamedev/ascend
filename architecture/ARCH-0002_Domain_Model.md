# ARCH-0002 — Domain Model

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0002 |
| **Nome** | Domain Model |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0006 Lexicon, ARCH-0001 System Architecture Overview |
| **Será utilizado por** | ARCH-0003 Core Engine Specification, ARCH-0005 Data Model, MVP Implementation |

---

## 1. Domain Vision

O domínio central do ASCEND é:

> **Desenvolvimento, demonstração e evolução de competências humanas.**

O sistema não modela cursos.  
Não modela aulas.  
Não modela consumo de conteúdo.

Ele modela:

```
Pessoa
 ↓
Jornada
 ↓
Missões
 ↓
Desafios
 ↓
Evidências
 ↓
Competências
```

---

## 2. Bounded Contexts

O domínio será dividido em contextos independentes.

```
ASCEND DOMAIN

┌─────────────────────────┐
│ Competency Context      │
│                         │
│ Skills                 │
│ Competencies           │
│ Levels                 │
└─────────────────────────┘

┌─────────────────────────┐
│ Learning Context        │
│                         │
│ Journeys                │
│ Missions                │
│ Challenges              │
└─────────────────────────┘

┌─────────────────────────┐
│ Evidence Context        │
│                         │
│ Artifacts               │
│ Reviews                 │
│ Validation              │
└─────────────────────────┘

┌─────────────────────────┐
│ Identity Context        │
│                         │
│ Builder                 │
│ Profile                 │
│ Achievements            │
└─────────────────────────┘

┌─────────────────────────┐
│ AI Context              │
│                         │
│ Agents                  │
│ Conversations           │
│ Recommendations         │
└─────────────────────────┘
```

---

## 3. Core Domain Entities

### Entity 1 — Builder

**Definição**

A pessoa que utiliza o ecossistema para desenvolver competências.

Substitui:

- ❌ aluno
- ❌ estudante

Porque nosso modelo não é passivo.

**Características**

```
Builder:
  id
  identity
  competencies
  journeys
  evidence
  achievements
  progression
```

**Regra de domínio**

Um Builder não é definido pelo conteúdo consumido.  
É definido pelas competências demonstradas.

---

### Entity 2 — Competency

**Definição**

Capacidade demonstrável de executar uma atividade dentro de um contexto.

**Exemplo:**

Não: *"Conhece Linux"*

Mas: *"Consegue administrar um ambiente Linux básico e justificar suas decisões."*

**Modelo:**

```
Competency:
  name
  description
  level
  criteria
  evidence_required
```

---

### Entity 3 — Skill

**Definição**

Elemento menor que compõe uma competência.

**Exemplo:**

Competência: *"Administrar servidor Linux"*

Possui Skills:

- Terminal
- Filesystem
- Users
- Permissions
- Processes

**Hierarquia:**

```
Skill
 ↓
Competency
 ↓
Mastery
```

---

### Entity 4 — Journey

**Definição**

A trajetória organizada para desenvolver uma ou mais competências.

**Exemplo:**

```
Cyber Security Journey
    ↓
Linux Foundations
    ↓
Networking
    ↓
Security Fundamentals
```

**Modelo:**

```
Journey:
  name
  objective
  competencies
  missions
  status
```

---

### Entity 5 — Mission

**Definição**

Uma unidade de progresso dentro de uma jornada.

**Modelo:**

```
Mission:
  objective
  difficulty
  prerequisites
  challenge
  evidence_required
  reward
```

**Exemplo:**

```
Mission: "Configurar um servidor Linux seguro"
Objetivo: Demonstrar capacidade de configurar usuários,
          permissões e serviços básicos.
Evidência:
  - configuração
  - relatório
  - explicação
```

---

### Entity 6 — Challenge

**Definição**

A atividade prática que força aplicação do conhecimento.

**Diferença:**

- Mission = objetivo.
- Challenge = execução.

**Fluxo:**

```
Mission
↓
Challenge
↓
Artifact
```

---

### Entity 7 — Evidence

**Definição**

Prova observável da competência desenvolvida.

**Esta é a entidade mais importante.**

**Tipos:**

- Code
- Document
- Report
- Project
- Experiment
- Presentation
- Analysis

**Modelo:**

```
Evidence:
  type
  artifact
  creator
  timestamp
  review
  competencies_supported
```

---

### Entity 8 — Assessment

**Definição**

Processo de avaliação da evidência.

Não é uma prova tradicional.  
É uma análise de capacidade.

Pode ser realizada por:

- Mentor Agent
- Reviewer Agent
- Comunidade
- Especialista

---

### Entity 9 — Achievement

**Definição**

Reconhecimento de evolução.

**Exemplos:**

- First Mission Completed
- Linux Builder
- Security Explorer
- Open Source Contributor

---

### Entity 10 — Agent

**Definição**

Entidade inteligente especializada em uma função.

**Modelo:**

```
Agent:
  role
  capabilities
  permissions
  knowledge_scope
  interaction_rules
```

---

## 4. Domain Relationships

Modelo geral:

```
                 Builder
                    |
                    |
                 Journey
                    |
                    |
                Mission
                    |
                    |
               Challenge
                    |
                    |
                Evidence
                    |
                    |
              Assessment
                    |
                    |
              Competency
```

---

## 5. Domain Events

O sistema será orientado a eventos.

Eventos importantes:

- BuilderCreated
- JourneyStarted
- MissionStarted
- ChallengeCompleted
- EvidenceSubmitted
- EvidenceReviewed
- CompetencyUnlocked
- AchievementEarned
- LevelAdvanced

---

## 6. Aggregate Roots

Seguindo DDD:

### Builder Aggregate

Controla:
- identidade
- progresso
- evolução

### Journey Aggregate

Controla:
- missões
- sequência
- objetivos

### Competency Aggregate

Controla:
- níveis
- critérios
- evidências necessárias

---

## 7. Core Domain Rules

### Regra 1

Nenhuma competência é desbloqueada sem evidência.

### Regra 2

Toda missão deve ter objetivo mensurável.

### Regra 3

Toda avaliação deve possuir justificativa.

### Regra 4

Progressão não é baseada apenas em tempo.

### Regra 5

Conteúdo é substituível.  
Competência permanece.

---

## 8. Modelo Mental Final

```
              COMPETENCY
                  ▲
                  |
              EVIDENCE
                  ▲
                  |
              CHALLENGE
                  ▲
                  |
              MISSION
                  ▲
                  |
              JOURNEY
                  ▲
                  |
              BUILDER
```

---

## Status

**ARCH-0002 — Domain Model**

- Estado: 🟡 Draft técnico
- Resultado: Domínio principal definido.
- Próximo: ARCH-0003 — Core Engine Specification
