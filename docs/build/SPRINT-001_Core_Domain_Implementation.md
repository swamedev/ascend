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
