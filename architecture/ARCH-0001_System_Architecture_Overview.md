# ARCH-0001 — System Architecture Overview

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0001 |
| **Nome** | System Architecture Overview |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0007 Engineering Philosophy |
| **Depende de** | Nenhum documento arquitetural anterior |
| **Será utilizado por** | ARCH-0002 Domain Model, ARCH-0003 Core Engine Spec, ARCH-0004 Agent Architecture, ARCH-0005 Data Model, ARCH-0006 MVP Technical Specification |

---

## 1. Architecture Vision

### Objetivo

Construir uma infraestrutura de desenvolvimento de competências onde:

- conhecimento é transformado em prática;
- prática gera evidência;
- evidência comprova competência;
- inteligência artificial acelera evolução humana.

A arquitetura deve permitir que o sistema cresça de uma **ferramenta pessoal de aprendizagem** para um **ecossistema global de desenvolvimento de competências**.

---

## 2. Architectural Thesis

A decisão central da arquitetura é:

> **Separar o modelo de competência da implementação tecnológica.**

O sistema deve funcionar como uma camada independente entre:

- pessoas;
- conhecimento;
- ferramentas;
- inteligência artificial.

### Representação

```
                 COMPETENCY MODEL
                       │
                       ▼
                  CORE ENGINE
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
    Interfaces      AI Agents      Packages
        │              │              │
        ▼              ▼              ▼
             External Ecosystem
```

---

## 3. Core Architectural Principles

### 3.1 Engine First

A Engine é o núcleo.

**Ela não sabe:**
- ensinar Cyber;
- ensinar programação;
- ensinar Cloud.

**Ela sabe:**
- gerenciar competências;
- executar missões;
- validar evidências;
- acompanhar evolução.

### 3.2 Content as Data

Conteúdo não fica preso ao código. Ele existe como **pacote independente**.

```
packages/
├── cyber-security/
├── software-development/
├── cloud-engineering/
└── artificial-intelligence/
```

A Engine apenas **interpreta** esses pacotes.

### 3.3 AI as Layer

IA não é o núcleo. **IA é uma camada.**

Isso evita dependência de:
- OpenAI;
- Anthropic;
- modelos futuros.

```
Core Engine
      ▲
      │
AI Interface Layer
      ▲
      │
Model Providers
```

### 3.4 Evidence Driven

A unidade mais importante do sistema não é o conteúdo. **É a evidência.**

```
Mission
 ↓
Challenge
 ↓
Artifact
 ↓
Review
 ↓
Competency Evidence
```

---

## 4. System Context

Visão externa do sistema.

```
                 Builder
                    │
                    ▼
 ┌─────────────────────────────────┐
 │                                 │
 │        ASCEND SYSTEM            │
 │                                 │
 │  ┌───────────────────────────┐  │
 │  │    Competency Engine      │  │
 │  │                           │  │
 │  │  • Missions               │  │
 │  │  • Evidence               │  │
 │  │  • Progress               │  │
 │  │  • Assessment             │  │
 │  │                           │  │
 │  └───────────────────────────┘  │
 │                                 │
 └─────────────────────────────────┘
        │                 │
        ▼                 ▼
    AI Providers      Git Ecosystem
```

---

## 5. Major System Components

### Component 1 — Core Engine

**Responsabilidade:** Executar o modelo de competência.

| Contém | Não contém |
|--------|------------|
| Regras | Conteúdo |
| Estados | Interface |
| Progresso | Modelos de IA |
| Validação | — |
| Eventos | — |

### Component 2 — Mission System

Responsável por transformar objetivos em desafios executáveis.

```yaml
mission:
  id: linux-basic-001
  objective:
    "Gerenciar usuários Linux"
  challenge:
    "Criar e documentar um ambiente Linux"
  evidence:
    - commands.log
    - report.md
    - screenshot.png
```

### Component 3 — Evidence System

**O coração da North Star.**

Responsável por:
- armazenar evidências;
- classificar;
- versionar;
- revisar.

| Tipo | Descrição |
|------|-----------|
| **Code** | Código fonte, scripts, configurações |
| **Document** | Relatórios, análises, documentação |
| **Project** | Projetos completos com múltiplos artefatos |
| **Presentation** | Explicações, apresentações técnicas |
| **Analysis** | Investigações, diagnósticos |
| **Experiment** | Testes, PoCs, protótipos |

### Component 4 — Progress System

Gerencia:
- jornada;
- níveis;
- XP;
- conquistas;
- evolução.

### Component 5 — Agent Layer

Camada inteligente. Cada agente possui: **missão, limites, contexto, ferramentas permitidas.**

| Agente | Propósito |
|--------|-----------|
| **Mentor Agent** | Guia estratégico da jornada |
| **Teacher Agent** | Explica conceitos e fundamenta |
| **Reviewer Agent** | Avalia evidências e fornece feedback |
| **Interviewer Agent** | Valida competência por questionamento |
| **Career Agent** | Orienta direção profissional |

### Component 6 — Package System

Permite expansão do ecossistema.

```
ascend-cyber/
ascend-dev/
ascend-cloud/
ascend-data/
```

Cada pacote contém:

| Componente | Descrição |
|------------|-----------|
| `missions/` | Missões e desafios |
| `skills/` | Habilidades e critérios |
| `assessments/` | Avaliações e Boss Fights |
| `resources/` | Materiais de referência |
| `projects/` | Projetos integradores |

---

## 6. Data Flow

Fluxo principal do sistema:

```
Builder chooses Journey
          │
          ▼
Mission generated
          │
          ▼
Builder performs Challenge
          │
          ▼
Evidence submitted
          │
          ▼
Reviewer evaluates
          │
          ▼
Competency updated
          │
          ▼
New Mission unlocked
```

---

## 7. Extension Model

O sistema deve permitir extensões em 4 dimensões:

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| **Learning Packages** | Novas áreas de competência | `ascend-devops`, `ascend-ml` |
| **AI Agents** | Novos especialistas | `Security Reviewer`, `Code Mentor` |
| **Interfaces** | Novas experiências | Web UI, Mobile, IDE Plugin |
| **Integrations** | Ferramentas externas | GitHub, GitLab, Jira |

---

## 8. Security Architecture

Mesmo sendo educacional, segurança é princípio fundamental.

| Princípio | Descrição |
|-----------|-----------|
| **Least Privilege** | Cada componente possui apenas permissões necessárias |
| **Local First** | Dados pertencem ao usuário |
| **Transparency** | Decisões automatizadas devem ser explicáveis |
| **Privacy by Design** | Coleta mínima de dados |

---

## 9. Scalability Strategy

A evolução será em camadas:

| Fase | Escopo | Características |
|------|--------|-----------------|
| **Fase 1** | CLI local | Single User, Local Storage |
| **Fase 2** | Aplicação web | Multi User, Cloud Storage |
| **Fase 3** | Ecossistema | Community, Marketplace, Organizations |

---

## 10. Technology Independence

A arquitetura **não deve depender de:**

- linguagem específica;
- framework específico;
- fornecedor de IA.

> **Tecnologias são substituíveis. Princípios não.**

---

## Architecture Overview Diagram

```
              ASCEND CDF
                   │
             Core Engine
                   │
      ┌────────────┼────────────┐
      │            │            │
 Mission      Evidence       Progress
 Engine       Engine         Engine
      │            │            │
      └────────────┼────────────┘
                   │
              Agent Layer
                   │
        Mentor │ Reviewer │ Teacher
                   │
              Data Layer
                   │
             CLI Interface
```

---

## Definition of Architecture Success

ARCH-0001 será considerado aprovado quando:

- [ ] qualquer engenheiro conseguir entender o sistema;
- [ ] novos módulos puderem ser adicionados sem alterar o núcleo;
- [ ] a Engine permanecer independente do conteúdo;
- [ ] a IA permanecer substituível;
- [ ] a evidência continuar sendo o centro do modelo.
