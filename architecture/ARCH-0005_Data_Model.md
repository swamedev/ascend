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
