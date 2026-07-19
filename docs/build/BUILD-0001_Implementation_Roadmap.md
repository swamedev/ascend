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
