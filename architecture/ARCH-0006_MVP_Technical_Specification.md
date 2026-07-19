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
