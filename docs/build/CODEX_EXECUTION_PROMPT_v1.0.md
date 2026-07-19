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
