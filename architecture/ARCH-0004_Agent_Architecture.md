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
