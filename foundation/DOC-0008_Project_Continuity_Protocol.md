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
