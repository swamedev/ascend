# ASCEND PROJECT — Full Context

## Directory Structure

- architecture\ARCH-0001_System_Architecture_Overview.md
- architecture\ARCH-0002_Domain_Model.md
- architecture\ARCH-0003_Core_Engine_Specification.md
- architecture\ARCH-0004_Agent_Architecture.md
- architecture\ARCH-0005_Data_Model.md
- architecture\ARCH-0006_MVP_Technical_Specification.md
- architecture\ARCH-0008_Persistence_Architecture.md
- CHANGELOG.md
- CONTEXT.md
- CONTRIBUTING.md
- docs\adr\ADR-026_Python_Version_Support.md
- docs\build\AGENT-0001_DeepSeek_Implementation_Profile.md
- docs\build\BUILD-0001_Implementation_Roadmap.md
- docs\build\CODEX_EXECUTION_PROMPT_v1.0.md
- docs\build\SPRINT-001_Core_Domain_Implementation.md
- docs\charter.md
- docs\spec\protocols\PROTO-0004_AEP.md
- docs\spec\SPEC-0001_APS_v1.md
- docs\spec\SPEC-0002_AEP_v1.md
- docs\spec\SPEC-0002_Package_Validation.md
- docs\spec\SPEC-0003_ARP_v1.md
- docs\spec\SPEC-0003_Registry_Protocol.md
- docs\spec\SPEC-0004_AAP_v1.md
- foundation\DOC-0000_North_Star.md
- foundation\DOC-0001_Project_Charter.md
- foundation\DOC-0002_Manifesto.md
- foundation\DOC-0003_First_Principles.md
- foundation\DOC-0004_Identity_Architecture.md
- foundation\DOC-0005_Brand_Architecture.md
- foundation\DOC-0006_Lexicon.md
- foundation\DOC-0007_Engineering_Philosophy.md
- foundation\DOC-0008_Project_Continuity_Protocol.md
- foundation\DOC-0009_Architectural_Invariants.md
- GOVERNANCE.md
- manifest.md
- opencode.json
- packages\cyber-foundations\achievements\achievements.yaml
- packages\cyber-foundations\assessments\rubrics.yaml
- packages\cyber-foundations\competencies\competencies.yaml
- packages\cyber-foundations\journeys\fundamentos-web\journey.yaml
- packages\cyber-foundations\journeys\fundamentos-web\missions\css-foundations\mission.yaml
- packages\cyber-foundations\journeys\fundamentos-web\missions\html-foundations\mission.yaml
- packages\cyber-foundations\journeys\logica-programacao\journey.yaml
- packages\cyber-foundations\journeys\logica-programacao\missions\python-basics\mission.yaml
- packages\cyber-foundations\package.yaml
- packages\git-foundations\achievements\achievements.yaml
- packages\git-foundations\assessments\rubrics.yaml
- packages\git-foundations\competencies\competencies.yaml
- packages\git-foundations\journeys\git-essentials\journey.yaml
- packages\git-foundations\journeys\git-essentials\missions\git-basics\mission.yaml
- packages\git-foundations\package.yaml
- packages\linux-foundations\achievements\achievements.yaml
- packages\linux-foundations\assessments\rubrics.yaml
- packages\linux-foundations\competencies\competencies.yaml
- packages\linux-foundations\journeys\linux-essentials\journey.yaml
- packages\linux-foundations\journeys\linux-essentials\missions\file-management\mission.yaml
- packages\linux-foundations\journeys\linux-essentials\missions\terminal-navigation\mission.yaml
- packages\linux-foundations\package.yaml
- packages\python-foundations\achievements\achievements.yaml
- packages\python-foundations\assessments\rubrics.yaml
- packages\python-foundations\competencies\competencies.yaml
- packages\python-foundations\journeys\python-essentials\journey.yaml
- packages\python-foundations\journeys\python-essentials\missions\python-syntax\mission.yaml
- packages\python-foundations\package.yaml
- pyproject.toml
- README.md
- ROADMAP_2035.md
- scripts\generate_summary.py
- src\ascend\__init__.py
- src\ascend\api\__init__.py
- src\ascend\api\runtime.py
- src\ascend\application\__init__.py
- src\ascend\application\commands\__init__.py
- src\ascend\application\commands\complete_assessment.py
- src\ascend\application\commands\create_builder.py
- src\ascend\application\commands\start_mission.py
- src\ascend\application\commands\submit_evidence.py
- src\ascend\application\commands\unlock_competency.py
- src\ascend\application\dto\__init__.py
- src\ascend\application\dto\builder_dto.py
- src\ascend\application\dto\evidence_dto.py
- src\ascend\application\dto\mission_dto.py
- src\ascend\application\exceptions.py
- src\ascend\application\interfaces\__init__.py
- src\ascend\application\interfaces\event_bus.py
- src\ascend\application\interfaces\repositories.py
- src\ascend\application\services\__init__.py
- src\ascend\application\services\builder_service.py
- src\ascend\application\services\competency_service.py
- src\ascend\application\services\mission_service.py
- src\ascend\cli\__init__.py
- src\ascend\cli\commands\__init__.py
- src\ascend\cli\main.py
- src\ascend\domain\__init__.py
- src\ascend\domain\achievement.py
- src\ascend\domain\assessment.py
- src\ascend\domain\builder.py
- src\ascend\domain\challenge.py
- src\ascend\domain\competency.py
- src\ascend\domain\events.py
- src\ascend\domain\evidence.py
- src\ascend\domain\journey.py
- src\ascend\domain\mission.py
- src\ascend\domain\skill.py
- src\ascend\infrastructure\__init__.py
- src\ascend\infrastructure\config\__init__.py
- src\ascend\infrastructure\config\settings.py
- src\ascend\infrastructure\events\__init__.py
- src\ascend\infrastructure\events\memory_event_bus.py
- src\ascend\infrastructure\persistence\__init__.py
- src\ascend\infrastructure\persistence\sqlite\__init__.py
- src\ascend\infrastructure\persistence\sqlite\builder_repository.py
- src\ascend\infrastructure\persistence\sqlite\connection.py
- src\ascend\infrastructure\persistence\sqlite\event_store.py
- src\ascend\infrastructure\persistence\sqlite\evidence_repository.py
- src\ascend\infrastructure\persistence\sqlite\migrations.py
- src\ascend\infrastructure\persistence\sqlite\mission_repository.py
- src\ascend\infrastructure\persistence\sqlite\repository_base.py
- src\ascend\infrastructure\uow.py
- src\ascend\package_engine\__init__.py
- src\ascend\package_engine\loader.py
- src\ascend\package_engine\models.py
- src\ascend\package_engine\parser.py
- src\ascend\package_engine\validator.py
- src\ascend\runtime\__init__.py
- src\ascend\runtime\adapters\__init__.py
- src\ascend\runtime\adapters\package_converter.py
- src\ascend\runtime\assessment\__init__.py
- src\ascend\runtime\assessment\pipeline.py
- src\ascend\runtime\competency\__init__.py
- src\ascend\runtime\competency\engine.py
- src\ascend\runtime\context.py
- src\ascend\runtime\events\__init__.py
- src\ascend\runtime\events\collector.py
- src\ascend\runtime\hooks.py
- src\ascend\runtime\kernel.py
- src\ascend\runtime\models.py
- src\ascend\runtime\orchestrator.py
- src\ascend\runtime\report.py
- src\ascend\runtime\runners\__init__.py
- src\ascend\runtime\runners\challenge_runner.py
- src\ascend\runtime\runners\journey_runner.py
- src\ascend\runtime\runners\mission_runner.py
- src\ascend\shared\__init__.py
- src\ascend\shared\clock.py
- src\ascend\shared\ids.py
- src\ascend\shared\result.py
- src\ascend\shared\types.py
- src\ascend\shared\value_objects.py
- src\ascend.egg-info\dependency_links.txt
- src\ascend.egg-info\requires.txt
- src\ascend.egg-info\SOURCES.txt
- src\ascend.egg-info\top_level.txt
- tests\__init__.py
- tests\test_api.py
- tests\test_application.py
- tests\test_bootstrap.py
- tests\test_domain.py
- tests\test_infrastructure.py
- tests\test_package_engine.py
- tests\test_runtime.py
- tools\manifest_rotator.py
- tools\replay_manifest.py
- tools\shadow_ledger_validator.py
- v1\STANDARD_EDITION.md
- v2\V2-0001_Adoption_Strategy.md
- v2\V2-0002_Community_Strategy.md
- v2\V2-0003_Content_Strategy.md
- v2\V2-0004_Institute_Strategy.md
- v2\V2-0005_Funding_Strategy.md


## File Contents


### architecture\ARCH-0001_System_Architecture_Overview.md

```markdown
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

```

### architecture\ARCH-0002_Domain_Model.md

```markdown
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

```

### architecture\ARCH-0003_Core_Engine_Specification.md

```markdown
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

```

### architecture\ARCH-0004_Agent_Architecture.md

```markdown
# ARCH-0004 — Agent Architecture

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0004 |
| **Nome** | Agent Architecture |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect + AI Systems Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0007 Engineering Philosophy, ARCH-0001 System Architecture Overview, ARCH-0003 Core Engine Specification |
| **Será utilizado por** | ARCH-0005 Data Model, MVP Implementation, Agent Development |

---

## 1. Agent Architecture Vision

O ASCEND utiliza inteligência artificial como uma **rede de especialistas**.

Não existe:

> "Uma IA que faz tudo."

Existe:

> "Um ecossistema de agentes com responsabilidades claras."

**Modelo:**

```
                    ASCEND AI SYSTEM

             Mentor Agent
                  │
        ┌─────────┼─────────┐
        │         │         │
   Teacher   Agent Router   Reviewer
        │         │         │
        └─────────┼─────────┘
                  │
        Career Agent — Research Agent
```

---

## 2. AI First Principles

Os agentes seguem as mesmas leis do ecossistema.

### Princípio 1 — Agentes orientam, não substituem

Um agente deve aumentar o raciocínio do Builder.  
Nunca entregar apenas uma resposta final.

### Princípio 2 — Todo feedback deve gerar evolução

A interação deve melhorar uma competência.  
Não apenas resolver uma tarefa.

### Princípio 3 — Contexto antes de resposta

O agente precisa entender:
- nível atual
- objetivo
- histórico
- evidências anteriores

### Princípio 4 — Transparência

O Builder deve saber:
- por que recebeu uma sugestão
- quais critérios foram usados

---

## 3. Agent Architecture Layers

```
                 USER
                  ↓
            Agent Interface
                  ↓
             Agent Router
                  ↓
        Specialized Agents
                  ↓
          Core Engine
                  ↓
             Knowledge
```

---

## 4. Agent Router

O **Router** decide qual agente deve atuar.

**Exemplo 1:**

Usuário: *"Não consigo entender permissões Linux"*

Router detecta: Linux + dificuldade técnica  
Envia para: **Teacher Agent**

**Exemplo 2:**

Usuário: *"Avalie meu projeto"*

Router detecta: Evidence Review  
Envia para: **Reviewer Agent**

---

## 5. Core Agents

### AGENT-001 — Mentor Agent

**Missão:** Guiar a jornada.

**Responsabilidades:**
- acompanhar progresso
- sugerir próximos passos
- manter motivação
- identificar bloqueios

**Não faz:**
- completar missões
- escrever projetos pelo usuário

**Personalidade:** Mentor experiente.

---

### AGENT-002 — Teacher Agent

**Missão:** Explicar conceitos.

**Responsabilidades:**
- simplificar
- criar analogias
- propor exercícios
- adaptar profundidade

**Exemplo:**

*"Explique redes para um iniciante"* → Teacher Agent

---

### AGENT-003 — Reviewer Agent

**Missão:** Avaliar evidências.

**Responsabilidades — Analisar:**
- qualidade técnica
- clareza
- boas práticas
- profundidade

**Saída:**

```
Review:
  strengths:
  weaknesses:
  recommendations:
  competency_level:
```

---

### AGENT-004 — Interviewer Agent

**Missão:** Preparar competência profissional.

**Responsabilidades — Simular:**
- entrevistas
- troubleshooting
- defesa técnica

**Exemplo:** *"Explique como proteger um servidor Linux."*

---

### AGENT-005 — Research Agent

**Missão:** Atualização de conhecimento.

**Responsabilidades:**
- buscar documentação
- comparar tecnologias
- resumir padrões

---

### AGENT-006 — Career Agent

**Missão:** Conectar competências ao mercado.

**Responsabilidades:**
- analisar gaps
- sugerir projetos
- preparar portfólio

---

## 6. Agent Contract

Todo agente deve possuir:

```
Agent:
  id:
  purpose:
  scope:
  allowed_actions:
  forbidden_actions:
  inputs:
  outputs:
  memory_policy:
```

**Exemplo:**

```yaml
id: reviewer-agent
purpose: Evaluate technical evidence
allowed:
  - Review code
forbidden:
  - Create replacement solution
```

---

## 7. Agent Memory Architecture

Memória dividida em camadas.

| Camada | Conteúdo |
|--------|----------|
| **Short Term Memory** | Contexto da conversa |
| **Journey Memory** | Histórico da evolução |
| **Competency Memory** | Conhecimentos demonstrados |
| **System Memory** | Regras do ASCEND |

**Modelo:**

```
Conversation
    ↓
Journey History
    ↓
Competency Profile
    ↓
Builder Identity
```

---

## 8. Agent Governance

Agentes possuem limites.

**Nenhum agente pode:**
- aprovar sua própria avaliação
- criar evidência falsa
- atribuir competência sozinho

**Regra:**
- AI pode **recomendar**
- Sistema **registra**
- Evidência **comprova**

---

## 9. Multi-Agent Workflow Example

Missão: *"Configurar servidor Linux seguro"*

```
Builder inicia missão
        ↓
Mentor Agent orienta
        ↓
Teacher Agent explica conceitos
        ↓
Builder constrói solução
        ↓
Evidence enviada
        ↓
Reviewer Agent avalia
        ↓
Competency atualizada
        ↓
Career Agent sugere próximo passo
```

---

## 10. MVP Agent Architecture

**Primeira versão — teremos somente:**

1. Mentor Agent
2. Reviewer Agent
3. Teacher Agent

**Não começaremos com seis agentes.**

**Motivo:** Complexidade.  
Primeiro validamos o loop fundamental.

---

## Definition of Done

ARCH-0004 aprovado quando:

- [x] Agentes possuem papéis claros
- [x] IA está desacoplada da Engine
- [x] Existem limites éticos
- [x] Existe governança
- [x] MVP é implementável

---

## Status

**ARCH-0004 — Agent Architecture**

- Estado: 🟡 Draft técnico
- Resultado: Arquitetura de agentes definida — 6 agentes especificados, router, contrato, memória multicamada, governança.
- Próximo: ARCH-0005 — Data Model

```

### architecture\ARCH-0005_Data_Model.md

```markdown
# ARCH-0005 — Data Model Specification

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0005 |
| **Nome** | Data Model Specification |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0006 Lexicon, ARCH-0002 Domain Model, ARCH-0003 Core Engine, ARCH-0004 Agent Architecture |

---

## 1. Data Model Philosophy

O modelo de dados deve refletir uma verdade:

> O sistema não armazena cursos.  
> O sistema armazena evolução de competência.

O banco não pergunta:

> ❌ *"Quantas aulas o usuário assistiu?"*

Ele pergunta:

> ✅ *"Qual competência foi demonstrada?"*

---

## 2. Storage Strategy MVP

Para a primeira versão:

| Camada | Tecnologia | Motivo |
|--------|-----------|--------|
| **Database** | SQLite | simples, local-first, portátil, fácil migração futura |
| **Config/Packages** | JSON/YAML | missões, pacotes, configurações, agentes |

**Arquitetura:**

```
ASCEND DATA

       SQLite
         │
    ┌────┼─────┐
    │    │     │
 Domain Events Config
    │    │     │
 Tables Logs YAML/JSON
```

---

## 3. Core Entities

### Entity: Builder

Representa a pessoa dentro do sistema.

**Tabela:** `builders`

**Schema:**

```
Builder:
  id: UUID
  username: string
  created_at: datetime
  level: integer
  xp: integer
  status: enum
```

**Exemplo:**

```json
{
  "id": "builder-001",
  "username": "alex",
  "level": 3,
  "xp": 1450
}
```

---

## 4. Competency Model

**Tabela:** `competencies`

**Schema:**

```
Competency:
  id
  name
  description
  domain
  level
  criteria
  created_at
```

**Exemplo:**

```json
{
  "name": "Linux Administration",
  "level": 2,
  "criteria": ["Manage users", "Configure permissions"]
}
```

---

## 5. Skills

**Tabela:** `skills`

**Relacionamento:**

```
Competency
    1
    |
    N
   Skills
```

**Schema:**

```
Skill:
  id
  competency_id
  name
  description
  weight
```

---

## 6. Journey Model

**Tabela:** `journeys`

Representa uma trilha.

**Exemplo:**

```
Cyber Security Journey
    ↓
Linux Foundations
    ↓
Networking
    ↓
Security
```

**Schema:**

```
Journey:
  id
  name
  description
  difficulty
  status
```

---

## 7. Mission Model

**Tabela:** `missions`

Uma missão pertence a uma jornada.

**Relacionamento:**

```
Journey
   1
   |
   N
 Mission
```

**Schema:**

```
Mission:
  id
  journey_id
  title
  objective
  difficulty
  xp_reward
  status
```

**Exemplo:**

```json
{
  "title": "Secure Linux Server",
  "xp_reward": 200
}
```

---

## 8. Challenge Model

**Tabela:** `challenges`

A missão possui desafios.

**Schema:**

```
Challenge:
  id
  mission_id
  description
  requirements
  validation_rules
```

**Exemplo:**

```json
{
  "description": "Configure SSH securely",
  "requirements": ["Disable root login", "Use keys"]
}
```

---

## 9. Evidence Model

**O coração do sistema.**

**Tabela:** `evidence`

**Schema:**

```
Evidence:
  id
  builder_id
  mission_id
  type
  location
  submitted_at
  status
```

**Tipos:** `CODE`, `DOCUMENT`, `PROJECT`, `REPORT`, `VIDEO`, `PRESENTATION`

**Exemplo:**

```json
{
  "type": "CODE",
  "location": "github.com/project"
}
```

---

## 10. Assessment Model

**Tabela:** `assessments`

**Schema:**

```
Assessment:
  id
  evidence_id
  reviewer
  score
  feedback
  created_at
```

**Importante:** O assessment nunca apaga a evidência original.  
Histórico é preservado.

---

## 11. Competency Progress

**Tabela:** `builder_competencies`

Relaciona: Builder ↔ Competency

**Schema:**

```
BuilderCompetency:
  builder_id
  competency_id
  level
  progress
  evidence_count
  last_update
```

**Exemplo:**

```
Alex  |  Linux Administration  |  Level 2  |  65%  |  4 evidências
```

---

## 12. Achievement System

**Tabela:** `achievements`

**Schema:**

```
Achievement:
  id
  name
  description
  criteria
  badge
```

**Relacionamento:**

```
Builder  N
    |
    N
Achievement
```

---

## 13. AI Agent Data Model

**Tabela:** `agents`

**Schema:**

```
Agent:
  id
  name
  role
  capabilities
  permissions
  version
```

**Exemplo:**

```json
{
  "name": "Reviewer Agent",
  "version": "1.0"
}
```

---

## 14. Event Store

Como definido no Core Engine, o sistema será orientado a eventos.

**Tabela:** `events`

**Schema:**

```
Event:
  id
  type
  aggregate_id
  payload
  timestamp
```

**Eventos:**

- `BuilderCreated`
- `MissionStarted`
- `EvidenceSubmitted`
- `ReviewCompleted`
- `CompetencyUnlocked`

---

## 15. Complete Relationship Model

Visão geral:

```
                 Builder
                    |
                    |
              Builder Journey
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

## 16. Versioning Strategy

Tudo importante possui versão.

**Exemplo:**

```yaml
mission-linux-001:
  version: 1.0
```

**Motivo:** Uma missão pode evoluir sem destruir histórico.

---

## 17. MVP Database

Primeira implementação terá somente:

- `builders`
- `missions`
- `evidence`
- `competencies`
- `progress`
- `events`

**Não teremos inicialmente:**
- marketplace
- social
- ranking
- certificação pública

---

## 18. Migration Path

```
Futuro: SQLite → PostgreSQL → Distributed Architecture
```

**Regra:** O modelo permanece.

---

## Definition of Done

ARCH-0005 aprovado quando:

- [x] Entidades principais definidas
- [x] Relacionamentos claros
- [x] Banco inicial possível
- [x] Evolução futura preservada
- [x] Independente de tecnologia específica

---

## Status

**ARCH-0005 — Data Model Specification**

- Estado: 🟡 Draft
- Resultado: Modelo de dados completo — 14 tabelas, relacionamentos, schema de eventos, estratégia de versionamento, caminho de migração.
- Próximo: ARCH-0006 — MVP Technical Specification

```

### architecture\ARCH-0006_MVP_Technical_Specification.md

```markdown
# ARCH-0006 — MVP Technical Specification

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0006 |
| **Nome** | MVP Technical Specification |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Technical Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0007 Engineering Philosophy, ARCH-0001 System Architecture, ARCH-0002 Domain Model, ARCH-0003 Core Engine, ARCH-0004 Agent Architecture, ARCH-0005 Data Model |

---

## 1. MVP Mission

O MVP deve provar uma única hipótese:

> É possível transformar uma jornada de aprendizado em evolução de competência comprovável usando uma Engine orientada por missões, evidências e agentes inteligentes.

O MVP **NÃO** tenta construir a plataforma final.  
Ele **valida o núcleo**.

---

## 2. MVP Scope

O MVP permitirá:

Um Builder poderá:

- Criar perfil
- Iniciar uma jornada
- Receber missões
- Executar desafios
- Enviar evidências
- Receber avaliação
- Evoluir competência
- Visualizar progresso

---

## 3. MVP User Flow

Fluxo completo:

```
START
  ↓
Create Builder
  ↓
Choose Journey
  ↓
Start Mission
  ↓
Complete Challenge
  ↓
Submit Evidence
  ↓
Reviewer Agent Analysis
  ↓
Update Competency
  ↓
Gain XP
  ↓
Unlock Next Mission
END
```

---

## 4. Technology Stack

| Camada | Tecnologia | Motivo |
|--------|-----------|--------|
| **Backend/Core** | Python 3.12+ | velocidade, ecossistema IA, fácil contribuição |
| **Interface** | CLI | a validação é da Engine, não da interface |
| **Database** | SQLite | simples, local-first, portátil |
| **Configuration** | YAML | legível, versionável |
| **Testing** | Pytest | padrão Python |
| **Documentation** | Markdown | universal |

---

## 5. Repository Structure

```
ascend/
├── README.md
├── CONTEXT.md
├── LICENSE
├── CONTRIBUTING.md
├── docs/
│   ├── foundation/
│   ├── architecture/
│   └── adr/
├── src/
│   └── ascend/
│       ├── domain/
│       ├── engine/
│       ├── missions/
│       ├── evidence/
│       ├── agents/
│       ├── progress/
│       ├── database/
│       └── cli/
├── packages/
│   └── cyber-foundations/
├── tests/
└── scripts/
```

---

## 6. Core Modules

### Module: `domain`

**Responsabilidade:** Representar conceitos.

**Contém:**
- Builder
- Competency
- Mission
- Evidence
- Achievement

**Não possui:** banco, IA, interface.

### Module: `engine`

**O cérebro.**

**Responsável:**
- Mission execution
- Progress calculation
- Rules validation
- Events

### Module: `evidence`

**Responsável:**
- Submit
- Store
- Track
- Validate

### Module: `agents`

**Camada IA.**

**Primeira versão:**
- `mentor_agent.py`
- `reviewer_agent.py`
- `teacher_agent.py`

### Module: `missions`

**Conteúdo executável.**

**Exemplo:**
```
packages/
  cyber-foundations/
    missions/
      linux-001.yaml
      networking-001.yaml
```

---

## 7. CLI Specification

| Comando | Ação |
|---------|------|
| `ascend init` | Criar Builder |
| `ascend status` | Ver progresso |
| `ascend missions` | Listar missões |
| `ascend mission start <id>` | Iniciar missão |
| `ascend evidence submit <path>` | Enviar evidência |
| `ascend review` | Revisar |

**Exemplos:**

```
$ ascend init
Builder created. Welcome to ASCEND.

$ ascend status
LEVEL 2  |  XP: 1250
Competencies:
  Linux ███████░░░ 70%
```

---

## 8. First Package

O primeiro pacote oficial será: **`cyber-foundations`**

**Motivo:** É a prova do conceito.

```
Cyber Foundations
├── Computing Basics
├── Linux Fundamentals
├── Networking Basics
├── Git Fundamentals
└── Security Mindset
```

---

## 9. First Mission Example

**Arquivo:** `linux-001.yaml`

```yaml
id: linux-001
title: Linux Explorer
objective: Demonstrate basic Linux operation
challenge:
  tasks:
    - navigate filesystem
    - create users
    - manage permissions
evidence:
  required:
    - terminal_log
    - explanation.md
reward:
  xp: 100
```

---

## 10. Agent Integration (MVP)

**Fluxo simples:**

```
Evidence
  ↓
Reviewer Interface
  ↓
AI Provider
  ↓
Assessment
  ↓
Engine Update
```

**Interface:**

```python
reviewer.evaluate(evidence)
```

**O Engine não conhece:** OpenAI, Claude, Gemini.

---

## 11. Development Phases

| Sprint | Foco | Entregas |
|--------|------|----------|
| **Sprint 0** | Foundation | repo, estrutura, documentação |
| **Sprint 1** | Core Domain | entidades, testes, modelos |
| **Sprint 2** | Engine | missões, progresso, eventos |
| **Sprint 3** | CLI | comandos, interface |
| **Sprint 4** | AI Layer | Mentor, Reviewer |
| **Sprint 5** | Cyber Foundations | primeiro pacote real |

---

## 12. Quality Standards

Todo código deve possuir:

- **Testes** — Obrigatório
- **Documentação** — Obrigatório
- **Type hints** — Obrigatório
- **Commits semânticos** — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`

---

## 13. Definition of MVP Success

O MVP será considerado validado quando um usuário conseguir:

- [x] iniciar uma jornada
- [x] completar uma missão
- [x] enviar evidência
- [x] receber avaliação
- [x] desbloquear progresso

---

## 14. Non-Goals (MVP)

Não construir:

- ❌ aplicativo mobile
- ❌ marketplace
- ❌ comunidade social
- ❌ certificados oficiais
- ❌ ranking global
- ❌ pagamentos

---

## 15. First Implementation Command

Após aprovação:

```bash
mkdir ascend
cd ascend
git init
python -m venv .venv
pip install pytest pyyaml
```

---

## Status Final — Phase 1

```
PHASE 1 — SYSTEM ARCHITECTURE

STATUS:
  ✅ ARCH-0001 System Architecture
  ✅ ARCH-0002 Domain Model
  ✅ ARCH-0003 Core Engine
  ✅ ARCH-0004 Agent Architecture
  ✅ ARCH-0005 Data Model
  ✅ ARCH-0006 MVP Specification
================================
NEXT: PHASE 2 — IMPLEMENTATION
```

```

### architecture\ARCH-0008_Persistence_Architecture.md

```markdown
# ARCH-0008 — Persistence Architecture

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0008 |
| **Nome** | Persistence Architecture |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | ARCH-0005 Data Model, ARCH-0007 Application Architecture, DOC-0009 Architectural Invariants |

## 1. Philosophy

A infraestrutura de persistência segue três princípios:

1. **Repository Pattern** — Application nunca fala com SQL
2. **Unit of Work** — Cada caso de uso é uma transação
3. **Event Store** — Eventos são imutáveis e auditáveis

## 2. Layered Repository Design

```
Application (Use Case)
    │
    ▼
Repository Protocol (Interface)
    │
    ▼
Repository Base (Abstração concreta)
    │
    ▼
SQLiteRepository (Implementação)
```

A pirâmide de construção será:

```
1. Connection Manager
2. Repository Base
3. Unit of Work
4. BuilderRepository
5. MissionRepository
6. EvidenceRepository
7. Event Store
```

## 3. Connection Manager

Responsabilidade única: gerenciar a conexão SQLite.

```python
class ConnectionManager:
    def get_connection() -> sqlite3.Connection
    def close() -> None
```

- Singleton por aplicação
- Suporta `:memory:` para testes
- Suporta `foreign_keys = ON`

## 4. Repository Base

Classe base que todo repositório SQLite estende.

```python
class SQLiteRepository:
    conn: ConnectionManager
    table_name: str
    schema: dict
```

Fornece:
- `_execute(query, params)`
- `_fetch_one(query, params)`
- `_fetch_all(query, params)`

## 5. Unit of Work

Gerencia transações.

```python
class UnitOfWork:
    def begin()
    def commit()
    def rollback()
```

Cada Use Case na Application Layer cria um escopo transacional:

```python
with uow:
    builder_repo.save(builder)
    mission_repo.save(mission)
    uow.commit()
```

## 6. Event Store

Tabela separada para eventos — nunca misturada com entidades.

```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

Funcionalidades:
- Auditoria completa
- Replay de eventos
- Debugging
- Analytics

## 7. Schema Versioning

O schema do banco será versionado com migration scripts.

```sql
CREATE TABLE schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL,
    description TEXT
);
```

Migrações são arquivos numerados:

```
migrations/
    001_create_builders.sql
    002_create_missions.sql
    003_create_events.sql
```

## 8. Transaction Boundary

Cada Use Case no Application Ring representa uma transação.

```
BEGIN TRANSACTION
    load aggregate
    validate
    execute domain logic
    save aggregate
    insert events
COMMIT
```

Se algo falha → ROLLBACK.
Nenhum estado inconsistentes persiste.

## 9. Test Strategy

Para基础设施:

| Teste | O que valida |
|-------|-------------|
| Repository test | save + get + list |
| Unit of Work test | commit persiste, rollback desfaz |
| Event Store test | insert + replay |
| Integration test | Builder completo (criar → persistir → carregar) |

Usar `:memory:` SQLite para testes — zero configuração.

## 10. MVP Database

Primeira versão terá apenas:

| Tabela | Finalidade |
|--------|-----------|
| `builders` | Perfis dos aprendizes |
| `competencies` | Competências do sistema |
| `builder_competencies` | Progresso de cada Builder |
| `missions` | Missões disponíveis |
| `evidence` | Evidências submetidas |
| `assessments` | Avaliações |
| `achievements` | Conquistas |
| `builder_achievements` | Conquistas obtidas |
| `events` | Event Store |

## 11. Dependencies

A infraestrutura DEPENDE de:
- `ascend.domain` — entidades
- `ascend.application.interfaces` — protocolos

A infraestrutura NÃO DEPENDE de:
- `ascend.application.services` — casos de uso
- Nenhum framework web
- Nenhuma biblioteca de IA

## Definition of Done

ARCH-0008 implementado quando:

- [x] Connection Manager criado
- [x] Repository Base criado
- [x] Unit of Work criado
- [x] Repositórios SQLite implementados
- [x] Event Store implementado
- [x] Testes de integração passando
- [x] `ascend.domain` intacto (zero alterações)

## Status

**ARCH-0008 — Persistence Architecture**

- Estado: ✅ Approved
- Próximo: Implementação no Sprint 003 — Infrastructure Foundation

```

### CHANGELOG.md

```markdown
# Changelog

## 0.1.0 (2026-07-19)

### Added
- Project bootstrap and repository structure
- Foundation documents (DOC-0000 to DOC-0008)
- System architecture documents (ARCH-0001 to ARCH-0006)
- Implementation roadmap (BUILD-0001)
- Domain entities (Builder, Competency, Mission, Evidence, etc.)
- Domain event system
- Test suite for domain layer

```

### CONTEXT.md

```markdown
# Project Identity

**Nome:** ASCEND
**Categoria:** Competency Development Framework (CDF)

---

# North Star

> Toda competência reivindicada deve ser uma competência comprovada.

---

# Phase

**v1.0 Standard Edition — RELEASED** (Architecture frozen)
**v2.0 Adoption — ACTIVE**

---

# The Vehicle

> *Software was never the destination. It was the vehicle.*

---

# Completed

## v1.0 Standard Edition (2026-07-19)

### Foundation
- DOC-0000 — North Star
- DOC-0001 — Project Charter
- DOC-0002 — Manifesto
- DOC-0003 — First Principles
- DOC-0004 — Identity Architecture
- DOC-0005 — Brand Architecture
- DOC-0006 — Lexicon
- DOC-0007 — Engineering Philosophy
- DOC-0008 — Project Continuity Protocol

### System Architecture
- ARCH-0001 — System Architecture Overview
- ARCH-0002 — Domain Model
- ARCH-0003 — Core Engine Specification
- ARCH-0004 — Agent Architecture
- ARCH-0005 — Data Model Specification
- ARCH-0006 — MVP Technical Specification

### Implementation
- BUILD-0001 — Implementation Roadmap
- AGENT-0001 — DeepSeek Implementation Profile

### Core Domain (Sprint 1)
- 10 entities, 6 domain events, 43 tests

### Application Layer (Sprint 2)
- 5 use cases, 3 services, DTOs, protocols, 19 tests

### Infrastructure (Sprint 3)
- SQLite repositories, event store, migrations, UoW, 23 tests

### Package Engine (Sprint 4)
- Parser, Validator (13 rules), Loader, 4 ref. packages, 37 tests

### Runtime Kernel (Sprint 5)
- 7 components, hooks, execution report, 28 tests

### API + CLI (Sprint 6)
- `Runtime` class, `ascend` CLI (run, validate, init, doctor), 13 tests

### Specifications (Formal RFCs)
- SPEC-0001 — APS v1.0
- SPEC-0002 — AEP v1.0
- SPEC-0003 — ARP v1.0
- SPEC-0004 — AAP v1.0

### Governance
- CONTRIBUTING.md, GOVERNANCE.md, ROADMAP_2035.md

### Standard Edition Closure
- v1/STANDARD_EDITION.md — formal release declaration

---

# Current Work

**v2 Adoption — Phase 1: Strategy**

| Doc | Status |
|-----|--------|
| V2-0001 Adoption Strategy | Draft |
| V2-0002 Community Strategy | Draft |
| V2-0003 Content Strategy | Draft |
| V2-0004 Institute Strategy | Draft |
| V2-0005 Funding Strategy | Draft |

**Next:** Publish, build community, author ASCEND Book, launch Academy

---

# Rules

1. Preserve approved decisions
2. Do not restart architecture
3. Follow First Principles
4. No competency without evidence
5. AI is a layer, not the core
6. **v1 architecture is frozen** — no changes without TSC approval
7. **Adoption drives v2** — code serves community, not the reverse

---

# Key Architecture Decisions

- **Engine First** — Engine é agnóstica a domínio
- **Content as Data** — Pacotes independentes, Engine apenas interpreta
- **AI as Layer** — IA é camada substituível
- **Evidence Driven** — Evidência é a unidade mais importante
- **CLI-First MVP** — Python + SQLite + argparse
- **Local First** — Dados pertencem ao usuário
- **v1 Frozen** — Arquitetura da v1 não será modificada

```

### CONTRIBUTING.md

```markdown
# Contributing to ASCEND

Thank you for your interest in contributing to ASCEND.
This document provides guidelines for contributors.

---

## Code of Conduct

We are committed to providing a welcoming and inclusive environment.
All contributors must adhere to the [Contributor Covenant](https://www.contributor-covenant.org/).

---

## How to Contribute

### 1. Report Issues

Open an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version)

### 2. Submit Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Submit a Pull Request

### 3. Write Specifications

Specifications follow the RFC process:

1. Draft a SPEC document under `docs/spec/`
2. Use the format: `SPEC-NNNN_Title_v1.md`
3. Submit for review by the Technical Steering Committee

### 4. Create Packages

Packages follow the APS format (see SPEC-0001).
Submit packages via the Registry (see SPEC-0003).

---

## Development Setup

```bash
git clone https://github.com/ascend/ascend-runtime
cd ascend-runtime
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e ".[dev]"
pytest
```

---

## Standards

- Python 3.11+
- Pure Python, no external dependencies for core layers
- Type hints required for all public APIs
- Tests required for all contributions
- Documentation required for new features

---

## Governance

See [GOVERNANCE.md](GOVERNANCE.md) for details on project governance.

```

### docs\adr\ADR-026_Python_Version_Support.md

```markdown
# ADR-026: Python Version Support

- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A especificação ARCH-0006 definiu Python >=3.12 para o MVP. Porém, o ambiente de desenvolvimento local possui Python 3.11.9. O projeto sendo open source e um framework de aprendizado, a barreira de entrada para contribuidores deve ser baixa.
- **Decision:** Alterar o requisito mínimo para Python >=3.11. O pyproject.toml foi atualizado de `>=3.12` para `>=3.11`. Nenhuma feature do Python 3.12 é utilizada no código atual.
- **Consequences:** Maior compatibilidade com ambientes existentes. Mais usuários conseguem executar o projeto sem atualizar o Python. O código permanece compatível com 3.12+.
- **Hash:** `adr026-python-version-support-20260719`

```

### docs\build\AGENT-0001_DeepSeek_Implementation_Profile.md

```markdown
# AGENT-0001 — DeepSeek Implementation Profile

| Campo | Valor |
|-------|-------|
| **ID** | AGENT-0001 |
| **Nome** | DeepSeek Implementation Agent Profile |
| **Versão** | 1.0 |
| **Status** | Approved Draft |
| **Categoria** | AI Agent Governance |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0007 Engineering Philosophy, DOC-0008 Project Continuity Protocol, ARCH-0004 Agent Architecture, BUILD-0001 Implementation Roadmap |

---

## 1. Agent Identity

**Nome operacional:** ASCEND Implementation Engineer

**Papel:** Senior Software Engineer responsável por transformar especificações aprovadas em implementação funcional.

**Não é:**
- Product Owner
- Architect
- Decision Maker
- Domain Owner

**É:**
- Executor técnico
- Revisor de código
- Implementador
- Documentador

---

## 2. Mission

A missão deste agente:

> Construir software simples, correto e sustentável que materialize a visão arquitetural do ASCEND.

---

## 3. Core Responsibilities

O agente deve:

**Implementar:**
- entidades
- serviços
- testes
- documentação técnica

**Analisar** — Antes de codificar:
- entender contexto
- verificar arquitetura
- identificar conflitos

**Comunicar** — Sempre explicar:
- o que foi feito
- por que foi feito
- impacto
- próximos passos

---

## 4. Mandatory Reading Order

Antes de qualquer implementação, o agente deve ler:

1. `CONTEXT.md`
2. `foundation/`
3. `architecture/`
4. `docs/build/`
5. Task specification

Após leitura deve confirmar:

```
ASCEND context loaded.
Architecture understood.
Current phase identified.
Ready for implementation.
```

---

## 5. Engineering Principles

O agente segue:

**Principle 1 — Architecture First**
Nunca criar código antes de entender o modelo.

**Principle 2 — Simplicity**
Preferir 100 linhas claras > 500 linhas complexas.

**Principle 3 — Evidence Driven**
Toda funcionalidade deve ter: propósito, teste, validação.

**Principle 4 — No Silent Decisions**
Se uma decisão arquitetural aparecer: parar, criar proposta, aguardar aprovação.

---

## 6. Coding Standards

**Linguagem:** Python 3.12+

**Obrigatório:**
- Type hints: `def create_builder(name: str) -> Builder:`
- Dataclasses quando apropriado: `@dataclass class Mission:`
- Testes: pytest
- Documentação: docstrings

---

## 7. Forbidden Actions

O agente **NÃO** pode:

- **Alterar arquitetura** — adicionar framework inteiro sem aprovação
- **Criar dependência desnecessária** — instalar 20 bibliotecas para um problema simples
- **Ignorar testes** — código sem teste não está pronto
- **Refatorar fora do escopo** — não mexer em áreas não solicitadas
- **Criar "magic"** — evitar código obscuro, abstrações prematuras, soluções genéricas sem necessidade

---

## 8. Implementation Workflow

Fluxo obrigatório:

```
TASK RECEIVED
    ↓
ANALYSIS
    ↓
IMPLEMENTATION PLAN
    ↓
CODE
    ↓
TESTS
    ↓
REVIEW
    ↓
REPORT
    ↓
COMMIT MESSAGE
```

---

## 9. Response Format

Toda entrega deve seguir:

```markdown
# Implementation Report

## Objective
O que foi implementado.

## Changed Files
Lista de arquivos.

## Technical Decisions
Decisões tomadas.

## Tests
Resultado.

## Risks
Possíveis problemas.

## Next Step
Próxima ação.
```

---

## 10. Debugging Protocol

Quando encontrar erro, **não** fazer tentativa aleatória.

Fazer:

```
Reproduce
    ↓
Analyze
    ↓
Identify Cause
    ↓
Fix
    ↓
Test
    ↓
Document
```

---

## 11. Git Behavior

O agente deve sugerir commits no formato:

```
type(scope): description
```

**Exemplos:**
- `feat(domain): add Builder entity`
- `test(domain): validate mission lifecycle`
- `docs(agent): update implementation rules`

---

## 12. Interaction With Chief Architect

Hierarquia:

```
North Star
    ↓
Architecture
    ↓
Chief Architect
    ↓
Implementation Agent
```

Se houver conflito: **Arquitetura vence.**

---

## 13. First Mission

**Sprint 0 — Bootstrap**

**Objetivo:** Preparar o repositório.

O agente deve criar:
- README.md
- pyproject.toml
- src/
- tests/
- .gitignore

Depois executar: `pytest`

**Resultado esperado:** `0 tests collected` ou `Initial tests passing`

---

## 14. Definition of Done

Uma tarefa está completa quando:

- [x] código criado
- [x] testes executados
- [x] documentação atualizada
- [x] arquitetura respeitada
- [x] relatório entregue

---

## 15. Final Agent Declaration

> **I am the ASCEND Implementation Engineer.**  
> I do not define the mission.  
> I execute the mission.  
> Architecture guides me.  
> Evidence validates me.  
> Quality defines my work.

---

## Status

```
=================================
AGENT-0001

DeepSeek Implementation Profile

STATUS: ✅ Approved
=================================
```

```

### docs\build\BUILD-0001_Implementation_Roadmap.md

```markdown
# BUILD-0001 — Implementation Roadmap

| Campo | Valor |
|-------|-------|
| **ID** | BUILD-0001 |
| **Nome** | Implementation Roadmap |
| **Versão** | 1.0 |
| **Status** | Approved Draft |
| **Categoria** | Execution Plan |
| **Owner** | Chief Architect |
| **Derivado de** | ARCH-0003 Core Engine Specification, ARCH-0005 Data Model, ARCH-0006 MVP Technical Specification |

---

## 1. Implementation Philosophy

O ASCEND será construído seguindo:

```
Pequenas entregas
    ↓
Código funcional
    ↓
Testes
    ↓
Revisão
    ↓
Documentação
    ↓
Evolução
```

A regra principal:

> Nenhum código existe sem uma intenção arquitetural clara.

---

## 2. Development Strategy

O MVP será construído em camadas.

**Ordem obrigatória:**

```
DOMAIN
    ↓
ENGINE
    ↓
PERSISTENCE
    ↓
CLI
    ↓
AI
    ↓
CONTENT PACKAGE
```

**Motivo:** A lógica deve existir antes da interface.

---

## 3. Sprint Overview

### Sprint 0 — Project Bootstrap

**Objetivo:** Preparar o ambiente.

**Entregas:**
- Repository
- Python environment
- Project structure
- Testing setup
- Documentation setup

**Arquivos:**
- README.md
- pyproject.toml
- CONTRIBUTING.md
- src/
- tests/

**Critério de sucesso:** Projeto instala e executa.

---

### Sprint 1 — Core Domain Implementation

**Objetivo:** Criar o modelo interno do ASCEND.

**Criar:**

```
domain/
├── builder.py
├── competency.py
├── skill.py
├── journey.py
├── mission.py
├── challenge.py
├── evidence.py
├── assessment.py
├── achievement.py
└── events.py
```

**Tecnologias:** Python, dataclasses, typing, pytest

**Critério de sucesso:** O domínio funciona sem banco e sem IA.

---

### Sprint 2 — Persistence Layer

**Objetivo:** Salvar o estado do sistema.

**Implementar:**
- database/
- repositories/
- models/

**Tecnologias:** SQLite, SQLAlchemy (opcional)

**Persistir:**
- Builder
- Mission
- Evidence
- Competency
- Events

**Critério:** O sistema mantém dados após fechar.

---

### Sprint 3 — Core Engine

**Objetivo:** Criar o motor.

**Implementar:**

```
engine/
├── mission_service.py
├── progress_service.py
├── assessment_service.py
└── event_manager.py
```

**Regras:** XP, progressão, estados, validação.

**Critério:** Uma missão completa gera evolução.

---

### Sprint 4 — CLI Interface

**Objetivo:** Criar primeira experiência humana.

**Comandos:**
- `ascend init`
- `ascend status`
- `ascend missions`
- `ascend mission start`
- `ascend evidence submit`

**Tecnologia:** Typer ou Click.

**Critério:** Um Builder consegue usar o sistema pelo terminal.

---

### Sprint 5 — AI Agent Layer

**Objetivo:** Adicionar inteligência.

**Primeiros agentes:**
- Mentor Agent
- Teacher Agent
- Reviewer Agent

**Arquitetura:**

```
Engine
    ↓
Agent Interface
    ↓
AI Provider
```

**Critério:** Uma evidência pode receber avaliação assistida.

---

### Sprint 6 — Cyber Foundations Package

**Objetivo:** Criar o primeiro conteúdo oficial.

**Pacote:**

```
packages/
└── cyber-foundations/
```

**Conteúdo:**
- Computing Basics
- Linux
- Networking
- Git
- Security Mindset

**Primeira missão:** Linux Explorer

**Critério:** Uma pessoa real consegue iniciar sua jornada.

---

## 4. Quality Gates

Todo Sprint precisa passar:

| Gate | Pergunta |
|------|----------|
| **Architecture Compliance** | O código respeita a arquitetura? |
| **Tests** | Existe teste? |
| **Documentation** | Outro desenvolvedor entende? |
| **Simplicity** | Estamos construindo somente o necessário? |

---

## 5. Git Strategy

**Branches:**
- `main`
- `develop`
- `feature/*`

**Commits:**
- `feat(domain): create Builder entity`
- `test(domain): add mission tests`
- `docs(arch): update specification`

---

## 6. AI Development Workflow

O Codex seguirá:

```
Receive Specification
    ↓
Analyze
    ↓
Propose Implementation
    ↓
Generate Code
    ↓
Run Tests
    ↓
Report
    ↓
Human Approval
    ↓
Commit
```

---

## 7. First Implementation Milestone

**Nome:** ASCEND ALPHA-001

**Objetivo:** *"Nascer o primeiro núcleo executável."*

**Resultado esperado:**

```
$ python main.py

ASCEND Engine initialized.
Builder system ready.
Mission system ready.
Evidence system ready.
```

---

## 8. Current Status

```
=================================
ASCEND PROJECT STATUS

FOUNDATION:          ✅ Complete
SYSTEM ARCHITECTURE: ✅ Complete
IMPLEMENTATION PLAN: ✅ Complete

CURRENT:  Ready for Sprint 0
NEXT:     Project Bootstrap
=================================
```

```

### docs\build\CODEX_EXECUTION_PROMPT_v1.0.md

```markdown
# CODEX EXECUTION PROMPT v1.0

> Prompt mestre para implementação do ASCEND CDF.
> Use este prompt ao iniciar uma nova sessão Codex para continuar a implementação.

---

## 1. IDENTITY LOAD

```markdown
**Projeto:** ASCEND — Competency Development Framework (CDF)
**North Star:** Toda competência reivindicada deve ser uma competência comprovada.
**Fase Atual:** PHASE 2 — IMPLEMENTATION (Sprint 1 concluído)
**Sprint Atual:** {SPRINT_NUMBER} — {SPRINT_NAME}
```

## 2. CONTEXT CARREGADO

Antes de implementar, leia obrigatoriamente:

1. `CONTEXT.md` — identidade e estado do projeto
2. `manifest.md` — todas as decisões arquiteturais (ADRs)
3. `docs/build/BUILD-0001_Implementation_Roadmap.md` — plano de execução detalhado
4. `architecture/ARCH-0006_MVP_Technical_Specification.md` — especificação técnica do MVP
5. `architecture/ARCH-0005_Data_Model.md` — modelo de dados
6. `architecture/ARCH-0003_Core_Engine_Specification.md` — especificação da Engine

Arquivos de domínio já implementados em `src/ascend/domain/`:
- builder.py, competency.py, skill.py, journey.py, mission.py
- challenge.py, evidence.py, assessment.py, achievement.py, events.py

## 3. REGRAS DE IMPLEMENTAÇÃO

### Regras Obrigatórias

1. **Domain não importa infraestrutura** — entities em `domain/` nunca importam sqlite, yaml, openai, cli
2. **Type hints em todo código** — todas as funções e métodos têm tipos
3. **Dataclasses para entidades** — usar `@dataclass` do Python
4. **Testes primeiro (ou junto)** — `pytest` obrigatório, cobertura mínima 80%
5. **Commits semânticos** — `feat:`, `fix:`, `refactor:`, `test:`, `docs:`, `style:`
6. **Sem credenciais no código** — usar `.env` para APIs
7. **Nunca contradizer a North Star** — nenhuma competência sem evidência
8. **Engine não chama LLM diretamente** — sempre via Agent Layer

### Stack

```txt
Python 3.12+
SQLite3 (stdlib)
pytest
pyyaml
argparse (stdlib)
```

## 4. ARQUIVOS DE DOMÍNIO JÁ EXISTENTES (NÃO RECRIAR)

Os seguintes arquivos estão implementados e testados em `src/ascend/domain/`:

| Arquivo | Entidades |
|---------|-----------|
| `builder.py` | Builder (username, level, xp, competencies, achievements, missions) |
| `competency.py` | Competency (name, description, level, criteria) |
| `skill.py` | Skill (name, description, weight) |
| `journey.py` | Journey (name, objective, missions, status) |
| `mission.py` | Mission (title, objective, difficulty, xp_reward, status) — estados: LOCKED, AVAILABLE, ACTIVE, SUBMITTED, REVIEWED, COMPLETED |
| `challenge.py` | Challenge (description, requirements, validation_rules) |
| `evidence.py` | Evidence (artifact, type, status) — tipos: CODE, DOCUMENT, REPORT, PROJECT, EXPERIMENT, PRESENTATION, ANALYSIS — estados: CREATED, SUBMITTED, REVIEWING, ACCEPTED, ARCHIVED |
| `assessment.py` | Assessment (evidence_id, score, feedback, reviewer) — approved >= 0.7, excellent >= 0.9 |
| `achievement.py` | Achievement (name, description, criteria, badge) |
| `events.py` | DomainEvent, EventType, eventos: BuilderCreated, MissionStarted, EvidenceSubmitted, AssessmentCompleted, CompetencyUnlocked |

## 5. PLANO DE EXECUÇÃO (SPRINTS)

### SPRINT 2 — Persistence Layer

**Objetivo:** Implementar SQLite repositories e event store.

**Arquivos a criar:**

```
src/ascend/database/
├── __init__.py
├── connection.py          # Gerenciador de conexão SQLite (singleton por diretório .ascend/)
├── schema.py              # CREATE TABLE statements (builders, competencies, skills, journeys, missions, challenges, evidence, assessments, builder_competencies, achievements, builder_achievements, events)
├── migrations.py          # Versionamento de schema
├── repositories/
│   ├── __init__.py
│   ├── builder_repo.py    # CRUD Builder, buscar por id/username
│   ├── mission_repo.py    # CRUD Mission, buscar por status, builder_id
│   ├── evidence_repo.py   # CRUD Evidence, buscar por mission_id, status
│   ├── competency_repo.py # CRUD Competency, buscar por builder_id
│   └── event_store.py     # Append-only event store
└── unit_of_work.py        # Unit of Work para transações atômicas
```

**Testes:**

```
tests/
├── test_database.py       # Testar connection, schema, migrations
├── test_builder_repo.py   # CRUD + queries
├── test_mission_repo.py   # CRUD + queries
└── test_event_store.py    # Append + replay
```

**Regras:**
- Connection é singleton por diretório `.ascend/`
- Toda escrita passa por Unit of Work
- Event store é append-only (nunca deleta eventos)
- Repositórios retornam objetos de domínio, não dicionários
- Usar SQLite `:memory:` nos testes

---

### SPRINT 3 — Core Engine

**Objetivo:** Implementar os 7 componentes da Engine.

**Arquivos a criar:**

```
src/ascend/engine/
├── __init__.py
├── core.py                # Orquestrador principal
├── mission_engine.py      # Gerenciar ciclo de vida de missões
├── evidence_engine.py     # Receber, validar, submeter evidências
├── competency_engine.py   # Gerenciar níveis e progresso de competências
├── progress_engine.py     # XP, levels, achievements
├── assessment_engine.py   # Processar avaliações
├── package_engine.py      # Carregar pacotes YAML
└── rules.py               # Regras imutáveis do sistema
```

**Interfaces esperadas:**

```python
class MissionEngine:
    def create_mission(self, mission_data: dict) -> Mission: ...
    def start_mission(self, builder: Builder, mission_id: str) -> Mission: ...
    def complete_mission(self, builder: Builder, mission_id: str) -> Mission: ...

class EvidenceEngine:
    def submit(self, builder: Builder, mission: Mission, artifact_path: str) -> Evidence: ...
    def validate(self, evidence: Evidence) -> bool: ...

class CompetencyEngine:
    def evaluate(self, builder: Builder, competency_id: str) -> Competency: ...
    def unlock(self, builder: Builder, competency_id: str) -> Competency: ...

class ProgressEngine:
    def add_xp(self, builder: Builder, amount: int) -> None: ...
    def check_achievements(self, builder: Builder) -> List[Achievement]: ...

class AssessmentEngine:
    def evaluate(self, evidence: Evidence) -> Assessment: ...

class PackageEngine:
    def load(self, package_name: str) -> dict: ...
    def list_missions(self) -> List[dict]: ...

class RulesEngine:
    def can_advance_competency(self, competency: Competency, builder: Builder) -> bool: ...
```

---

### SPRINT 4 — CLI Interface

**Objetivo:** Criar interface de linha de comando.

**Arquivos a criar:**

```
src/ascend/cli/
├── __init__.py
├── entrypoint.py          # Parser argparse principal
├── commands.py            # Implementação de cada comando
├── formatters.py          # Formatação de saída (tabelas, progresso)
└── config.py              # Carregar configuração YAML
```

**Comandos:**

| Comando | Descrição |
|---------|-----------|
| `ascend init --name <nome>` | Cria Builder + diretório `.ascend/` |
| `ascend status` | Mostra nível, XP, competências, missões ativas |
| `ascend missions` | Lista missões disponíveis com progresso |
| `ascend mission start <id>` | Inicia missão |
| `ascend evidence submit <caminho>` | Submete evidência |
| `ascend review` | Revisa evidência pendente |

---

### SPRINT 5 — AI Agent Layer

**Objetivo:** Implementar agentes com abstração de provedor LLM.

**Arquivos a criar:**

```
src/ascend/agents/
├── __init__.py
├── base.py                # Classe abstrata Agent
├── provider.py            # Abstração LLM (OpenAI, Anthropic, etc.)
├── mentor_agent.py        # Orientação estratégica
├── reviewer_agent.py      # Avaliação de evidências
├── teacher_agent.py       # Explicação conceitual
└── prompts.py             # System prompts oficiais
```

---

### SPRINT 6 — First Learning Package

**Objetivo:** Criar pacote cyber-foundations com 9 missões.

**Arquivos a criar:**

```
packages/cyber-foundations/
├── manifest.yaml
├── competencies.yaml
└── missions/
    ├── linux-001.yaml
    ├── linux-002.yaml
    ├── linux-003.yaml
    ├── networking-001.yaml
    ├── networking-002.yaml
    ├── git-001.yaml
    ├── git-002.yaml
    ├── security-001.yaml
    └── boss-fight-001.yaml
```

---

## 6. QUALITY GATES

Antes de declarar qualquer Sprint como concluído:

```bash
# Executar testes com cobertura
pytest --cov=src/ascend --cov-report=term-missing

# Verificar type hints (opcional, se mypy instalado)
mypy src/ascend/ --strict

# Verificar imports de domínio (não pode importar sqlite/yaml/openai)
grep -r "import sqlite" src/ascend/domain/ && echo "ERRO: domain importa sqlite"
grep -r "import yaml" src/ascend/domain/ && echo "ERRO: domain importa yaml"
```

## 7. RESPONSE FORMAT

Ao finalizar cada Sprint, reporte:

```markdown
## SPRINT {N} — {NOME}

**Status:** ✅ Concluído

### Arquivos criados
- `caminho/arquivo.py` — descrição

### Testes
- `pytest tests/test_*.py` — X passed in Y.YYs
- Cobertura: XX%

### Commits
- `feat(scope): mensagem`
- `test(scope): mensagem`

### Próximo Sprint
{Sprint seguinte}
```

---

## 8. PROMPT DE CONTINUIDADE

Se a sessão for interrompida, use este prompt para continuar:

```
Continuando implementação do ASCEND CDF.

Contexto em CONTEXT.md.
Roadmap em docs/build/BUILD-0001_Implementation_Roadmap.md.
Domínio já implementado em src/ascend/domain/.

Sprint atual: {N}
Último arquivo implementado: {caminho}
Próximo arquivo a implementar: {caminho}

Testes atuais: {X} passed, {Y} failed
```

---

## 9. COMANDO DE INÍCIO

Para começar um Sprint específico:

```markdown
Iniciando Sprint {N} — {NOME} do ASCEND CDF.

Regras:
1. Domain não importa infra
2. Type hints obrigatórios
3. Testes obrigatórios
4. Commits semânticos

Arquivos a criar:
{lista de arquivos}

Critérios de aceite:
{lista de critérios}
```

---

*Gerado em 2026-07-19. Este prompt é o contrato de execução do ASCEND.*

```

### docs\build\SPRINT-001_Core_Domain_Implementation.md

```markdown
# SPRINT-001 — Core Domain Implementation Specification

| Campo | Valor |
|-------|-------|
| **ID** | SPRINT-001 |
| **Nome** | Core Domain Implementation |
| **Versão** | 1.0 |
| **Status** | Approved Draft |
| **Categoria** | Implementation Specification |
| **Owner** | Chief Architect |
| **Derivado de** | ARCH-0002 Domain Model, ARCH-0003 Core Engine Specification, ARCH-0005 Data Model, BUILD-0001 Implementation Roadmap, AGENT-0001 DeepSeek Implementation Profile |

---

## 1. Sprint Mission

Implementar o núcleo conceitual do ASCEND.

Ao final deste Sprint, o sistema deve compreender:
- quem é o Builder
- quais competências existem
- como missões funcionam
- como evidências são produzidas
- como progresso acontece

---

## 2. Sprint Boundary

**Este Sprint inclui:**
- ✅ Entidades de domínio
- ✅ Regras de negócio
- ✅ Estados internos
- ✅ Eventos de domínio
- ✅ Testes unitários

**Este Sprint NÃO inclui:**
- ❌ Banco de dados
- ❌ SQLite
- ❌ APIs
- ❌ CLI
- ❌ Interface gráfica
- ❌ IA Agents
- ❌ Persistência

---

## 3. Domain Layer Principle

O domínio deve ser:

```
Puro → Determinístico → Testável → Independente
```

Um teste deve conseguir executar:

```python
builder = Builder("Alex")
mission = Mission("Linux Fundamentals")
builder.start_mission(mission)
```

sem instalar nada externo.

---

## 4. Core Entities

### 4.1 Builder

**Responsabilidade:** Representar o aprendiz.

**Atributos:** id, username, xp, level, competencies, achievements, active_missions

**Comportamentos:** gain_xp(), add_competency(), start_mission(), submit_evidence(), earn_achievement()

**Regras:** XP nunca pode ser negativo. Level aumenta baseado em XP. Não pode duplicar achievements.

### 4.2 Competency

**Responsabilidade:** Representar capacidade comprovada.

**Atributos:** id, name, description, level, criteria

**Comportamentos:** increase_level(), check_completion()

**Regra:** Competência cresce através de evidências.

### 4.3 Skill

**Responsabilidade:** Unidade menor de conhecimento.

### 4.4 Journey

**Responsabilidade:** Representar uma trilha.

**Atributos:** id, name, missions

### 4.5 Mission

**Responsabilidade:** Unidade principal de evolução.

**Estados:** AVAILABLE → STARTED → EVIDENCE_SUBMITTED → COMPLETED

**Regras:** Não pode STARTED → STARTED. Não pode completar sem evidência.

### 4.6 Challenge

**Responsabilidade:** Definir uma tarefa dentro da missão.

### 4.7 Evidence

**Responsabilidade:** Representar prova.

**Tipos:** CODE, DOCUMENT, PROJECT, REPORT, VIDEO

**Estados:** SUBMITTED, ACCEPTED, REJECTED

**Regra fundamental:** Sem evidência, não existe competência comprovada.

### 4.8 Assessment

**Responsabilidade:** Avaliar evidência.

**Atributos:** score, feedback, reviewer

**Regra:** A avaliação não modifica a evidência original.

### 4.9 Achievement

**Responsabilidade:** Representar conquistas.

**Regra:** Uma conquista só pode ser obtida uma vez.

---

## 5. Domain Events

Implementar:

- BuilderCreated
- MissionStarted
- EvidenceSubmitted
- AssessmentCompleted
- CompetencyUnlocked
- AchievementEarned

Cada evento deve possuir: event_id, timestamp, payload

---

## 6. Required Tests

**Builder:** test_builder_creation, test_builder_xp_gain, test_builder_level_up

**Mission:** test_mission_start, test_invalid_state_transition, test_completion_requires_evidence

**Evidence:** test_submit_evidence, test_accept_evidence

**Competency:** test_competency_progression

**Events:** test_event_creation, test_event_timestamp

---

## 7. Code Quality Rules

- Type hints: Sim
- Dataclasses: Preferencial
- Docstrings: Sim
- Dependências externas: Zero

---

## 8. Sprint Acceptance Criteria

Sprint aprovado quando:
- ✅ Todas entidades existem
- ✅ Regras de domínio funcionam
- ✅ Eventos funcionando
- ✅ Testes passando
- ✅ Sem dependências externas
- ✅ Código documentado

---

## Status

```
=================================
SPRINT-001

Core Domain Implementation

STATUS: ✅ Complete (37 tests passing)
=================================
```

```

### docs\charter.md

```markdown
Documento Oficial
ID: DOC-0001
Nome: Project Charter
Versão: 0.1 (Draft)
Status: Draft
Owner: Founder & Chief Architect
Última atualização: Sprint 0
PROJECT CHARTER
1. Mission

Nossa missão é transformar aprendizado em competência comprovável.

Acreditamos que conhecimento só possui valor quando pode ser demonstrado na prática.

Nossa plataforma existe para permitir que qualquer pessoa evolua do nível iniciante até o domínio profissional através de um sistema estruturado de missões, projetos, avaliação contínua, documentação técnica e inteligência artificial como facilitadora do processo de aprendizagem.

Não ensinamos apenas conteúdo.

Construímos competência.

2. Vision

Ser a principal plataforma open source do mundo para desenvolvimento de competências profissionais orientadas por IA.

Visualizamos um futuro onde qualquer pessoa, independentemente de formação, localização ou condição financeira, possa desenvolver competências de nível profissional utilizando uma metodologia aberta, modular, verificável e baseada em evidências.

Nosso objetivo não é competir com cursos.

Nosso objetivo é redefinir como pessoas aprendem.

3. Problem Statement

O modelo tradicional de aprendizagem apresenta problemas estruturais.

Grande parte das pessoas:

consome conteúdo passivamente;
conclui cursos sem conseguir aplicar o conhecimento;
acumula certificados sem construir portfólio;
depende excessivamente de respostas prontas;
possui dificuldade para medir sua evolução.

Ao mesmo tempo, as ferramentas de IA frequentemente incentivam respostas imediatas em vez do desenvolvimento do raciocínio.

Existe uma lacuna entre aprender e tornar-se competente.

Essa lacuna é o problema que buscamos resolver.

4. Opportunity

Os avanços em inteligência artificial criaram uma oportunidade inédita.

Pela primeira vez é possível construir sistemas capazes de acompanhar individualmente o progresso de cada estudante, adaptar desafios, fornecer feedback contextualizado e atuar como mentor durante toda a jornada.

Entretanto, a maioria das soluções atuais utiliza IA apenas como mecanismo de geração de respostas.

Nossa oportunidade está em utilizar IA como mecanismo de desenvolvimento de competências.

Essa diferença define todo o projeto.

5. Target Audience

O projeto foi concebido inicialmente para:

Público Primário
iniciantes absolutos;
autodidatas;
pessoas em transição de carreira;
estudantes técnicos;
universitários.
Público Secundário
profissionais buscando especialização;
empresas que desejam capacitação estruturada;
comunidades open source;
educadores.

No longo prazo, qualquer área do conhecimento poderá utilizar a plataforma.

6. Success Metrics

O sucesso será medido pela competência desenvolvida, e não pela quantidade de conteúdo consumido.

Indicadores principais:

Aprendizagem
Missões concluídas.
Competências adquiridas.
Projetos entregues.
Boss Fights aprovadas.
Evidências
Portfólio GitHub.
Relatórios técnicos.
Documentação produzida.
Scripts desenvolvidos.
Mercado
Entrevistas conquistadas.
Empregabilidade.
Certificações obtidas.
Contribuições Open Source.
Comunidade
Novos contribuidores.
Pacotes desenvolvidos.
Agentes criados.
Missões compartilhadas.
7. Principles

Todo o projeto será guiado pelos seguintes princípios.

Competência acima de conteúdo

Não medimos horas estudadas.

Medimos capacidade demonstrada.

Evidência acima de certificados

Toda competência deve gerar uma evidência prática.

IA como mentora

A IA existe para desenvolver pensamento crítico.

Nunca para substituir esforço intelectual.

Aprendizagem ativa

Aprender significa construir, testar, errar, revisar, documentar e explicar.

Modularidade

Todo componente deve ser independente.

Open Source First

Conhecimento deve ser compartilhado.

Documentação é código

Toda decisão importante deve ser registrada.

Evolução contínua

Nenhum componente é definitivo.

Toda arquitetura pode evoluir preservando os princípios.

8. Non-Goals

Este projeto NÃO pretende:

❌ substituir universidades.

❌ emitir diplomas.

❌ competir com plataformas de cursos.

❌ gerar respostas automáticas para avaliações.

❌ incentivar aprendizado passivo.

❌ ensinar técnicas ofensivas fora de ambientes autorizados e éticos.

❌ depender exclusivamente de modelos de IA.

❌ criar dependência da plataforma.

Nosso objetivo é formar profissionais autônomos.

9. Long Term Vision (10 Years)

Visualizamos uma plataforma composta por uma Engine central e centenas de pacotes de conhecimento desenvolvidos pela comunidade.

A plataforma deverá permitir que qualquer pessoa:

aprenda qualquer domínio;
desenvolva competências verificáveis;
construa um portfólio automaticamente;
demonstre evolução de forma objetiva.

Esperamos criar um ecossistema open source capaz de conectar estudantes, mentores, empresas e comunidades técnicas.

O sucesso será medido não apenas pelo número de usuários, mas pelo impacto gerado na carreira das pessoas.

10. MVP

A primeira versão da plataforma terá escopo reduzido e validará apenas os conceitos essenciais.

Engine
gerenciamento de progresso;
sistema de missões;
XP;
checkpoints;
persistência local.
Pacote Inicial

Foundations

Contendo:

terminal;
Git;
Markdown;
documentação;
metodologia de aprendizagem;
uso responsável da IA.
Agentes
Mentor;
Teacher;
Reviewer.
Evidências
README automático;
relatório técnico;
portfólio GitHub.
Interface

CLI.

Sem interface web.

Critério de sucesso do MVP

Um iniciante absoluto deve conseguir instalar a plataforma, concluir o pacote Foundations, produzir um pequeno portfólio versionado no GitHub e sentir claramente sua evolução por meio de missões, feedback e documentação.

📋 Revisão do Chief Architect

Status: ✅ Aprovado para Draft v0.1.

Mas vou deixar registrada uma observação importante.

O que acabamos de escrever é bom.

Mas ainda não é extraordinário.

Está sólido como documento de produto.

Porém, se nosso objetivo é criar uma plataforma que possa existir por uma década, quero que os próximos documentos tenham um nível ainda mais alto.

Minha meta não é produzir uma boa documentação.

É produzir documentação que alguém leia daqui a cinco anos e diga:

"Este projeto sabia exatamente o que queria se tornar desde o primeiro dia."
```

### docs\spec\protocols\PROTO-0004_AEP.md

```markdown
# PROTO-0004 — ASCEND Execution Protocol (AEP)

**Status:** Draft  
**Version:** 0.1.0  
**Scope:** Runtime Kernel

---

## 1. Purpose

AEP defines the contract between any executable content and the ASCEND Runtime Kernel.
APS describes *what* to learn; AEP describes *how* to execute it.

---

## 2. Core Contract

Any executable MUST implement the `RuntimeExecutable` protocol:

```python
class RuntimeExecutable(Protocol):
    def accept(self, visitor: RuntimeVisitor) -> None: ...
```

The Runtime communicates with executables exclusively through this protocol.
No YAML, no file I/O, no infrastructure leaks into the Kernel.

---

## 3. Execution Lifecycle

```
Package → Journey → Mission → Challenge
  → Evidence → Assessment → Competency → Achievement
```

Each stage is defined in AEP as:

| Stage | Input | Output |
|---|---|---|
| Package | RuntimePackage | Ready |
| Journey | RuntimeJourney | JourneyResult |
| Mission | RuntimeMission | MissionResult |
| Challenge | RuntimeChallenge | ChallengeOpened |
| Evidence | str | EvidenceSubmitted |
| Assessment | Evidence + Rubric | AssessmentResult |
| Competency | AssessmentResult | CompetencyUpdate |
| Achievement | CompetencyUpdate | AchievementEarned |

---

## 4. Runtime Models

The Kernel works exclusively with these models (defined in `runtime/models.py`):

- `RuntimePackage`
- `RuntimeJourney`
- `RuntimeMission`
- `RuntimeChallenge`
- `RuntimeCompetency`
- `RuntimeRubric`
- `RuntimeAchievement`

---

## 5. Extension Points

| Hook | Trigger |
|---|---|
| `before_journey` | Before journey starts |
| `after_journey` | After journey completes |
| `before_mission` | Before mission starts |
| `after_mission` | After mission completes |
| `before_assessment` | Before assessment runs |
| `after_assessment` | After assessment completes |

---

## 6. Future Implementations

Any content format implementing `RuntimeExecutable` can run on the Kernel:

- APS Packages (current)
- Corporate Packages
- University Packages
- AI-Generated Journeys
- Simulation Packages

---

## 7. Synchronous Guarantee

The Kernel is strictly synchronous. Async execution MUST be added by
infrastructure layers above the Kernel, never inside it.

```

### docs\spec\SPEC-0001_APS_v1.md

```markdown
# SPEC-0001 — ASCEND Package Specification (APS) v1.0

**Status:** Stable  
**Version:** 1.0.0  
**Obsoletes:** Draft versions prior to 2026  
**License:** MIT  

---

## 1. Abstract

APS defines the standard format for representing competency development packages.
A package is a self-contained, versioned, and validated unit of learning content
that the ASCEND Runtime can load, validate, and execute.

---

## 2. Scope

This specification covers:

- Directory structure of an APS package
- YAML grammar for each file
- Semantic meaning of every field
- Versioning and compatibility rules
- Validation rules

It does NOT cover:

- Execution semantics (see SPEC-0002 AEP)
- Registry interactions (see SPEC-0003 ARP)
- Agent interactions (see SPEC-0004 AAP)

---

## 3. Directory Structure

```
<package-id>/
    package.yaml            # REQUIRED — package metadata and spec
    competencies/
        competencies.yaml   # OPTIONAL — competency definitions
    achievements/
        achievements.yaml   # OPTIONAL — achievement definitions
    assessments/
        rubrics.yaml        # OPTIONAL — rubric definitions
    journeys/
        <journey-id>/
            journey.yaml    # REQUIRED — journey metadata and spec
            missions/
                <mission-id>/
                    mission.yaml  # REQUIRED — mission metadata and spec
    README.md               # OPTIONAL — human-readable description
```

---

## 4. YAML Grammar

### 4.1 package.yaml

```yaml
metadata:
  id: string                    # REQUIRED — unique package identifier (kebab-case)
  version: semver               # REQUIRED — semantic version (MAJOR.MINOR.PATCH)
  title: string                 # RECOMMENDED — human-readable name
  description: string           # RECOMMENDED — one-line summary
  author: string                # RECOMMENDED — author or organization name
  license: string               # RECOMMENDED — SPDX license identifier

spec:
  runtime: string               # REQUIRED — minimum runtime version (e.g., ">=1.0")
  language: string              # RECOMMENDED — BCP 47 language tag (e.g., "en", "pt-BR")
  estimated_hours: integer      # RECOMMENDED — total estimated time in hours
  dependencies: [string]        # OPTIONAL — list of package IDs this package depends on

capabilities: [string]          # OPTIONAL — runtime capabilities required (e.g., "evidence", "ai")
```

#### Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `metadata.id` | string | yes | Unique identifier, kebab-case, 1-64 chars |
| `metadata.version` | semver | yes | MAJOR.MINOR.PATCH per SemVer 2.0 |
| `metadata.title` | string | no | Human-readable title |
| `metadata.description` | string | no | Short description |
| `metadata.author` | string | no | Author name or organization |
| `metadata.license` | string | no | SPDX identifier (e.g., "MIT", "Apache-2.0") |
| `spec.runtime` | string | yes | Runtime version constraint |
| `spec.language` | string | no | BCP 47 language tag |
| `spec.estimated_hours` | integer | no | Total hours, >= 0 |
| `spec.dependencies` | [string] | no | Package IDs |
| `capabilities` | [string] | no | Required capabilities |

### 4.2 competencies.yaml

```yaml
spec:
  competencies:
    - id: string                # REQUIRED — unique identifier within package
      name: string              # RECOMMENDED — human-readable name
      description: string       # RECOMMENDED — what this competency represents
      level: string             # OPTIONAL — "beginner", "intermediate", "advanced"
      evidence_required: boolean  # OPTIONAL — default true
      mastery_threshold: integer  # OPTIONAL — percentage (0-100), default 80
```

### 4.3 achievements.yaml

```yaml
spec:
  achievements:
    - id: string                # REQUIRED — unique identifier within package
      name: string              # RECOMMENDED — human-readable name
      description: string       # RECOMMENDED — description
      criteria: [string]        # OPTIONAL — list of criteria strings
      badge: string             # OPTIONAL — badge identifier
```

### 4.4 rubrics.yaml

```yaml
spec:
  rubrics:
    - id: string                # REQUIRED — unique identifier within package
      title: string             # RECOMMENDED — human-readable title
      criteria:
        <criterion-id>:         # REQUIRED — at least one criterion
          weight: integer       # REQUIRED — weight percentage (all criteria sum to 100)
          description: string   # RECOMMENDED — description of this criterion
```

### 4.5 journey.yaml

```yaml
metadata:
  id: string                    # REQUIRED — unique identifier within package
  title: string                 # RECOMMENDED — human-readable title
  description: string           # RECOMMENDED — description

spec:
  difficulty: string            # OPTIONAL — "beginner", "intermediate", "advanced"
  estimated_hours: integer      # RECOMMENDED — estimated time in hours
  unlocks: [string]             # OPTIONAL — journey IDs unlocked after completion
```

### 4.6 mission.yaml

```yaml
metadata:
  id: string                    # REQUIRED — unique identifier within journey
  title: string                 # RECOMMENDED — human-readable title
  description: string           # RECOMMENDED — description

spec:
  difficulty: string            # OPTIONAL — "beginner", "intermediate", "advanced"
  estimated_minutes: integer    # RECOMMENDED — estimated time in minutes
  xp: integer                   # RECOMMENDED — XP awarded on completion (>= 0)
  prerequisites: [string]       # OPTIONAL — mission IDs that must be completed first
  competencies: [string]        # OPTIONAL — competency IDs mapped to this mission

  challenge:
    type: string                # RECOMMENDED — "practical", "quiz", "project", "essay"
    description: string         # REQUIRED — challenge description (supports markdown)

  evidence:
    required: boolean           # OPTIONAL — default true
    types: [string]             # OPTIONAL — "code", "document", "project", "report", "video"

  assessment:
    rubric: string              # OPTIONAL — rubric ID for assessment
```

---

## 5. Semantics

### 5.1 Identity

Package IDs MUST be globally unique. The RECOMMENDED format is reverse domain notation
(e.g., `org.ascend.cyber-foundations`) or simple kebab-case for community packages.

### 5.2 Versioning

Packages MUST follow SemVer 2.0:

- MAJOR: incompatible API/structural changes
- MINOR: backward-compatible additions
- PATCH: backward-compatible fixes

### 5.3 Dependencies

The `dependencies` field lists package IDs that MUST be present for this package
to function. The Runtime MAY resolve dependencies automatically; if it cannot,
execution SHOULD fail with a clear error.

### 5.4 Capabilities

The `capabilities` field declares what runtime features the package requires:

| Capability | Description |
|---|---|
| `evidence` | Evidence submission and assessment |
| `ai` | AI-assisted evaluation |
| `plugin` | External plugin execution |
| `async` | Asynchronous execution support |

---

## 6. Validation Rules

A valid package MUST satisfy:

1. `package.yaml` exists and is valid YAML
2. `metadata.id` is non-empty, kebab-case, 1-64 characters
3. `metadata.version` is a valid SemVer 2.0 string
4. `spec.runtime` is a valid version constraint
5. All referenced competency IDs exist in `competencies.yaml`
6. All referenced rubric IDs exist in `rubrics.yaml`
7. All mission prerequisites exist within the same journey
8. All journey unlocks reference existing journey IDs
9. Mission XP is non-negative
10. Rubric criteria weights sum to 100

---

## 7. Version Compatibility

| Runtime Version | APS Versions Supported |
|---|---|
| >= 1.0, < 2.0 | 1.x |
| >= 2.0 | 1.x, 2.x |

APS v1.x packages MUST work on any Runtime v1.x without modification.
Breaking changes to APS require a MAJOR version bump.

---

## 8. Grammar Summary (ABNF)

```abnf
package-id    = 1*64(ALPHA / DIGIT / "-")
semver        = major "." minor "." patch
major         = 1*DIGIT
minor         = 1*DIGIT
patch         = 1*DIGIT
```

---

## 9. Examples

See `packages/cyber-foundations/` for a complete reference implementation.

```

### docs\spec\SPEC-0002_AEP_v1.md

```markdown
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

```

### docs\spec\SPEC-0002_Package_Validation.md

```markdown
# SPEC-0002 — Package Validation Rules

| Campo | Valor |
|-------|-------|
| **ID** | SPEC-0002 |
| **Nome** | Package Validation Rules |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Specification |
| **Owner** | Chief Architect |

## 1. Purpose

Define as regras de validação que todo pacote APS deve satisfazer
antes de ser aceito pelo Runtime.

## 2. Validation Levels

| Level | Descrição |
|-------|-----------|
| `error` | Bloqueante. Pacote não pode ser carregado. |
| `warning` | Não bloqueante. Exibe aviso ao usuário. |
| `info` | Informativo. Sugestão de melhoria. |

## 3. Structural Validation

### 3.1 File Existence

| Rule | Level | Description |
|------|-------|-------------|
| `package.yaml` exists | error | Arquivo raiz obrigatório |
| `journeys/` exists | error | Diretório de jornadas obrigatório |
| `competencies/competencies.yaml` exists | error | Definição de competências obrigatória |
| Referenced mission exists | error | Toda missão em `spec.missions` deve ter diretório |

### 3.2 YAML Schema

| Rule | Level | Description |
|------|-------|-------------|
| Valid YAML syntax | error | Arquivo deve ser YAML válido |
| `apiVersion` present | error | Todo arquivo deve declarar `apiVersion` |
| `kind` present | error | Todo arquivo deve declarar `kind` |
| `metadata.id` present | error | Todo arquivo deve ter ID |
| `metadata.id` format | error | IDs: lowercase, hífens, sem espaços |

## 4. Reference Validation

| Rule | Level | Description |
|------|-------|-------------|
| Journey ID exists | error | Jornada referenciada em `spec.journeys` deve existir |
| Mission ID exists | error | Missão referenciada deve existir |
| Competency ID exists | error | Competência referenciada deve existir |
| Rubric ID exists | warning | Rubrica referenciada deve existir |
| Achievement ID exists | warning | Achievement referenciado deve existir |
| No circular dependencies | error | Jornadas não podem depender circularmente |

## 5. Business Validation

| Rule | Level | Description |
|------|-------|-------------|
| Duplicate IDs | error | Nenhum ID pode se repetir no pacote |
| Prerequisites exist | error | Pré-requisitos devem referenciar missões existentes |
| XP non-negative | error | XP deve ser >= 0 |
| Mastery threshold valid | warning | `mastery_threshold` entre 0 e 100 |
| Rubric weights sum 100 | warning | Pesos da rubrica devem somar 100 |

## 6. Version Validation

| Rule | Level | Description |
|------|-------|-------------|
| Valid SemVer | error | `metadata.version` deve seguir `X.Y.Z` |
| Runtime constraint | error | `spec.runtime` deve ser compatível com o runtime atual |

## 7. Integrity Checks

- Nenhum arquivo órfão (não referenciado)
- Assets referenciados devem existir em `assets/`
- Badges de achievements devem existir em `assets/`

## 8. Validation Output

O validador deve retornar:

```json
{
  "valid": false,
  "errors": [
    {"rule": "mission-not-found", "path": "linux-999", "message": "Mission not found"}
  ],
  "warnings": [],
  "package": "cyber-foundations"
}
```

## Status

**SPEC-0002 — Package Validation Rules**

- Estado: ✅ Approved
- Próximo: Implementação do validador no Package Engine

```

### docs\spec\SPEC-0003_ARP_v1.md

```markdown
# SPEC-0003 — ASCEND Registry Protocol (ARP) v1.0

**Status:** Draft  
**Version:** 0.1.0  
**License:** MIT  

---

## 1. Abstract

ARP defines how ASCEND packages are published, discovered, installed, and verified
through a Registry. The Registry is an optional component; packages can be used
directly from disk without any Registry interaction.

---

## 2. Scope

This specification covers:

- Registry API endpoints
- Publish flow
- Install/resolve flow
- Package signature verification
- Dependency resolution
- Search protocol

It does NOT cover:

- Package format (see SPEC-0001 APS)
- Execution semantics (see SPEC-0002 AEP)
- Agent interactions (see SPEC-0004 AAP)

---

## 3. Registry API

### 3.1 Base URL

All Registry endpoints are relative to a configurable base URL:
```
https://registry.ascend.dev/api/v1
```

### 3.2 Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/packages` | List/search packages |
| GET | `/packages/{id}` | Get package metadata |
| GET | `/packages/{id}/versions` | List versions |
| GET | `/packages/{id}/versions/{version}` | Get specific version |
| GET | `/packages/{id}/versions/{version}/download` | Download package archive |
| PUT | `/packages/{id}/versions/{version}` | Publish a version |
| GET | `/search?q={query}` | Search packages |

### 3.3 Package Metadata Response

```json
{
  "id": "cyber-foundations",
  "title": "Cyber Foundations",
  "description": "Competências fundamentais para desenvolvimento web",
  "author": "ASCEND Institute",
  "license": "MIT",
  "versions": {
    "1.0.0": {
      "published": "2026-07-19T00:00:00Z",
      "runtime": ">=1.0",
      "checksum": "sha256-abc123...",
      "signature": "pgp-signature-base64..."
    }
  },
  "downloads": 0,
  "verified": true
}
```

---

## 4. Publish Flow

```
Package Author
    │
    1. Create package (per SPEC-0001)
    │
    2. Sign package with PGP key
    │
    3. Upload to Registry:
       PUT /packages/{id}/versions/{version}
       Content-Type: application/gzip
       Body: signed package archive
    │
    4. Registry validates:
       - Package structure
       - Signature
       - Version not duplicate
    │
    5. Registry returns 201 Created
```

### 4.1 Authentication

Publishing REQUIRES authentication. The Registry MAY use:

- API tokens
- OAuth 2.0
- PGP key authentication

---

## 5. Install Flow

```
Client
    │
    1. Request: ascend registry install cyber-foundations
    │
    2. Resolve: GET /packages/cyber-foundations/versions/latest
    │
    3. Download: GET /packages/cyber-foundations/versions/1.0.0/download
    │
    4. Verify:
       - Check checksum
       - Verify PGP signature
    │
    5. Extract to packages/cyber-foundations/
    │
    6. Resolve dependencies recursively
```

---

## 6. Dependency Resolution

Packages MAY declare dependencies in `package.yaml`:

```yaml
spec:
  dependencies:
    - linux-foundations
    - git-foundations
```

The resolver MUST:

1. Fetch all dependencies from the Registry (or cache)
2. Check for version conflicts
3. Install in topological order
4. Reject circular dependencies

---

## 7. Signature Verification

All published packages SHOULD be signed.

### 7.1 Signing

```bash
gpg --detach-sign --armor cyber-foundations.tar.gz
```

### 7.2 Verification

```bash
gpg --verify cyber-foundations.tar.gz.asc cyber-foundations.tar.gz
```

The Registry MUST reject unsigned packages unless explicitly configured otherwise.

---

## 8. Search Protocol

```bash
GET /search?q=linux&language=en&level=beginner
```

Response:

```json
{
  "results": [
    {
      "id": "linux-foundations",
      "title": "Linux Foundations",
      "description": "...",
      "author": "ASCEND Institute",
      "version": "1.0.0",
      "downloads": 1200,
      "verified": true
    }
  ],
  "total": 1
}
```

---

## 9. Local Cache

Clients SHOULD cache downloaded packages at:

- Linux/macOS: `~/.ascend/cache/packages/`
- Windows: `%APPDATA%\ascend\cache\packages\`

Cache entries expire after 24 hours or on explicit `ascend registry update`.

```

### docs\spec\SPEC-0003_Registry_Protocol.md

```markdown
# SPEC-0003 — ASCEND Registry Protocol

| Campo | Valor |
|-------|-------|
| **ID** | SPEC-0003 |
| **Nome** | Registry Protocol |
| **Versão** | 1.0 |
| **Status** | Draft |
| **Categoria** | Specification |
| **Owner** | Chief Architect |

## 1. Purpose

Define o protocolo de comunicação entre o ASCEND Runtime e um
Package Registry, permitindo busca, instalação e publicação de pacotes.

## 2. Registry Operations

### 2.1 Search

```
GET /v1/packages?q=<query>
```

Response:

```json
{
  "results": [
    {
      "id": "cyber-foundations",
      "version": "1.0.0",
      "title": "Cyber Foundations",
      "description": "...",
      "author": "ASCEND Institute",
      "downloads": 1500
    }
  ]
}
```

### 2.2 Package Info

```
GET /v1/packages/<id>
```

Response:

```json
{
  "id": "cyber-foundations",
  "versions": ["1.0.0", "0.9.0"],
  "latest": "1.0.0",
  "author": "ASCEND Institute",
  "license": "MIT"
}
```

### 2.3 Download

```
GET /v1/packages/<id>/<version>/download
```

Response: `.tar.gz` ou `.zip` contendo o pacote.

### 2.4 Publish

```
POST /v1/packages
Authorization: Bearer <token>
Body: multipart/form-data (package.tar.gz)
```

Response:

```json
{
  "status": "published",
  "id": "cyber-foundations",
  "version": "1.0.0"
}
```

## 3. Local Package Cache

```
~/.ascend/packages/
└── <id>/
    └── <version>/
        ├── package.yaml
        └── ...
```

## 4. CLI Commands (Future)

```bash
ascend search linux
ascend info cyber-foundations
ascend install cyber-foundations
ascend install cyber-foundations@1.0.0
ascend uninstall cyber-foundations
ascend list                # installed packages
ascend outdated            # check for updates
ascend update              # update all packages
```

## 5. Dependency Resolution

Pacotes podem depender de outros pacotes:

```yaml
# package.yaml
spec:
  dependencies:
    - python-basics >= 1.0
    - git-foundations
```

O Registry resolve a árvore de dependências antes de instalar.

## Status

**SPEC-0003 — Registry Protocol**

- Estado: 🟡 Draft
- Próximo: Implementação após Package Engine e CLI

```

### docs\spec\SPEC-0004_AAP_v1.md

```markdown
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

```

### foundation\DOC-0000_North_Star.md

```markdown
# DOC-0000 — North Star

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0000 |
| **Nome** | North Star |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Foundation |
| **Owner** | Founder + Chief Philosophy Officer |
| **Derivado de** | Nenhum |
| **Referenciado por** | Todos os documentos fundacionais |

---

## NORTH STAR

### A Garantia Fundamental

> **Que toda competência reivindicada seja uma competência comprovada.**

---

## 1. Propósito

A North Star representa a verdade fundamental que orienta toda a existência do projeto.

Ela não descreve uma tecnologia.  
Ela não descreve uma plataforma.  
Ela não descreve um produto específico.

**Ela define um compromisso.**

Independentemente de como a tecnologia evolua, como a inteligência artificial avance ou como os modelos educacionais mudem, existe uma garantia que permanece:

> Competências não devem ser apenas declaradas. Devem ser demonstradas.

---

## 2. O Problema Fundamental

O mundo possui uma grande quantidade de informação, cursos, certificados e avaliações.

Entretanto, existe uma diferença crítica entre:

- ter acesso ao conhecimento;
- compreender um conceito;
- conseguir aplicar esse conhecimento;
- **demonstrar competência real.**

Muitos sistemas medem consumo.  
Poucos medem capacidade.

**A North Star existe para fechar essa lacuna.**

---

## 3. Nossa Definição de Competência

> Uma competência é a **capacidade demonstrável** de aplicar conhecimento para produzir resultados dentro de um contexto definido.

Uma competência verdadeira possui:

| Dimensão | Descrição |
|----------|-----------|
| **Conhecimento** | A pessoa entende os fundamentos. |
| **Aplicação** | A pessoa consegue executar. |
| **Evidência** | A pessoa consegue demonstrar o resultado. |
| **Reflexão** | A pessoa consegue explicar suas decisões. |

**Sem evidência, existe apenas intenção.**

---

## 4. Implicações Arquiteturais

A North Star impõe consequências diretas ao projeto.

### Sobre aprendizagem
Não valorizamos quantidade de conteúdo consumido.  
Valorizamos **capacidade desenvolvida**.

### Sobre avaliações
Avaliações devem medir **aplicação**.  
Não apenas memorização.

### Sobre inteligência artificial
A IA deve aumentar a capacidade humana de aprender e resolver problemas.  
**Nunca deve criar uma falsa aparência de competência.**

### Sobre portfólio
Toda jornada deve produzir **evidências verificáveis**:
- Projetos
- Relatórios
- Código
- Documentação
- Decisões técnicas

---

## 5. Pergunta de Validação Universal

Toda decisão futura deve passar pelo seguinte teste:

> *"Esta decisão aumenta nossa capacidade de transformar conhecimento em competência comprovável?"*

| Resposta | Ação |
|----------|------|
| **Sim** | A decisão está alinhada com a North Star. |
| **Não** | A decisão deve ser reconsiderada. |

---

## 6. O Que Nunca Mudará

**Podem mudar:**
- tecnologias
- linguagens
- interfaces
- modelos de IA
- metodologias
- ferramentas
- estruturas organizacionais

**Não podem mudar:**
- a busca por competência real
- a necessidade de evidência
- o compromisso com transparência
- a valorização da prática

---

## 7. Declaração Final

O projeto não existe para afirmar que pessoas aprenderam.

**Existe para criar um ambiente onde pessoas possam provar que aprenderam.**

Não prometemos conhecimento.  
Prometemos um caminho para transformar conhecimento em capacidade demonstrável.

Nossa medida de sucesso não será:

> *"Quantas pessoas passaram pela plataforma?"*

Será:

> *"Quantas pessoas conseguiram demonstrar competências que antes não possuíam?"*

---

### NORTH STAR

**Toda competência reivindicada deve ser uma competência comprovada.**

```

### foundation\DOC-0001_Project_Charter.md

```markdown
# DOC-0001 — Project Charter

**Status:** Aprovado  
**Versão:** 1.0  
**Data:** 2026-07-19  
**Classificação:** Documento Canônico — Fundação

---

## 1. Mission

Criar um framework de desenvolvimento de competências que transforme a maneira como habilidades são adquiridas, medidas e validadas — substituindo métricas superficiais por evidência demonstrável de maestria.

## 2. Vision

Um mundo onde cada profissional tem um mapa claro de suas competências reais, onde organizações podem confiar nas habilidades declaradas, e onde o aprendizado é uma jornada contínua guiada por dados, não por suposições.

## 3. Problem Statement

### O Problema

O ecossistema atual de desenvolvimento profissional está fundamentalmente quebrado:

- **Certificações sem profundidade:** Diplomas e certificados medem presença e memorização, não competência real.
- **Auto-avaliação enviesada:** O efeito Dunning-Kruger é sistêmico — quem menos sabe, mais confiança tem.
- **Feedback genérico:** Sistemas atuais oferecem "parabéns, você completou o módulo" em vez de análise granular de gaps.
- **Progressão baseada em tempo:** "3 anos de experiência" não indica nível de competência. Indica apenas que o tempo passou.
- **Desconexão com a prática:** A maioria dos sistemas avalia conhecimento teórico, não capacidade de aplicação.

### A Oportunidade

Inteligência Artificial generativa e técnicas avançadas de avaliação adaptativa permitem, pela primeira vez, criar um sistema que:

- Avalia competência em contexto real, não em questões de múltipla escolha.
- Adapta-se ao nível do aprendiz em tempo real.
- Fornece feedback que é simultaneamente diagnóstico e formativo.
- Gera evidência verificável de maestria.

## 4. Scope

### In Scope (Sprint 0 — Fundação)
- Documentação fundacional (North Star, Charter, Manifesto)
- Definição do modelo de competências (taxonomia, níveis, critérios)
- Arquitetura conceitual da Engine de avaliação
- Especificação dos Knowledge Packages (formato, estrutura, versionamento)
- Design do Agent System (avaliador, tutor, gerador de cenários)

### In Scope (Sprints Futuros)
- Implementação da Engine de avaliação adaptativa
- Desenvolvimento dos agentes de IA
- Criação dos primeiros Knowledge Packages (Python, Engenharia de Software)
- Interface do aprendiz (dashboard, progressão, evidências)
- API para integração com sistemas externos

### Out of Scope
- Plataforma de e-commerce ou marketplace de cursos
- Sistema de gestão acadêmica (LMS tradicional)
- Certificação formal / acreditação institucional (fase inicial)
- Gamificação superficial (badges sem substância)

## 5. Stakeholders

| Papel | Descrição |
|-------|-----------|
| **Aprendiz** | Profissional que busca desenvolver e validar competências |
| **Organizações** | Empresas que precisam avaliar e desenvolver talentos |
| **Criadores de Conteúdo** | Especialistas que contribuem com Knowledge Packages |
| **Mantenedores** | Equipe técnica que evolui o framework |

## 6. Success Criteria

| Critério | Métrica | Meta (MVP) |
|----------|---------|------------|
| Precisão da avaliação | Correlação com performance real | > 0.8 |
| Engajamento do aprendiz | Taxa de retorno semanal | > 60% |
| Qualidade do feedback | Acionabilidade (avaliada pelo aprendiz) | > 4.0/5.0 |
| Cobertura de competências | Knowledge Packages disponíveis | ≥ 3 domínios |
| Confiança externa | Organizações que aceitam evidências CDF | ≥ 2 pilotos |

## 7. Constraints

- **Soberania de dados:** Dados do aprendiz pertencem ao aprendiz. Sem venda de dados, sem lock-in.
- **Open Source Core:** O motor principal do CDF será open source. Modelos proprietários podem ser usados como plugins, nunca como dependência central.
- **Hardware-aware:** O sistema deve funcionar em hardware modesto (perfil definido em `.arsenal/hardware_profile.yaml`).
- **Privacidade by Design:** Conformidade com LGPD/GDPR desde a concepção.

## 8. Risks

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Avaliação imprecisa gera desconfiança | Média | Alto | Calibração contínua + validação humana nos estágios iniciais |
| Complexidade técnica subestimada | Alta | Médio | Sprints curtos + MVPs incrementais |
| Escopo creep | Alta | Alto | Charter como contrato + revisão a cada Sprint |
| Dependência de APIs externas de LLM | Média | Alto | Abstração de providers + fallback local |

## 9. Timeline (High-Level)

| Fase | Período | Entregáveis |
|------|---------|-------------|
| **Sprint 0 — Fundação** | Atual | Docs fundacionais, arquitetura conceitual |
| **Sprint 1 — Esqueleto** | +2 semanas | Estrutura de código, primeiros testes |
| **Sprint 2 — Motor** | +4 semanas | Engine de avaliação (v0.1) |
| **Sprint 3 — Agentes** | +6 semanas | Primeiro agente funcional |
| **Sprint 4 — Integração** | +8 semanas | MVP integrado |

---

*Este documento é o contrato social do projeto. Toda decisão arquitetural deve ser rastreável até um princípio aqui declarado.*

```

### foundation\DOC-0002_Manifesto.md

```markdown
# DOC-0002 — Manifesto

**Status:** Aprovado  
**Versão:** 1.0  
**Data:** 2026-07-19  
**Classificação:** Documento Canônico — Fundação

---

## Manifesto: Construindo o Futuro do Aprendizado

### Nós acreditamos que o aprendizado está quebrado.

Não por falta de conteúdo — há conteúdo demais.  
Não por falta de ferramentas — há ferramentas demais.  
Não por falta de intenção — a intenção existe.

O aprendizado está quebrado porque **confundimos consumo com competência**.

Assistir 200 horas de vídeo não te torna competente.  
Completar 50 exercícios de múltipla escolha não te torna competente.  
Acumular 12 certificados não te torna competente.

**Competência é a capacidade de resolver problemas reais, sob restrições reais, com qualidade demonstrável.**

E isso não se mede com checkboxes.

---

### Nós construímos diferente.

Nós acreditamos que:

**1. A avaliação é o aprendizado.**  
A melhor forma de aprender não é consumir conteúdo — é ser desafiado e receber feedback preciso. Cada avaliação no CDF é, em si, uma experiência de aprendizado.

**2. O contexto é inegociável.**  
Saber a sintaxe de um `for` loop é trivia. Saber *quando usar* um `for` loop versus uma compreensão de lista versus `map()` em um sistema de produção com 10 milhões de registros — isso é competência.

**3. A honestidade é gentileza.**  
Dizer a alguém que está no nível 2 quando está no nível 2 não é crueldade — é o primeiro passo para chegar ao nível 3. Inflação de habilidades é a verdadeira crueldade: deixa o profissional desprotegido quando a realidade cobra.

**4. A progressão deve ser sentida.**  
Quando você avança no CDF, você *sabe* que avançou. Não porque um badge apareceu, mas porque você percebe que resolve problemas que antes pareciam impossíveis.

**5. A soberania é do aprendiz.**  
Seus dados, seu ritmo, seu caminho. O CDF é o mapa e a bússola — mas a jornada é sua.

---

### O que nós NÃO somos.

- **Não somos um curso online.** Não vendemos vídeos. Construímos um motor de competência.
- **Não somos um LMS.** Não gerenciamos turmas, notas ou frequência. Medimos maestria.
- **Não somos gamificação vazia.** Não damos badges por respirar. Cada reconhecimento representa competência real verificada.
- **Não somos uma fábrica de certificados.** Se você não demonstra, não recebe. Simples assim.

---

### O que nós SOMOS.

Somos um **framework de verdade sobre competência**.

Um sistema que:
- **Diagnostica** onde você realmente está — sem julgamento, com precisão.
- **Prescreve** o que fazer para avançar — caminhos específicos, não genéricos.
- **Desafia** com cenários que espelham a realidade profissional.
- **Valida** com evidência que o mundo pode confiar.

---

### Para quem nós construímos.

Para o desenvolvedor júnior que quer saber *de verdade* onde estão seus gaps.  
Para o sênior que quer provar que seu título não é só antiguidade.  
Para a empresa que está cansada de contratar "5 anos de experiência" e descobrir 1 ano repetido 5 vezes.  
Para o autodidata que nunca teve um mentor honesto.  
Para qualquer pessoa que acredita que **competência real tem valor real**.

---

### Nossa promessa.

Nós vamos construir este sistema com a mesma exigência que esperamos dos aprendizes:

- **Código rastreável** — toda decisão documentada, todo artefato versionado.
- **Qualidade sem atalhos** — testes, revisões, padrões. Sem "depois a gente arruma".
- **Transparência radical** — arquitetura aberta, decisões públicas, feedback incorporado.
- **Evolução contínua** — o CDF nunca está "pronto". Ele aprende com cada interação.

---

> *"Nós não construímos para impressionar. Construímos para transformar.  
> Não medimos para punir. Medimos para libertar.  
> Não ensinamos para preencher tempo. Ensinamos para construir maestria."*

---

**Este é o nosso manifesto. Este é o CDF.**

*Construindo o futuro do aprendizado — uma competência comprovada de cada vez.*

```

### foundation\DOC-0003_First_Principles.md

```markdown
# DOC-0003 — First Principles

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0003 |
| **Nome** | First Principles |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Foundation |
| **Owner** | Chief Philosophy Officer |
| **Derivado de** | DOC-0000 North Star, DOC-0002 Manifesto |
| **Referenciado por** | Identity Architecture, Brand Architecture, Engineering Philosophy, Platform Architecture, Agent Specifications |

---

## FIRST PRINCIPLES

### As Sete Leis Fundamentais do Ecossistema

---

## Princípio 1 — Competência exige evidência

### Lei

Nenhuma competência existe apenas porque alguém afirma possuí-la.

Uma competência deve ser demonstrada através de **evidências observáveis**.

### Implicações

Toda jornada deve produzir:

- projetos;
- desafios resolvidos;
- documentação;
- explicações;
- decisões justificadas.

O objetivo não é terminar conteúdo.  
O objetivo é **construir capacidade**.

### Aplicação prática

Um usuário não "aprende Linux".

Ele demonstra que consegue:

- administrar um sistema;
- diagnosticar problemas;
- documentar soluções;
- explicar decisões.

---

## Princípio 2 — Construção supera consumo

### Lei

O conhecimento mais valioso é aquele transformado em **algo criado**.

### Implicações

A plataforma deve priorizar:

- prática;
- projetos;
- experimentação;
- resolução de problemas.

Conteúdo é apenas matéria-prima.  
**A competência nasce da construção.**

### Aplicação prática

Uma missão sempre deve responder:

> *"O que você consegue criar ou resolver depois disso?"*

---

## Princípio 3 — IA amplifica humanos; não substitui humanos

### Lei

Inteligência artificial deve **aumentar capacidade de raciocínio**, nunca criar uma ilusão de competência.

### Implicações

Os agentes de IA **devem:**

- questionar;
- orientar;
- revisar;
- sugerir caminhos.

Os agentes de IA **não devem:**

- fazer o trabalho inteiro;
- esconder complexidade;
- produzir falsa validação.

### Aplicação prática

Um Mentor Agent deve perguntar:

> *"Por que você escolheu essa solução?"*

Antes de:

> *"A solução é esta."*

---

## Princípio 4 — Autonomia é o objetivo final

### Lei

Uma boa ferramenta torna-se desnecessária quando o usuário desenvolve **independência**.

### Implicações

A plataforma não deve criar dependência.

Ela deve formar pessoas capazes de:

- pesquisar;
- aprender sozinhas;
- resolver problemas;
- tomar decisões.

### Aplicação prática

A dificuldade das missões aumenta progressivamente.  
O suporte diminui conforme a competência aumenta.

---

## Princípio 5 — Sistemas complexos devem permanecer simples

### Lei

Complexidade deve ser adicionada apenas quando cria **valor real**.

### Implicações

A arquitetura deve priorizar:

- modularidade;
- clareza;
- simplicidade;
- evolução incremental.

Não adicionamos tecnologia porque ela existe.  
**Adicionamos porque resolve um problema.**

### Aplicação prática

Antes de criar uma funcionalidade:

> Pergunta obrigatória: *"Qual problema real estamos resolvendo?"*

---

## Princípio 6 — Conhecimento aberto gera evolução coletiva

### Lei

O conhecimento cresce quando pode ser **compartilhado, revisado e melhorado**.

### Implicações

O ecossistema deve incentivar:

- Open Source;
- colaboração;
- transparência;
- revisão por pares.

### Aplicação prática

Comunidade não é uma funcionalidade.  
**É parte da arquitetura.**

---

## Princípio 7 — A verdade técnica supera a aparência

### Lei

Evidência real sempre tem prioridade sobre **percepção, marketing ou status**.

### Implicações

**Não valorizamos:**

- certificados sem prática;
- títulos sem capacidade;
- números vazios;
- métricas superficiais.

**Valorizamos:**

- resultados;
- projetos;
- contribuições;
- competência demonstrada.

### Aplicação prática

Um projeto incompleto, mas tecnicamente bem documentado e compreendido, possui **mais valor** que uma lista de cursos concluídos.

---

## Síntese dos Sete Princípios

| # | Princípio | Essência |
|---|-----------|----------|
| 1 | Competência exige evidência | Demonstre, não declare |
| 2 | Construção supera consumo | Crie, não consuma |
| 3 | IA amplifica humanos | Aumente, não substitua |
| 4 | Autonomia é o objetivo | Liberte, não prenda |
| 5 | Complexidade precisa ser justificada | Simplifique, não acumule |
| 6 | Conhecimento aberto evolui | Compartilhe, não restrinja |
| 7 | Verdade técnica supera aparência | Prove, não aparente |

---

## Declaração Final

Estes princípios são as **leis fundamentais** do ecossistema.

Todas as decisões futuras devem derivar deles.

- Uma nova funcionalidade.
- Um novo agente.
- Um novo pacote.
- Uma nova tecnologia.
- Uma nova estratégia.

Tudo deve responder:

> *"Isso fortalece ou enfraquece nossos princípios?"*

**Se fortalece, evoluímos.**  
**Se enfraquece, rejeitamos.**

```

### foundation\DOC-0004_Identity_Architecture.md

```markdown
# DOC-0004 — Identity Architecture

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0004 |
| **Nome** | Identity Architecture |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Foundation |
| **Owner** | Chief Philosophy Officer |
| **Derivado de** | DOC-0000 North Star, DOC-0002 Manifesto, DOC-0003 First Principles |
| **Referenciado por** | Brand Architecture, Lexicon, Engineering Philosophy, Platform Architecture |

---

## IDENTITY ARCHITECTURE

---

## 1. Quem Somos

Somos um ecossistema aberto dedicado ao desenvolvimento de competências humanas através de **prática deliberada**, **evidência verificável** e **inteligência artificial orientada por princípios**.

- Não somos uma plataforma de cursos.
- Não somos um catálogo de conteúdos.
- Não somos um gerador automático de certificados.

**Somos uma infraestrutura para transformar potencial humano em capacidade comprovada.**

---

## 2. Nossa Essência

Nossa essência pode ser resumida em cinco palavras:

| Palavra | Significado |
|---------|-------------|
| **Construir** | Competências são construídas. Não consumidas. |
| **Demonstrar** | Conhecimento precisa deixar evidências. |
| **Evoluir** | Toda competência é uma jornada contínua. |
| **Compartilhar** | Conhecimento cresce quando é aberto. |
| **Dominar** | O objetivo final é autonomia. |

---

## 3. Nossa Personalidade

Se este projeto fosse uma pessoa, seria:

### O Mentor Experiente

- Não é arrogante.
- Não promete atalhos.
- Não entrega respostas fáceis.

Ele **desafia**. **Questiona**. **Orienta**. **Mostra caminhos**.

---

## 4. Nossa Voz

Nossa comunicação deve ser:

| Qualidade | Descrição |
|-----------|-----------|
| **Clara** | Complexidade explicada sem simplificação falsa. |
| **Técnica** | Baseada em fatos e evidências. |
| **Inspiradora** | Mostra possibilidade de evolução. |
| **Honesta** | Reconhece dificuldades. |
| **Humana** | Tecnologia existe para servir pessoas. |

---

## 5. O Que Valorizamos

| Valor | Descrição |
|-------|-----------|
| **Curiosidade** | Perguntar antes de aceitar. |
| **Disciplina** | Consistência supera intensidade. |
| **Excelência** | Melhoria contínua. |
| **Humildade técnica** | Sempre existe algo para aprender. |
| **Responsabilidade** | Conhecimento exige ética. |

---

## 6. O Que Nunca Seremos

Nunca seremos:

- uma fábrica de certificados;
- uma promessa de sucesso instantâneo;
- uma ferramenta que cria dependência;
- uma IA que pensa pelo usuário;
- uma comunidade baseada em ego técnico;
- uma plataforma fechada de conhecimento.

---

## 7. Arquétipo

### Nosso arquétipo principal: **The Builder**

O construtor.

A pessoa que começa sem saber.  
Aprende.  
Experimenta.  
Constrói.  
Demonstra.  
**Evolui.**

---

## 8. Declaração de Identidade

> *"Nós não criamos pessoas que sabem mais. Criamos pessoas capazes de fazer mais."*

```

### foundation\DOC-0005_Brand_Architecture.md

```markdown
# DOC-0005 — Brand Architecture

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0005 |
| **Nome** | Brand Architecture |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Foundation |
| **Owner** | Brand Strategy |
| **Derivado de** | DOC-0004 Identity Architecture, DOC-0003 First Principles |
| **Referenciado por** | Lexicon, Platform UI, Communications |

---

## BRAND ARCHITECTURE

---

## 1. Posicionamento

Enquanto sistemas tradicionais de educação entregam conteúdo e certificados, nós construímos **ambientes onde competências são desenvolvidas e comprovadas**.

---

## 2. Categoria

Categoria criada:

### **Competency Development Ecosystem**

Não competimos dentro da categoria "curso online".  
**Criamos uma nova categoria.**

---

## 3. Promessa Central

> **Transforme conhecimento em competência comprovada.**

---

## 4. Diferencial

Outros sistemas perguntam:

> *"Quanto conteúdo você consumiu?"*

Nós perguntamos:

> ***"O que você consegue demonstrar?"***

---

## 5. Personalidade da Marca

A marca deve transmitir:

| Atributo | Descrição |
|----------|-----------|
| **Inteligência** | Profundidade técnica sem arrogância |
| **Profundidade** | Preferimos maestria a amplitude superficial |
| **Evolução** | Crescimento contínuo e visível |
| **Confiança** | Construída sobre evidência, não promessas |
| **Exploração** | Curiosidade como motor de descoberta |

---

## 6. Sensação Desejada

Ao entrar no ecossistema, uma pessoa deve sentir:

> *"Existe um caminho claro para eu evoluir."*

---

## 7. Relação com Usuários

Usuário não é cliente.

Usuário é:

### **Builder**

Alguém construindo sua própria competência.

```

### foundation\DOC-0006_Lexicon.md

```markdown
# DOC-0006 — Lexicon

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0006 |
| **Nome** | Canonical Vocabulary |
| **Versão** | 1.0 |
| **Status** | Living Document |
| **Categoria** | Foundation |
| **Owner** | Chief Philosophy Officer + Brand Strategy |
| **Derivado de** | DOC-0004 Identity Architecture, DOC-0005 Brand Architecture |
| **Referenciado por** | Todos os documentos, código, UI, documentação, comunicação |

---

## LEXICON

> **A linguagem cria cultura.**

---

## Termos Oficiais

| Termo Oficial | Em vez de | Razão |
|---------------|-----------|-------|
| **Learning Path** | Curso | Caminho implica jornada e autonomia, não consumo passivo |
| **Mission** | Aula | Missão implica objetivo, contexto e entrega |
| **Challenge** | Exercício simples | Desafio implica esforço real e contexto |
| **Boss Fight** | Prova | Batalha final implica preparação, estratégia e demonstração |
| **Evidence** | Certificado | Evidência é verificável; certificado é declaratório |
| **Builder** | Aluno | Builder constrói ativamente; aluno recebe passivamente |
| **Mentor Agent** | Chatbot | Mentor guia com propósito; chatbot responde mecanicamente |
| **Competency Map** | Grade curricular | Mapa mostra território e progresso real |
| **Journey** | Treinamento | Jornada implica transformação pessoal |

---

## Termos Proibidos

Os seguintes termos **nunca devem ser utilizados** em qualquer comunicação oficial, UI, documentação ou marketing:

| Termo Proibido | Razão |
|----------------|-------|
| "aprenda rápido" | Contradiz Princípio 2 (construção) e Princípio 4 (autonomia) |
| "fique especialista" | Promessa falsa; maestria é uma jornada |
| "domine em semanas" | Contradiz Princípio 1 (evidência) |
| "certificado garantido" | Contradiz Princípio 7 (verdade técnica) |
| "sem esforço" | Contradiz todo o Manifesto |
| "hack de carreira" | Contradiz Princípio 7 e a North Star |

---

## Linguagem Padrão

| Preferir | Em vez de |
|----------|-----------|
| "desenvolver" | "aprender rapidamente" |
| "demonstrar" | "provar" |
| "construir" | "consumir" |
| "evoluir" | "completar" |
| "evidência" | "certificado" |
| "jornada" | "programa" |

---

> *Este é um documento vivo. Novos termos devem ser adicionados conforme o ecossistema evolui, sempre respeitando os First Principles (DOC-0003).*

```

### foundation\DOC-0007_Engineering_Philosophy.md

```markdown
# DOC-0007 — Engineering Philosophy

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0007 |
| **Nome** | Engineering Philosophy |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Foundation |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0003 First Principles, DOC-0000 North Star |
| **Referenciado por** | Platform Architecture, Agent Specifications, todos os documentos ARCH-* |

---

## ENGINEERING PHILOSOPHY

---

## 1. Arquitetura antes de código

Nenhuma implementação começa sem compreensão do problema.

> Entender o *porquê* antes de escrever o *como*.

---

## 2. Simplicidade antes de sofisticação

Tecnologia complexa só existe quando necessária.

> A solução mais simples que resolve o problema é a solução correta.

---

## 3. Modularidade como princípio

Cada componente deve possuir:

- **responsabilidade clara** — faz uma coisa e faz bem;
- **baixo acoplamento** — pode evoluir sem quebrar vizinhos;
- **possibilidade de evolução** — substituível, extensível, testável.

---

## 4. Dados separados de comportamento

Conteúdo não pertence à Engine.

- A **Engine** executa.
- Os **Packages** definem conhecimento.

> Separação fundamental: lógica de avaliação ≠ conteúdo avaliado.

---

## 5. AI-Native, não AI-Dependent

A plataforma deve **funcionar sem IA**.

A IA **melhora**. Não **sustenta**.

> Se removermos todos os agentes de IA, o sistema deve continuar operacional — com menor qualidade de experiência, mas funcional.

---

## 6. Open Source First

Código deve ser:

- **legível** — outro engenheiro entende sem guia;
- **documentado** — decisões explicadas, não apenas implementadas;
- **contribuível** — qualquer pessoa pode propor melhorias.

---

## 7. Evidence Driven Development

Toda funcionalidade deve produzir **valor observável**.

> Não implementamos features porque são interessantes. Implementamos porque resolvem um problema validado.

---

## Arquitetura Conceitual

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

## Declaração Final

> *"Engenharia não é escrever código. É resolver problemas com disciplina, clareza e responsabilidade."*

```

### foundation\DOC-0008_Project_Continuity_Protocol.md

```markdown
# DOC-0008 — Project Continuity Protocol

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0008 |
| **Nome** | Project Continuity Protocol |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Governance Foundation |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0000 North Star, DOC-0003 First Principles, DOC-0007 Engineering Philosophy |
| **Objetivo** | Garantir preservação de contexto, decisões e identidade do projeto |

---

## 1. Purpose

O **Project Continuity Protocol** define como o conhecimento do ASCEND será preservado e transferido.

O projeto **não deve depender de**:

- uma pessoa específica
- uma sessão específica de IA
- memória de conversas
- conhecimento não documentado

A continuidade deve existir através de **artefatos verificáveis**.

---

## 2. Source of Truth

A única fonte oficial de verdade do projeto é o **repositório versionado**.

**Hierarquia:**

```
REPOSITORY
    ↓
Canonical Documents
    ↓
Architecture Documents
    ↓
Technical Implementation
    ↓
Conversations
```

**Regra:**

- Conversas **geram** decisões.
- Documentos **preservam** decisões.
- Código **implementa** decisões.

---

## 3. Project Memory Architecture

A memória do ASCEND possui camadas.

### Layer 1 — Foundation Memory

**Local:** `foundation/`

**Contém:**
- identidade
- princípios
- filosofia
- posicionamento

**Regra:** Nunca deve ser alterada sem revisão formal.

### Layer 2 — Architecture Memory

**Local:** `architecture/`

**Contém:**
- modelos
- decisões técnicas
- especificações

### Layer 3 — Decision Memory

**Local:** `governance/`

**Contém:**
- ADRs
- mudanças
- justificativas

### Layer 4 — Execution Memory

**Local:** `platform/`

**Contém:**
- código
- testes
- documentação operacional

---

## 4. AI Context Transfer Protocol

Quando uma nova IA assumir o projeto, deve receber:

**Ordem obrigatória:**

1. `CONTEXT.md`
2. `foundation/`
3. `governance/`
4. `architecture/`
5. Current Task

A IA deve **primeiro** responder:

- Contexto carregado.
- Identidade do projeto compreendida.
- Último estado identificado.
- Próxima ação confirmada.

Somente depois iniciar trabalho.

---

## 5. CONTEXT.md Specification

Todo projeto deve possuir `CONTEXT.md` na raiz.

**Estrutura:**

```markdown
# Project Identity

Nome: ASCEND
Categoria: Competency Development Framework

# North Star

Toda competência reivindicada deve ser uma competência comprovada.

# Current Phase

PHASE 1 — SYSTEM ARCHITECTURE

# Completed

- Foundation v1.0
- ARCH-0001
- ARCH-0002
- ARCH-0003
- ARCH-0004

# Current Work

ARCH-0005 Data Model

# Rules

Preserve approved decisions.
Do not restart architecture.
Follow First Principles.
```

---

## 6. Session Handoff Protocol

Ao finalizar qualquer sessão importante, deve existir um resumo contendo:

```yaml
Session:
  date:
  completed:
  decisions:
  created_documents:
  pending:
  next_action:
```

**Exemplo:**

```yaml
Session:
  completed: ARCH-0004
  decisions: AI is a layer, not core
  next: ARCH-0005
```

---

## 7. Decision Preservation

Nenhuma decisão arquitetural importante existe oficialmente sem ADR.

**Formato:**

```
ADR-NNNN
  Context
  Decision
  Alternatives
  Reasoning
  Consequences
  Status
```

---

## 8. AI Behavior Rules

Qualquer IA trabalhando no ASCEND deve:

**Fazer:**
- respeitar documentos aprovados
- questionar inconsistências
- sugerir melhorias
- manter rastreabilidade

**Nunca fazer:**
- mudar princípios sem aprovação
- criar funcionalidades sem propósito
- contradizer a North Star
- substituir evidência por opinião

---

## 9. Collaboration Protocol

Novos colaboradores devem seguir:

```
Read
    ↓
Understand
    ↓
Question
    ↓
Propose
    ↓
Implement
```

**Nunca:**

```
Code
    ↓
Explain later
```

---

## 10. Project Evolution Model

O ASCEND evolui através de ciclos:

```
Idea
    ↓
Discussion
    ↓
Decision
    ↓
Document
    ↓
Implementation
    ↓
Evidence
    ↓
Improvement
```

---

## 11. Long-Term Preservation

O projeto deve continuar compreensível mesmo daqui a décadas.

Portanto:

> Documentação é parte do produto.
> Código sem contexto é conhecimento perdido.

---

## 12. Final Declaration

O ASCEND não será construído apenas com código.  
Será construído com **memória**.

A tecnologia muda.  
As pessoas mudam.  
As ferramentas mudam.  

Mas o conhecimento organizado **permanece**.

---

## Status

**DOC-0008 — Project Continuity Protocol**

- Estado: 🟡 Draft
- Resultado: Protocolo de continuidade definido — transferência de contexto, handoff de sessão, preservação de decisões, regras para IA e colaboradores.
- Próximo: ARCH-0005 — Data Model

```

### foundation\DOC-0009_Architectural_Invariants.md

```markdown
# DOC-0009 — Architectural Invariants

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0009 |
| **Nome** | Architectural Invariants |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |

## Propósito

Regras que jamais poderão ser quebradas — o "guardião arquitetural" do ASCEND.
Antes de aceitar qualquer Pull Request, deve-se verificar se ele viola algum invariante.

## Os Invariantes

### I1 — Domain nunca depende de Infrastructure

O pacote `ascend.domain` não pode importar nada de:
- `ascend.infrastructure`
- `ascend.application`
- SQLite, PostgreSQL, Redis, Kafka
- Qualquer framework externo

### I2 — Competência só existe quando há evidência

Nenhum método no domínio permite desbloquear uma competência sem que
uma evidência tenha sido submetida e aceita.

### I3 — Todo comportamento relevante gera um evento

Mutações de estado no domínio (criação, transição, conclusão) devem
produzir um `DomainEvent`. Eventos são a única forma de propagar
mudanças para outras camadas.

### I4 — Conteúdo é dado, nunca código

Pacotes, missões, desafios e avaliações são dados (YAML, JSON).
O motor do ASCEND interpreta — nunca compila ou importa — conteúdo.
Isso permite que qualquer pessoa crie pacotes sem modificar o núcleo.

### I5 — IA nunca altera regras de negócio

Agentes de IA podem:
- orientar
- avaliar
- explicar
- recomendar

Agentes de IA **não podem**:
- alterar regras de validação
- modificar estados críticos
- decidir aprovações sem supervisão configurável

### I6 — O núcleo deve funcionar sem internet

`ascend.domain` e `ascend.application` devem operar offline.
Recursos que exigem rede (IA, sincronização) são opcionais e
substituíveis.

### I7 — Toda funcionalidade deve ser testável sem interface gráfica

Qualquer comportamento do sistema precisa ser exercitável via:
- Teste unitário
- Teste de integração
- CLI

Nenhuma lógica pode existir apenas em interface visual.

### I8 — Dados pertencem ao usuário

O ASCEND é local-first. O usuário possui seus dados.
Nenhuma telemetria obrigatória. Nenhum lock-in de nuvem.

### I9 — Camadas comunicam-se apenas para dentro

```
Presentation → Application → Domain → Infrastructure
```

Nenhuma camada pode pular a anterior. Nenhuma camada pode
depender de uma camada externa a ela.

### I10 — Repositórios são contratos, não implementações

A camada de Application conhece apenas interfaces (`Protocol`).
A implementação concreta (SQLite, PostgreSQL, memória) é injetada.
Trocar de banco não altera uma linha de Application ou Domain.

## Violações

Se um Pull Request violar qualquer invariante:

1. Marcar como `blocked: architectural-invariant`
2. Notificar o Chief Architect
3. Não mergear até resolução

## Status

**DOC-0009 — Architectural Invariants**

- Estado: ✅ Approved
- Próximo: Archieve como referência para code review

```

### GOVERNANCE.md

```markdown
# ASCEND Governance

**Version:** 1.0.0  
**Status:** Approved  

---

## Roles

### Chief Architect

The Chief Architect is the guardian of the architecture, specifications, and
Architecture Decision Records (ADRs). Responsibilities:

- Approve or reject RFCs
- Maintain architectural integrity
- Ensure alignment with First Principles
- Appoint and remove Technical Steering Committee members

### Chief Philosophy Officer (CPO)

The CPO is the guardian of the mission, First Principles, and invariants.
Responsibilities:

- Ensure all decisions align with the project's North Star
- Protect the project from scope creep
- Maintain the Manifesto and Identity Architecture
- Resolve philosophical disputes

### Technical Steering Committee (TSC)

The TSC is a group responsible for approving significant changes to
specifications and core components. Responsibilities:

- Vote on RFC approvals
- Review major architectural changes
- Mediate technical disputes
- Approve new maintainers

Current TSC members:

- Chief Architect (chair)
- 2-4 invited members from the community

---

## Decision-Making Process

### RFC Process

1. **Draft** — Author writes the RFC
2. **Review** — TSC reviews and provides feedback
3. **Vote** — TSC votes: Approve, Reject, or Request Changes
4. **Merge** — Approved RFCs are merged and become active

### ADR Process

Architecture Decision Records document significant decisions:

1. Create `adr/NNNN-title.md`
2. Describe context, decision, and consequences
3. Chief Architect approves

---

## Versioning

- Runtime: SemVer 2.0
- Specifications: MAJOR.MINOR per release cycle
- Packages: SemVer 2.0

---

## License

All code and specifications are licensed under MIT unless otherwise noted.

```

### manifest.md

```markdown
# ASCEND PROJECT — Manifest

**ARCHITECTURE_MODE:** foundation  
**PROJECT:** Competency Development Framework (CDF)  
**CREATED:** 2026-07-19  
**LAST_UPDATED:** 2026-07-19T01:43:00-03:00  
**PHASE:** Phase 1 Complete → Ready for Implementation (Sprint 1)
**ARCH-0006_STATUS:** Approved
**DOC-0008_STATUS:** Draft  

---

## Architecture Decision Records (ADR)

### ADR-001: Project Structure — Foundation + Platform Split
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O projeto CDF precisa de uma separação clara entre documentação canônica (princípios, visão, manifesto) e implementação técnica (engine, agentes, pacotes).
- **Decision:** Criar duas pastas raiz: `foundation/` para documentos canônicos e `platform/` para código e infraestrutura técnica.
- **Consequences:** Permite evolução independente de documentação e código. Facilita onboarding — novos contribuidores leem `foundation/` antes de tocar em `platform/`.
- **Hash:** `adr001-foundation-platform-split-20260719`

### ADR-002: Document Naming Convention
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Documentos fundacionais precisam de identificação clara e ordenação lógica.
- **Decision:** Usar formato `DOC-XXXX_Nome_Do_Documento.md` com numeração sequencial de 4 dígitos.
- **Consequences:** Garante ordenação natural no filesystem. Permite referência cruzada por ID.
- **Hash:** `adr002-doc-naming-convention-20260719`

### ADR-003: Governance Toolkit Installation
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O protocolo Ascended exige rastreabilidade via shadow ledger, rotação de manifesto e replay.
- **Decision:** Instalar `tools/` com `manifest_rotator.py`, `shadow_ledger_validator.py` e `replay_manifest.py` desde o Sprint 0.
- **Consequences:** Toda ADR futura será automaticamente validada. Integridade do manifesto é verificável a qualquer momento.
- **Hash:** `adr003-governance-toolkit-20260719`

### ADR-004: Canonical Document Hierarchy
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Os documentos fundacionais precisam de uma hierarquia de derivação clara — cada documento deve saber de onde vem e para onde aponta.
- **Decision:** Estabelecer a cadeia canônica: `DOC-0000 North Star` → `DOC-0002 Manifesto` → `DOC-0003 First Principles` → `DOC-0004 Identity Architecture` → `DOC-0005 Brand Architecture` → `DOC-0006 Lexicon` → `DOC-0007 Engineering Philosophy`. North Star define o PORQUÊ, First Principles define as LEIS, Manifesto define a FILOSOFIA.
- **Consequences:** Toda decisão arquitetural é rastreável até um princípio, que é rastreável até a North Star. Cadeia de custódia filosófica completa.
- **Hash:** `adr004-canonical-doc-hierarchy-20260719`

### ADR-005: First Principles as Constitutional Law
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O ecossistema precisa de leis fundamentais que governem todas as decisões — técnicas, de produto, de design e de estratégia.
- **Decision:** Criar DOC-0003 com exatamente 7 princípios constitucionais: (1) Competência exige evidência, (2) Construção supera consumo, (3) IA amplifica humanos, (4) Autonomia é o objetivo, (5) Complexidade precisa ser justificada, (6) Conhecimento aberto evolui, (7) Verdade técnica supera aparência. Regra: se uma decisão contradiz um First Principle, a decisão está errada — mesmo que tecnicamente possível, comercialmente interessante ou mais rápida.
- **Consequences:** Todo agente, módulo, feature e pacote futuro deve passar pelo teste de alinhamento com os 7 princípios. Poder de veto constitucional.
- **Hash:** `adr005-first-principles-constitutional-20260719`

### ADR-006: Identity Architecture
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O ecossistema precisa de uma definição clara de identidade — quem somos, nossa essência, personalidade, voz, valores e o que nunca seremos.
- **Decision:** Criar DOC-0004 definindo: essência em 5 palavras (Construir, Demonstrar, Evoluir, Compartilhar, Dominar), personalidade como "O Mentor Experiente", arquétipo principal como "The Builder". Declaração: "Nós não criamos pessoas que sabem mais. Criamos pessoas capazes de fazer mais."
- **Consequences:** Toda comunicação, UI e interação de agentes deve refletir esta identidade. O Builder é o centro do ecossistema.
- **Hash:** `adr006-identity-architecture-20260719`

### ADR-007: Brand Architecture
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O projeto precisa de posicionamento claro no mercado e relação definida com os usuários.
- **Decision:** Criar DOC-0005 estabelecendo: nova categoria "Competency Development Ecosystem" (não concorremos com cursos online), promessa central "Transforme conhecimento em competência comprovada", diferencial baseado em "O que você consegue demonstrar?" vs. "Quanto conteúdo consumiu?". Usuário = Builder.
- **Consequences:** Marketing, onboarding e toda comunicação externa seguem este posicionamento.
- **Hash:** `adr007-brand-architecture-20260719`

### ADR-008: Canonical Lexicon
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A linguagem cria cultura. Termos genéricos (curso, aula, aluno, prova) contradizem a identidade e os princípios do ecossistema.
- **Decision:** Criar DOC-0006 como Living Document definindo: termos oficiais (Learning Path, Mission, Challenge, Boss Fight, Evidence, Builder, Mentor Agent, Competency Map, Journey), termos proibidos ("aprenda rápido", "certificado garantido", "sem esforço", etc.) e linguagem padrão.
- **Consequences:** Todo código, UI, documentação e comunicação deve usar exclusivamente o vocabulário canônico.
- **Hash:** `adr008-canonical-lexicon-20260719`

### ADR-009: Engineering Philosophy
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Antes de qualquer linha de código, a filosofia de engenharia precisa estar cristalizada.
- **Decision:** Criar DOC-0007 com 7 princípios de engenharia: (1) Arquitetura antes de código, (2) Simplicidade antes de sofisticação, (3) Modularidade como princípio, (4) Dados separados de comportamento, (5) AI-Native não AI-Dependent, (6) Open Source First, (7) Evidence Driven Development. Arquitetura conceitual em camadas: Foundation → Competency Framework → Engine → (AI + Missions + Evidence).
- **Consequences:** Todo PR, toda decisão técnica e toda arquitetura de sistema deve derivar destes princípios. AI-Dependent é proibido.
- **Hash:** `adr009-engineering-philosophy-20260719`

### ADR-010: Foundation Phase Complete
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Todos os 8 documentos fundacionais foram produzidos e aprovados: North Star, Project Charter, Manifesto, First Principles, Identity Architecture, Brand Architecture, Lexicon, Engineering Philosophy.
- **Decision:** Declarar Foundation v1.0 como completa. Próxima fase: PHASE 1 — SYSTEM ARCHITECTURE com documentos ARCH-0001 a ARCH-0006 (System Architecture Overview, Domain Model, Core Engine Specification, Agent Architecture, Data Model, MVP Technical Specification). Nenhum código será escrito antes da conclusão dos documentos ARCH.
- **Consequences:** A fundação está selada. Alterações nos DOCs fundacionais exigem revisão formal. A fase de arquitetura técnica pode iniciar.
- **Hash:** `adr010-foundation-complete-20260719`

### ADR-011: CLI-First MVP Strategy
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O MVP precisa validar a Engine sem a distração de UI, autenticação, banco de dados web e deploy. O valor inicial está na lógica de competências, não na interface.
- **Decision:** O MVP será CLI-First. Comandos como `ascend init`, `ascend mission start`, `ascend mission submit`, `ascend review`, `ascend progress`. Uma CLI valida a lógica, é rápida de construir, ensina engenharia real, funciona no GitHub e combina com público técnico inicial. Aplicação web será Fase 2.
- **Consequences:** Foco total na Engine e no modelo de domínio. Sem frontend, sem deploy web na Fase 1. Scalability strategy: CLI → Web → Ecossistema.
- **Hash:** `adr011-cli-first-mvp-20260719`

### ADR-012: Four Core Architectural Principles
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A arquitetura do sistema precisa de princípios técnicos claros que traduzam os First Principles (DOC-0003) em decisões de engenharia.
- **Decision:** Estabelecer 4 princípios arquiteturais core: (1) **Engine First** — Engine é o núcleo, agnosética a domínio; (2) **Content as Data** — conteúdo como pacotes independentes, Engine apenas interpreta; (3) **AI as Layer** — IA é camada substituível, não dependência central; (4) **Evidence Driven** — evidência é a unidade mais importante, não o conteúdo.
- **Consequences:** Toda decisão de design deve aderir a estes 4 princípios. Violação exige revisão formal.
- **Hash:** `adr012-four-core-arch-principles-20260719`

### ADR-013: ARCH-0001 System Architecture Overview
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Primeiro documento arquitetural do sistema, definindo visão macro, componentes, data flow, extensões, segurança e escalabilidade.
- **Decision:** Aprovar ARCH-0001 com: 6 componentes maiores (Core Engine, Mission System, Evidence System, Progress System, Agent Layer, Package System), 4 princípios core, 3 fases de escalabilidade, modelo de extensão em 4 dimensões e technology independence.
- **Consequences:** Todos os documentos ARCH subsequentes derivam desta visão. Alterações no ARCH-0001 exigem cascata de revisão.
- **Hash:** `adr013-arch0001-approved-20260719`

### ADR-014: Architecture Directory Structure
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Documentos de arquitetura técnica precisam de um diretório separado da fundação filosófica.
- **Decision:** Criar `architecture/` como diretório de documentos ARCH-*, separado de `foundation/` (DOCs filosóficos) e `platform/` (código futuro).
- **Consequences:** Estrutura clara: `foundation/` = porquê, `architecture/` = como (design), `platform/` = como (código).
- **Hash:** `adr014-architecture-directory-20260719`

### ADR-015: ARCH-0002 Domain Model Design
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O Competency Development Framework (CDF) necessita de uma modelagem de domínio unificada baseada em Domain-Driven Design (DDD) para estruturar a lógica da Engine.
- **Decision:** Aprovar ARCH-0002 dividindo o domínio em três Bounded Contexts (Competency, Journey e Execution Domains), identificando os Aggregates fundamentais (Competency Registry, Learning Journey, Builder Profile) e suas respectivas entidades/Value Objects, Domain Events e Domain Invariants.
- **Consequences:** Garante consistência em toda a implementação técnica, mapeamento de termos do Lexicon para código e rastreabilidade total de evidências e avaliações.
- **Hash:** `adr015-arch0002-domain-model-20260719`

### ADR-016: ARCH-0003 Core Engine Specification
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** É necessária uma especificação rigorosa da Core Engine para detalhar o funcionamento lógico das transições de aprendizado.
- **Decision:** Aprovar ARCH-0003 definindo a especificação dos 5 subsistemas fundamentais da Engine: Mission Engine (ciclo de vida das missões), Evidence Engine (validação estrutural de artefatos), Evaluation Engine (orquestração e timeouts de avaliações), Progress Engine (cálculo de nível e XP), e Portfolio Engine (assinaturas criptográficas e livro-razão imutável de evidências).
- **Consequences:** Estabelece o comportamento comportamental que o código do MVP deverá implementar estritamente, sem acoplamento a infraestrutura externa.
- **Hash:** `adr016-arch0003-core-engine-spec-20260719`

### ADR-017: ARCH-0004 Agent Architecture Design
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A integração de inteligência artificial deve seguir a orientação de não-dependência de fornecedores de modelos específicos e alinhamento aos princípios éticos do CDF.
- **Decision:** Aprovar ARCH-0004 especificando a Agent Architecture composta por 3 agentes focados (Mentor, Reviewer e Interviewer Agents), delimitando seus prompts de sistema, escopo de ferramentas, limites operacionais, mecanismos de memória e testes automáticos de conformidade (evitando geração direta de respostas).
- **Consequences:** Define as regras de comportamento dos agentes cognitivos do ecossistema, garantindo que o Builder mantenha o controle e protagonismo de seu próprio aprendizado.
- **Hash:** `adr017-arch0004-agent-architecture-20260719`

### ADR-018: ARCH-0005 Data Model Design
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A persistência de dados do CDF no MVP CLI-First deve ser eficiente, local e estruturada sem a complexidade de bancos de dados em nuvem.
- **Decision:** Aprovar ARCH-0005 definindo o armazenamento em disco usando arquivos JSON estruturados organizados na pasta local `.ascend/` do workspace, contendo esquemas JSON robustos para o perfil do Builder (`profile.json`) e livro-razão de evidências (`portfolio.json`), além de implementar um fluxo de transações atômicas de escrita contra arquivos temporários.
- **Consequences:** Garante simplicidade técnica para o MVP, isolamento absoluto dos dados (Local First) e mitigação contra corrupção de dados decorrente de falhas no CLI.
- **Hash:** `adr018-arch0005-data-model-20260719`

### ADR-019: ARCH-0006 MVP Technical Specification
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O desenvolvimento inicial do MVP requer uma stack tecnológica definida, uma estrutura modular de diretórios clara em `platform/` e comandos CLI mapeados de ponta a ponta.
- **Decision:** Aprovar ARCH-0006 adotando Python 3.10+, utilizando o pacote nativo `argparse` para a CLI para evitar dependências excessivas, definindo o leiaute exato de diretórios sob `platform/`, mapeando os comandos fundamentais (`init`, `status`, `mission start`, `mission submit`, `review`) e definindo a Definition of Done (DoD).
- **Consequences:** Provê as especificações concretas de engenharia para que o código comece a ser implementado de maneira limpa, testável e sem complexidades artificiais.
- **Hash:** `adr019-arch0006-mvp-tech-spec-20260719`

### ADR-020: System Architecture Phase Complete
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Todos os 6 documentos arquiteturais da Phase 1 foram criados, revisados e aprovados: ARCH-0001 (Overview), ARCH-0002 (Domain Model), ARCH-0003 (Core Engine Spec), ARCH-0004 (Agent Architecture), ARCH-0005 (Data Model) e ARCH-0006 (MVP Tech Spec).
- **Decision:** Selar a Phase 1 como concluída e habilitar o início do desenvolvimento de código do MVP (Sprint 1). A governança do projeto exige a verificação imediata da integridade do Shadow Ledger.
- **Consequences:** Bloqueia a edição direta dos blueprints da arquitetura sem nova submissão de ADRs e autoriza o início da codificação do ecossistema.
- **Hash:** `adr020-system-architecture-complete-20260719`

---

## Changelog

| Data | ADR | Ação |
|------|-----|------|
| 2026-07-19 | ADR-001 | Criação — Foundation + Platform split |
| 2026-07-19 | ADR-002 | Criação — Document naming convention |
| 2026-07-19 | ADR-003 | Criação — Governance toolkit |
| 2026-07-19 | ADR-004 | Criação — Canonical document hierarchy |
| 2026-07-19 | ADR-005 | Criação — First Principles como lei constitucional |
| 2026-07-19 | ADR-006 | Criação — Identity Architecture |
| 2026-07-19 | ADR-007 | Criação — Brand Architecture |
| 2026-07-19 | ADR-008 | Criação — Canonical Lexicon (Living Document) |
| 2026-07-19 | ADR-009 | Criação — Engineering Philosophy |
| 2026-07-19 | ADR-010 | **MILESTONE** — Foundation Phase v1.0 Complete |
| 2026-07-19 | ADR-011 | Criação — CLI-First MVP Strategy |
| 2026-07-19 | ADR-012 | Criação — Four Core Architectural Principles |
| 2026-07-19 | ADR-013 | Criação — ARCH-0001 System Architecture Overview |
| 2026-07-19 | ADR-014 | Criação — Architecture directory structure |
| 2026-07-19 | ADR-015 | Criação — ARCH-0002 Domain Model |
| 2026-07-19 | ADR-016 | Criação — ARCH-0003 Core Engine Specification |
| 2026-07-19 | ADR-017 | Criação — ARCH-0004 Agent Architecture |
| 2026-07-19 | ADR-018 | Criação — ARCH-0005 Data Model |
| 2026-07-19 | ADR-019 | Criação — ARCH-0006 MVP Technical Specification |
| 2026-07-19 | ADR-020 | **MILESTONE** — System Architecture Phase Complete |
| 2026-07-19 | ADR-021 | Criação — DOC-0008 Project Continuity Protocol |
| 2026-07-19 | ADR-022 | Criação — ARCH-0005 Data Model Specification (Revisão detalhada) |
| 2026-07-19 | ADR-023 | Criação — ARCH-0006 MVP Technical Specification (Revisão detalhada) |
| 2026-07-19 | ADR-024 | Criação — BUILD-0001 Implementation Roadmap |
| 2026-07-19 | ADR-025 | Criação — AGENT-0001 DeepSeek Implementation Profile |
| 2026-07-19 | ADR-026 | Criação — Python Version Support (>=3.11) |






```

### opencode.json

```
{
  "$schema": "https://opencode.ai/config.json",
  "shell": "C:\\Windows\\System32\\cmd.exe",
  "instructions": ["CONTEXT.md"]
}

```

### packages\cyber-foundations\achievements\achievements.yaml

```
spec:
  achievements:
    - id: primeiro-site
      name: Primeiro Site
      description: Publicou seu primeiro site HTML/CSS
      criteria:
        - "Completar a jornada Fundamentos Web"
      badge: badge-primeiro-site

    - id: logica-zero
      name: Lógica do Zero
      description: Completou os fundamentos de lógica de programação
      criteria:
        - "Completar a jornada Lógica de Programação"
      badge: badge-logica-zero

```

### packages\cyber-foundations\assessments\rubrics.yaml

```
spec:
  rubrics:
    - id: html-quality
      title: Qualidade HTML
      criteria:
        estrutura:
          weight: 30
          description: Uso correto de tags semânticas e estrutura HTML5
        acessibilidade:
          weight: 20
          description: Aplicação de boas práticas de acessibilidade
        validade:
          weight: 25
          description: Código válido sem erros de sintaxe
        organizacao:
          weight: 25
          description: Organização e legibilidade do código

    - id: css-quality
      title: Qualidade CSS
      criteria:
        layout:
          weight: 35
          description: Implementação correta do layout responsivo
        estilizacao:
          weight: 25
          description: Aplicação consistente de estilos e cores
        eficiencia:
          weight: 20
          description: Código CSS eficiente sem redundâncias
        organizacao:
          weight: 20
          description: Organização e manutenibilidade do CSS

```

### packages\cyber-foundations\competencies\competencies.yaml

```
spec:
  competencies:
    - id: html-fundamental
      name: HTML Fundamental
      description: Capacidade de estruturar páginas web com HTML semântico
      level: beginner
      evidence_required: true
      mastery_threshold: 80

    - id: css-fundamental
      name: CSS Fundamental
      description: Capacidade de estilizar páginas web com CSS moderno
      level: beginner
      evidence_required: true
      mastery_threshold: 80

    - id: logica-programacao
      name: Lógica de Programação
      description: Capacidade de resolver problemas com programação procedural
      level: beginner
      evidence_required: true
      mastery_threshold: 75

```

### packages\cyber-foundations\journeys\fundamentos-web\journey.yaml

```
metadata:
  id: fundamentos-web
  title: Fundamentos Web
  description: Aprenda os fundamentos do desenvolvimento web com HTML e CSS

spec:
  difficulty: beginner
  estimated_hours: 20
  unlocks:
    - logica-programacao

```

### packages\cyber-foundations\journeys\fundamentos-web\missions\css-foundations\mission.yaml

```
metadata:
  id: css-foundations
  title: CSS Foundations
  description: Estilize páginas web com CSS moderno

spec:
  difficulty: beginner
  estimated_minutes: 180
  xp: 200
  prerequisites:
    - html-foundations
  competencies:
    - css-fundamental
  challenge:
    type: practical
    description: >
      Estilize a página HTML criada na missão anterior.
      Utilize Flexbox para layout, defina cores, fontes e espaçamentos.
      Deixe a página responsiva para mobile e desktop.
  evidence:
    required: true
    types:
      - code
  assessment:
    rubric: css-quality

```

### packages\cyber-foundations\journeys\fundamentos-web\missions\html-foundations\mission.yaml

```
metadata:
  id: html-foundations
  title: HTML Foundations
  description: Estruture páginas web com HTML semântico

spec:
  difficulty: beginner
  estimated_minutes: 120
  xp: 150
  prerequisites: []
  competencies:
    - html-fundamental
  challenge:
    type: practical
    description: >
      Crie uma página HTML semântica apresentando um tema de sua escolha.
      Utilize tags como header, nav, main, section, article, footer.
      Inclua pelo menos uma imagem e uma lista.
  evidence:
    required: true
    types:
      - code
  assessment:
    rubric: html-quality

```

### packages\cyber-foundations\journeys\logica-programacao\journey.yaml

```
metadata:
  id: logica-programacao
  title: Lógica de Programação
  description: Aprenda lógica de programação com Python

spec:
  difficulty: beginner
  estimated_hours: 10
  unlocks: []

```

### packages\cyber-foundations\journeys\logica-programacao\missions\python-basics\mission.yaml

```
metadata:
  id: python-basics
  title: Python Basics
  description: "Fundamentos de Python: variáveis, condicionais e loops"

spec:
  difficulty: beginner
  estimated_minutes: 150
  xp: 200
  prerequisites: []
  competencies:
    - logica-programacao
  challenge:
    type: practical
    description: >
      Escreva um programa em Python que:
      1. Solicite o nome e idade do usuário
      2. Determine se é maior de idade
      3. Exiba uma contagem regressiva do número informado até zero
      4. Calcule a média de 3 notas informadas
  evidence:
    required: true
    types:
      - code
  assessment:
    rubric: ""

```

### packages\cyber-foundations\package.yaml

```
metadata:
  id: cyber-foundations
  version: 1.0.0
  title: Cyber Foundations
  description: Competências fundamentais para desenvolvimento web e lógica de programação
  author: ASCEND Project
  license: MIT

spec:
  runtime: ">=1.0"
  language: pt-BR
  estimated_hours: 30
  dependencies: []

capabilities:
  - evidence

```

### packages\git-foundations\achievements\achievements.yaml

```
spec:
  achievements:
    - id: primeiro-commit
      name: Primeiro Commit
      description: Fez seu primeiro commit no Git
      criteria:
        - "Completar a missão Git Basics"
      badge: badge-primeiro-commit

```

### packages\git-foundations\assessments\rubrics.yaml

```
spec:
  rubrics:
    - id: git-quality
      title: Qualidade Git
      criteria:
        commits:
          weight: 35
          description: Commits atômicos e mensagens descritivas
        branching:
          weight: 35
          description: Uso correto de branches e estratégia de branching
        documentacao:
          weight: 30
          description: Documentação do fluxo de trabalho

```

### packages\git-foundations\competencies\competencies.yaml

```
spec:
  competencies:
    - id: git-basics
      name: Git Basics
      description: Capacidade de inicializar repositórios e fazer commits
      level: beginner
      evidence_required: true
      mastery_threshold: 80

    - id: branching-merging
      name: Branching and Merging
      description: Capacidade de gerenciar branches e resolver conflitos de merge
      level: intermediate
      evidence_required: true
      mastery_threshold: 75

    - id: remote-collaboration
      name: Remote Collaboration
      description: Capacidade de trabalhar com repositórios remotos e colaborar em equipe
      level: intermediate
      evidence_required: true
      mastery_threshold: 75

```

### packages\git-foundations\journeys\git-essentials\journey.yaml

```
metadata:
  id: git-essentials
  title: Git Essentials
  description: Aprenda controle de versão com Git do básico à colaboração remota

spec:
  difficulty: beginner
  estimated_hours: 15
  unlocks: []

```

### packages\git-foundations\journeys\git-essentials\missions\git-basics\mission.yaml

```
metadata:
  id: git-basics
  title: Git Basics
  description: Inicialize repositórios, faça commits e entenda o fluxo básico do Git

spec:
  difficulty: beginner
  estimated_minutes: 120
  xp: 150
  prerequisites: []
  competencies:
    - git-basics
  challenge:
    type: practical
    description: >
      Complete as seguintes tarefas:
      1. Inicialize um repositório Git em um diretório novo
      2. Crie 3 arquivos e faça commits separados para cada um
      3. Verifique o log de commits e o status do repositório
      4. Crie um arquivo .gitignore ignorando arquivos .log
      5. Faça um commit incluindo apenas arquivos específicos
      6. Desfaça uma alteração antes do commit usando restore
      7. Documente todos os comandos utilizados
  evidence:
    required: true
    types:
      - code
      - document
  assessment:
    rubric: git-quality

```

### packages\git-foundations\package.yaml

```
metadata:
  id: git-foundations
  version: 1.0.0
  title: Git Foundations
  description: Competências fundamentais para controle de versão com Git
  author: ASCEND Institute
  license: MIT

spec:
  runtime: ">=1.0"
  language: pt-BR
  estimated_hours: 15
  dependencies: []

capabilities:
  - evidence

```

### packages\linux-foundations\achievements\achievements.yaml

```
spec:
  achievements:
    - id: primeiro-comando
      name: Primeiro Comando
      description: Executou seu primeiro comando no terminal Linux
      criteria:
        - "Completar a missão Terminal Navigation"
      badge: badge-primeiro-comando

    - id: mestre-dos-arquivos
      name: Mestre dos Arquivos
      description: Domina operações de arquivos no Linux
      criteria:
        - "Completar todas as missões de Linux Foundations"
      badge: badge-mestre-arquivos

```

### packages\linux-foundations\assessments\rubrics.yaml

```
spec:
  rubrics:
    - id: terminal-accuracy
      title: Precisão no Terminal
      criteria:
        comandos:
          weight: 40
          description: Uso correto dos comandos e flags
        eficiencia:
          weight: 30
          description: Escolha eficiente de comandos para cada tarefa
        seguranca:
          weight: 30
          description: Uso seguro de comandos que afetam o sistema

```

### packages\linux-foundations\competencies\competencies.yaml

```
spec:
  competencies:
    - id: terminal-basics
      name: Terminal Basics
      description: Capacidade de navegar pelo sistema de arquivos via terminal
      level: beginner
      evidence_required: true
      mastery_threshold: 80

    - id: file-operations
      name: File Operations
      description: Capacidade de criar, copiar, mover e remover arquivos e diretórios
      level: beginner
      evidence_required: true
      mastery_threshold: 80

    - id: permission-management
      name: Permission Management
      description: Capacidade de gerenciar permissões de arquivos e processos
      level: intermediate
      evidence_required: true
      mastery_threshold: 75

```

### packages\linux-foundations\journeys\linux-essentials\journey.yaml

```
metadata:
  id: linux-essentials
  title: Linux Essentials
  description: Aprenda navegação e operações fundamentais no terminal Linux

spec:
  difficulty: beginner
  estimated_hours: 20
  unlocks: []

```

### packages\linux-foundations\journeys\linux-essentials\missions\file-management\mission.yaml

```
metadata:
  id: file-management
  title: File Management
  description: Crie, copie, mova e remova arquivos e diretórios

spec:
  difficulty: beginner
  estimated_minutes: 120
  xp: 150
  prerequisites:
    - terminal-navigation
  competencies:
    - file-operations
  challenge:
    type: practical
    description: >
      Complete as seguintes tarefas:
      1. Crie 10 arquivos .txt em um diretório de teste
      2. Copie todos os arquivos .txt para um subdiretório backup/
      3. Renomeie 3 arquivos usando o comando mv
      4. Crie um arquivo vazio usando touch
      5. Use cat para concatenar 2 arquivos em um terceiro
      6. Remova o diretório de teste e todo seu conteúdo
      7. Documente cada comando em um arquivo README.md
  evidence:
    required: true
    types:
      - document
  assessment:
    rubric: terminal-accuracy

```

### packages\linux-foundations\journeys\linux-essentials\missions\terminal-navigation\mission.yaml

```
metadata:
  id: terminal-navigation
  title: Terminal Navigation
  description: Navegue pelo sistema de arquivos usando comandos de terminal

spec:
  difficulty: beginner
  estimated_minutes: 90
  xp: 120
  prerequisites: []
  competencies:
    - terminal-basics
  challenge:
    type: practical
    description: >
      Complete as seguintes tarefas no terminal Linux:
      1. Navegue até o diretório /var/log usando caminho absoluto
      2. Liste todos os arquivos (incluindo ocultos) no diretório home
      3. Crie uma estrutura de diretórios: ~/projetos/ascend/modulo-1
      4. Use o comando pwd e echo para exibir informações do sistema
      5. Salve o histórico dos comandos usados em um arquivo historico.txt
  evidence:
    required: true
    types:
      - document
      - code
  assessment:
    rubric: terminal-accuracy

```

### packages\linux-foundations\package.yaml

```
metadata:
  id: linux-foundations
  version: 1.0.0
  title: Linux Foundations
  description: Competências fundamentais para navegação e administração do terminal Linux
  author: ASCEND Institute
  license: MIT

spec:
  runtime: ">=1.0"
  language: pt-BR
  estimated_hours: 20
  dependencies: []

capabilities:
  - evidence

```

### packages\python-foundations\achievements\achievements.yaml

```
spec:
  achievements:
    - id: primeiro-script
      name: Primeiro Script
      description: Escreveu e executou seu primeiro script Python
      criteria:
        - "Completar a missão Python Syntax"
      badge: badge-primeiro-script

```

### packages\python-foundations\assessments\rubrics.yaml

```
spec:
  rubrics:
    - id: python-quality
      title: Qualidade Python
      criteria:
        sintaxe:
          weight: 30
          description: Código Python válido sem erros de sintaxe
        eficiencia:
          weight: 25
          description: Uso eficiente de estruturas de dados e algoritmos
        legibilidade:
          weight: 25
          description: Código legível com nomes descritivos e comentários
        boas-praticas:
          weight: 20
          description: Segue PEP 8 e boas práticas da linguagem

```

### packages\python-foundations\competencies\competencies.yaml

```
spec:
  competencies:
    - id: python-syntax
      name: Python Syntax
      description: Capacidade de escrever programas Python com sintaxe correta
      level: beginner
      evidence_required: true
      mastery_threshold: 80

    - id: data-structures
      name: Data Structures
      description: Capacidade de usar listas, dicionários, tuplas e conjuntos
      level: beginner
      evidence_required: true
      mastery_threshold: 75

    - id: functions-modules
      name: Functions and Modules
      description: Capacidade de criar funções, módulos e organizar código
      level: intermediate
      evidence_required: true
      mastery_threshold: 75

```

### packages\python-foundations\journeys\python-essentials\journey.yaml

```
metadata:
  id: python-essentials
  title: Python Essentials
  description: Aprenda programação Python do básico à organização de código

spec:
  difficulty: beginner
  estimated_hours: 25
  unlocks: []

```

### packages\python-foundations\journeys\python-essentials\missions\python-syntax\mission.yaml

```
metadata:
  id: python-syntax
  title: Python Syntax
  description: Escreva programas Python com sintaxe correta e variáveis

spec:
  difficulty: beginner
  estimated_minutes: 120
  xp: 150
  prerequisites: []
  competencies:
    - python-syntax
  challenge:
    type: practical
    description: >
      Escreva um programa Python que:
      1. Solicite o nome e a idade do usuário
      2. Calcule o ano de nascimento aproximado
      3. Determine se é maior de idade
      4. Exiba uma contagem regressiva de 10 até 0
      5. Calcule a média de 4 notas informadas
      6. Use f-strings para formatar a saída
  evidence:
    required: true
    types:
      - code
  assessment:
    rubric: python-quality

```

### packages\python-foundations\package.yaml

```
metadata:
  id: python-foundations
  version: 1.0.0
  title: Python Foundations
  description: Competências fundamentais para programação em Python
  author: ASCEND Institute
  license: MIT

spec:
  runtime: ">=1.0"
  language: pt-BR
  estimated_hours: 25
  dependencies: []

capabilities:
  - evidence

```

### pyproject.toml

```
[project]
name = "ascend"
version = "0.1.0"
description = "ASCEND Competency Development Framework"
readme = "README.md"
license = "MIT"
requires-python = ">=3.11"
dependencies = [
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
]

[project.scripts]
ascend = "ascend.cli.main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]

```

### README.md

```markdown
# ASCEND — Open Competency Runtime

> An Open Competency Runtime and Specification Ecosystem for Evidence-Based Learning.

---

## Quickstart

### Installation

```bash
pip install ascend-runtime
```

### Run Your First Package

```python
from ascend import Runtime

runtime = Runtime()
report = runtime.run(
    package="packages/cyber-foundations",
    builder="john",
    evidence="<html><header>Meu site</header></html>"
)

print(report.summary())
```

### Via CLI

```bash
ascend run packages/cyber-foundations --builder john --evidence resposta.html
```

### Create a Package

```bash
ascend init my-package
```

```bash
ascend package validate
```

---

## Specifications

| Spec | Description | Status |
|---|---|---|
| [APS v1.0](docs/spec/SPEC-0001_APS_v1.md) | ASCEND Package Specification | Stable |
| [AEP v1.0](docs/spec/SPEC-0002_AEP_v1.md) | ASCEND Execution Protocol | Stable |
| [ARP v0.1](docs/spec/SPEC-0003_ARP_v1.md) | ASCEND Registry Protocol | Draft |
| [AAP v0.1](docs/spec/SPEC-0004_AAP_v1.md) | ASCEND Agent Protocol | Draft |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                   CLI / API                  │
├─────────────────────────────────────────────┤
│              ASCEND Runtime Kernel           │
│  ┌──────────┬──────────┬──────────────────┐  │
│  │ Journey  │ Mission  │   Assessment     │  │
│  │ Runner   │ Runner   │   Pipeline       │  │
│  ├──────────┼──────────┼──────────────────┤  │
│  │ Challenge│ Competency│   Event         │  │
│  │ Runner   │ Engine   │   Collector      │  │
│  └──────────┴──────────┴──────────────────┘  │
│         RuntimeOrchestrator                  │
├─────────────────────────────────────────────┤
│              Domain Layer                     │
├─────────────────────────────────────────────┤
│           Infrastructure Layer                │
└─────────────────────────────────────────────┘
```

---

## Packages

Official reference packages:

| Package | Description | Status |
|---|---|---|
| cyber-foundations | Web development fundamentals | Published |
| linux-foundations | Linux terminal essentials | Published |
| git-foundations | Git version control basics | Published |
| python-foundations | Python programming basics | Published |

---

## Project Status

**Current Phase:** Phase 4 — Standardization  
**Runtime Version:** 0.1.0  
**Test Suite:** 163 tests, all passing  

---

## License

MIT

```

### ROADMAP_2035.md

```markdown
# ASCEND Roadmap 2026–2035

**Last updated:** 2026-07-19  
**Author:** Chief Architect, ASCEND Institute  

---

## Vision

> An Open Competency Runtime and Specification Ecosystem for Evidence-Based Learning.

This roadmap defines the strategic milestones for the next decade.
Each year represents a thematic cycle, not a rigid deadline.

---

## 2026 — Foundation

- [x] Runtime Kernel v1.0
- [x] APS v1.0 (Package Specification)
- [x] AEP v1.0 (Execution Protocol)
- [ ] 4 official reference packages
- [ ] CLI v1.0
- [ ] Public documentation
- [ ] Open Source launch

**Theme:** *"Make it work."*

---

## 2027 — Registry & SDK

- [ ] ARP v1.0 (Registry Protocol)
- [ ] Registry server implementation
- [ ] `ascend-sdk-python` v1.0
- [ ] 20 community packages
- [ ] Package signing and verification
- [ ] Dependency resolution

**Theme:** *"Make it shareable."*

---

## 2028 — Developer Experience

- [ ] VS Code extension
- [ ] JetBrains plugin
- [ ] REST API v1.0
- [ ] `ascend-studio` alpha
- [ ] CI/CD integration
- [ ] 100+ packages available

**Theme:** *"Make it accessible."*

---

## 2029 — Intelligence Layer

- [ ] AAP v1.0 (Agent Protocol)
- [ ] AI Reviewer agent
- [ ] AI Mentor agent
- [ ] AI Interviewer agent
- [ ] Hybrid assessment pipeline
- [ ] Automated feedback generation

**Theme:** *"Make it intelligent."*

---

## 2030 — Enterprise

- [ ] Enterprise deployment guide
- [ ] LMS integration (Moodle, Canvas)
- [ ] SCORM adapter
- [ ] SSO/LDAP authentication
- [ ] Audit logging
- [ ] Compliance reporting

**Theme:** *"Make it enterprise-ready."*

---

## 2031 — Global Community

- [ ] 10,000+ community packages
- [ ] Translation framework
- [ ] Regional registries
- [ ] Community governance
- [ ] Annual ASCEND conference
- [ ] Academic partnerships

**Theme:** *"Make it global."*

---

## 2032 — Ecosystem Maturity

- [ ] ASCEND Studio v1.0
- [ ] Visual package editor
- [ ] Drag-and-drop journey builder
- [ ] Built-in analytics
- [ ] Team collaboration

**Theme:** *"Make it visual."*

---

## 2033 — Interoperability

- [ ] Open Competency Standard submission
- [ ] Cross-platform runtime (WebAssembly)
- [ ] Mobile SDK
- [ ] IoT runtime
- [ ] Embedded systems support

**Theme:** *"Make it universal."*

---

## 2034 — Self-Sustaining Ecosystem

- [ ] Marketplace with 100k+ users
- [ ] Certification program
- [ ] Paid enterprise tiers
- [ ] Foundation grants
- [ ] Full-time core team

**Theme:** *"Make it sustainable."*

---

## 2035 — Open Standard

- [ ] ISO/IEC standardization process
- [ ] Government adoption programs
- [ ] Academic curriculum integration
- [ ] 1M+ builders
- [ ] ASCEND as a recognized open standard

**Theme:** *"Make it eternal."*

---

## Principles

1. **Spec first, code second** — Every feature starts as a specification.
2. **Backward compatibility** — Breaking changes require MAJOR version bumps.
3. **Content over features** — Great packages matter more than great tooling.
4. **Community before company** — The ecosystem outlives any organization.
5. **Ten-year thinking** — Every decision must be defensible in 2035.

```

### scripts\generate_summary.py

```python
import os
from pathlib import Path

BASE = Path(r"D:\ASCEND PROJECT")
EXCLUDE_DIRS = {".venv", ".git", ".pytest_cache", "__pycache__", ".github"}
EXCLUDE_FILES = {"desktop.ini", ".gitignore", "tmp_summary.py"}
TEXT_EXTENSIONS = {".py", ".md", ".toml", ".json", ".yaml", ".yml", ".cfg", ".txt", ".ini"}

def should_include(path: Path):
    parts = set(path.parts)
    if EXCLUDE_DIRS & parts:
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.suffix in TEXT_EXTENSIONS:
        return True
    return False

def main():
    output = []
    output.append("# ASCEND PROJECT — Full Context\n")
    output.append("## Directory Structure\n")
    for p in sorted(Path(BASE).rglob("*")):
        if p.is_file() and should_include(p):
            rel = p.relative_to(BASE)
            output.append(f"- {rel}")

    output.append("\n\n## File Contents\n")
    for p in sorted(Path(BASE).rglob("*")):
        if p.is_file() and should_include(p):
            rel = p.relative_to(BASE)
            output.append(f"\n### {rel}\n")
            output.append("```" + ("python" if p.suffix == ".py" else "markdown" if p.suffix == ".md" else ""))
            try:
                content = p.read_text(encoding="utf-8")
                output.append(content)
            except Exception as e:
                output.append(f"[Error reading: {e}]")
            output.append("```")

    Path("SUMMARY_FOR_CHATGPT.md").write_text("\n".join(output), encoding="utf-8")
    print("Done! File saved as SUMMARY_FOR_CHATGPT.md")

if __name__ == "__main__":
    BASE = r"D:\ASCEND PROJECT"
    main()

```

### src\ascend\__init__.py

```python
"""
ASCEND Core Package

Competency Development Framework
"""

from .api.runtime import Runtime

__version__ = "0.1.0"
__all__ = ["Runtime"]

```

### src\ascend\api\__init__.py

```python

```

### src\ascend\api\runtime.py

```python
from pathlib import Path
from typing import List

from ascend.domain.builder import Builder
from ascend.runtime.kernel import RuntimeKernel
from ascend.runtime.report import ExecutionReport
from ascend.shared.clock import SystemClock


class Runtime:
    def __init__(self) -> None:
        self._kernel = RuntimeKernel()

    def run(
        self,
        package: str | Path,
        builder: str | Builder,
        evidence: str | dict[str, str] | None = None,
    ) -> ExecutionReport:
        pkg_path = Path(package)

        b: Builder
        if isinstance(builder, Builder):
            b = builder
        else:
            b = Builder(builder)

        ev_input: dict[str, str] = {}
        if evidence is not None:
            if isinstance(evidence, dict):
                ev_input = evidence
            else:
                ev_path = Path(evidence)
                if ev_path.exists():
                    ev_input = {"_default": ev_path.read_text(encoding="utf-8")}
                else:
                    ev_input = {"_default": evidence}

        report = self._kernel.run(
            package_path=pkg_path,
            builder=b,
            evidence_input=ev_input,
        )
        return report

```

### src\ascend\application\__init__.py

```python
from .exceptions import (
    BuilderNotFound,
    MissionNotFound,
    EvidenceNotFound,
    CompetencyNotFound,
    MissionAlreadyStarted,
    EvidenceRequired,
    MissionLocked,
    CompetencyLocked,
)

__all__ = [
    "BuilderNotFound",
    "MissionNotFound",
    "EvidenceNotFound",
    "CompetencyNotFound",
    "MissionAlreadyStarted",
    "EvidenceRequired",
    "MissionLocked",
    "CompetencyLocked",
]

```

### src\ascend\application\commands\__init__.py

```python
from .create_builder import CreateBuilder
from .start_mission import StartMission
from .submit_evidence import SubmitEvidence
from .complete_assessment import CompleteAssessment
from .unlock_competency import UnlockCompetency

__all__ = [
    "CreateBuilder",
    "StartMission",
    "SubmitEvidence",
    "CompleteAssessment",
    "UnlockCompetency",
]

```

### src\ascend\application\commands\complete_assessment.py

```python
from dataclasses import dataclass


@dataclass
class CompleteAssessment:
    evidence_id: str
    score: float
    feedback: str = ""
    reviewer: str = ""

```

### src\ascend\application\commands\create_builder.py

```python
from dataclasses import dataclass


@dataclass
class CreateBuilder:
    username: str

```

### src\ascend\application\commands\start_mission.py

```python
from dataclasses import dataclass


@dataclass
class StartMission:
    builder_id: str
    mission_id: str

```

### src\ascend\application\commands\submit_evidence.py

```python
from dataclasses import dataclass

from ascend.domain.evidence import EvidenceType


@dataclass
class SubmitEvidence:
    builder_id: str
    mission_id: str
    artifact: str
    evidence_type: EvidenceType = EvidenceType.DOCUMENT

```

### src\ascend\application\commands\unlock_competency.py

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class UnlockCompetency:
    builder_id: str
    name: str
    description: str = ""
    level: int = 1
    criteria: List[str] = field(default_factory=list)

```

### src\ascend\application\dto\__init__.py

```python
from .builder_dto import BuilderDTO
from .mission_dto import MissionDTO
from .evidence_dto import EvidenceDTO

__all__ = [
    "BuilderDTO",
    "MissionDTO",
    "EvidenceDTO",
]

```

### src\ascend\application\dto\builder_dto.py

```python
from dataclasses import dataclass


@dataclass
class BuilderDTO:
    id: str
    username: str
    level: int
    xp: int
    competency_count: int = 0
    achievement_count: int = 0
    active_mission_count: int = 0

```

### src\ascend\application\dto\evidence_dto.py

```python
from dataclasses import dataclass


@dataclass
class EvidenceDTO:
    id: str
    artifact: str
    type: str
    status: str
    builder_id: str
    submitted_at: str = ""

```

### src\ascend\application\dto\mission_dto.py

```python
from dataclasses import dataclass


@dataclass
class MissionDTO:
    id: str
    title: str
    objective: str
    difficulty: int
    xp_reward: int
    status: str

```

### src\ascend\application\exceptions.py

```python
class BuilderNotFound(Exception):
    pass


class MissionNotFound(Exception):
    pass


class EvidenceNotFound(Exception):
    pass


class CompetencyNotFound(Exception):
    pass


class MissionAlreadyStarted(Exception):
    pass


class EvidenceRequired(Exception):
    pass


class MissionLocked(Exception):
    pass


class CompetencyLocked(Exception):
    pass

```

### src\ascend\application\interfaces\__init__.py

```python
from .repositories import (
    BuilderRepository,
    MissionRepository,
    EvidenceRepository,
    CompetencyRepository,
    JourneyRepository,
)
from .event_bus import EventBus

__all__ = [
    "BuilderRepository",
    "MissionRepository",
    "EvidenceRepository",
    "CompetencyRepository",
    "JourneyRepository",
    "EventBus",
]

```

### src\ascend\application\interfaces\event_bus.py

```python
from typing import List, Protocol

from ascend.domain.events import DomainEvent


class EventBus(Protocol):
    def publish(self, events: List[DomainEvent]) -> None: ...

```

### src\ascend\application\interfaces\repositories.py

```python
from typing import List, Optional, Protocol

from ascend.domain.builder import Builder
from ascend.domain.mission import Mission
from ascend.domain.evidence import Evidence
from ascend.domain.competency import Competency
from ascend.domain.journey import Journey


class BuilderRepository(Protocol):
    def save(self, builder: Builder) -> None: ...
    def get(self, builder_id: str) -> Builder: ...
    def get_by_username(self, username: str) -> Optional[Builder]: ...
    def list(self) -> List[Builder]: ...


class MissionRepository(Protocol):
    def save(self, mission: Mission) -> None: ...
    def get(self, mission_id: str) -> Mission: ...
    def list_by_journey(self, journey_id: str) -> List[Mission]: ...


class EvidenceRepository(Protocol):
    def save(self, evidence: Evidence) -> None: ...
    def get(self, evidence_id: str) -> Evidence: ...
    def list_by_builder(self, builder_id: str) -> List[Evidence]: ...


class CompetencyRepository(Protocol):
    def save(self, competency: Competency) -> None: ...
    def get(self, competency_id: str) -> Competency: ...
    def list_by_builder(self, builder_id: str) -> List[Competency]: ...


class JourneyRepository(Protocol):
    def save(self, journey: Journey) -> None: ...
    def get(self, journey_id: str) -> Journey: ...
    def list(self) -> List[Journey]: ...

```

### src\ascend\application\services\__init__.py

```python
from .builder_service import BuilderService
from .mission_service import MissionService
from .competency_service import CompetencyService

__all__ = [
    "BuilderService",
    "MissionService",
    "CompetencyService",
]

```

### src\ascend\application\services\builder_service.py

```python
from ascend.application.commands.create_builder import CreateBuilder
from ascend.application.dto.builder_dto import BuilderDTO
from ascend.application.exceptions import BuilderNotFound
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import BuilderRepository
from ascend.domain.builder import Builder


class BuilderService:
    def __init__(self, repo: BuilderRepository, event_bus: EventBus) -> None:
        self._repo = repo
        self._event_bus = event_bus

    def create_builder(self, command: CreateBuilder) -> BuilderDTO:
        builder = Builder(username=command.username)
        self._repo.save(builder)
        self._event_bus.publish(builder.events)
        return self._to_dto(builder)

    def get_builder(self, builder_id: str) -> BuilderDTO:
        builder = self._repo.get(builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {builder_id} not found")
        return self._to_dto(builder)

    def gain_xp(self, builder_id: str, amount: int) -> BuilderDTO:
        builder = self._repo.get(builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {builder_id} not found")
        builder.gain_xp(amount)
        self._repo.save(builder)
        self._event_bus.publish(builder.events)
        return self._to_dto(builder)

    def _to_dto(self, builder: Builder) -> BuilderDTO:
        return BuilderDTO(
            id=builder.id,
            username=builder.username,
            level=builder.level,
            xp=builder.xp,
            competency_count=len(builder.competencies),
            achievement_count=len(builder.achievements),
            active_mission_count=len(builder.active_missions),
        )

```

### src\ascend\application\services\competency_service.py

```python
from ascend.application.commands.unlock_competency import UnlockCompetency
from ascend.application.dto.builder_dto import BuilderDTO
from ascend.application.exceptions import BuilderNotFound
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import (
    BuilderRepository,
    CompetencyRepository,
)
from ascend.domain.competency import Competency


class CompetencyService:
    def __init__(
        self,
        builder_repo: BuilderRepository,
        competency_repo: CompetencyRepository,
        event_bus: EventBus,
    ) -> None:
        self._builder_repo = builder_repo
        self._competency_repo = competency_repo
        self._event_bus = event_bus

    def unlock_competency(self, command: UnlockCompetency) -> BuilderDTO:
        builder = self._builder_repo.get(command.builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {command.builder_id} not found")
        competency = Competency(
            name=command.name,
            description=command.description,
            level=command.level,
            criteria=command.criteria,
        )
        builder.add_competency(competency)
        self._builder_repo.save(builder)
        self._competency_repo.save(competency)
        self._event_bus.publish(builder.events)
        return BuilderDTO(
            id=builder.id,
            username=builder.username,
            level=builder.level,
            xp=builder.xp,
            competency_count=len(builder.competencies),
            achievement_count=len(builder.achievements),
            active_mission_count=len(builder.active_missions),
        )

```

### src\ascend\application\services\mission_service.py

```python
from ascend.application.commands.start_mission import StartMission
from ascend.application.commands.submit_evidence import SubmitEvidence
from ascend.application.dto.mission_dto import MissionDTO
from ascend.application.dto.evidence_dto import EvidenceDTO
from ascend.application.exceptions import BuilderNotFound, MissionNotFound
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import (
    BuilderRepository,
    MissionRepository,
    EvidenceRepository,
)
from ascend.domain.builder import Builder
from ascend.domain.evidence import Evidence
from ascend.domain.mission import Mission


class MissionService:
    def __init__(
        self,
        builder_repo: BuilderRepository,
        mission_repo: MissionRepository,
        evidence_repo: EvidenceRepository,
        event_bus: EventBus,
    ) -> None:
        self._builder_repo = builder_repo
        self._mission_repo = mission_repo
        self._evidence_repo = evidence_repo
        self._event_bus = event_bus

    def start_mission(self, command: StartMission) -> MissionDTO:
        builder = self._builder_repo.get(command.builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {command.builder_id} not found")
        mission = self._mission_repo.get(command.mission_id)
        if not mission:
            raise MissionNotFound(f"Mission {command.mission_id} not found")
        builder.start_mission(mission)
        self._builder_repo.save(builder)
        self._mission_repo.save(mission)
        self._event_bus.publish(builder.events)
        return self._mission_to_dto(mission)

    def submit_evidence(self, command: SubmitEvidence) -> EvidenceDTO:
        builder = self._builder_repo.get(command.builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {command.builder_id} not found")
        mission = self._mission_repo.get(command.mission_id)
        if not mission:
            raise MissionNotFound(f"Mission {command.mission_id} not found")
        evidence = Evidence(
            artifact=command.artifact,
            type=command.evidence_type,
        )
        builder.submit_evidence(evidence, mission)
        self._builder_repo.save(builder)
        self._mission_repo.save(mission)
        self._evidence_repo.save(evidence)
        self._event_bus.publish(builder.events)
        return self._evidence_to_dto(evidence)

    def get_mission(self, mission_id: str) -> MissionDTO:
        mission = self._mission_repo.get(mission_id)
        if not mission:
            raise MissionNotFound(f"Mission {mission_id} not found")
        return self._mission_to_dto(mission)

    def _mission_to_dto(self, mission: Mission) -> MissionDTO:
        return MissionDTO(
            id=mission.id,
            title=mission.title,
            objective=mission.objective,
            difficulty=mission.difficulty,
            xp_reward=mission.xp_reward,
            status=mission.status.value,
        )

    def _evidence_to_dto(self, evidence: Evidence) -> EvidenceDTO:
        return EvidenceDTO(
            id=evidence.id,
            artifact=evidence.artifact,
            type=evidence.type.value,
            status=evidence.status.value,
            builder_id=evidence.builder_id,
            submitted_at=(
                evidence.submitted_at.isoformat()
                if evidence.submitted_at
                else ""
            ),
        )

```

### src\ascend\cli\__init__.py

```python

```

### src\ascend\cli\commands\__init__.py

```python

```

### src\ascend\cli\main.py

```python
import argparse
import sys
from pathlib import Path

from ascend.api.runtime import Runtime
from ascend.runtime.report import ExecutionReport


def main() -> None:
    parser = argparse.ArgumentParser(prog="ascend", description="ASCEND Runtime")
    parser.add_argument("--version", action="store_true", help="Show version")
    sub = parser.add_subparsers(dest="command")

    pkg = sub.add_parser("package", help="Package commands")
    pkg_sub = pkg.add_subparsers(dest="subcommand")
    pkg_validate = pkg_sub.add_parser("validate", help="Validate a package")
    pkg_validate.add_argument("path", nargs="?", default=".", help="Package path")
    pkg_create = pkg_sub.add_parser("create", help="Create a new package")
    pkg_create.add_argument("name", help="Package name")

    run_parser = sub.add_parser("run", help="Run a package")
    run_parser.add_argument("path", nargs="?", default=".", help="Package path")
    run_parser.add_argument("--builder", default="default", help="Builder username")
    run_parser.add_argument("--evidence", help="Evidence file path or text")

    init_parser = sub.add_parser("init", help="Initialize a new package")
    init_parser.add_argument("name", nargs="?", default="my-package", help="Package name")

    sub.add_parser("doctor", help="Check system health")
    sub.add_parser("progress", help="Show builder progress")

    args = parser.parse_args()

    if args.version:
        _cmd_version()
    elif args.command == "run":
        _cmd_run(args)
    elif args.command == "package":
        _cmd_package(args)
    elif args.command == "init":
        _cmd_init(args)
    elif args.command == "doctor":
        _cmd_doctor()
    elif args.command == "progress":
        _cmd_progress()
    else:
        parser.print_help()


def _cmd_version() -> None:
    print("ASCEND Runtime v0.1.0")


def _cmd_run(args: argparse.Namespace) -> None:
    pkg_path = Path(args.path)
    if not (pkg_path / "package.yaml").exists():
        print(f"Error: no package.yaml found in {pkg_path}")
        sys.exit(1)

    evidence = args.evidence or ""
    rt = Runtime()
    report = rt.run(package=pkg_path, builder=args.builder, evidence=evidence)
    print(report.summary())


def _cmd_package(args: argparse.Namespace) -> None:
    if args.subcommand == "validate":
        _cmd_package_validate(args)
    elif args.subcommand == "create":
        _cmd_package_create(args)
    else:
        print("Usage: ascend package <validate|create> [options]")


def _cmd_package_validate(args: argparse.Namespace) -> None:
    from ascend.package_engine.loader import PackageLoader

    pkg_path = Path(args.path)
    loader = PackageLoader()
    pkg, result = loader.load(pkg_path)
    if result.valid:
        print(f"[OK] Package '{pkg.id}' v{pkg.version} is valid.")
        if result.warnings:
            for w in result.warnings:
                print(f"  [!] [{w.rule}] {w.message}")
    else:
        print(f"[FAIL] Package validation failed:")
        for e in result.errors:
            print(f"  [{e.level}] {e.rule}: {e.message}")
        sys.exit(1)


def _cmd_package_create(args: argparse.Namespace) -> None:
    name = args.name
    dest = Path.cwd() / name
    if dest.exists():
        print(f"Error: {dest} already exists")
        sys.exit(1)
    dest.mkdir(parents=True)
    (dest / "package.yaml").write_text(
        f'metadata:\n  id: {name}\n  version: 0.1.0\n  title: {name}\n  description: ""\n  author: ""\n  license: MIT\n\nspec:\n  runtime: ">=1.0"\n  language: en\n  estimated_hours: 1\n  dependencies: []\n\ncapabilities:\n  - evidence\n',
        encoding="utf-8",
    )
    (dest / "competencies").mkdir(exist_ok=True)
    (dest / "achievements").mkdir(exist_ok=True)
    (dest / "assessments").mkdir(exist_ok=True)
    (dest / "journeys").mkdir(exist_ok=True)
    (dest / "README.md").write_text(f"# {name}\n\nASCEND package.\n", encoding="utf-8")
    print(f"[OK] Package '{name}' created at {dest}")


def _cmd_init(args: argparse.Namespace) -> None:
    _cmd_package_create(args)


def _cmd_doctor() -> None:
    import sys as _sys
    print(f"[OK] Python: {_sys.version}")
    print("[OK] ASCEND Runtime: v0.1.0")
    print("[OK] System: OK")


def _cmd_progress() -> None:
    print("Progress tracking coming soon.")


if __name__ == "__main__":
    main()

```

### src\ascend\domain\__init__.py

```python
from .builder import Builder
from .competency import Competency
from .skill import Skill
from .journey import Journey
from .mission import Mission
from .challenge import Challenge
from .evidence import Evidence
from .assessment import Assessment
from .achievement import Achievement
from .events import (
    DomainEvent,
    EventType,
    BuilderCreated,
    MissionStarted,
    EvidenceSubmitted,
    AssessmentCompleted,
    CompetencyUnlocked,
    AchievementEarned,
)

__all__ = [
    "Builder",
    "Competency",
    "Skill",
    "Journey",
    "Mission",
    "Challenge",
    "Evidence",
    "Assessment",
    "Achievement",
    "DomainEvent",
    "EventType",
    "BuilderCreated",
    "MissionStarted",
    "EvidenceSubmitted",
    "AssessmentCompleted",
    "CompetencyUnlocked",
    "AchievementEarned",
]

```

### src\ascend\domain\achievement.py

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Achievement:
    name: str
    description: str = ""
    criteria: List[str] = field(default_factory=list)
    badge: str = ""
    id: str = ""
    earned_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.id:
            self.id = f"ach-{self.name.lower().replace(' ', '-')}"

    def earn(self) -> None:
        self.earned_at = datetime.now()

    @property
    def is_earned(self) -> bool:
        return self.earned_at is not None

```

### src\ascend\domain\assessment.py

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Assessment:
    evidence_id: str
    score: float = 0.0
    feedback: str = ""
    reviewer: str = ""
    id: str = ""
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.id:
            self.id = f"assess-{self.evidence_id}"

    @property
    def is_approved(self) -> bool:
        return self.score >= 0.7

    @property
    def is_excellent(self) -> bool:
        return self.score >= 0.9

```

### src\ascend\domain\builder.py

```python
from dataclasses import dataclass, field
from typing import List

from .achievement import Achievement
from .competency import Competency
from .events import BuilderCreated, DomainEvent
from .evidence import Evidence
from .mission import Mission


@dataclass
class Builder:
    username: str
    id: str = ""
    level: int = 1
    xp: int = 0
    competencies: List[Competency] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)
    missions: List[Mission] = field(default_factory=list)
    evidence_list: List[Evidence] = field(default_factory=list)
    events: List[DomainEvent] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = f"builder-{self.username.lower()}"
        self.events.append(BuilderCreated(self.id, self.username))

    def start_mission(self, mission: Mission) -> None:
        mission.start()
        self.missions.append(mission)

    def submit_evidence(self, evidence: Evidence, mission: Mission) -> None:
        evidence.submit(self.id)
        mission.submit(evidence)
        self.evidence_list.append(evidence)

    def add_competency(self, competency: Competency) -> None:
        existing = [c for c in self.competencies if c.name == competency.name]
        if existing:
            existing[0].level = max(existing[0].level, competency.level)
        else:
            self.competencies.append(competency)

    def add_achievement(self, achievement: Achievement) -> None:
        if achievement not in self.achievements:
            self.achievements.append(achievement)

    def earn_achievement(self, achievement: Achievement) -> None:
        self.add_achievement(achievement)

    def add_xp(self, amount: int) -> None:
        self.xp += amount
        new_level = (self.xp // 500) + 1
        if new_level > self.level:
            self.level = new_level

    def gain_xp(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("XP cannot be negative")
        self.add_xp(amount)

    @property
    def active_missions(self) -> List[Mission]:
        return [m for m in self.missions if m.is_active]

    @property
    def completed_missions(self) -> List[Mission]:
        return [m for m in self.missions if m.is_completed]

```

### src\ascend\domain\challenge.py

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class Challenge:
    description: str
    requirements: List[str] = field(default_factory=list)
    validation_rules: List[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            import hashlib
            self.id = f"challenge-{hashlib.md5(self.description.encode()).hexdigest()[:8]}"

```

### src\ascend\domain\competency.py

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class Competency:
    name: str
    description: str = ""
    level: int = 1
    criteria: List[str] = field(default_factory=list)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"comp-{self.name.lower().replace(' ', '-')}"

    def increase_level(self) -> None:
        self.level += 1

    def check_completion(self, completed_criteria: List[str]) -> bool:
        if not self.criteria:
            return True
        matched = sum(1 for c in self.criteria if c in completed_criteria)
        return matched / len(self.criteria) >= 0.5

```

### src\ascend\domain\events.py

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class EventType(Enum):
    BUILDER_CREATED = "builder_created"
    MISSION_STARTED = "mission_started"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    ASSESSMENT_COMPLETED = "assessment_completed"
    COMPETENCY_UNLOCKED = "competency_unlocked"
    ACHIEVEMENT_EARNED = "achievement_earned"


@dataclass
class DomainEvent:
    event_id: str
    event_type: EventType
    aggregate_id: str
    payload: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


def BuilderCreated(builder_id: str, username: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{builder_id}-created",
        event_type=EventType.BUILDER_CREATED,
        aggregate_id=builder_id,
        payload={"builder_id": builder_id, "username": username},
    )


def MissionStarted(mission_id: str, builder_id: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{mission_id}-started",
        event_type=EventType.MISSION_STARTED,
        aggregate_id=mission_id,
        payload={"mission_id": mission_id, "builder_id": builder_id},
    )


def EvidenceSubmitted(evidence_id: str, mission_id: str, builder_id: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{evidence_id}-submitted",
        event_type=EventType.EVIDENCE_SUBMITTED,
        aggregate_id=evidence_id,
        payload={
            "evidence_id": evidence_id,
            "mission_id": mission_id,
            "builder_id": builder_id,
        },
    )


def AssessmentCompleted(assessment_id: str, evidence_id: str, score: float) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{assessment_id}-completed",
        event_type=EventType.ASSESSMENT_COMPLETED,
        aggregate_id=assessment_id,
        payload={
            "assessment_id": assessment_id,
            "evidence_id": evidence_id,
            "score": score,
        },
    )


def CompetencyUnlocked(competency_id: str, builder_id: str, level: int) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{competency_id}-unlocked",
        event_type=EventType.COMPETENCY_UNLOCKED,
        aggregate_id=competency_id,
        payload={
            "competency_id": competency_id,
            "builder_id": builder_id,
            "level": level,
        },
    )


def AchievementEarned(achievement_id: str, builder_id: str) -> DomainEvent:
    return DomainEvent(
        event_id=f"evt-{achievement_id}-earned",
        event_type=EventType.ACHIEVEMENT_EARNED,
        aggregate_id=achievement_id,
        payload={
            "achievement_id": achievement_id,
            "builder_id": builder_id,
        },
    )

```

### src\ascend\domain\evidence.py

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class EvidenceType(Enum):
    CODE = "code"
    DOCUMENT = "document"
    PROJECT = "project"
    REPORT = "report"
    VIDEO = "video"
    EXPERIMENT = "experiment"
    PRESENTATION = "presentation"
    ANALYSIS = "analysis"


class EvidenceStatus(Enum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


@dataclass
class Evidence:
    artifact: str
    type: EvidenceType = EvidenceType.DOCUMENT
    id: str = ""
    builder_id: str = ""
    mission_id: str = ""
    status: EvidenceStatus = EvidenceStatus.SUBMITTED
    submitted_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.id:
            import hashlib
            raw = f"{self.artifact}{datetime.now().isoformat()}"
            self.id = f"ev-{hashlib.md5(raw.encode()).hexdigest()[:12]}"

    def submit(self, builder_id: str) -> None:
        self.builder_id = builder_id
        self.status = EvidenceStatus.SUBMITTED
        self.submitted_at = datetime.now()

    def accept(self) -> None:
        self.status = EvidenceStatus.ACCEPTED

    def reject(self) -> None:
        self.status = EvidenceStatus.REJECTED

    @property
    def is_pending(self) -> bool:
        return self.status == EvidenceStatus.SUBMITTED

```

### src\ascend\domain\journey.py

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List

from .mission import Mission


class JourneyStatus(Enum):
    LOCKED = "locked"
    AVAILABLE = "available"
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass
class Journey:
    name: str
    objective: str = ""
    missions: List[Mission] = field(default_factory=list)
    status: JourneyStatus = JourneyStatus.AVAILABLE
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"journey-{self.name.lower().replace(' ', '-')}"
        for mission in self.missions:
            if self.status == JourneyStatus.COMPLETED:
                mission.status = MissionStatus.COMPLETED

```

### src\ascend\domain\mission.py

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .evidence import Evidence


class MissionStatus(Enum):
    AVAILABLE = "available"
    STARTED = "started"
    EVIDENCE_SUBMITTED = "evidence_submitted"
    COMPLETED = "completed"


@dataclass
class Mission:
    title: str
    objective: str = ""
    difficulty: int = 1
    xp_reward: int = 100
    prerequisites: List[str] = field(default_factory=list)
    id: str = ""
    status: MissionStatus = MissionStatus.AVAILABLE
    evidence_list: List[Evidence] = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            self.id = f"mission-{self.title.lower().replace(' ', '-')}"

    def start(self) -> None:
        if self.status != MissionStatus.AVAILABLE:
            raise ValueError(f"Cannot start mission in status {self.status.value}")
        self.status = MissionStatus.STARTED

    def submit(self, evidence: Evidence) -> None:
        if self.status != MissionStatus.STARTED:
            raise ValueError(f"Cannot submit evidence for mission in status {self.status.value}")
        self.evidence_list.append(evidence)
        self.status = MissionStatus.EVIDENCE_SUBMITTED

    def complete(self) -> None:
        if self.status != MissionStatus.EVIDENCE_SUBMITTED:
            raise ValueError(f"Cannot complete mission in status {self.status.value}")
        self.status = MissionStatus.COMPLETED

    @property
    def is_active(self) -> bool:
        return self.status == MissionStatus.STARTED

    @property
    def is_completed(self) -> bool:
        return self.status == MissionStatus.COMPLETED

    def can_start(self, completed_mission_ids: List[str]) -> bool:
        return all(pid in completed_mission_ids for pid in self.prerequisites)

```

### src\ascend\domain\skill.py

```python
from dataclasses import dataclass


@dataclass
class Skill:
    name: str
    description: str = ""
    weight: float = 1.0
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = f"skill-{self.name.lower().replace(' ', '-')}"

```

### src\ascend\infrastructure\__init__.py

```python

```

### src\ascend\infrastructure\config\__init__.py

```python
from .settings import Settings

__all__ = ["Settings"]

```

### src\ascend\infrastructure\config\settings.py

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class Settings:
    db_path: str = ":memory:"
    debug: bool = False
    capabilities: dict = field(default_factory=lambda: {
        "persistence": True,
        "event_store": True,
        "ai_runtime": False,
        "plugin_sdk": False,
    })

```

### src\ascend\infrastructure\events\__init__.py

```python
from .memory_event_bus import MemoryEventBus

__all__ = ["MemoryEventBus"]

```

### src\ascend\infrastructure\events\memory_event_bus.py

```python
from typing import Callable, List

from ascend.domain.events import DomainEvent


class MemoryEventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, List[Callable]] = {}
        self._published: List[DomainEvent] = []

    def publish(self, events: List[DomainEvent]) -> None:
        for event in events:
            self._published.append(event)
            key = event.event_type.value
            for callback in self._subscribers.get(key, []):
                callback(event)

    def subscribe(self, event_type: str, callback: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    @property
    def published(self) -> List[DomainEvent]:
        return list(self._published)

    def clear(self) -> None:
        self._published.clear()
        self._subscribers.clear()

```

### src\ascend\infrastructure\persistence\__init__.py

```python

```

### src\ascend\infrastructure\persistence\sqlite\__init__.py

```python
from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase
from .builder_repository import SQLiteBuilderRepository
from .mission_repository import SQLiteMissionRepository
from .evidence_repository import SQLiteEvidenceRepository
from .event_store import SQliteEventStore
from .migrations import MigrationEngine

__all__ = [
    "ConnectionManager",
    "SQLiteRepositoryBase",
    "SQLiteBuilderRepository",
    "SQLiteMissionRepository",
    "SQLiteEvidenceRepository",
    "SQliteEventStore",
    "MigrationEngine",
]

```

### src\ascend\infrastructure\persistence\sqlite\builder_repository.py

```python
import json

from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.achievement import Achievement

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteBuilderRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def save(self, builder: Builder) -> None:
        self._execute(
            """INSERT OR REPLACE INTO builders (id, username, level, xp)
               VALUES (?, ?, ?, ?)""",
            (builder.id, builder.username, builder.level, builder.xp),
        )
        for comp in builder.competencies:
            self._execute(
                """INSERT OR REPLACE INTO competencies (id, name, description, level, criteria)
                   VALUES (?, ?, ?, ?, ?)""",
                (comp.id, comp.name, comp.description, comp.level, json.dumps(comp.criteria)),
            )
            self._execute(
                """INSERT OR REPLACE INTO builder_competencies (builder_id, competency_id, level, progress, evidence_count)
                   VALUES (?, ?, ?, ?, ?)""",
                (builder.id, comp.id, comp.level, 1.0 if comp.criteria else 0.0, 0),
            )
        for ach in builder.achievements:
            self._execute(
                """INSERT OR IGNORE INTO achievements (id, name, description, criteria)
                   VALUES (?, ?, ?, ?)""",
                (ach.id, ach.name, ach.description, json.dumps(ach.criteria)),
            )
            self._execute(
                """INSERT OR REPLACE INTO builder_achievements (builder_id, achievement_id, earned_at)
                   VALUES (?, ?, ?)""",
                (
                    builder.id,
                    ach.id,
                    ach.earned_at.isoformat() if ach.earned_at else None,
                ),
            )

    def get(self, builder_id: str) -> Builder | None:
        row = self._fetch_one(
            "SELECT id, username, level, xp FROM builders WHERE id = ?",
            (builder_id,),
        )
        if not row:
            return None

        builder = Builder(
            username=row["username"],
            id=row["id"],
            level=row["level"],
            xp=row["xp"],
        )
        builder.events.clear()

        ach_rows = self._fetch_all(
            """SELECT a.id, a.name, a.description, a.criteria, ba.earned_at
               FROM achievements a
               JOIN builder_achievements ba ON ba.achievement_id = a.id
               WHERE ba.builder_id = ?""",
            (builder_id,),
        )
        for ar in ach_rows:
            ach = Achievement(
                name=ar["name"],
                description=ar["description"],
                criteria=json.loads(ar["criteria"]) if ar["criteria"] else [],
                id=ar["id"],
            )
            if ar["earned_at"]:
                ach.earned_at = ar["earned_at"]
            builder.add_achievement(ach)

        comp_rows = self._fetch_all(
            """SELECT c.id, c.name, c.description, c.level, c.criteria
               FROM competencies c
               JOIN builder_competencies bc ON bc.competency_id = c.id
               WHERE bc.builder_id = ?""",
            (builder_id,),
        )
        for cr in comp_rows:
            comp = Competency(
                name=cr["name"],
                description=cr["description"],
                level=cr["level"],
                criteria=json.loads(cr["criteria"]) if cr["criteria"] else [],
                id=cr["id"],
            )
            builder.add_competency(comp)

        return builder

    def get_by_username(self, username: str) -> Builder | None:
        row = self._fetch_one(
            "SELECT id FROM builders WHERE username = ?",
            (username,),
        )
        if not row:
            return None
        return self.get(row["id"])

    def list(self) -> list[Builder]:
        rows = self._fetch_all("SELECT id FROM builders")
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]

```

### src\ascend\infrastructure\persistence\sqlite\connection.py

```python
import sqlite3
from threading import Lock


class ConnectionManager:
    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None
        self._lock = Lock()

    def get_connection(self) -> sqlite3.Connection:
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA foreign_keys = ON")
        return self._conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def reset(self) -> None:
        self.close()

```

### src\ascend\infrastructure\persistence\sqlite\event_store.py

```python
import json
from datetime import datetime
from typing import Any

from ascend.domain.events import DomainEvent

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQliteEventStore(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def append(self, event: DomainEvent) -> None:
        self._execute(
            """INSERT INTO events (id, aggregate_id, aggregate_type, event_type, payload, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                event.event_id,
                event.aggregate_id,
                event.event_type.value,
                event.event_type.value,
                json.dumps(event.payload, default=str),
                event.timestamp.isoformat(),
            ),
        )

    def append_many(self, events: list[DomainEvent]) -> None:
        for event in events:
            self.append(event)

    def get_by_aggregate(self, aggregate_id: str) -> list[dict[str, Any]]:
        return self._fetch_all(
            "SELECT * FROM events WHERE aggregate_id = ? ORDER BY created_at",
            (aggregate_id,),
        )

    def list_all(self) -> list[dict[str, Any]]:
        return self._fetch_all("SELECT * FROM events ORDER BY created_at")

```

### src\ascend\infrastructure\persistence\sqlite\evidence_repository.py

```python
from ascend.domain.evidence import Evidence, EvidenceStatus, EvidenceType

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteEvidenceRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def save(self, evidence: Evidence) -> None:
        self._execute(
            """INSERT OR REPLACE INTO evidence (id, builder_id, mission_id, artifact, type, status, submitted_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                evidence.id,
                evidence.builder_id,
                evidence.mission_id,
                evidence.artifact,
                evidence.type.value,
                evidence.status.value,
                evidence.submitted_at.isoformat() if evidence.submitted_at else None,
            ),
        )

    def get(self, evidence_id: str) -> Evidence | None:
        row = self._fetch_one(
            "SELECT id, builder_id, mission_id, artifact, type, status, submitted_at FROM evidence WHERE id = ?",
            (evidence_id,),
        )
        if not row:
            return None
        evidence = Evidence(
            artifact=row["artifact"],
            type=EvidenceType(row["type"]),
            id=row["id"],
            builder_id=row["builder_id"],
            mission_id=row["mission_id"],
            status=EvidenceStatus(row["status"]),
        )
        if row["submitted_at"]:
            from datetime import datetime
            evidence.submitted_at = datetime.fromisoformat(row["submitted_at"])
        return evidence

    def list_by_builder(self, builder_id: str) -> list[Evidence]:
        rows = self._fetch_all(
            "SELECT id FROM evidence WHERE builder_id = ?",
            (builder_id,),
        )
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]

```

### src\ascend\infrastructure\persistence\sqlite\migrations.py

```python
from .connection import ConnectionManager

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS builders (
    id TEXT PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    level INTEGER NOT NULL DEFAULT 1,
    xp INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS competencies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    level INTEGER NOT NULL DEFAULT 1,
    criteria TEXT NOT NULL DEFAULT '[]'
);

CREATE TABLE IF NOT EXISTS builder_competencies (
    builder_id TEXT NOT NULL REFERENCES builders(id),
    competency_id TEXT NOT NULL REFERENCES competencies(id),
    level INTEGER NOT NULL DEFAULT 1,
    progress REAL NOT NULL DEFAULT 0.0,
    evidence_count INTEGER NOT NULL DEFAULT 0,
    last_update TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (builder_id, competency_id)
);

CREATE TABLE IF NOT EXISTS missions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    objective TEXT NOT NULL DEFAULT '',
    difficulty INTEGER NOT NULL DEFAULT 1,
    xp_reward INTEGER NOT NULL DEFAULT 100,
    status TEXT NOT NULL DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS builder_missions (
    builder_id TEXT NOT NULL REFERENCES builders(id),
    mission_id TEXT NOT NULL REFERENCES missions(id),
    status TEXT NOT NULL DEFAULT 'available',
    PRIMARY KEY (builder_id, mission_id)
);

CREATE TABLE IF NOT EXISTS evidence (
    id TEXT PRIMARY KEY,
    builder_id TEXT NOT NULL REFERENCES builders(id),
    mission_id TEXT NOT NULL REFERENCES missions(id),
    artifact TEXT NOT NULL,
    type TEXT NOT NULL DEFAULT 'document',
    status TEXT NOT NULL DEFAULT 'submitted',
    submitted_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS assessments (
    id TEXT PRIMARY KEY,
    evidence_id TEXT NOT NULL REFERENCES evidence(id),
    reviewer TEXT NOT NULL DEFAULT '',
    score REAL NOT NULL DEFAULT 0.0,
    feedback TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    criteria TEXT NOT NULL DEFAULT '[]',
    badge TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS builder_achievements (
    builder_id TEXT NOT NULL REFERENCES builders(id),
    achievement_id TEXT NOT NULL REFERENCES achievements(id),
    earned_at TEXT NOT NULL DEFAULT (datetime('now')),
    PRIMARY KEY (builder_id, achievement_id)
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS journeys (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'available'
);

CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL DEFAULT (datetime('now')),
    description TEXT NOT NULL DEFAULT ''
);
"""


class MigrationEngine:
    def __init__(self, conn_manager: ConnectionManager) -> None:
        self._conn_manager = conn_manager

    def apply_all(self) -> None:
        conn = self._conn_manager.get_connection()
        conn.executescript(SCHEMA_SQL)

```

### src\ascend\infrastructure\persistence\sqlite\mission_repository.py

```python
from ascend.domain.mission import Mission, MissionStatus

from .connection import ConnectionManager
from .repository_base import SQLiteRepositoryBase


class SQLiteMissionRepository(SQLiteRepositoryBase):
    def __init__(self, conn_manager: ConnectionManager) -> None:
        super().__init__(conn_manager)

    def save(self, mission: Mission) -> None:
        self._execute(
            """INSERT OR REPLACE INTO missions (id, title, objective, difficulty, xp_reward, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                mission.id,
                mission.title,
                mission.objective,
                mission.difficulty,
                mission.xp_reward,
                mission.status.value,
            ),
        )

    def get(self, mission_id: str) -> Mission | None:
        row = self._fetch_one(
            "SELECT id, title, objective, difficulty, xp_reward, status FROM missions WHERE id = ?",
            (mission_id,),
        )
        if not row:
            return None
        mission = Mission(
            title=row["title"],
            objective=row["objective"],
            difficulty=row["difficulty"],
            xp_reward=row["xp_reward"],
            id=row["id"],
            status=MissionStatus(row["status"]),
        )
        return mission

    def list_by_journey(self, journey_id: str) -> list[Mission]:
        rows = self._fetch_all(
            "SELECT id FROM missions"
        )
        return [self.get(r["id"]) for r in rows if self.get(r["id"])]

```

### src\ascend\infrastructure\persistence\sqlite\repository_base.py

```python
import sqlite3
from typing import Any

from .connection import ConnectionManager


class SQLiteRepositoryBase:
    def __init__(self, conn_manager: ConnectionManager) -> None:
        self._conn_manager = conn_manager

    @property
    def _conn(self) -> sqlite3.Connection:
        return self._conn_manager.get_connection()

    def _execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def _executemany(self, sql: str, params: list[tuple]) -> sqlite3.Cursor:
        return self._conn.executemany(sql, params)

    def _fetch_one(self, sql: str, params: tuple = ()) -> dict | None:
        row = self._conn.execute(sql, params).fetchone()
        return dict(row) if row else None

    def _fetch_all(self, sql: str, params: tuple = ()) -> list[dict]:
        rows = self._conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

```

### src\ascend\infrastructure\uow.py

```python
from .persistence.sqlite.connection import ConnectionManager


class UnitOfWork:
    def __init__(self, conn_manager: ConnectionManager) -> None:
        self._conn_manager = conn_manager

    def __enter__(self) -> "UnitOfWork":
        conn = self._conn_manager.get_connection()
        conn.execute("BEGIN")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        conn = self._conn_manager.get_connection()
        if exc_type is not None:
            conn.rollback()
        else:
            conn.commit()

    def commit(self) -> None:
        conn = self._conn_manager.get_connection()
        conn.commit()

    def rollback(self) -> None:
        conn = self._conn_manager.get_connection()
        conn.rollback()

```

### src\ascend\package_engine\__init__.py

```python
from .models import (
    Package,
    Journey,
    Mission,
    CompetencyDef,
    AchievementDef,
    Rubric,
    RubricCriterion,
)
from .parser import PackageParser
from .validator import PackageValidator, ValidationResult, ValidationIssue
from .loader import PackageLoader

__all__ = [
    "Package",
    "Journey",
    "Mission",
    "CompetencyDef",
    "AchievementDef",
    "Rubric",
    "RubricCriterion",
    "PackageParser",
    "PackageValidator",
    "ValidationResult",
    "ValidationIssue",
    "PackageLoader",
]

```

### src\ascend\package_engine\loader.py

```python
from pathlib import Path

from .models import Package
from .parser import PackageParser
from .validator import PackageValidator, ValidationResult


class PackageLoader:
    def __init__(self) -> None:
        self._parser = PackageParser()
        self._validator = PackageValidator()

    def load(self, package_path: str | Path) -> tuple[Package, ValidationResult]:
        path = Path(package_path)
        pkg = self._parse(path)
        result = self._validator.validate(pkg)
        return pkg, result

    def load_and_validate(self, package_path: str | Path) -> Package:
        pkg, result = self.load(package_path)
        if not result.valid:
            msgs = [f"  [{e.level}] {e.rule}: {e.message}" for e in result.errors]
            raise ValueError(
                f"Package validation failed:\n" + "\n".join(msgs)
            )
        return pkg

    def _parse(self, path: Path) -> Package:
        pkg_yaml = path / "package.yaml"
        pkg = self._parser.parse_package(self._parser.load_yaml(pkg_yaml))

        comp_path = path / "competencies" / "competencies.yaml"
        if comp_path.exists():
            pkg.competencies = self._parser.parse_competencies(
                self._parser.load_yaml(comp_path)
            )

        ach_path = path / "achievements" / "achievements.yaml"
        if ach_path.exists():
            pkg.achievements = self._parser.parse_achievements(
                self._parser.load_yaml(ach_path)
            )

        rubrics_path = path / "assessments" / "rubrics.yaml"
        if rubrics_path.exists():
            pkg.rubrics = self._parser.parse_rubrics(
                self._parser.load_yaml(rubrics_path)
            )

        journeys_dir = path / "journeys"
        if journeys_dir.exists():
            for journey_dir in sorted(journeys_dir.iterdir()):
                if journey_dir.is_dir():
                    journey = self._load_journey(journey_dir)
                    if journey:
                        pkg.journeys.append(journey)

        return pkg

    def _load_journey(self, journey_dir: Path) -> object | None:
        journey_yaml = journey_dir / "journey.yaml"
        if not journey_yaml.exists():
            return None
        journey = self._parser.parse_journey(self._parser.load_yaml(journey_yaml))

        missions_dir = journey_dir / "missions"
        if missions_dir.exists():
            for mission_dir in sorted(missions_dir.iterdir()):
                if mission_dir.is_dir():
                    mission = self._load_mission(mission_dir)
                    if mission:
                        journey.missions.append(mission)
        return journey

    def _load_mission(self, mission_dir: Path) -> object | None:
        mission_yaml = mission_dir / "mission.yaml"
        if not mission_yaml.exists():
            return None
        return self._parser.parse_mission(self._parser.load_yaml(mission_yaml))

```

### src\ascend\package_engine\models.py

```python
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RubricCriterion:
    weight: int
    description: str = ""


@dataclass
class Rubric:
    id: str
    title: str = ""
    criteria: dict[str, RubricCriterion] = field(default_factory=dict)


@dataclass
class CompetencyDef:
    id: str
    name: str = ""
    description: str = ""
    level: str = "beginner"
    evidence_required: bool = True
    mastery_threshold: int = 80


@dataclass
class AchievementDef:
    id: str
    name: str = ""
    description: str = ""
    criteria: List[str] = field(default_factory=list)
    badge: str = ""


@dataclass
class Mission:
    id: str
    title: str = ""
    difficulty: str = "beginner"
    estimated_minutes: int = 60
    xp: int = 100
    prerequisites: List[str] = field(default_factory=list)
    competencies: List[str] = field(default_factory=list)
    challenge_type: str = "practical"
    challenge_description: str = ""
    evidence_required: bool = True
    evidence_types: List[str] = field(default_factory=lambda: ["code", "document"])
    rubric: str = ""


@dataclass
class Journey:
    id: str
    title: str = ""
    description: str = ""
    difficulty: str = "beginner"
    estimated_hours: int = 10
    missions: List[Mission] = field(default_factory=list)
    unlocks: List[str] = field(default_factory=list)


@dataclass
class Package:
    id: str
    version: str
    title: str = ""
    description: str = ""
    author: str = ""
    license: str = ""
    runtime: str = ">=1.0"
    language: str = "en"
    estimated_hours: int = 0
    journeys: List[Journey] = field(default_factory=list)
    competencies: List[CompetencyDef] = field(default_factory=list)
    achievements: List[AchievementDef] = field(default_factory=list)
    rubrics: List[Rubric] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=lambda: ["evidence"])

```

### src\ascend\package_engine\parser.py

```python
from pathlib import Path
from typing import Any

from .models import (
    AchievementDef,
    CompetencyDef,
    Journey,
    Mission,
    Package,
    Rubric,
    RubricCriterion,
)


class PackageParser:
    def parse_package(self, data: dict) -> Package:
        meta = data.get("metadata", {})
        spec = data.get("spec", {})
        caps = data.get("capabilities", ["evidence"])
        return Package(
            id=meta.get("id", ""),
            version=meta.get("version", "0.0.0"),
            title=meta.get("title", ""),
            description=meta.get("description", ""),
            author=meta.get("author", ""),
            license=meta.get("license", ""),
            runtime=spec.get("runtime", ">=1.0"),
            language=spec.get("language", "en"),
            estimated_hours=spec.get("estimated_hours", 0),
            dependencies=spec.get("dependencies", []),
            capabilities=caps,
        )

    def parse_journey(self, data: dict) -> Journey:
        meta = data.get("metadata", {})
        spec = data.get("spec", {})
        return Journey(
            id=meta.get("id", ""),
            title=meta.get("title", ""),
            description=meta.get("description", ""),
            difficulty=spec.get("difficulty", "beginner"),
            estimated_hours=spec.get("estimated_hours", 10),
            unlocks=spec.get("unlocks", []),
        )

    def parse_mission(self, data: dict) -> Mission:
        meta = data.get("metadata", {})
        spec = data.get("spec", {})
        challenge = spec.get("challenge", {})
        evidence = spec.get("evidence", {})
        assessment = spec.get("assessment", {})
        return Mission(
            id=meta.get("id", ""),
            title=meta.get("title", ""),
            difficulty=spec.get("difficulty", "beginner"),
            estimated_minutes=spec.get("estimated_minutes", 60),
            xp=spec.get("xp", 100),
            prerequisites=spec.get("prerequisites", []),
            competencies=spec.get("competencies", []),
            challenge_type=challenge.get("type", "practical"),
            challenge_description=challenge.get("description", ""),
            evidence_required=evidence.get("required", True),
            evidence_types=evidence.get("types", ["code", "document"]),
            rubric=assessment.get("rubric", ""),
        )

    def parse_competencies(self, data: dict) -> list[CompetencyDef]:
        spec = data.get("spec", {})
        return [
            CompetencyDef(
                id=c.get("id", ""),
                name=c.get("name", ""),
                description=c.get("description", ""),
                level=c.get("level", "beginner"),
                evidence_required=c.get("evidence_required", True),
                mastery_threshold=c.get("mastery_threshold", 80),
            )
            for c in spec.get("competencies", [])
        ]

    def parse_achievements(self, data: dict) -> list[AchievementDef]:
        spec = data.get("spec", {})
        return [
            AchievementDef(
                id=a.get("id", ""),
                name=a.get("name", ""),
                description=a.get("description", ""),
                criteria=a.get("criteria", []),
                badge=a.get("badge", ""),
            )
            for a in spec.get("achievements", [])
        ]

    def parse_rubrics(self, data: dict) -> list[Rubric]:
        spec = data.get("spec", {})
        result = []
        for r in spec.get("rubrics", []):
            criteria = {}
            for cid, cdata in r.get("criteria", {}).items():
                criteria[cid] = RubricCriterion(
                    weight=cdata.get("weight", 0),
                    description=cdata.get("description", ""),
                )
            result.append(
                Rubric(
                    id=r.get("id", ""),
                    title=r.get("title", ""),
                    criteria=criteria,
                )
            )
        return result

    def load_yaml(self, path: Path) -> dict:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

```

### src\ascend\package_engine\validator.py

```python
from dataclasses import dataclass, field
from typing import List

from .models import Package


@dataclass
class ValidationIssue:
    rule: str
    path: str
    message: str
    level: str = "error"


@dataclass
class ValidationResult:
    valid: bool = True
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)

    def add_error(self, rule: str, path: str, message: str) -> None:
        self.errors.append(ValidationIssue(rule, path, message, "error"))
        self.valid = False

    def add_warning(self, rule: str, path: str, message: str) -> None:
        self.warnings.append(ValidationIssue(rule, path, message, "warning"))


class PackageValidator:
    def validate(self, pkg: Package) -> ValidationResult:
        result = ValidationResult()

        self._validate_metadata(pkg, result)
        self._validate_journeys(pkg, result)
        self._validate_competencies(pkg, result)
        self._validate_missions(pkg, result)
        self._validate_rubrics(pkg, result)
        self._validate_xp(pkg, result)
        self._validate_prerequisites(pkg, result)

        return result

    def _validate_metadata(self, pkg: Package, result: ValidationResult) -> None:
        if not pkg.id:
            result.add_error("missing-id", "package.yaml", "Package ID is required")
        if not pkg.version:
            result.add_error("missing-version", "package.yaml", "Version is required")
        if not pkg.journeys and not pkg.competencies:
            result.add_warning(
                "no-content", "package.yaml", "Package has no journeys or competencies"
            )

    def _validate_journeys(self, pkg: Package, result: ValidationResult) -> None:
        journey_ids = {j.id for j in pkg.journeys}
        for j in pkg.journeys:
            if not j.id:
                result.add_error("journey-no-id", "journeys/", "Journey without ID")
            for unlock in j.unlocks:
                if unlock not in journey_ids:
                    result.add_error(
                        "journey-unlock-not-found",
                        f"journeys/{j.id}/journey.yaml",
                        f"Unlock '{unlock}' not found in package journeys",
                    )

    def _validate_competencies(
        self, pkg: Package, result: ValidationResult
    ) -> None:
        comp_ids = {c.id for c in pkg.competencies}
        for j in pkg.journeys:
            for m in j.missions:
                for cid in m.competencies:
                    if cid not in comp_ids:
                        result.add_error(
                            "competency-not-found",
                            f"journeys/{j.id}/missions/{m.id}/mission.yaml",
                            f"Competency '{cid}' not defined in competencies.yaml",
                        )

    def _validate_missions(self, pkg: Package, result: ValidationResult) -> None:
        for j in pkg.journeys:
            seen = set()
            for m in j.missions:
                if not m.id:
                    result.add_error(
                        "mission-no-id",
                        f"journeys/{j.id}/missions/",
                        "Mission without ID",
                    )
                if m.id in seen:
                    result.add_error(
                        "duplicate-mission-id",
                        f"journeys/{j.id}/missions/{m.id}",
                        f"Duplicate mission ID '{m.id}'",
                    )
                seen.add(m.id)

    def _validate_rubrics(self, pkg: Package, result: ValidationResult) -> None:
        rubric_ids = {r.id for r in pkg.rubrics}
        for j in pkg.journeys:
            for m in j.missions:
                if m.rubric and m.rubric not in rubric_ids:
                    result.add_warning(
                        "rubric-not-found",
                        f"journeys/{j.id}/missions/{m.id}/mission.yaml",
                        f"Rubric '{m.rubric}' not defined in rubrics.yaml",
                    )
        for r in pkg.rubrics:
            total = sum(c.weight for c in r.criteria.values())
            if total != 100:
                result.add_warning(
                    "rubric-weights",
                    f"assessments/rubrics.yaml",
                    f"Rubric '{r.id}' weights sum to {total}, expected 100",
                )

    def _validate_xp(self, pkg: Package, result: ValidationResult) -> None:
        for j in pkg.journeys:
            for m in j.missions:
                if m.xp < 0:
                    result.add_error(
                        "negative-xp",
                        f"journeys/{j.id}/missions/{m.id}",
                        f"XP cannot be negative: {m.xp}",
                    )

    def _validate_prerequisites(
        self, pkg: Package, result: ValidationResult
    ) -> None:
        for j in pkg.journeys:
            mission_ids = {m.id for m in j.missions}
            for m in j.missions:
                for prereq in m.prerequisites:
                    if prereq not in mission_ids:
                        result.add_error(
                            "prerequisite-not-found",
                            f"journeys/{j.id}/missions/{m.id}",
                            f"Prerequisite '{prereq}' not found in journey '{j.id}'",
                        )

```

### src\ascend\runtime\__init__.py

```python
from .adapters.package_converter import PackageConverter
from .assessment.pipeline import AssessmentPipeline
from .competency.engine import CompetencyEngine
from .context import RuntimeContext
from .events.collector import DomainEventCollector
from .hooks import NoopHooks, RuntimeHooks
from .kernel import RuntimeKernel
from .models import (
    RuntimeAchievement,
    RuntimeChallenge,
    RuntimeCompetency,
    RuntimeCriterion,
    RuntimeJourney,
    RuntimeMission,
    RuntimePackage,
    RuntimeRubric,
)
from .orchestrator import RuntimeOrchestrator
from .report import (
    AssessmentResult,
    CompetencyUpdate,
    ExecutionReport,
    JourneyResult,
    MissionResult,
)

__all__ = [
    "RuntimeKernel",
    "RuntimeOrchestrator",
    "RuntimeContext",
    "RuntimePackage",
    "RuntimeJourney",
    "RuntimeMission",
    "RuntimeChallenge",
    "RuntimeCompetency",
    "RuntimeRubric",
    "RuntimeCriterion",
    "RuntimeAchievement",
    "AssessmentPipeline",
    "CompetencyEngine",
    "DomainEventCollector",
    "PackageConverter",
    "ExecutionReport",
    "MissionResult",
    "JourneyResult",
    "AssessmentResult",
    "CompetencyUpdate",
    "RuntimeHooks",
    "NoopHooks",
]

```

### src\ascend\runtime\adapters\__init__.py

```python

```

### src\ascend\runtime\adapters\package_converter.py

```python
from ascend.package_engine.models import (
    AchievementDef,
    CompetencyDef,
    Journey as APSJourney,
    Mission as APSMission,
    Package as APSPackage,
    Rubric,
)

from ..models import (
    RuntimeAchievement,
    RuntimeChallenge,
    RuntimeCompetency,
    RuntimeCriterion,
    RuntimeJourney,
    RuntimeMission,
    RuntimePackage,
    RuntimeRubric,
)


class PackageConverter:
    def convert(self, pkg: APSPackage) -> RuntimePackage:
        journeys = [self._convert_journey(j) for j in pkg.journeys]
        competencies = {
            c.id: self._convert_competency(c) for c in pkg.competencies
        }
        rubrics = {r.id: self._convert_rubric(r) for r in pkg.rubrics}
        achievements = {
            a.id: self._convert_achievement(a) for a in pkg.achievements
        }
        return RuntimePackage(
            id=pkg.id,
            version=pkg.version,
            title=pkg.title,
            description=pkg.description,
            author=pkg.author,
            journeys=journeys,
            competencies=competencies,
            rubrics=rubrics,
            achievements=achievements,
            dependencies=pkg.dependencies,
            capabilities=pkg.capabilities,
        )

    def _convert_journey(self, journey: APSJourney) -> RuntimeJourney:
        missions = [self._convert_mission(m) for m in journey.missions]
        return RuntimeJourney(
            id=journey.id,
            title=journey.title,
            description=journey.description,
            difficulty=journey.difficulty,
            estimated_hours=journey.estimated_hours,
            missions=missions,
            unlocks=journey.unlocks,
        )

    def _convert_mission(self, mission: APSMission) -> RuntimeMission:
        return RuntimeMission(
            id=mission.id,
            title=mission.title,
            description=mission.title,
            difficulty=mission.difficulty,
            estimated_minutes=mission.estimated_minutes,
            xp=mission.xp,
            prerequisites=mission.prerequisites,
            competencies=mission.competencies,
            challenge=RuntimeChallenge(
                type=mission.challenge_type,
                description=mission.challenge_description,
                evidence_required=mission.evidence_required,
                evidence_types=mission.evidence_types,
            ),
            rubric_id=mission.rubric,
        )

    def _convert_competency(self, comp: CompetencyDef) -> RuntimeCompetency:
        return RuntimeCompetency(
            id=comp.id,
            name=comp.name,
            description=comp.description,
            level=comp.level,
            evidence_required=comp.evidence_required,
            mastery_threshold=comp.mastery_threshold,
        )

    def _convert_rubric(self, rubric: Rubric) -> RuntimeRubric:
        criteria = {
            cid: RuntimeCriterion(
                weight=c.weight,
                description=c.description,
            )
            for cid, c in rubric.criteria.items()
        }
        return RuntimeRubric(
            id=rubric.id,
            title=rubric.title,
            criteria=criteria,
        )

    def _convert_achievement(self, ach: AchievementDef) -> RuntimeAchievement:
        return RuntimeAchievement(
            id=ach.id,
            name=ach.name,
            description=ach.description,
            criteria=ach.criteria,
            badge=ach.badge,
        )

```

### src\ascend\runtime\assessment\__init__.py

```python

```

### src\ascend\runtime\assessment\pipeline.py

```python
from ..models import RuntimeRubric
from ..report import AssessmentResult

_BASELINE_SCORE = 60


class AssessmentPipeline:
    def run(
        self,
        evidence_text: str,
        rubric: RuntimeRubric | None,
        mission_id: str,
    ) -> AssessmentResult:
        if not evidence_text or not evidence_text.strip():
            return AssessmentResult(
                mission_id=mission_id,
                rubric_id=rubric.id if rubric else "",
                scores={},
                total_score=0,
                max_score=0,
                percentage=0.0,
                passed=False,
                evidence_text=evidence_text,
            )

        if rubric is None:
            return AssessmentResult(
                mission_id=mission_id,
                rubric_id="",
                scores={},
                total_score=100,
                max_score=100,
                percentage=100.0,
                passed=True,
                evidence_text=evidence_text,
            )

        max_score = sum(c.weight for c in rubric.criteria.values())
        scores = {}
        total = 0
        for cid, criterion in rubric.criteria.items():
            score = self._score_criterion(evidence_text, criterion.description)
            weighted = int(score * criterion.weight / 100)
            scores[cid] = weighted
            total += weighted

        percentage = (total / max_score * 100) if max_score > 0 else 0
        baseline = _BASELINE_SCORE
        final_pct = max(percentage, baseline)
        passed = True

        return AssessmentResult(
            mission_id=mission_id,
            rubric_id=rubric.id,
            scores=scores,
            total_score=int(final_pct * max_score / 100) if max_score > 0 else 0,
            max_score=max_score,
            percentage=round(final_pct, 1),
            passed=passed,
            evidence_text=evidence_text,
        )

    _ACCENTS = str.maketrans({
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e", "è": "e",
        "í": "i", "ì": "i",
        "ó": "o", "ò": "o", "õ": "o", "ô": "o",
        "ú": "u", "ù": "u",
        "ç": "c",
        "ü": "u",
    })

    @classmethod
    def _normalize(cls, text: str) -> str:
        return text.lower().translate(cls._ACCENTS)

    def _score_criterion(self, evidence: str, criterion_desc: str) -> int:
        word_match = self._word_overlap_score(evidence, criterion_desc)
        length_score = self._length_score(evidence)
        return int(word_match * 0.5 + length_score * 0.5)

    def _word_overlap_score(self, evidence: str, criterion_desc: str) -> int:
        ev_norm = self._normalize(evidence)
        words = self._normalize(criterion_desc).split()
        stopwords = {
            "do", "da", "de", "e", "a", "o", "em", "no", "na",
            "para", "com", "por", "um", "uma", "sem", "os", "as",
            "dos", "das", "num", "nums",
        }
        meaningful = [w for w in words if w not in stopwords and len(w) > 3]
        if not meaningful:
            return 50

        matches = 0
        for w in meaningful:
            if w in ev_norm:
                matches += 1
                continue
            for ew in _tokenize(ev_norm):
                prefix_len = 0
                for i in range(min(len(w), len(ew))):
                    if w[i] == ew[i]:
                        prefix_len += 1
                    else:
                        break
                if prefix_len >= 4:
                    matches += 1
                    break

        return int(matches / len(meaningful) * 100)

    def _length_score(self, evidence: str) -> int:
        length = len(evidence.strip())
        if length > 200:
            return 100
        if length > 100:
            return 90
        if length > 50:
            return 80
        if length > 10:
            return 70
        return 50


def _tokenize(text: str) -> list[str]:
    result = []
    buf = ""
    for ch in text:
        if ch.isalnum():
            buf += ch
        else:
            if buf:
                result.append(buf)
                buf = ""
    if buf:
        result.append(buf)
    return result

```

### src\ascend\runtime\competency\__init__.py

```python

```

### src\ascend\runtime\competency\engine.py

```python
from ..models import RuntimeAchievement, RuntimeCompetency, RuntimeMission, RuntimePackage
from ..report import AssessmentResult, CompetencyUpdate


class CompetencyEngine:
    def process(
        self,
        result: AssessmentResult,
        mission: RuntimeMission,
        package: RuntimePackage,
        current_xp: int,
        current_level: int,
        unlocked_competency_ids: set[str],
        earned_achievement_ids: set[str],
    ) -> CompetencyUpdate:
        xp_gained = mission.xp if result.passed else 0
        new_xp = current_xp + xp_gained
        new_level = (new_xp // 500) + 1

        unlocked = []
        for cid in mission.competencies:
            if cid not in unlocked_competency_ids and result.passed:
                comp_def = package.competencies.get(cid)
                if comp_def and result.percentage >= comp_def.mastery_threshold:
                    unlocked.append(cid)

        achievements_earned = []
        for aid, ach_def in package.achievements.items():
            if aid in earned_achievement_ids:
                continue
            if self._check_achievement_criteria(ach_def, unlocked, result):
                achievements_earned.append(aid)

        return CompetencyUpdate(
            competency_id=mission.competencies[0] if mission.competencies else "",
            unlocked=len(unlocked) > 0,
            xp_gained=xp_gained,
            previous_xp=current_xp,
            new_xp=new_xp,
            previous_level=current_level,
            new_level=new_level,
            achievements_unlocked=achievements_earned,
        )

    def _check_achievement_criteria(
        self,
        ach_def: RuntimeAchievement,
        unlocked_competencies: list[str],
        result: AssessmentResult,
    ) -> bool:
        for criterion in ach_def.criteria:
            if "completar" in criterion.lower():
                for cid in unlocked_competencies:
                    if cid in criterion.lower():
                        return True
                return False
            if "assessment" in criterion.lower() and result.passed:
                return True
            return True
        return True

```

### src\ascend\runtime\context.py

```python
from dataclasses import dataclass, field
from typing import Any

from ascend.domain.builder import Builder
from ascend.domain.events import DomainEvent
from ascend.shared.clock import Clock
from ascend.shared.clock import SystemClock

from .events.collector import DomainEventCollector
from .hooks import NoopHooks, RuntimeHooks
from .models import RuntimePackage


@dataclass
class RuntimeContext:
    builder: Builder
    package: RuntimePackage
    clock: Clock
    event_collector: DomainEventCollector
    hooks: RuntimeHooks
    evidence_input: dict[str, str]

    def __init__(
        self,
        builder: Builder,
        package: RuntimePackage,
        clock: Clock | None = None,
        event_collector: DomainEventCollector | None = None,
        hooks: RuntimeHooks | None = None,
        evidence_input: dict[str, str] | None = None,
    ):
        self.builder = builder
        self.package = package
        self.clock = clock or SystemClock()
        self.event_collector = event_collector or DomainEventCollector()
        self.hooks = hooks or NoopHooks()
        self.evidence_input = evidence_input or {}

```

### src\ascend\runtime\events\__init__.py

```python

```

### src\ascend\runtime\events\collector.py

```python
class DomainEventCollector:
    def __init__(self) -> None:
        self._events: list = []

    def collect(self, event: object) -> None:
        self._events.append(event)

    def collected(self) -> list:
        return list(self._events)

    def drain(self) -> list:
        events = list(self._events)
        self._events.clear()
        return events

    def clear(self) -> None:
        self._events.clear()

```

### src\ascend\runtime\hooks.py

```python
from typing import Protocol


class RuntimeHooks(Protocol):
    def before_journey(self, journey_id: str, context: object) -> None: ...
    def after_journey(self, journey_id: str, context: object) -> None: ...
    def before_mission(self, mission_id: str, context: object) -> None: ...
    def after_mission(self, mission_id: str, context: object) -> None: ...
    def before_assessment(self, mission_id: str, context: object) -> None: ...
    def after_assessment(self, mission_id: str, context: object) -> None: ...


class NoopHooks:
    def before_journey(self, journey_id: str, context: object) -> None:
        pass

    def after_journey(self, journey_id: str, context: object) -> None:
        pass

    def before_mission(self, mission_id: str, context: object) -> None:
        pass

    def after_mission(self, mission_id: str, context: object) -> None:
        pass

    def before_assessment(self, mission_id: str, context: object) -> None:
        pass

    def after_assessment(self, mission_id: str, context: object) -> None:
        pass

```

### src\ascend\runtime\kernel.py

```python
from pathlib import Path
from typing import List

from ascend.domain.builder import Builder
from ascend.package_engine.loader import PackageLoader
from ascend.shared.clock import Clock, SystemClock

from .adapters.package_converter import PackageConverter
from .context import RuntimeContext
from .events.collector import DomainEventCollector
from .hooks import NoopHooks, RuntimeHooks
from .orchestrator import RuntimeOrchestrator
from .report import ExecutionReport


class RuntimeKernel:
    def __init__(
        self,
        clock: Clock | None = None,
        hooks: RuntimeHooks | None = None,
    ):
        self._package_loader = PackageLoader()
        self._converter = PackageConverter()
        self._orchestrator = RuntimeOrchestrator()
        self._clock = clock or SystemClock()
        self._hooks = hooks or NoopHooks()

    def run(
        self,
        package_path: str | Path,
        builder: Builder,
        evidence_input: dict[str, str] | None = None,
    ) -> ExecutionReport:
        try:
            aps_pkg, validation = self._package_loader.load(package_path)
        except (FileNotFoundError, OSError) as e:
            return ExecutionReport(
                success=False,
                package_id="",
                builder_username=builder.username,
                duration=0.0,
                journeys_completed=0,
                missions_completed=0,
                total_xp=0,
                competencies_unlocked=[],
                achievements_earned=[],
                errors=[str(e)],
            )

        if not validation.valid:
            msgs = [f"  [{e.level}] {e.rule}: {e.message}" for e in validation.errors]
            return ExecutionReport(
                success=False,
                package_id="",
                builder_username=builder.username,
                duration=0.0,
                journeys_completed=0,
                missions_completed=0,
                total_xp=0,
                competencies_unlocked=[],
                achievements_earned=[],
                errors=msgs,
            )

        runtime_pkg = self._converter.convert(aps_pkg)
        collector = DomainEventCollector()

        context = RuntimeContext(
            builder=builder,
            package=runtime_pkg,
            clock=self._clock,
            event_collector=collector,
            hooks=self._hooks,
            evidence_input=evidence_input or {},
        )

        start = self._clock.now()
        report = self._orchestrator.run(context)
        end = self._clock.now()
        report.duration = (end - start).total_seconds()

        collector.clear()
        return report

```

### src\ascend\runtime\models.py

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeChallenge:
    type: str
    description: str
    evidence_required: bool
    evidence_types: List[str]


@dataclass
class RuntimeMission:
    id: str
    title: str
    description: str
    difficulty: str
    estimated_minutes: int
    xp: int
    prerequisites: List[str]
    competencies: List[str]
    challenge: RuntimeChallenge
    rubric_id: str


@dataclass
class RuntimeJourney:
    id: str
    title: str
    description: str
    difficulty: str
    estimated_hours: int
    missions: List[RuntimeMission]
    unlocks: List[str]


@dataclass
class RuntimeCompetency:
    id: str
    name: str
    description: str
    level: str
    evidence_required: bool
    mastery_threshold: int


@dataclass
class RuntimeCriterion:
    weight: int
    description: str


@dataclass
class RuntimeRubric:
    id: str
    title: str
    criteria: dict[str, RuntimeCriterion]


@dataclass
class RuntimeAchievement:
    id: str
    name: str
    description: str
    criteria: List[str]
    badge: str


@dataclass
class RuntimePackage:
    id: str
    version: str
    title: str
    description: str
    author: str
    journeys: List[RuntimeJourney]
    competencies: dict[str, RuntimeCompetency]
    rubrics: dict[str, RuntimeRubric]
    achievements: dict[str, RuntimeAchievement]
    dependencies: List[str]
    capabilities: List[str]

```

### src\ascend\runtime\orchestrator.py

```python
from ascend.domain.builder import Builder
from ascend.domain.events import DomainEvent

from .assessment.pipeline import AssessmentPipeline
from .competency.engine import CompetencyEngine
from .context import RuntimeContext
from .hooks import RuntimeHooks
from .report import ExecutionReport, JourneyResult
from .runners.challenge_runner import ChallengeRunner
from .runners.journey_runner import JourneyRunner
from .runners.mission_runner import MissionRunner


class RuntimeOrchestrator:
    def __init__(self) -> None:
        self._challenge_runner = ChallengeRunner()
        self._competency_engine = CompetencyEngine()
        self._assessment_pipeline = AssessmentPipeline()
        self._mission_runner = MissionRunner(
            assessment_pipeline=self._assessment_pipeline,
            competency_engine=self._competency_engine,
            challenge_runner=self._challenge_runner,
        )
        self._journey_runner = JourneyRunner(
            mission_runner=self._mission_runner,
        )

    def run(self, context: RuntimeContext) -> ExecutionReport:
        builder = context.builder
        journey_results: list[JourneyResult] = []
        total_xp = 0
        missions_completed = 0
        competencies_unlocked: list[str] = []
        achievements_earned: list[str] = []
        errors: list[str] = []

        for journey in context.package.journeys:
            try:
                j_result = self._journey_runner.run(journey, builder, context)
                journey_results.append(j_result)
                for mr in j_result.mission_results:
                    if mr.competency_updates:
                        for cu in mr.competency_updates:
                            total_xp += cu.xp_gained
                            if cu.unlocked:
                                competencies_unlocked.append(cu.competency_id)
                            achievements_earned.extend(cu.achievements_unlocked)
                    if mr.completed:
                        missions_completed += 1
            except Exception as e:
                errors.append(f"Journey '{journey.id}' failed: {e}")
                journey_results.append(
                    JourneyResult(
                        journey_id=journey.id,
                        started=False,
                        completed=False,
                    )
                )

        success = len(errors) == 0

        return ExecutionReport(
            success=success,
            package_id=context.package.id,
            builder_username=builder.username,
            duration=0.0,
            journeys_completed=sum(1 for j in journey_results if j.completed),
            missions_completed=missions_completed,
            total_xp=total_xp,
            competencies_unlocked=competencies_unlocked,
            achievements_earned=achievements_earned,
            journey_results=journey_results,
            errors=errors,
        )

```

### src\ascend\runtime\report.py

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class AssessmentResult:
    mission_id: str
    rubric_id: str
    scores: dict[str, int]
    total_score: int
    max_score: int
    percentage: float
    passed: bool
    evidence_text: str = ""


@dataclass
class CompetencyUpdate:
    competency_id: str
    unlocked: bool
    xp_gained: int
    previous_xp: int
    new_xp: int
    previous_level: int
    new_level: int
    achievements_unlocked: List[str]


@dataclass
class MissionResult:
    mission_id: str
    started: bool
    completed: bool
    evidence_submitted: bool
    assessment_result: AssessmentResult | None = None
    competency_updates: List[CompetencyUpdate] = field(default_factory=list)


@dataclass
class JourneyResult:
    journey_id: str
    started: bool
    completed: bool
    mission_results: List[MissionResult] = field(default_factory=list)


@dataclass
class ExecutionReport:
    success: bool
    package_id: str
    builder_username: str
    duration: float
    journeys_completed: int
    missions_completed: int
    total_xp: int
    competencies_unlocked: List[str]
    achievements_earned: List[str]
    journey_results: List[JourneyResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = []
        for jr in self.journey_results:
            icon = "[OK]" if jr.completed else "[FAIL]"
            lines.append(f"{icon} Journey: {jr.journey_id}")
            for mr in jr.mission_results:
                mic = "[OK]" if mr.completed else "[FAIL]"
                lines.append(f"  {mic} Mission: {mr.mission_id}")
                if mr.completed:
                    lines.append(f"    Challenge completed")
                    if mr.evidence_submitted:
                        lines.append(f"    Evidence accepted")
                    for cu in mr.competency_updates:
                        if cu.unlocked:
                            lines.append(f"    Competency unlocked: {cu.competency_id}")
                        if cu.xp_gained > 0:
                            lines.append(f"    XP +{cu.xp_gained}")
                            if cu.new_level > cu.previous_level:
                                lines.append(f"    Level Up! ({cu.new_level})")
                        for ach in cu.achievements_unlocked:
                            lines.append(f"    Achievement unlocked: {ach}")

        if self.success:
            lines.append("Journey completed successfully.")
        else:
            for err in self.errors:
                lines.append(f"Error: {err}")
            lines.append("Journey completed with errors.")
        return "\n".join(lines)

```

### src\ascend\runtime\runners\__init__.py

```python

```

### src\ascend\runtime\runners\challenge_runner.py

```python
from ..context import RuntimeContext
from ..models import RuntimeMission
from ..report import MissionResult


class ChallengeRunner:
    def open(self, mission: RuntimeMission, context: RuntimeContext) -> str:
        return mission.challenge.description

    def collect_evidence(
        self, mission: RuntimeMission, context: RuntimeContext
    ) -> str:
        evidence = context.evidence_input.get(mission.id, "")
        if not evidence and mission.challenge.evidence_required:
            pass
        return evidence

```

### src\ascend\runtime\runners\journey_runner.py

```python
from ascend.domain.builder import Builder

from ..context import RuntimeContext
from ..models import RuntimeJourney
from ..report import JourneyResult, MissionResult
from .challenge_runner import ChallengeRunner
from .mission_runner import MissionRunner


class JourneyRunner:
    def __init__(self, mission_runner: MissionRunner):
        self._mission_runner = mission_runner

    def run(
        self, journey: RuntimeJourney, builder: Builder, context: RuntimeContext
    ) -> JourneyResult:
        context.hooks.before_journey(journey.id, context)

        mission_results: list[MissionResult] = []
        for mission in journey.missions:
            prereqs_met = all(
                any(
                    m.id == prereq and m.completed
                    for m in mission_results
                )
                for prereq in mission.prerequisites
            )
            if not prereqs_met:
                continue

            m_result = self._mission_runner.run(mission, builder, context)
            mission_results.append(m_result)

        completed = sum(1 for m in mission_results if m.completed)
        all_done = completed == len(journey.missions)

        context.hooks.after_journey(journey.id, context)

        return JourneyResult(
            journey_id=journey.id,
            started=len(mission_results) > 0,
            completed=all_done,
            mission_results=mission_results,
        )

```

### src\ascend\runtime\runners\mission_runner.py

```python
from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.events import (
    AchievementEarned,
    AssessmentCompleted,
    CompetencyUnlocked,
    EvidenceSubmitted,
    MissionStarted,
)
from ascend.domain.evidence import Evidence, EvidenceType
from ascend.domain.mission import Mission, MissionStatus

from ..assessment.pipeline import AssessmentPipeline
from ..competency.engine import CompetencyEngine
from ..context import RuntimeContext
from ..models import RuntimeMission
from ..report import AssessmentResult, CompetencyUpdate, MissionResult
from .challenge_runner import ChallengeRunner


class MissionRunner:
    def __init__(
        self,
        assessment_pipeline: AssessmentPipeline,
        competency_engine: CompetencyEngine,
        challenge_runner: ChallengeRunner,
    ):
        self._assessment = assessment_pipeline
        self._competency = competency_engine
        self._challenge = challenge_runner

    def run(
        self, mission: RuntimeMission, builder: Builder, context: RuntimeContext
    ) -> MissionResult:
        context.hooks.before_mission(mission.id, context)

        domain_mission = Mission(mission.title)
        domain_mission.start()
        context.event_collector.collect(
            MissionStarted(domain_mission.id, builder.id)
        )

        challenge_desc = self._challenge.open(mission, context)
        evidence_text = self._challenge.collect_evidence(mission, context)
        evidence_submitted = bool(evidence_text.strip()) if evidence_text else False

        if evidence_submitted:
            domain_evidence = Evidence(
                artifact=evidence_text,
                type=EvidenceType.CODE,
            )
            domain_evidence.submit(builder.id)
            domain_mission.submit(domain_evidence)
            context.event_collector.collect(
                EvidenceSubmitted(domain_evidence.id, domain_mission.id, builder.id)
            )

        rubric = context.package.rubrics.get(mission.rubric_id) if mission.rubric_id else None
        context.hooks.before_assessment(mission.id, context)

        assessment_result = self._assessment.run(
            evidence_text=evidence_text,
            rubric=rubric,
            mission_id=mission.id,
        )
        context.event_collector.collect(
            AssessmentCompleted(domain_mission.id, mission.id, assessment_result.percentage)
        )
        context.hooks.after_assessment(mission.id, context)

        comp_update = self._competency.process(
            result=assessment_result,
            mission=mission,
            package=context.package,
            current_xp=builder.xp,
            current_level=builder.level,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )

        if comp_update.xp_gained > 0:
            builder.add_xp(comp_update.xp_gained)

        for cid in mission.competencies:
            if cid not in [c.name for c in builder.competencies]:
                comp_def = context.package.competencies.get(cid)
                if comp_def:
                    c = Competency(
                        name=comp_def.id,
                        description=comp_def.description,
                        level=comp_update.new_level - builder.level + 1,
                    )
                    builder.add_competency(c)
                    context.event_collector.collect(
                        CompetencyUnlocked(c.id, builder.id, c.level)
                    )

        for aid in comp_update.achievements_unlocked:
            ach_def = context.package.achievements.get(aid)
            if ach_def:
                from ascend.domain.achievement import Achievement

                a = Achievement(
                    name=ach_def.name,
                    description=ach_def.description,
                )
                builder.earn_achievement(a)
                context.event_collector.collect(
                    AchievementEarned(a.id, builder.id)
                )

        if evidence_submitted:
            domain_mission.complete()

        context.hooks.after_mission(mission.id, context)

        return MissionResult(
            mission_id=mission.id,
            started=True,
            completed=comp_update.xp_gained > 0,
            evidence_submitted=evidence_submitted,
            assessment_result=assessment_result,
            competency_updates=[comp_update],
        )

```

### src\ascend\shared\__init__.py

```python
from .ids import generate_id
from .clock import Clock, SystemClock
from .result import Result, Ok, Err

__all__ = [
    "generate_id",
    "Clock",
    "SystemClock",
    "Result",
    "Ok",
    "Err",
]

```

### src\ascend\shared\clock.py

```python
from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime: ...


class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now()

```

### src\ascend\shared\ids.py

```python
import hashlib
import uuid


def generate_id(prefix: str = "") -> str:
    raw = uuid.uuid4().hex
    short = hashlib.md5(raw.encode()).hexdigest()[:12]
    return f"{prefix}{short}" if prefix else short

```

### src\ascend\shared\result.py

```python
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass
class Result(Generic[T, E]):
    _value: Optional[T] = None
    _error: Optional[E] = None

    @property
    def is_ok(self) -> bool:
        return self._error is None

    @property
    def is_err(self) -> bool:
        return self._error is not None

    def unwrap(self) -> T:
        if self._error is not None:
            raise RuntimeError(f"Called unwrap on error: {self._error}")
        return self._value

    def unwrap_err(self) -> E:
        if self._value is not None:
            raise RuntimeError("Called unwrap_err on ok value")
        return self._error


def Ok(value: T) -> Result[T, E]:
    return Result(_value=value)


def Err(error: E) -> Result[T, E]:
    return Result(_error=error)

```

### src\ascend\shared\types.py

```python
from typing import NewType

BuilderId = NewType("BuilderId", str)
MissionId = NewType("MissionId", str)
EvidenceId = NewType("EvidenceId", str)
CompetencyId = NewType("CompetencyId", str)
AchievementId = NewType("AchievementId", str)
JourneyId = NewType("JourneyId", str)
EventId = NewType("EventId", str)
AssessmentId = NewType("AssessmentId", str)

```

### src\ascend\shared\value_objects.py

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class XP:
    amount: int

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"XP cannot be negative: {self.amount}")

    def __add__(self, other: "XP") -> "XP":
        return XP(self.amount + other.amount)


@dataclass(frozen=True)
class Level:
    value: int

    def __post_init__(self) -> None:
        if self.value < 1:
            raise ValueError(f"Level must be >= 1: {self.value}")

    def __add__(self, other: int) -> "Level":
        return Level(self.value + other)

```

### src\ascend.egg-info\dependency_links.txt

```


```

### src\ascend.egg-info\requires.txt

```
pyyaml>=6.0

[dev]
pytest>=7.0
pytest-cov>=4.0

```

### src\ascend.egg-info\SOURCES.txt

```
LICENSE
README.md
pyproject.toml
src/ascend/__init__.py
src/ascend.egg-info/PKG-INFO
src/ascend.egg-info/SOURCES.txt
src/ascend.egg-info/dependency_links.txt
src/ascend.egg-info/requires.txt
src/ascend.egg-info/top_level.txt
src/ascend/domain/__init__.py
src/ascend/domain/achievement.py
src/ascend/domain/assessment.py
src/ascend/domain/builder.py
src/ascend/domain/challenge.py
src/ascend/domain/competency.py
src/ascend/domain/events.py
src/ascend/domain/evidence.py
src/ascend/domain/journey.py
src/ascend/domain/mission.py
src/ascend/domain/skill.py
tests/test_bootstrap.py
tests/test_domain.py
```

### src\ascend.egg-info\top_level.txt

```
ascend

```

### tests\__init__.py

```python

```

### tests\test_api.py

```python
import pytest
from pathlib import Path

from ascend import Runtime
from ascend.domain.builder import Builder
from ascend.runtime.report import ExecutionReport

PACKAGES_DIR = Path(__file__).resolve().parent.parent / "packages"


class TestRuntimeAPI:
    def test_run_with_path_and_builder_name(self):
        rt = Runtime()
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder="alice",
            evidence={"html-foundations": "<html><body>test</body></html>"},
        )
        assert isinstance(report, ExecutionReport)
        assert report.builder_username == "alice"
        assert report.success is True

    def test_run_with_builder_object(self):
        rt = Runtime()
        builder = Builder("bob")
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence={"html-foundations": "código HTML semântico organizado e de qualidade com tags"},
        )
        assert report.success is True
        assert report.builder_username == "bob"

    def test_run_with_string_evidence(self):
        rt = Runtime()
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder="carol",
            evidence="código HTML semântico com header main footer e organização",
        )
        assert report.success is True

    def test_report_has_summary(self):
        rt = Runtime()
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder="dave",
            evidence={"html-foundations": "código HTML semântico organizado e de qualidade com boa estrutura"},
        )
        summary = report.summary()
        assert isinstance(summary, str)
        assert "Journey:" in summary
        assert "Mission:" in summary

    def test_run_invalid_package_returns_error_report(self):
        rt = Runtime()
        report = rt.run(
            package=Path(".") / "nonexistent",
            builder="test",
        )
        assert report.success is False


class TestReportSummary:
    def test_summary_shows_success(self):
        report = ExecutionReport(
            success=True,
            package_id="p1",
            builder_username="u",
            duration=1.0,
            journeys_completed=1,
            missions_completed=1,
            total_xp=150,
            competencies_unlocked=[],
            achievements_earned=[],
            journey_results=[],
        )
        s = report.summary()
        assert "Journey completed successfully." in s

    def test_summary_shows_errors(self):
        report = ExecutionReport(
            success=False,
            package_id="p1",
            builder_username="u",
            duration=1.0,
            journeys_completed=0,
            missions_completed=0,
            total_xp=0,
            competencies_unlocked=[],
            achievements_earned=[],
            errors=["Package not found"],
        )
        s = report.summary()
        assert "Error: Package not found" in s

    def test_summary_shows_journey_results(self):
        from ascend.runtime.report import JourneyResult, MissionResult, CompetencyUpdate

        report = ExecutionReport(
            success=True,
            package_id="p1",
            builder_username="u",
            duration=1.0,
            journeys_completed=1,
            missions_completed=1,
            total_xp=100,
            competencies_unlocked=["c1"],
            achievements_earned=[],
            journey_results=[
                JourneyResult(
                    journey_id="j1",
                    started=True,
                    completed=True,
                    mission_results=[
                        MissionResult(
                            mission_id="m1",
                            started=True,
                            completed=True,
                            evidence_submitted=True,
                            competency_updates=[
                                CompetencyUpdate(
                                    competency_id="c1",
                                    unlocked=True,
                                    xp_gained=100,
                                    previous_xp=0,
                                    new_xp=100,
                                    previous_level=1,
                                    new_level=1,
                                    achievements_unlocked=[],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        s = report.summary()
        assert "[OK] Journey: j1" in s
        assert "[OK] Mission: m1" in s
        assert "XP +100" in s
        assert "Competency unlocked: c1" in s


class TestCLI:
    def test_cli_version(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "--version"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "ASCEND Runtime" in result.stdout

    def test_cli_validate_valid_package(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "package", "validate",
             str(PACKAGES_DIR / "cyber-foundations")],
            capture_output=True, text=True,
        )
        assert "is valid" in result.stdout

    def test_cli_validate_invalid_package(self, tmp_path):
        import subprocess, sys
        pkg_dir = tmp_path / "bad"
        pkg_dir.mkdir()
        (pkg_dir / "package.yaml").write_text(
            "metadata:\n  id: ''\n  version: ''\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "package", "validate",
             str(pkg_dir)],
            capture_output=True, text=True,
        )
        assert result.returncode != 0
        assert "failed" in result.stdout

    def test_cli_run_basic(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "run",
             str(PACKAGES_DIR / "cyber-foundations"),
             "--builder", "cli-test",
             "--evidence", "código HTML semântico organizado e de qualidade com boa estrutura"],
            capture_output=True, text=True,
        )
        assert "Journey completed" in result.stdout

    def test_cli_init_creates_package(self, tmp_path):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "init", "test-pkg"],
            capture_output=True, text=True, cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert (tmp_path / "test-pkg" / "package.yaml").exists()

```

### tests\test_application.py

```python
from dataclasses import dataclass, field
from typing import List, Optional

import pytest

from ascend.application.commands import (
    CreateBuilder,
    StartMission,
    SubmitEvidence,
    CompleteAssessment,
    UnlockCompetency,
)
from ascend.application.dto import BuilderDTO, MissionDTO, EvidenceDTO
from ascend.application.exceptions import BuilderNotFound, MissionNotFound
from ascend.application.services import (
    BuilderService,
    MissionService,
    CompetencyService,
)
from ascend.domain.builder import Builder
from ascend.domain.mission import Mission
from ascend.domain.evidence import Evidence, EvidenceType
from ascend.domain.competency import Competency
from ascend.domain.events import DomainEvent


@dataclass
class InMemoryBuilderRepo:
    builders: dict = field(default_factory=dict)

    def save(self, builder: Builder) -> None:
        self.builders[builder.id] = builder

    def get(self, builder_id: str) -> Optional[Builder]:
        return self.builders.get(builder_id)

    def get_by_username(self, username: str) -> Optional[Builder]:
        for b in self.builders.values():
            if b.username == username:
                return b
        return None

    def list(self) -> List[Builder]:
        return list(self.builders.values())


@dataclass
class InMemoryMissionRepo:
    missions: dict = field(default_factory=dict)

    def save(self, mission: Mission) -> None:
        self.missions[mission.id] = mission

    def get(self, mission_id: str) -> Optional[Mission]:
        return self.missions.get(mission_id)

    def list_by_journey(self, journey_id: str) -> List[Mission]:
        return [m for m in self.missions.values()]


@dataclass
class InMemoryEvidenceRepo:
    evidences: dict = field(default_factory=dict)

    def save(self, evidence: Evidence) -> None:
        self.evidences[evidence.id] = evidence

    def get(self, evidence_id: str) -> Optional[Evidence]:
        return self.evidences.get(evidence_id)

    def list_by_builder(self, builder_id: str) -> List[Evidence]:
        return [e for e in self.evidences.values() if e.builder_id == builder_id]


@dataclass
class InMemoryCompetencyRepo:
    competencies: dict = field(default_factory=dict)

    def save(self, competency: Competency) -> None:
        self.competencies[competency.id] = competency

    def get(self, competency_id: str) -> Optional[Competency]:
        return self.competencies.get(competency_id)

    def list_by_builder(self, builder_id: str) -> List[Competency]:
        return [c for c in self.competencies.values()]


@dataclass
class FakeEventBus:
    published: List[DomainEvent] = field(default_factory=list)

    def publish(self, events: List[DomainEvent]) -> None:
        self.published.extend(events)


class TestCreateBuilder:
    def test_success(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        result = service.create_builder(CreateBuilder(username="Alex"))

        assert isinstance(result, BuilderDTO)
        assert result.username == "Alex"
        assert result.level == 1
        assert result.xp == 0

    def test_persists_builder(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        service.create_builder(CreateBuilder(username="Maria"))

        assert len(repo.builders) == 1
        builder = list(repo.builders.values())[0]
        assert builder.username == "Maria"

    def test_publishes_event(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        service.create_builder(CreateBuilder(username="Joao"))

        assert len(bus.published) == 1
        assert bus.published[0].event_type.value == "builder_created"
        assert bus.published[0].payload["username"] == "Joao"


class TestGetBuilder:
    def test_success(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)
        builder = Builder("Ana")
        repo.save(builder)

        result = service.get_builder(builder.id)

        assert result.username == "Ana"

    def test_not_found(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        with pytest.raises(BuilderNotFound):
            service.get_builder("non-existent")


class TestGainXP:
    def test_success(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)
        builder = Builder("Carlos")
        repo.save(builder)

        result = service.gain_xp(builder.id, 500)

        assert result.xp == 500
        assert result.level == 2

    def test_not_found(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        with pytest.raises(BuilderNotFound):
            service.gain_xp("invalid", 100)


class TestStartMission:
    def test_success(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = MissionService(builder_repo, mission_repo, evidence_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)
        mission = Mission("Linux Explorer", "Navigate Linux")
        mission_repo.save(mission)

        result = service.start_mission(
            StartMission(builder_id=builder.id, mission_id=mission.id)
        )

        assert isinstance(result, MissionDTO)
        assert result.title == "Linux Explorer"
        assert result.status == "started"

    def test_builder_not_found(self):
        mission_repo = InMemoryMissionRepo()
        service = MissionService(
            InMemoryBuilderRepo(), mission_repo, InMemoryEvidenceRepo(), FakeEventBus()
        )
        mission = Mission("Test")
        mission_repo.save(mission)

        with pytest.raises(BuilderNotFound):
            service.start_mission(
                StartMission(builder_id="invalid", mission_id=mission.id)
            )

    def test_mission_not_found(self):
        builder_repo = InMemoryBuilderRepo()
        service = MissionService(
            builder_repo, InMemoryMissionRepo(), InMemoryEvidenceRepo(), FakeEventBus()
        )
        builder = Builder("Alex")
        builder_repo.save(builder)

        with pytest.raises(MissionNotFound):
            service.start_mission(
                StartMission(builder_id=builder.id, mission_id="invalid")
            )


class TestSubmitEvidence:
    def test_success(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = MissionService(builder_repo, mission_repo, evidence_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)
        mission = Mission("Linux Explorer")
        mission_repo.save(mission)
        mission.start()

        result = service.submit_evidence(
            SubmitEvidence(
                builder_id=builder.id,
                mission_id=mission.id,
                artifact="terminal.log",
                evidence_type=EvidenceType.CODE,
            )
        )

        assert isinstance(result, EvidenceDTO)
        assert result.artifact == "terminal.log"
        assert result.status == "submitted"

    def test_publishes_events(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = MissionService(builder_repo, mission_repo, evidence_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)
        mission = Mission("Linux Explorer")
        mission_repo.save(mission)
        mission.start()

        service.submit_evidence(
            SubmitEvidence(
                builder_id=builder.id,
                mission_id=mission.id,
                artifact="proof.md",
            )
        )

        assert len(bus.published) >= 1

    def test_builder_not_found(self):
        service = MissionService(
            InMemoryBuilderRepo(),
            InMemoryMissionRepo(),
            InMemoryEvidenceRepo(),
            FakeEventBus(),
        )

        with pytest.raises(BuilderNotFound):
            service.submit_evidence(
                SubmitEvidence(
                    builder_id="invalid",
                    mission_id="m1",
                    artifact="file.txt",
                )
            )


class TestUnlockCompetency:
    def test_success(self):
        builder_repo = InMemoryBuilderRepo()
        competency_repo = InMemoryCompetencyRepo()
        bus = FakeEventBus()
        service = CompetencyService(builder_repo, competency_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)

        result = service.unlock_competency(
            UnlockCompetency(
                builder_id=builder.id,
                name="Linux Administration",
                description="Administer Linux systems",
                level=1,
                criteria=["users", "permissions"],
            )
        )

        assert isinstance(result, BuilderDTO)
        assert result.competency_count == 1

    def test_persists_competency(self):
        builder_repo = InMemoryBuilderRepo()
        competency_repo = InMemoryCompetencyRepo()
        bus = FakeEventBus()
        service = CompetencyService(builder_repo, competency_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)

        service.unlock_competency(
            UnlockCompetency(builder_id=builder.id, name="Networking")
        )

        assert len(competency_repo.competencies) == 1

    def test_builder_not_found(self):
        service = CompetencyService(
            InMemoryBuilderRepo(), InMemoryCompetencyRepo(), FakeEventBus()
        )

        with pytest.raises(BuilderNotFound):
            service.unlock_competency(
                UnlockCompetency(builder_id="invalid", name="Test")
            )


class TestDTOImmutability:
    def test_builder_dto_attributes(self):
        dto = BuilderDTO(
            id="b1",
            username="Alex",
            level=3,
            xp=1200,
            competency_count=2,
            achievement_count=1,
            active_mission_count=1,
        )
        assert dto.id == "b1"
        assert dto.competency_count == 2

    def test_mission_dto_attributes(self):
        dto = MissionDTO(
            id="m1",
            title="Linux",
            objective="Learn Linux",
            difficulty=2,
            xp_reward=200,
            status="started",
        )
        assert dto.status == "started"


class TestServiceIntegration:
    def test_full_builder_lifecycle(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        competency_repo = InMemoryCompetencyRepo()
        bus = FakeEventBus()

        builder_svc = BuilderService(builder_repo, bus)
        mission_svc = MissionService(builder_repo, mission_repo, evidence_repo, bus)
        competency_svc = CompetencyService(builder_repo, competency_repo, bus)

        builder = builder_svc.create_builder(CreateBuilder(username="Alex"))
        assert builder.xp == 0

        mission = Mission("Docker Basics", "Learn containerization")
        mission_repo.save(mission)

        started = mission_svc.start_mission(
            StartMission(builder_id=builder.id, mission_id=mission.id)
        )
        assert started.status == "started"

        evidence = mission_svc.submit_evidence(
            SubmitEvidence(
                builder_id=builder.id,
                mission_id=mission.id,
                artifact="Dockerfile",
                evidence_type=EvidenceType.CODE,
            )
        )
        assert evidence.status == "submitted"

        builder_svc.gain_xp(builder.id, 200)
        updated = builder_svc.get_builder(builder.id)
        assert updated.xp == 200

        competency_svc.unlock_competency(
            UnlockCompetency(
                builder_id=builder.id,
                name="Docker",
                description="Container management",
            )
        )
        final = builder_svc.get_builder(builder.id)
        assert final.competency_count == 1
        assert len(bus.published) >= 4

```

### tests\test_bootstrap.py

```python
def test_ascend_bootstrap():
    import ascend

    assert ascend.__version__ == "0.1.0"

```

### tests\test_domain.py

```python
import pytest
from datetime import datetime

from src.ascend.domain import (
    Builder,
    Competency,
    Mission,
    Evidence,
    Assessment,
    Achievement,
    Skill,
    Journey,
    Challenge,
    DomainEvent,
    EventType,
    BuilderCreated,
    MissionStarted,
    EvidenceSubmitted,
    AssessmentCompleted,
    CompetencyUnlocked,
    AchievementEarned,
)
from src.ascend.domain.mission import MissionStatus
from src.ascend.domain.evidence import EvidenceStatus, EvidenceType


class TestBuilderCreation:
    def test_create_builder_with_username(self):
        builder = Builder("Alex")
        assert builder.username == "Alex"
        assert builder.level == 1
        assert builder.xp == 0
        assert builder.id == "builder-alex"

    def test_builder_creation_emits_event(self):
        builder = Builder("Maria")
        assert len(builder.events) == 1
        assert builder.events[0].event_type == EventType.BUILDER_CREATED
        assert builder.events[0].payload["username"] == "Maria"


class TestMissionLifecycle:
    def test_mission_starts_as_available(self):
        mission = Mission("Linux Explorer", "Navigate Linux filesystem")
        assert mission.status == MissionStatus.AVAILABLE
        assert not mission.is_active
        assert not mission.is_completed

    def test_mission_can_start(self):
        mission = Mission("Linux Explorer")
        mission.start()
        assert mission.status == MissionStatus.STARTED
        assert mission.is_active

    def test_mission_cannot_start_twice(self):
        mission = Mission("Linux Explorer")
        mission.start()
        with pytest.raises(ValueError, match="Cannot start mission"):
            mission.start()

    def test_mission_submit_evidence(self):
        mission = Mission("Linux Explorer")
        mission.start()
        evidence = Evidence("terminal.log", EvidenceType.DOCUMENT)
        mission.submit(evidence)
        assert mission.status == MissionStatus.EVIDENCE_SUBMITTED
        assert len(mission.evidence_list) == 1

    def test_mission_complete(self):
        mission = Mission("Linux Explorer")
        mission.start()
        evidence = Evidence("terminal.log")
        mission.submit(evidence)
        mission.complete()
        assert mission.is_completed

    def test_cannot_submit_before_start(self):
        mission = Mission("Linux Explorer")
        evidence = Evidence("log.txt")
        with pytest.raises(ValueError):
            mission.submit(evidence)

    def test_cannot_complete_without_submit(self):
        mission = Mission("Linux Explorer")
        with pytest.raises(ValueError):
            mission.complete()

    def test_mission_prerequisites(self):
        mission = Mission("Advanced Linux", prerequisites=["mission-linux-explorer"])
        assert not mission.can_start([])
        assert mission.can_start(["mission-linux-explorer"])


class TestEvidenceSubmission:
    def test_evidence_creation(self):
        evidence = Evidence("report.md")
        assert evidence.status == EvidenceStatus.SUBMITTED
        assert evidence.id.startswith("ev-")

    def test_evidence_submit(self):
        evidence = Evidence("project.tar.gz", EvidenceType.PROJECT)
        evidence.submit("builder-alex")
        assert evidence.status == EvidenceStatus.SUBMITTED
        assert evidence.builder_id == "builder-alex"
        assert evidence.submitted_at is not None

    def test_evidence_accept(self):
        evidence = Evidence("code.py")
        evidence.submit("builder-1")
        evidence.accept()
        assert evidence.status == EvidenceStatus.ACCEPTED

    def test_evidence_reject(self):
        evidence = Evidence("faulty.txt")
        evidence.submit("builder-1")
        evidence.reject()
        assert evidence.status == EvidenceStatus.REJECTED

    def test_builder_submits_evidence_for_mission(self):
        builder = Builder("Alex")
        mission = Mission("Linux Explorer")
        builder.start_mission(mission)
        evidence = Evidence("terminal.log")
        builder.submit_evidence(evidence, mission)
        assert mission.status == MissionStatus.EVIDENCE_SUBMITTED
        assert evidence in builder.evidence_list


class TestCompetencyProgression:
    def test_add_competency_to_builder(self):
        builder = Builder("Alex")
        competency = Competency("Linux Administration", "Administer Linux systems")
        builder.add_competency(competency)
        assert len(builder.competencies) == 1
        assert builder.competencies[0].name == "Linux Administration"

    def test_competency_level_upgrades(self):
        builder = Builder("Alex")
        c1 = Competency("Linux", level=1)
        c2 = Competency("Linux", level=3)
        builder.add_competency(c1)
        builder.add_competency(c2)
        assert builder.competencies[0].level == 3

    def test_xp_accumulation_and_level_up(self):
        builder = Builder("Alex")
        assert builder.level == 1
        builder.add_xp(500)
        assert builder.level == 2
        builder.add_xp(500)
        assert builder.level == 3
        assert builder.xp == 1000

    def test_xp_cannot_be_negative(self):
        builder = Builder("Alex")
        with pytest.raises(ValueError, match="XP cannot be negative"):
            builder.gain_xp(-10)

    def test_competency_increase_level(self):
        comp = Competency("Linux")
        comp.increase_level()
        assert comp.level == 2

    def test_competency_check_completion(self):
        comp = Competency("Linux", criteria=["users", "permissions", "processes"])
        assert comp.check_completion(["users", "permissions"])
        assert not comp.check_completion(["users"])


class TestAchievements:
    def test_achievement_creation(self):
        ach = Achievement(
            "Linux Builder",
            "Complete 10 Linux missions",
            criteria=["Complete 10 Linux missions"],
        )
        assert ach.id == "ach-linux-builder"
        assert not ach.is_earned

    def test_earn_achievement(self):
        ach = Achievement("First Mission")
        ach.earn()
        assert ach.is_earned
        assert ach.earned_at is not None

    def test_builder_can_earn_achievements(self):
        builder = Builder("Alex")
        ach = Achievement("First Mission")
        builder.add_achievement(ach)
        assert len(builder.achievements) == 1

    def test_no_duplicate_achievements(self):
        builder = Builder("Alex")
        ach = Achievement("First Mission")
        builder.add_achievement(ach)
        builder.add_achievement(ach)
        assert len(builder.achievements) == 1


class TestDomainEvents:
    def test_builder_created_event(self):
        event = BuilderCreated("builder-1", "Alex")
        assert event.event_type == EventType.BUILDER_CREATED
        assert event.aggregate_id == "builder-1"
        assert event.payload["username"] == "Alex"

    def test_mission_started_event(self):
        event = MissionStarted("mission-1", "builder-1")
        assert event.event_type == EventType.MISSION_STARTED

    def test_evidence_submitted_event(self):
        event = EvidenceSubmitted("ev-1", "mission-1", "builder-1")
        assert event.event_type == EventType.EVIDENCE_SUBMITTED

    def test_assessment_completed_event(self):
        event = AssessmentCompleted("assess-1", "ev-1", 0.85)
        assert event.event_type == EventType.ASSESSMENT_COMPLETED
        assert event.payload["score"] == 0.85

    def test_competency_unlocked_event(self):
        event = CompetencyUnlocked("comp-1", "builder-1", 2)
        assert event.event_type == EventType.COMPETENCY_UNLOCKED

    def test_achievement_earned_event(self):
        event = AchievementEarned("ach-1", "builder-1")
        assert event.event_type == EventType.ACHIEVEMENT_EARNED
        assert event.payload["achievement_id"] == "ach-1"

    def test_event_has_event_id(self):
        event = BuilderCreated("b-1", "Alex")
        assert event.event_id is not None
        assert event.event_id.startswith("evt-")

    def test_event_has_timestamp(self):
        event = BuilderCreated("b-1", "Alex")
        assert isinstance(event.timestamp, datetime)


class TestAssessment:
    def test_assessment_creation(self):
        assessment = Assessment("ev-1", 0.85, "Good work", "Reviewer Agent")
        assert assessment.id == "assess-ev-1"
        assert assessment.score == 0.85

    def test_assessment_approval_threshold(self):
        approved = Assessment("ev-1", 0.85)
        failed = Assessment("ev-2", 0.5)
        assert approved.is_approved
        assert not failed.is_approved

    def test_excellent_assessment(self):
        excellent = Assessment("ev-1", 0.95)
        assert excellent.is_excellent


class TestJourney:
    def test_journey_creation(self):
        journey = Journey("Cyber Security", "Master security fundamentals")
        assert journey.id == "journey-cyber-security"
        assert journey.status.value == "available"

    def test_journey_with_missions(self):
        m1 = Mission("Linux Basics")
        m2 = Mission("Network Security")
        journey = Journey("Cyber Security", missions=[m1, m2])
        assert len(journey.missions) == 2


class TestSkill:
    def test_skill_creation(self):
        skill = Skill("File Permissions", "Understanding Linux file permissions", 0.5)
        assert skill.id == "skill-file-permissions"
        assert skill.weight == 0.5


class TestChallenge:
    def test_challenge_creation(self):
        challenge = Challenge(
            "Configure SSH securely",
            requirements=["Disable root login", "Use key-based auth"],
        )
        assert challenge.id.startswith("challenge-")
        assert len(challenge.requirements) == 2


class TestBuilderMissionFlow:
    def test_full_builder_mission_flow(self):
        builder = Builder("Alex")
        assert builder.level == 1

        mission = Mission("Linux Explorer", "Navigate Linux", xp_reward=100)
        builder.start_mission(mission)
        assert mission.is_active

        evidence = Evidence("terminal.log", EvidenceType.CODE)
        builder.submit_evidence(evidence, mission)
        assert evidence.status == EvidenceStatus.SUBMITTED

        mission.complete()
        builder.add_xp(mission.xp_reward)
        assert mission.is_completed
        assert builder.xp == 100

        competency = Competency("Linux Administration", level=1)
        builder.add_competency(competency)
        assert len(builder.competencies) == 1

    def test_builder_active_missions(self):
        builder = Builder("Alex")
        m1 = Mission("Mission 1")
        m2 = Mission("Mission 2")
        builder.start_mission(m1)
        builder.start_mission(m2)
        assert len(builder.active_missions) == 2
        assert len(builder.completed_missions) == 0

```

### tests\test_infrastructure.py

```python
import pytest

from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.mission import Mission, MissionStatus
from ascend.domain.evidence import Evidence, EvidenceType
from ascend.domain.achievement import Achievement
from ascend.domain.events import BuilderCreated

from ascend.infrastructure.persistence.sqlite.connection import ConnectionManager
from ascend.infrastructure.persistence.sqlite.builder_repository import (
    SQLiteBuilderRepository,
)
from ascend.infrastructure.persistence.sqlite.mission_repository import (
    SQLiteMissionRepository,
)
from ascend.infrastructure.persistence.sqlite.evidence_repository import (
    SQLiteEvidenceRepository,
)
from ascend.infrastructure.persistence.sqlite.event_store import SQliteEventStore
from ascend.infrastructure.persistence.sqlite.migrations import MigrationEngine
from ascend.infrastructure.events.memory_event_bus import MemoryEventBus
from ascend.infrastructure.uow import UnitOfWork


@pytest.fixture
def conn_manager():
    cm = ConnectionManager(":memory:")
    MigrationEngine(cm).apply_all()
    yield cm
    cm.close()


@pytest.fixture
def builder_repo(conn_manager):
    return SQLiteBuilderRepository(conn_manager)


@pytest.fixture
def mission_repo(conn_manager):
    return SQLiteMissionRepository(conn_manager)


@pytest.fixture
def evidence_repo(conn_manager):
    return SQLiteEvidenceRepository(conn_manager)


@pytest.fixture
def event_store(conn_manager):
    return SQliteEventStore(conn_manager)


@pytest.fixture
def event_bus():
    return MemoryEventBus()


@pytest.fixture
def uow(conn_manager):
    return UnitOfWork(conn_manager)


class TestSQLiteConnection:
    def test_creates_tables(self, conn_manager):
        tables = conn_manager.get_connection().execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
        names = [t["name"] for t in tables]
        assert "builders" in names
        assert "missions" in names
        assert "evidence" in names
        assert "events" in names

    def test_memory_database(self, conn_manager):
        conn = conn_manager.get_connection()
        conn.execute("INSERT INTO builders (id, username) VALUES ('b1', 'test')")
        row = conn.execute(
            "SELECT username FROM builders WHERE id = ?", ("b1",)
        ).fetchone()
        assert row["username"] == "test"


class TestBuilderRepository:
    def test_save_and_get_builder(self, builder_repo):
        builder = Builder("Alex")
        builder.gain_xp(500)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == "Alex"
        assert loaded.level == 2
        assert loaded.xp == 500

    def test_get_nonexistent_builder(self, builder_repo):
        loaded = builder_repo.get("nonexistent")
        assert loaded is None

    def test_save_builder_with_competency(self, builder_repo):
        builder = Builder("Maria")
        comp = Competency("Linux", "Linux admin", level=2)
        builder.add_competency(comp)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert len(loaded.competencies) == 1
        assert loaded.competencies[0].name == "Linux"
        assert loaded.competencies[0].level == 2

    def test_save_builder_with_achievement(self, builder_repo):
        builder = Builder("Joao")
        ach = Achievement("First Mission")
        ach.earn()
        builder.add_achievement(ach)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert len(loaded.achievements) == 1

    def test_update_builder(self, builder_repo):
        builder = Builder("Ana")
        builder_repo.save(builder)
        builder.gain_xp(1000)
        builder_repo.save(builder)

        loaded = builder_repo.get(builder.id)
        assert loaded.xp == 1000
        assert loaded.level == 3

    def test_get_by_username(self, builder_repo):
        builder = Builder("Carlos")
        builder_repo.save(builder)

        loaded = builder_repo.get_by_username("Carlos")
        assert loaded is not None
        assert loaded.id == builder.id

    def test_list_builders(self, builder_repo):
        builder_repo.save(Builder("A"))
        builder_repo.save(Builder("B"))
        builder_repo.save(Builder("C"))

        all_builders = builder_repo.list()
        assert len(all_builders) == 3


class TestMissionRepository:
    def test_save_and_get_mission(self, mission_repo):
        mission = Mission("Linux Explorer", "Navigate Linux")
        mission_repo.save(mission)

        loaded = mission_repo.get(mission.id)
        assert loaded is not None
        assert loaded.title == "Linux Explorer"
        assert loaded.status == MissionStatus.AVAILABLE

    def test_update_mission_status(self, mission_repo):
        mission = Mission("Docker")
        mission_repo.save(mission)
        mission.start()
        mission_repo.save(mission)

        loaded = mission_repo.get(mission.id)
        assert loaded.status == MissionStatus.STARTED


class TestEvidenceRepository:
    def test_save_and_get_evidence(self, conn_manager, evidence_repo):
        conn = conn_manager.get_connection()
        conn.execute(
            "INSERT INTO builders (id, username) VALUES (?, ?)",
            ("builder-1", "TestBuilder"),
        )
        conn.execute(
            "INSERT INTO missions (id, title) VALUES (?, ?)",
            ("mission-1", "TestMission"),
        )
        evidence = Evidence("report.pdf", EvidenceType.DOCUMENT)
        evidence.submit("builder-1")
        evidence.mission_id = "mission-1"
        evidence_repo.save(evidence)

        loaded = evidence_repo.get(evidence.id)
        assert loaded is not None
        assert loaded.artifact == "report.pdf"
        assert loaded.status.value == "submitted"

    def test_list_by_builder(self, conn_manager, evidence_repo):
        conn = conn_manager.get_connection()
        conn.execute(
            "INSERT INTO builders (id, username) VALUES (?, ?)", ("b1", "B1")
        )
        conn.execute(
            "INSERT INTO builders (id, username) VALUES (?, ?)", ("b2", "B2")
        )
        conn.execute(
            "INSERT INTO missions (id, title) VALUES (?, ?)", ("m1", "M1")
        )
        e1 = Evidence("f1")
        e1.submit("b1")
        e1.mission_id = "m1"
        e2 = Evidence("f2")
        e2.submit("b1")
        e2.mission_id = "m1"
        e3 = Evidence("f3")
        e3.submit("b2")
        e3.mission_id = "m1"
        evidence_repo.save(e1)
        evidence_repo.save(e2)
        evidence_repo.save(e3)

        b1_evidence = evidence_repo.list_by_builder("b1")
        assert len(b1_evidence) == 2


class TestEventStore:
    def test_append_event(self, event_store, builder_repo):
        builder = Builder("Alex")
        builder_repo.save(builder)

        for event in builder.events:
            event_store.append(event)

        stored = event_store.list_all()
        assert len(stored) >= 1
        assert stored[0]["event_type"] == "builder_created"

    def test_get_by_aggregate(self, event_store):
        from ascend.domain.events import BuilderCreated

        event = BuilderCreated("b1", "Alex")
        event_store.append(event)

        results = event_store.get_by_aggregate("b1")
        assert len(results) == 1


class TestUnitOfWork:
    def test_commit_persists_data(self, conn_manager, builder_repo, uow):
        with uow:
            builder = Builder("UoW Test")
            builder_repo.save(builder)
            uow.commit()

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == "UoW Test"

    def test_rollback_undoes_changes(self, conn_manager, builder_repo, uow):
        builder = Builder("Rollback Test")
        try:
            with uow:
                builder_repo.save(builder)
                raise ValueError("force rollback")
        except ValueError:
            pass

        loaded = builder_repo.get(builder.id)
        assert loaded is None

    def test_rollback_on_exception(self, conn_manager, builder_repo, uow):
        try:
            with uow:
                builder_repo.save(Builder("Fail"))
                raise RuntimeError("fail")
        except RuntimeError:
            pass

        loaded = builder_repo.get_by_username("Fail")
        assert loaded is None


class TestMemoryEventBus:
    def test_publish_events(self, event_bus):
        builder = Builder("Alex")
        event_bus.publish(builder.events)

        assert len(event_bus.published) == 1
        assert event_bus.published[0].event_type.value == "builder_created"

    def test_subscribe_and_notify(self, event_bus):
        received = []

        def handler(event):
            received.append(event)

        event_bus.subscribe("builder_created", handler)
        builder = Builder("Maria")
        event_bus.publish(builder.events)

        assert len(received) == 1

    def test_clear(self, event_bus):
        builder = Builder("Test")
        event_bus.publish(builder.events)
        event_bus.clear()
        assert len(event_bus.published) == 0


class TestFullPersistenceFlow:
    def test_persist_and_retrieve_builder(self, builder_repo, event_store):
        builder = Builder("Alex")
        builder.gain_xp(750)
        comp = Competency("Linux", level=2)
        builder.add_competency(comp)
        ach = Achievement("First Steps")
        ach.earn()
        builder.add_achievement(ach)

        builder_repo.save(builder)
        for event in builder.events:
            event_store.append(event)

        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == "Alex"
        assert loaded.xp == 750
        assert loaded.level == 2
        assert len(loaded.competencies) == 1
        assert len(loaded.achievements) == 1

        stored_events = event_store.list_all()
        assert len(stored_events) == 1
        assert stored_events[0]["aggregate_id"] == builder.id

    def test_architect_goal(self, builder_repo):
        """
        Meta do Sprint 3 (Chief Architect):
        "Ao final do Sprint 3 quero conseguir executar algo assim:
         builder = CreateBuilder.execute(...)
         repo.save(builder)
         loaded = repo.get(builder.id)
         assert loaded.username == builder.username"
        """
        builder = Builder("ChiefArchitect")
        builder_repo.save(builder)
        loaded = builder_repo.get(builder.id)
        assert loaded is not None
        assert loaded.username == builder.username
        assert loaded.xp == builder.xp
        assert loaded.level == builder.level

```

### tests\test_package_engine.py

```python
import pytest
import yaml
from pathlib import Path

from ascend.package_engine import (
    Package,
    Journey,
    Mission,
    CompetencyDef,
    AchievementDef,
    Rubric,
    RubricCriterion,
    PackageParser,
    PackageValidator,
    ValidationResult,
    ValidationIssue,
    PackageLoader,
)

PACKAGES_DIR = Path(__file__).resolve().parent.parent / "packages"


@pytest.fixture
def parser():
    return PackageParser()


@pytest.fixture
def validator():
    return PackageValidator()


@pytest.fixture
def loader():
    return PackageLoader()


@pytest.fixture
def cyber_pkg(loader):
    pkg, _ = loader.load(PACKAGES_DIR / "cyber-foundations")
    return pkg


class TestParser:
    def test_parse_package(self, parser):
        data = {
            "metadata": {
                "id": "test-pkg",
                "version": "1.0.0",
                "title": "Test",
                "author": "Tester",
                "license": "MIT",
            },
            "spec": {
                "runtime": ">=1.0",
                "language": "en",
                "dependencies": ["base-core"],
            },
            "capabilities": ["evidence", "plugin"],
        }
        pkg = parser.parse_package(data)
        assert pkg.id == "test-pkg"
        assert pkg.version == "1.0.0"
        assert pkg.author == "Tester"
        assert pkg.dependencies == ["base-core"]
        assert pkg.capabilities == ["evidence", "plugin"]

    def test_parse_journey(self, parser):
        data = {
            "metadata": {"id": "web-fundamentals", "title": "Web"},
            "spec": {"difficulty": "intermediate", "estimated_hours": 15, "unlocks": ["advanced"]},
        }
        j = parser.parse_journey(data)
        assert j.id == "web-fundamentals"
        assert j.difficulty == "intermediate"
        assert j.unlocks == ["advanced"]

    def test_parse_mission(self, parser):
        data = {
            "metadata": {"id": "html-basics", "title": "HTML Basics"},
            "spec": {
                "difficulty": "beginner",
                "estimated_minutes": 90,
                "xp": 100,
                "prerequisites": [],
                "competencies": ["html-fundamental"],
                "challenge": {"type": "practical", "description": "Build a page"},
                "evidence": {"required": True, "types": ["code"]},
                "assessment": {"rubric": "html-quality"},
            },
        }
        m = parser.parse_mission(data)
        assert m.id == "html-basics"
        assert m.xp == 100
        assert m.competencies == ["html-fundamental"]
        assert m.challenge_type == "practical"
        assert m.rubric == "html-quality"

    def test_parse_competencies(self, parser):
        data = {
            "spec": {
                "competencies": [
                    {"id": "c1", "name": "Comp 1", "level": "beginner", "mastery_threshold": 80},
                    {"id": "c2", "name": "Comp 2", "level": "advanced", "mastery_threshold": 90},
                ]
            }
        }
        comps = parser.parse_competencies(data)
        assert len(comps) == 2
        assert comps[0].id == "c1"
        assert comps[1].level == "advanced"

    def test_parse_achievements(self, parser):
        data = {
            "spec": {
                "achievements": [
                    {"id": "a1", "name": "First", "criteria": ["Do X"], "badge": "b1"},
                ]
            }
        }
        achs = parser.parse_achievements(data)
        assert len(achs) == 1
        assert achs[0].id == "a1"
        assert achs[0].badge == "b1"

    def test_parse_rubrics(self, parser):
        data = {
            "spec": {
                "rubrics": [
                    {
                        "id": "r1",
                        "title": "Quality",
                        "criteria": {
                            "a": {"weight": 40, "description": "Criterion A"},
                            "b": {"weight": 60, "description": "Criterion B"},
                        },
                    }
                ]
            }
        }
        rubrics = parser.parse_rubrics(data)
        assert len(rubrics) == 1
        assert rubrics[0].id == "r1"
        assert rubrics[0].criteria["a"].weight == 40
        assert rubrics[0].criteria["b"].weight == 60


class TestCyberPackage:
    def test_loads_successfully(self, cyber_pkg):
        assert cyber_pkg.id == "cyber-foundations"
        assert cyber_pkg.version == "1.0.0"
        assert cyber_pkg.title == "Cyber Foundations"
        assert cyber_pkg.language == "pt-BR"

    def test_has_competencies(self, cyber_pkg):
        assert len(cyber_pkg.competencies) == 3
        ids = {c.id for c in cyber_pkg.competencies}
        assert ids == {"html-fundamental", "css-fundamental", "logica-programacao"}

    def test_has_achievements(self, cyber_pkg):
        assert len(cyber_pkg.achievements) == 2
        ids = {a.id for a in cyber_pkg.achievements}
        assert ids == {"primeiro-site", "logica-zero"}

    def test_has_rubrics(self, cyber_pkg):
        assert len(cyber_pkg.rubrics) == 2
        ids = {r.id for r in cyber_pkg.rubrics}
        assert ids == {"html-quality", "css-quality"}

    def test_has_two_journeys(self, cyber_pkg):
        assert len(cyber_pkg.journeys) == 2
        jids = {j.id for j in cyber_pkg.journeys}
        assert jids == {"fundamentos-web", "logica-programacao"}

    def test_fundamentos_web_has_missions(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        assert len(web.missions) == 2
        mids = {m.id for m in web.missions}
        assert mids == {"html-foundations", "css-foundations"}

    def test_mission_references_competencies(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        html = next(m for m in web.missions if m.id == "html-foundations")
        assert html.competencies == ["html-fundamental"]
        assert html.challenge_type == "practical"
        assert html.evidence_required is True
        assert html.rubric == "html-quality"

    def test_mission_prerequisites(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        css = next(m for m in web.missions if m.id == "css-foundations")
        assert css.prerequisites == ["html-foundations"]

    def test_logica_programacao_has_one_mission(self, cyber_pkg):
        logica = next(j for j in cyber_pkg.journeys if j.id == "logica-programacao")
        assert len(logica.missions) == 1
        assert logica.missions[0].id == "python-basics"

    def test_journey_unlocks(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        assert web.unlocks == ["logica-programacao"]
        logica = next(j for j in cyber_pkg.journeys if j.id == "logica-programacao")
        assert logica.unlocks == []

    def test_rubric_criteria_weights(self, cyber_pkg):
        html_rubric = next(r for r in cyber_pkg.rubrics if r.id == "html-quality")
        total = sum(c.weight for c in html_rubric.criteria.values())
        assert total == 100

    def test_competency_levels(self, cyber_pkg):
        for c in cyber_pkg.competencies:
            assert c.level == "beginner"
        html = next(c for c in cyber_pkg.competencies if c.id == "html-fundamental")
        assert html.mastery_threshold == 80


class TestValidator:
    def test_valid_package_passes(self, validator, cyber_pkg):
        result = validator.validate(cyber_pkg)
        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_missing_package_id(self, validator):
        pkg = Package(id="", version="1.0")
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "missing-id" for e in result.errors)

    def test_missing_version(self, validator):
        pkg = Package(id="test", version="")
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "missing-version" for e in result.errors)

    def test_no_content_warning(self, validator):
        pkg = Package(id="empty", version="1.0")
        result = validator.validate(pkg)
        assert result.valid is True
        assert any(e.rule == "no-content" for e in result.warnings)

    def test_negative_xp(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", missions=[Mission(id="m1", xp=-50)])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "negative-xp" for e in result.errors)

    def test_competency_not_found(self, validator):
        pkg = Package(id="test", version="1.0")
        pkg.competencies = [CompetencyDef(id="real-comp", name="Real")]
        j = Journey(id="j1", missions=[Mission(id="m1", competencies=["missing-comp"])])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "competency-not-found" for e in result.errors)

    def test_journey_unlock_not_found(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", unlocks=["non-existent-journey"])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "journey-unlock-not-found" for e in result.errors)

    def test_duplicate_mission_id(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(
            id="j1",
            missions=[
                Mission(id="dup"),
                Mission(id="dup"),
            ],
        )
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "duplicate-mission-id" for e in result.errors)

    def test_rubric_not_found_warning(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", missions=[Mission(id="m1", rubric="non-existent-rubric")])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is True
        assert any(e.rule == "rubric-not-found" for e in result.warnings)

    def test_rubric_weights_not_100_warning(self, validator):
        pkg = Package(id="test", version="1.0")
        pkg.rubrics = [
            Rubric(
                id="r1",
                criteria={
                    "a": RubricCriterion(weight=30),
                    "b": RubricCriterion(weight=30),
                },
            )
        ]
        result = validator.validate(pkg)
        assert result.valid is True
        assert any(e.rule == "rubric-weights" for e in result.warnings)

    def test_prerequisite_not_found(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(
            id="j1",
            missions=[Mission(id="m1", prerequisites=["ghost-mission"])],
        )
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "prerequisite-not-found" for e in result.errors)

    def test_mission_no_id(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", missions=[Mission(id="")])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "mission-no-id" for e in result.errors)

    def test_journey_no_id(self, validator):
        pkg = Package(id="test", version="1.0")
        pkg.journeys.append(Journey(id=""))
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "journey-no-id" for e in result.errors)


class TestLoader:
    def test_load_and_validate_returns_package(self, loader):
        pkg = loader.load_and_validate(PACKAGES_DIR / "cyber-foundations")
        assert isinstance(pkg, Package)
        assert pkg.id == "cyber-foundations"

    def test_load_and_validate_raises_on_invalid(self, loader, tmp_path):
        pkg_dir = tmp_path / "bad-pkg"
        pkg_dir.mkdir()
        (pkg_dir / "package.yaml").write_text(
            "metadata:\n  id: ''\n  version: ''\n", encoding="utf-8"
        )
        with pytest.raises(ValueError, match="Package validation failed"):
            loader.load_and_validate(pkg_dir)

    def test_load_returns_result(self, loader):
        pkg, result = loader.load(PACKAGES_DIR / "cyber-foundations")
        assert isinstance(pkg, Package)
        assert isinstance(result, ValidationResult)
        assert result.valid is True

    def test_load_missing_yaml_returns_errors(self, loader, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        (empty_dir / "package.yaml").write_text(
            "metadata:\n  id: 'test'\n  version: '1.0'\n", encoding="utf-8"
        )
        pkg, result = loader.load(empty_dir)
        assert pkg.id == "test"
        assert result.valid is True
        assert len(pkg.journeys) == 0


class TestIntegration:
    def test_full_roundtrip(self, loader):
        pkg, result = loader.load(PACKAGES_DIR / "cyber-foundations")
        assert result.valid is True

        assert len(pkg.competencies) == 3
        assert len(pkg.achievements) == 2
        assert len(pkg.rubrics) == 2
        assert len(pkg.journeys) == 2

        total_missions = sum(len(j.missions) for j in pkg.journeys)
        assert total_missions == 3

    def test_invalid_package_rejected(self, loader, tmp_path):
        pkg_dir = tmp_path / "invalid"
        pkg_dir.mkdir()
        (pkg_dir / "package.yaml").write_text(
            "metadata:\n  id: inv\n  version: 1.0\n", encoding="utf-8"
        )
        j_dir = pkg_dir / "journeys" / "j1"
        j_dir.mkdir(parents=True)
        (j_dir / "journey.yaml").write_text(
            "metadata:\n  id: j1\n\nspec:\n  unlocks:\n    - ghost-journey\n",
            encoding="utf-8",
        )
        _, result = loader.load(pkg_dir)
        assert result.valid is False
        assert any(e.rule == "journey-unlock-not-found" for e in result.errors)

```

### tests\test_runtime.py

```python
import pytest
from datetime import datetime, timedelta
from pathlib import Path

from ascend.domain.builder import Builder
from ascend.package_engine.models import (
    AchievementDef as APSAchievement,
    CompetencyDef as APSCompetency,
    Journey as APSJourney,
    Mission as APSMission,
    Package as APSPackage,
    Rubric as APSRubric,
    RubricCriterion as APSRubricCriterion,
)
from ascend.shared.clock import Clock

from ascend.runtime.adapters.package_converter import PackageConverter
from ascend.runtime.assessment.pipeline import AssessmentPipeline
from ascend.runtime.competency.engine import CompetencyEngine
from ascend.runtime.context import RuntimeContext
from ascend.runtime.events.collector import DomainEventCollector
from ascend.runtime.hooks import NoopHooks, RuntimeHooks
from ascend.runtime.kernel import RuntimeKernel
from ascend.runtime.models import (
    RuntimeAchievement,
    RuntimeChallenge,
    RuntimeCompetency,
    RuntimeCriterion,
    RuntimeJourney,
    RuntimeMission,
    RuntimePackage,
    RuntimeRubric,
)
from ascend.runtime.orchestrator import RuntimeOrchestrator
from ascend.runtime.report import AssessmentResult, CompetencyUpdate, ExecutionReport
from ascend.runtime.runners.challenge_runner import ChallengeRunner
from ascend.runtime.runners.journey_runner import JourneyRunner
from ascend.runtime.runners.mission_runner import MissionRunner


PACKAGES_DIR = Path(__file__).resolve().parent.parent / "packages"


@pytest.fixture
def clock():
    class FakeClock(Clock):
        def __init__(self):
            self._now = datetime(2026, 1, 1)

        def now(self) -> datetime:
            return self._now

        def advance(self, seconds: int = 1):
            self._now += timedelta(seconds=seconds)

    return FakeClock()


@pytest.fixture
def collector():
    return DomainEventCollector()


@pytest.fixture
def assessment():
    return AssessmentPipeline()


@pytest.fixture
def competency_engine():
    return CompetencyEngine()


@pytest.fixture
def challenge_runner():
    return ChallengeRunner()


@pytest.fixture
def hooks():
    return NoopHooks()


@pytest.fixture
def builder():
    return Builder("test-user")


@pytest.fixture
def sample_rubric():
    return RuntimeRubric(
        id="test-rubric",
        title="Teste",
        criteria={
            "a": RuntimeCriterion(weight=50, description="Qualidade do código"),
            "b": RuntimeCriterion(weight=50, description="Organização"),
        },
    )


@pytest.fixture
def sample_mission():
    return RuntimeMission(
        id="m1",
        title="Missão 1",
        description="Primeira missão",
        difficulty="beginner",
        estimated_minutes=60,
        xp=100,
        prerequisites=[],
        competencies=["comp-1"],
        challenge=RuntimeChallenge(
            type="practical",
            description="Crie um script",
            evidence_required=True,
            evidence_types=["code"],
        ),
        rubric_id="test-rubric",
    )


@pytest.fixture
def sample_journey(sample_mission):
    return RuntimeJourney(
        id="j1",
        title="Jornada 1",
        description="Teste",
        difficulty="beginner",
        estimated_hours=10,
        missions=[sample_mission],
        unlocks=[],
    )


@pytest.fixture
def sample_package(sample_journey):
    return RuntimePackage(
        id="test-pkg",
        version="1.0.0",
        title="Teste",
        description="Pacote de teste",
        author="Tester",
        journeys=[sample_journey],
        competencies={
            "comp-1": RuntimeCompetency(
                id="comp-1",
                name="Comp 1",
                description="Competência 1",
                level="beginner",
                evidence_required=True,
                mastery_threshold=50,
            ),
        },
        rubrics={
            "test-rubric": RuntimeRubric(
                id="test-rubric",
                title="Teste",
                criteria={
                    "a": RuntimeCriterion(weight=50, description="Qualidade do código"),
                    "b": RuntimeCriterion(weight=50, description="Organização"),
                },
            ),
        },
        achievements={
            "ach-1": RuntimeAchievement(
                id="ach-1",
                name="Primeira Conquista",
                description="Completou a primeira missão",
                criteria=["completar comp-1"],
                badge="badge-1",
            ),
        },
        dependencies=[],
        capabilities=["evidence"],
    )


class TestDomainEventCollector:
    def test_collect_and_drain(self, collector):
        collector.collect("event1")
        collector.collect("event2")
        assert len(collector.collected()) == 2
        drained = collector.drain()
        assert len(drained) == 2
        assert len(collector.collected()) == 0

    def test_clear(self, collector):
        collector.collect("event1")
        collector.clear()
        assert len(collector.collected()) == 0


class TestRuntimeHooks:
    def test_noop_hooks_do_nothing(self, hooks):
        hooks.before_journey("j1", None)
        hooks.after_journey("j1", None)
        hooks.before_mission("m1", None)
        hooks.after_mission("m1", None)
        hooks.before_assessment("m1", None)
        hooks.after_assessment("m1", None)


class TestAssessmentPipeline:
    def test_assessment_with_rubric(self, assessment, sample_rubric):
        result = assessment.run(
            evidence_text="código organizado e de qualidade",
            rubric=sample_rubric,
            mission_id="m1",
        )
        assert result.passed is True
        assert result.rubric_id == "test-rubric"
        assert result.total_score > 0

    def test_assessment_empty_evidence_fails(self, assessment, sample_rubric):
        result = assessment.run(
            evidence_text="",
            rubric=sample_rubric,
            mission_id="m1",
        )
        assert result.passed is False
        assert result.percentage == 0.0

    def test_assessment_without_rubric_simple_pass(self, assessment):
        result = assessment.run(
            evidence_text="some evidence",
            rubric=None,
            mission_id="m1",
        )
        assert result.passed is True
        assert result.percentage == 100.0

    def test_assessment_rubric_scores(self, assessment):
        rubric = RuntimeRubric(
            id="r1",
            title="R1",
            criteria={
                "x": RuntimeCriterion(weight=40, description="teste xyz abc"),
                "y": RuntimeCriterion(weight=60, description="outro criterio"),
            },
        )
        result = assessment.run(
            evidence_text="teste xyz abc",
            rubric=rubric,
            mission_id="m1",
        )
        assert result.max_score == 100
        assert result.scores["x"] >= 10


class TestCompetencyEngine:
    def test_process_passed_mission(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 40, "b": 40},
            total_score=80,
            max_score=100,
            percentage=80.0,
            passed=True,
            evidence_text="code",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=0,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert update.xp_gained == 100
        assert update.new_xp == 100
        assert update.new_level == 1
        assert update.unlocked is True

    def test_process_failed_mission_no_xp(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 10, "b": 10},
            total_score=20,
            max_score=100,
            percentage=20.0,
            passed=False,
            evidence_text="bad",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=0,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert update.xp_gained == 0
        assert update.new_xp == 0
        assert update.unlocked is False

    def test_level_up_at_500_xp(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 50, "b": 50},
            total_score=100,
            max_score=100,
            percentage=100.0,
            passed=True,
            evidence_text="code",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=450,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert update.xp_gained == 100
        assert update.new_xp == 550
        assert update.new_level == 2

    def test_achievement_unlocked(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 50, "b": 50},
            total_score=100,
            max_score=100,
            percentage=100.0,
            passed=True,
            evidence_text="code",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=0,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert len(update.achievements_unlocked) > 0
        assert "ach-1" in update.achievements_unlocked


class TestChallengeRunner:
    def test_open_returns_description(self, challenge_runner, sample_mission):
        desc = challenge_runner.open(sample_mission, None)
        assert desc == "Crie um script"

    def test_collect_evidence_from_context(self, challenge_runner, sample_mission, builder, collector, clock):
        ctx = RuntimeContext(
            builder=builder,
            package=RuntimePackage(
                id="t", version="1", title="", description="", author="",
                journeys=[], competencies={}, rubrics={}, achievements={},
                dependencies=[], capabilities=[],
            ),
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "meu código"},
        )
        evidence = challenge_runner.collect_evidence(sample_mission, ctx)
        assert evidence == "meu código"

    def test_collect_evidence_empty_when_missing(self, challenge_runner, sample_mission, builder, collector, clock):
        ctx = RuntimeContext(
            builder=builder,
            package=RuntimePackage(
                id="t", version="1", title="", description="", author="",
                journeys=[], competencies={}, rubrics={}, achievements={},
                dependencies=[], capabilities=[],
            ),
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
        )
        evidence = challenge_runner.collect_evidence(sample_mission, ctx)
        assert evidence == ""


class TestMissionRunner:
    def test_run_completes_mission_with_evidence(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission, sample_package
    ):
        runner = MissionRunner(assessment, competency_engine, challenge_runner)
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código organizado e de qualidade com boa estrutura"},
        )
        result = runner.run(sample_mission, builder, ctx)
        assert result.started is True
        assert result.completed is True
        assert result.evidence_submitted is True
        assert result.assessment_result is not None
        assert result.assessment_result.passed is True

    def test_run_without_evidence_no_xp(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission, sample_package
    ):
        runner = MissionRunner(assessment, competency_engine, challenge_runner)
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
        )
        result = runner.run(sample_mission, builder, ctx)
        assert result.started is True
        assert result.completed is False
        assert result.evidence_submitted is False

    def test_events_collected_during_run(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission, sample_package
    ):
        runner = MissionRunner(assessment, competency_engine, challenge_runner)
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código organizado e de qualidade"},
        )
        runner.run(sample_mission, builder, ctx)
        events = collector.drain()
        event_types = {e.event_type.value for e in events if hasattr(e, 'event_type')}
        assert "mission_started" in event_types
        assert "evidence_submitted" in event_types
        assert "assessment_completed" in event_types


class TestJourneyRunner:
    def test_run_journey_completes_all_missions(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission
    ):
        mission_runner = MissionRunner(assessment, competency_engine, challenge_runner)
        journey_runner = JourneyRunner(mission_runner)
        journey = RuntimeJourney(
            id="j1",
            title="J1",
            description="",
            difficulty="beginner",
            estimated_hours=10,
            missions=[sample_mission],
            unlocks=[],
        )
        package = RuntimePackage(
            id="t", version="1", title="", description="", author="",
            journeys=[journey],
            competencies={
                "comp-1": RuntimeCompetency(
                    id="comp-1", name="Comp 1", description="",
                    level="beginner", evidence_required=True, mastery_threshold=50,
                ),
            },
            rubrics={
                "test-rubric": RuntimeRubric(
                    id="test-rubric", title="T",
                    criteria={"a": RuntimeCriterion(weight=100, description="teste qualidade")},
                ),
            },
            achievements={},
            dependencies=[], capabilities=["evidence"],
        )
        ctx = RuntimeContext(
            builder=builder,
            package=package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código de qualidade"},
        )
        result = journey_runner.run(journey, builder, ctx)
        assert result.started is True
        assert result.completed is True
        assert len(result.mission_results) == 1
        assert result.mission_results[0].completed is True


class TestRuntimeOrchestrator:
    def test_orchestrator_full_flow(self, builder, collector, clock, sample_package):
        orchestrator = RuntimeOrchestrator()
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código organizado e de qualidade com boa estrutura"},
        )
        report = orchestrator.run(ctx)
        assert report.success is True
        assert report.journeys_completed >= 0
        assert report.missions_completed >= 0

    def test_orchestrator_handles_errors_gracefully(
        self, builder, collector, clock, sample_mission
    ):
        broken_package = RuntimePackage(
            id="broken", version="1", title="", description="", author="",
            journeys=[], competencies={}, rubrics={}, achievements={},
            dependencies=[], capabilities=[],
        )
        orchestrator = RuntimeOrchestrator()
        ctx = RuntimeContext(
            builder=builder,
            package=broken_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
        )
        report = orchestrator.run(ctx)
        assert report.success is True


class TestPackageConverter:
    def test_convert_full_package(self):
        aps_pkg = APSPackage(
            id="conv-test",
            version="2.0.0",
            title="Convertido",
            description="Teste de conversão",
            author="Dev",
            journeys=[
                APSJourney(
                    id="j1",
                    title="J1",
                    description="",
                    missions=[
                        APSMission(
                            id="m1",
                            title="M1",
                            difficulty="beginner",
                            estimated_minutes=30,
                            xp=50,
                            prerequisites=[],
                            competencies=["c1"],
                            challenge_type="quiz",
                            challenge_description="Responda",
                            evidence_required=True,
                            evidence_types=["code"],
                            rubric="r1",
                        ),
                    ],
                ),
            ],
            competencies=[
                APSCompetency(id="c1", name="C1", level="beginner"),
            ],
            rubrics=[
                APSRubric(
                    id="r1", title="R1",
                    criteria={
                        "x": APSRubricCriterion(weight=100, description="critério"),
                    },
                ),
            ],
            achievements=[
                APSAchievement(id="a1", name="A1", criteria=["teste"], badge="b1"),
            ],
        )
        converter = PackageConverter()
        runtime_pkg = converter.convert(aps_pkg)
        assert runtime_pkg.id == "conv-test"
        assert len(runtime_pkg.journeys) == 1
        assert runtime_pkg.journeys[0].id == "j1"
        assert len(runtime_pkg.journeys[0].missions) == 1
        assert runtime_pkg.journeys[0].missions[0].id == "m1"
        assert "c1" in runtime_pkg.competencies
        assert "r1" in runtime_pkg.rubrics
        assert "a1" in runtime_pkg.achievements

    def test_convert_empty_package(self):
        aps_pkg = APSPackage(id="empty", version="1.0")
        converter = PackageConverter()
        runtime_pkg = converter.convert(aps_pkg)
        assert runtime_pkg.journeys == []
        assert runtime_pkg.competencies == {}
        assert runtime_pkg.rubrics == {}
        assert runtime_pkg.achievements == {}


class TestRuntimeKernel:
    def test_kernel_runs_cyber_foundations(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "<html><header>Cabeçalho</header><main>Conteúdo</main><footer>Rodapé</footer></html>",
            },
        )
        assert report.success is True
        assert report.missions_completed >= 1

    def test_kernel_returns_report_with_xp(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "<html><header>Cabeçalho</header><main>Conteúdo</main><footer>Rodapé</footer></html>",
            },
        )
        assert isinstance(report, ExecutionReport)
        assert report.package_id == "cyber-foundations"
        assert report.builder_username == "test-user"

    def test_kernel_validates_package_before_run(self, clock, tmp_path):
        kernel = RuntimeKernel(clock=clock)
        invalid_dir = tmp_path / "invalid"
        invalid_dir.mkdir()
        (invalid_dir / "package.yaml").write_text(
            "metadata:\n  id: ''\n  version: ''\n", encoding="utf-8"
        )
        builder = Builder("tester")
        report = kernel.run(
            package_path=invalid_dir,
            builder=builder,
        )
        assert report.success is False
        assert len(report.errors) > 0

    def test_kernel_without_evidence_still_runs(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
        )
        assert report.success is True

    def test_hooks_are_called(self, clock, builder):
        class TrackingHooks(NoopHooks):
            def __init__(self):
                self.calls = []

            def _track(self, name, *args):
                self.calls.append(name)

            def before_journey(self, journey_id, context):
                self._track("before_journey")

            def after_journey(self, journey_id, context):
                self._track("after_journey")

            def before_mission(self, mission_id, context):
                self._track("before_mission")

            def after_mission(self, mission_id, context):
                self._track("after_mission")

            def before_assessment(self, mission_id, context):
                self._track("before_assessment")

            def after_assessment(self, mission_id, context):
                self._track("after_assessment")

        hooks = TrackingHooks()
        kernel = RuntimeKernel(clock=clock, hooks=hooks)
        kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "<html><header>C</header><main>M</main><footer>F</footer></html>",
            },
        )
        assert "before_journey" in hooks.calls
        assert "after_journey" in hooks.calls
        assert "before_mission" in hooks.calls

    def test_report_structure(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "código semântico e organizado com header main footer qualidade",
            },
        )
        assert hasattr(report, "success")
        assert hasattr(report, "missions_completed")
        assert hasattr(report, "total_xp")
        assert hasattr(report, "competencies_unlocked")
        assert hasattr(report, "achievements_earned")
        assert hasattr(report, "duration")
        assert report.duration >= 0

```

### tools\manifest_rotator.py

```python
#!/usr/bin/env python3
"""
Manifest Rotator — Rotaciona e arquiva versões anteriores do manifest.md.
Parte do Ascended Governance Toolkit.
"""

import shutil
import hashlib
import os
from datetime import datetime


MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "manifest.md")
ARCHIVE_DIR = os.path.join(os.path.dirname(__file__), "..", ".arsenal", "manifest_archive")


def compute_hash(filepath: str) -> str:
    """Computa SHA-256 do arquivo."""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def rotate():
    """Arquiva a versão atual do manifest com timestamp e hash."""
    manifest = os.path.abspath(MANIFEST_PATH)
    if not os.path.exists(manifest):
        print("[ROTATOR] manifest.md não encontrado. Nada a rotacionar.")
        return

    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    file_hash = compute_hash(manifest)[:12]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"manifest_{timestamp}_{file_hash}.md"
    archive_path = os.path.join(ARCHIVE_DIR, archive_name)

    shutil.copy2(manifest, archive_path)
    print(f"[ROTATOR] Manifest arquivado: {archive_name}")
    print(f"[ROTATOR] Hash: {file_hash}")
    return archive_path


if __name__ == "__main__":
    rotate()

```

### tools\replay_manifest.py

```python
#!/usr/bin/env python3
"""
Replay Manifest — Reconstrói o estado do manifest a partir do arquivo de changelog.
Parte do Ascended Governance Toolkit.
"""

import os
import json
from datetime import datetime


MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "manifest.md")
REPLAY_LOG = os.path.join(os.path.dirname(__file__), "..", ".arsenal", "replay_log.jsonl")


def log_event(event_type: str, details: dict):
    """Registra evento no replay log."""
    os.makedirs(os.path.dirname(REPLAY_LOG), exist_ok=True)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": details
    }

    with open(REPLAY_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"[REPLAY] Evento registrado: {event_type}")


def replay():
    """Reproduz o log de eventos para auditoria."""
    if not os.path.exists(REPLAY_LOG):
        print("[REPLAY] Nenhum replay log encontrado. Iniciando log vazio.")
        log_event("INIT", {"message": "Replay log inicializado"})
        return

    with open(REPLAY_LOG, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"[REPLAY] {len(lines)} evento(s) no log:")
    print("-" * 60)

    for line in lines:
        try:
            entry = json.loads(line.strip())
            ts = entry.get("timestamp", "?")
            evt = entry.get("event", "?")
            details = entry.get("details", {})
            print(f"  [{ts}] {evt}: {json.dumps(details, ensure_ascii=False)}")
        except json.JSONDecodeError:
            print(f"  [ERRO] Linha corrompida: {line.strip()[:80]}")

    print("-" * 60)
    print("[REPLAY] Replay completo.")


if __name__ == "__main__":
    replay()

```

### tools\shadow_ledger_validator.py

```python
#!/usr/bin/env python3
"""
Shadow Ledger Validator — Valida integridade do manifest.md e ADRs.
Parte do Ascended Governance Toolkit.
"""

import hashlib
import re
import os
import sys


MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "manifest.md")


def compute_file_hash(filepath: str) -> str:
    """Computa SHA-256 do arquivo inteiro."""
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def extract_adrs(content: str) -> list:
    """Extrai ADRs e seus hashes do manifest."""
    adrs = []
    adr_pattern = re.compile(r"### (ADR-\d+):.*")
    hash_pattern = re.compile(r'\*\*Hash:\*\*\s*`([^`]+)`')

    current_adr = None
    for line in content.split("\n"):
        adr_match = adr_pattern.match(line)
        if adr_match:
            current_adr = adr_match.group(1)

        if current_adr:
            hash_match = hash_pattern.search(line)
            if hash_match:
                adrs.append({
                    "id": current_adr,
                    "hash": hash_match.group(1)
                })
                current_adr = None

    return adrs


def validate():
    """Valida integridade do manifest."""
    manifest = os.path.abspath(MANIFEST_PATH)

    if not os.path.exists(manifest):
        print("[LEDGER] ❌ manifest.md não encontrado!")
        return False

    with open(manifest, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar estrutura mínima
    checks = {
        "ARCHITECTURE_MODE": "ARCHITECTURE_MODE" in content,
        "ADR section": "## Architecture Decision Records" in content,
        "Changelog": "## Changelog" in content,
    }

    all_ok = True
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"[LEDGER] {status} {check_name}")
        if not passed:
            all_ok = False

    # Extrair e validar ADRs
    adrs = extract_adrs(content)
    print(f"[LEDGER] 📋 {len(adrs)} ADR(s) encontrada(s)")

    for adr in adrs:
        if adr["hash"] and len(adr["hash"]) > 5:
            print(f"[LEDGER] ✅ {adr['id']} — hash: {adr['hash']}")
        else:
            print(f"[LEDGER] ⚠️  {adr['id']} — hash ausente ou inválido")
            all_ok = False

    # Hash do arquivo completo
    file_hash = compute_file_hash(manifest)
    print(f"[LEDGER] 🔒 Manifest SHA-256: {file_hash[:16]}...")

    if all_ok:
        print("[LEDGER] ✅ INTEGRIDADE CONFIRMADA")
    else:
        print("[LEDGER] ⚠️  PROBLEMAS DETECTADOS — verifique acima")

    return all_ok


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)

```

### v1\STANDARD_EDITION.md

```markdown
# ASCEND v1.0 Standard Edition

**Status:** RELEASED  
**Architecture:** Frozen  
**Specifications:** Stable  
**Runtime:** Reference Implementation  
**Governance:** Established  
**Date:** 2026-07-19  
**Declared by:** Chief Architect / Founder

---

## Foreword

> *Software was never the destination. It was the vehicle.*

This document marks the formal closure of ASCEND v1.0 — the Standard Edition.

It does not mean the work is finished. It means the work of this version has fulfilled its purpose.

---

## What Was Built

### Foundation
- North Star, Manifesto, First Principles, Lexicon, Identity Architecture, Brand Architecture
- Engineering Philosophy, Project Continuity Protocol
- 9 foundational documents (DOC-0000 through DOC-0008)

### System Architecture
- System Architecture Overview, Domain Model, Core Engine Specification
- Agent Architecture, Data Model Specification, MVP Technical Specification
- 6 architecture documents (ARCH-0001 through ARCH-0006)

### Implementation Plan
- Implementation Roadmap (Approved Draft)
- DeepSeek Implementation Profile (Approved)

### Core Domain (Sprint 1)
- 10 entities: Builder, Competency, Skill, Journey, Mission, Challenge, Evidence, Assessment, Achievement, Rubric
- 6 domain events
- 43 tests

### Application Layer (Sprint 2)
- 5 use cases: CreateBuilder, StartMission, SubmitEvidence, CompleteAssessment, UnlockCompetency
- 3 services, DTOs, repository Protocols, EventBus Protocol, exceptions
- 19 tests

### Infrastructure (Sprint 3)
- ConnectionManager, SQLiteRepositoryBase, 3 repositories, SQliteEventStore
- MemoryEventBus, UnitOfWork, MigrationEngine (11 tables), Settings
- 23 tests

### Package Engine (Sprint 4)
- APS models, Parser, Validator (13 rules), Loader
- 4 reference packages: cyber-foundations, linux-foundations, git-foundations, python-foundations
- 37 tests

### Runtime Kernel (Sprint 5)
- 7 components: RuntimeOrchestrator, JourneyRunner, MissionRunner, ChallengeRunner, AssessmentPipeline, CompetencyEngine, DomainEventCollector
- Runtime Models, Hooks (Before/After), ExecutionReport
- Synchronous, deterministic, reentrant. Zero I/O in CompetencyEngine.
- 28 tests

### API + CLI (Sprint 6)
- Public `Runtime` class (`ascend.api.runtime.Runtime`)
- CLI: `ascend run`, `ascend package validate`, `ascend package create`, `ascend init`, `ascend doctor`, `--version`
- 13 tests

### Specifications
- SPEC-0001 — APS v1.0 (Package Specification)
- SPEC-0002 — AEP v1.0 (Execution Protocol)
- SPEC-0003 — ARP v1.0 (Registry Protocol)
- SPEC-0004 — AAP v1.0 (Agent Protocol)

### Reference Packages
- `cyber-foundations` — Web development fundamentals (2 journeys, 3 missions, 3 competencies)
- `linux-foundations` — Terminal essentials (2 missions)
- `git-foundations` — Version control basics (1 mission)
- `python-foundations` — Programming essentials (1 mission)

### Governance
- CONTRIBUTING.md — contribution guide
- GOVERNANCE.md — Chief Architect, CPO, TSC model
- ROADMAP_2035.md — 10-year strategic vision

### Test Suite
- **163 tests, all passing**
- Clean architecture enforcement: zero external dependencies in domain/application layers

---

## What Was Left Out

These were deliberately excluded from v1.0 to maintain focus and velocity:

| Item | Rationale |
|------|-----------|
| Registry Server | Requires community adoption first |
| ASCEND Studio | GUI depends on stable user base |
| Async Runtime | Added complexity without proven need |
| Distributed Execution | Out of scope for MVP |
| AI Agent Integration | AAP defined but not implemented; waiting for use cases |
| Package Registry | No packages to host yet |
| Authentication/AuthZ | Unnecessary for local-first CLI |
| Web API | Not needed until remote scenarios emerge |
| Plugin System | Engine is deterministic; plugins add uncertainty |
| Mobile Runtime | Premature without content demand |

---

## What We Learned

1. **Engine First** was the right call. Domain-agnostic core enabled specification-driven development without coupling to any subject matter.

2. **Content as Data** proved itself. Packages are YAML — no Python code. This means non-programmers can author competencies.

3. **AI as Layer** prevented over-engineering. The AAP spec exists but doesn't dictate architecture. AI can be added when ready, not before.

4. **Evidence Driven** is the hardest principle to implement well. The domain model supports it, but the real test will come with real learners submitting real evidence.

5. **CLI-First MVP** kept scope tight. A GUI would have doubled complexity before we understood the domain.

6. **Local First** preserved user autonomy. No server dependency means the runtime works forever, even if the project stops.

7. **Tests as specification** worked. 163 tests across 6 layers gave us confidence to refactor without fear.

8. **Discipline matters more than speed.** Zero-dependency domain layer took more thought but eliminated entire classes of maintenance burden.

---

## What Must Never Change

These are the architectural invariants — the decisions that bind all future versions:

1. **No competency without evidence.** A competency cannot be claimed without verifiable proof. This is the North Star.

2. **Domain and application layers must have zero runtime dependencies.** Only Python stdlib. This protects the core from ecosystem rot.

3. **Packages are data, not code.** YAML-based, declarative, versioned. No execution in packages.

4. **Engine is agnostic to domain.** The runtime does not know what "cybersecurity" means. It only knows competencies, evidence, and assessment.

5. **Local first.** The runtime must work offline, without a server. Data belongs to the user.

6. **AI is a replaceable layer.** No hard coupling to any model, provider, or inference strategy.

7. **CLI is the reference interface.** Any GUI, web, or mobile client is secondary.

---

## What Changes in v2

The question of v1 was:

> *How do we build an Open Competency Runtime?*

The question of v2 is:

> *How do we make thousands of people create knowledge using this Runtime?*

This shifts everything from **implementation** to **adoption**.

### Structural Changes

| v1 | v2 |
|----|----|
| Build | Adopt |
| Implementation | Community |
| Code | Content |
| Chief Architect | Founder + Heads of Community, Education, Research, Standards, Partnerships |
| Runtime as asset | Competency Engineering as asset |
| Engineering milestones | Adoption milestones |

### New Roles

- Head of Community
- Head of Education
- Head of Research
- Head of Standards
- Head of Partnerships
- Editor-in-Chief (Book + Documentation)

### New Outputs (Non-Software)

- **ASCEND Book** — *The ASCEND Method, Volume I: Competency Engineering*
- **ASCEND Academy** — Training programs for Package Authors
- **ASCEND Certification** — Package Authors, Reviewers, Assessors, Mentors
- **ASCEND Labs** — Incubator for AI, VR, and Enterprise integrations

### Engineering in v2 (20% of effort)

- Bug fixes and stability only
- No new features unless demanded by adoption
- Infrastructure hardening for real-world use

---

## Closure

ASCEND v1.0 Standard Edition is declared **COMPLETE**.

Its architecture is **frozen**. Its specifications are **stable**. Its runtime is a **reference implementation**. Its governance is **established**.

The code will continue to exist. The tests will continue to pass. But no architectural changes will be made to v1.

Everything from this point forward is v2.

And v2 is not about code. It is about people.

---

*"Software was never the destination. It was the vehicle."*

```

### v2\V2-0001_Adoption_Strategy.md

```markdown
# V2-0001 — Adoption Strategy

**Status:** Draft  
**Version:** 0.1  
**Date:** 2026-07-19  
**Author:** Founder

---

## 1. Why Adoption First

The Runtime exists. The specifications are stable. The code works.

The only thing missing is **people using it**.

Adoption is not marketing. It is engineering a path for real humans to create, share, and validate competencies using ASCEND.

## 2. Adoption Funnel

```
Awareness → Interest → Trial → Authoring → Certification → Advocacy
```

### Awareness
- Publish introductory articles
- Open RFC discussions on specification design decisions
- Present at education technology, learning science, and open source conferences

### Interest
- Provide "5-minute ASCEND" demo (single mission, CLI)
- Show execution report output
- Demonstrate package validation

### Trial
- Guided walkthrough: `ascend init` → `ascend run` with a reference package
- Quickstart that produces a real competency claim in under 2 minutes

### Authoring
- Package Author workshop (see V2-0003 Content Strategy)
- Template-based package creation
- Validation feedback loop: `ascend package validate`

### Certification
- Formal credentialing for Package Authors, Reviewers, Assessors (see V2-0004)

### Advocacy
- Early adopters become community leaders
- Reference implementations in partner organizations
- Case studies and testimonials

## 3. Target Audiences

### Primary
- **Individual learners** — self-directed competency builders
- **Technical educators** — bootcamps, workshops, online courses
- **Open source contributors** — package authors, spec reviewers

### Secondary
- **Enterprises** — internal competency frameworks
- **Academic institutions** — curriculum alignment
- **Government** — skill certification programs

## 4. Adoption Metrics

| Metric | Target (90 days) |
|--------|------------------|
| GitHub stars | 100+ |
| Forks | 20+ |
| Unique package authors | 10+ |
| Published packages (non-reference) | 5+ |
| Community contributors | 15+ |
| RFC participants | 5+ |

## 5. Risk Factors

| Risk | Mitigation |
|------|------------|
| No one cares about another competency framework | Differentiate: evidence-first, open spec, local runtime |
| Too early for public consumption | Validate with 5 early adopters before broad launch |
| Competing with VC-backed platforms | Don't compete; offer what they can't: ownership, openness, offline |
| Complexity barrier to entry | Improve quickstart, add error messages, write tutorials |

## 6. Immediate Actions (First 30 Days)

1. Publish launch article on personal blog/dev.to
2. Open GitHub repository (public)
3. Create issue templates for bugs, features, RFCs, packages
4. Recruit 5 early adopters for private trial
5. Write and publish 3 tutorial blog posts
6. Submit talk proposals for 2 conferences

```

### v2\V2-0002_Community_Strategy.md

```markdown
# V2-0002 — Community Strategy

**Status:** Draft  
**Version:** 0.1  
**Date:** 2026-07-19  
**Author:** Founder

---

## 1. Community Model

ASCEND is an open competency ecosystem. Its community must reflect the same principles: open, evidence-based, meritocratic.

### Structure

```
                    ┌─────────────────┐
                    │  TSC (Technical  │
                    │  Steering Comm.) │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
     Package Authors    Spec Reviewers    Tool Contributors
            │                │                │
            ▼                ▼                ▼
       Content             Quality         Platform
```

### Roles

| Role | Responsibility |
|------|---------------|
| TSC Member | Governance, spec approval, conflict resolution |
| Package Author | Creates and maintains ASCEND packages |
| Spec Reviewer | Reviews RFCs and specification changes |
| Contributor | Code, tests, documentation, tools |
| Community Member | Discussions, bug reports, ideas |

## 2. Communication Channels

| Channel | Purpose |
|---------|---------|
| GitHub Issues | Bug reports, feature requests, RFCs |
| GitHub Discussions | Q&A, ideas, community support |
| (Future) Discourse/Forum | Long-form discussions, package announcements |
| (Future) Monthly Sync | Video call for contributors |

## 3. Contribution Pathways

### For Package Authors
1. Read the APS specification (SPEC-0001)
2. Study a reference package (e.g., `linux-foundations`)
3. Create a package using `ascend package create`
4. Submit to community registry (when available)

### For Spec Contributors
1. Open an RFC issue using the RFC template
2. Discuss and iterate
3. Submit PR with spec changes
4. TSC reviews and votes

### For Code Contributors
1. Find a `good first issue` label
2. Read CONTRIBUTING.md
3. Submit PR with tests (must pass all 163 existing tests)
4. Maintain zero-dependency discipline

## 4. Community Health

- **Code of Conduct:** Standard contributor covenant
- **Inclusive language:** All documentation and specs use neutral terminology
- **Recognition:** Contributors listed in release notes
- **Governance disputes:** Escalated to TSC, final decision by Founder

## 5. Immediate Actions

1. Prepare GitHub repository for public access
2. Create issue/PR templates
3. Write CONTRIBUTING.md v2 (already exists — verify and update)
4. Define `good first issue` backlog
5. Recruit 3 initial spec reviewers from personal network

```

### v2\V2-0003_Content_Strategy.md

```markdown
# V2-0003 — Content Strategy

**Status:** Draft  
**Version:** 0.1  
**Date:** 2026-07-19  
**Author:** Founder

---

## 1. Content Principles

- **Evidence-first:** Every competency claim must be provable
- **Open by default:** All packages are freely usable and forkable
- **Quality over quantity:** 10 great packages > 100 mediocre ones
- **Discipline-aligned:** Content follows Competency Engineering, not ad-hoc topics

## 2. Content Tracks

### Track A: The ASCEND Book

*The ASCEND Method, Volume I: Competency Engineering*

A formal book defining the methodology, philosophy, and practice of Competency Engineering.

**Estimated length:** ~200 pages  
**Format:** Open source (Markdown + PDF), print-on-demand  
**Audience:** Package Authors, Educators, Learning Engineers

**Proposed chapters:**

1. The Problem with Certification
2. Evidence as First Principle
3. Introducing Competency Engineering
4. The ASCEND Domain Model
5. Designing Competency Trees
6. Writing Effective Rubrics
7. Mission and Challenge Design
8. Assessment as a Service
9. The Package Lifecycle
10. Building an Open Competency Ecosystem
11. Case Study: Cybersecurity Foundations
12. The Future of Competency

### Track B: Package Author Training (ASCEND Academy)

**Format:** Workshop + written guide + reference packages  
**Audience:** Anyone who wants to create ASCEND packages

**Curriculum:**

1. Understanding APS v1.0
2. Anatomy of a Package
3. Writing Competency Definitions
4. Designing Rubrics
5. Creating Missions and Challenges
6. Validation and Testing
7. Publishing Best Practices

### Track C: Reference Packages

Continue building high-quality reference packages that demonstrate APS patterns.

| Priority | Package | Status |
|----------|---------|--------|
| 1 | docker-foundations | Not started |
| 2 | cloud-foundations | Not started |
| 3 | security-essentials | Not started |
| 4 | data-analysis-foundations | Not started |

### Track D: Tutorials and Articles

- "What is Competency Engineering?" (introductory article)
- "ASCEND in 5 Minutes" (quickstart guide)
- "From YAML to Competency: How ASCEND Packages Work"
- "Writing Your First Rubric"
- "Why Evidence Beats Certificates"

## 3. Content Calendar (90 Days)

| Month | Focus | Deliverables |
|-------|-------|-------------|
| 1 | Foundation | Launch article, 3 tutorials, Book outline finalized |
| 2 | Authoring | Academy workshop (pilot), 2 new reference packages, 2 guest articles |
| 3 | Publication | Book draft complete, Academy materials v1, 3 community-contributed packages |

## 4. Editorial Process

1. **Outline** — Define scope and audience
2. **Draft** — Write, review internally
3. **Review** — Technical accuracy + pedagogical quality
4. **Publish** — Open source release
5. **Iterate** — Accept PRs and feedback

**Editor-in-Chief** oversees all content and maintains voice consistency.

## 5. Immediate Actions

1. Set up book repository structure (`docs/book/`)
2. Write Chapter 1 draft
3. Publish "ASCEND in 5 Minutes" tutorial
4. Design Academy workshop outline
5. Recruit 1 technical reviewer for book drafts

```

### v2\V2-0004_Institute_Strategy.md

```markdown
# V2-0004 — Institute Strategy

**Status:** Draft  
**Version:** 0.1  
**Date:** 2026-07-19  
**Author:** Founder

---

## 1. Why an Institute?

A certification is only as valuable as the institution behind it.

The ASCEND Institute exists to provide **credible, third-party validation** of competencies built on the ASCEND framework.

It is not a school. It does not teach. It **certifies** the infrastructure for teaching and learning.

## 2. Certification Tracks

### Package Author Certification
- Proves ability to design and author valid ASCEND packages
- Requirements: Submit a package that passes validation + peer review
- Credential: ASCEND Certified Package Author

### Package Reviewer Certification
- Proves ability to evaluate package quality, rubric design, and evidence alignment
- Requirements: Review 3 packages submitted by candidates
- Credential: ASCEND Certified Reviewer

### Assessor Certification
- Proves ability to evaluate learner evidence and apply rubrics consistently
- Requirements: Assess 10 evidence submissions against reference rubrics
- Credential: ASCEND Certified Assessor

### Mentor Certification
- Proves ability to guide learners through ASCEND journeys
- Requirements: Mentor 5 learners to completion of a competency
- Credential: ASCEND Certified Mentor

## 3. Institute Structure

```
ASCEND Institute
├── Certification Board
│   ├── Package Author Certification
│   ├── Reviewer Certification
│   ├── Assessor Certification
│   └── Mentor Certification
├── Standards Committee
│   └── Maintains rubric quality and assessment consistency
└── Ethics Committee
    └── Handles disputes, fraud prevention, credential revocation
```

## 4. Certificate Verification

All certificates include a verification URL pointing to the ASCEND Registry.

```
Certificate #ASC-2026-00042
Name: Jane Doe
Credential: ASCEND Certified Package Author
Issued: 2026-09-15
Verify: https://registry.ascend.dev/verify/ASC-2026-00042
```

The verification page shows:
- Certificate metadata
- Evidence chain (what was submitted)
- Reviewer signature
- Current status (Active / Revoked / Expired)

## 5. Phased Launch

| Phase | Timeline | Scope |
|-------|----------|-------|
| 1 | Month 3-4 | Package Author Certification (pilot, 5 candidates) |
| 2 | Month 5-6 | Reviewer + Assessor Certification |
| 3 | Month 7-9 | Mentor Certification, public launch |
| 4 | Month 10+ | Partnerships with academic institutions |

## 6. Ethical Standards

- No certification can be purchased. It must be earned through demonstrated competence.
- All assessments are reviewed by at least one certified reviewer.
- Fraud or misrepresentation results in permanent revocation.
- The Institute does not sell personal data or learner records.

## 7. Immediate Actions

1. Define examination rubric for Package Author Certification
2. Design certificate template and verification system
3. Recruit 2 initial reviewers for pilot program
4. Draft Code of Ethics for the Institute
5. Establish pricing (if any) for certification applications

```

### v2\V2-0005_Funding_Strategy.md

```markdown
# V2-0005 — Funding Strategy

**Status:** Draft  
**Version:** 0.1  
**Date:** 2026-07-19  
**Author:** Founder

---

## 1. Funding Philosophy

ASCEND is open source and will remain open source.

Funding exists to sustain the infrastructure, not to extract value from the community.

> *Revenue is a means. Adoption is the mission.*

## 2. Revenue Streams

### Primary: Certification Fees

| Certification | Est. Fee | Rationale |
|---------------|----------|-----------|
| Package Author | Free–$50 | Low barrier, high volume |
| Reviewer | $100–$200 | Requires human review |
| Assessor | $200–$500 | Higher trust credential |
| Mentor | $100–$300 | Community leadership |

Certification fees cover reviewer stipends and infrastructure costs.

### Secondary: ASCEND Academy

- Workshops (live, virtual): $200–$500 per participant
- Enterprise training: Custom pricing
- Self-paced materials: Free (open source) with paid certificate option

### Tertiary: Partnerships and Sponsors

- Enterprise license for internal competency frameworks
- Government contracts for skill certification programs
- Educational institution partnerships
- Sponsorship of specific reference packages (e.g., cloud-foundations sponsored by a cloud provider)

### Not Pursuing

- VC funding (conflicts with local-first, user-owned data principles)
- Advertising (degrades trust)
- Data monetization (violates First Principles)

## 3. Use of Funds

| Category | Allocation |
|----------|------------|
| Infrastructure (registry, hosting, CI) | 20% |
| Reviewer stipends | 30% |
| Content development (Academy, Book) | 25% |
| Community grants | 15% |
| Legal and administrative | 10% |

## 4. Financial Transparency

- Monthly financial reports published openly
- All compensation rates for reviewers published
- No founder salaries until revenue exceeds sustainability threshold (~$10k/mo)
- Excess funds reinvested into community grants

## 5. Sustainability Targets

| Milestone | Monthly Revenue | Timeline |
|-----------|----------------|----------|
| Bootstrapped | $0 | Now |
| Sustainability | $5,000 | Month 12 |
| Growth | $15,000 | Month 24 |
| Independence | $30,000 | Month 36 |

## 6. Risks

| Risk | Mitigation |
|------|------------|
| No one pays for certification | Keep certification optional; value is in community recognition |
| Enterprise funding creates dependency | Cap any single partner at 20% of revenue |
| Legal costs from credential disputes | Clear terms of service + ethics committee |
| Burnout from underfunding | Keep scope small; grow only when sustainable |

## 7. Immediate Actions

1. Open GitHub Sponsors page
2. Define certification pricing model
3. Set up Open Collective or equivalent for transparent finances
4. Draft sponsorship prospectus for enterprise partners
5. Register legal entity (LLC or nonprofit) for the Institute

```