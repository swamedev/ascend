# DOC-0009 — Architectural Invariants

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0009 |
| **Nome** | Architectural Invariants |
| **Versão** | 7.0 |
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

### I11 — API Independence (no interface knows the Runtime directly)

Nenhuma interface (REST, SDK, CLI, UI gráfica) pode importar,
instanciar ou depender diretamente do Runtime (`ascend.runtime`).

Toda comunicação entre interfaces e Runtime passa
obrigatoriamente pela Application Layer (use cases).

```
UI/SDK → API → Application Layer → Runtime
```

Isso garante que:
- Trocar de Runtime não exige mudar interfaces
- Trocar de interface não exige mudar o Runtime
- A Application Layer é o único contrato que importa

### I12 — SDK Independence (no Feature imports HTTP directly)

Nenhuma Feature, Componente ou Hook no frontend pode importar
diretamente bibliotecas HTTP (`fetch`, `axios`, `ky`, etc.) ou
instanciar Transportes.

Toda comunicação entre a Experience Layer e a Platform Layer passa
obrigatoriamente pelos **SDK Clients**.

```
Feature → SDK Client → Transport → API/Runtime
```

Isso garante que:
- Trocar de API não exige mudar a interface
- Trocar de Transporte (Mock → REST → Offline) não exige mudar Features
- O SDK é o único contrato que a Experience Layer conhece

### I13 — Canonical Language

Toda camada do ASCEND deve utilizar o mesmo modelo canônico para representar os conceitos do domínio. O pacote `@ascend/contracts` é a fonte única da verdade para todos os tipos de domínio. Traduções entre camadas devem ser excepcionais, documentadas e justificadas por RFC.

### I14 — Cognitive Independence

Nenhum componente cognitivo pode alterar o Runtime.

A Cognitive Layer pode:
- Observar eventos e estado do Runtime (somente leitura)
- Analisar padrões através de observações
- Gerar insights e recomendações estruturados
- Publicar insights para a Experience Layer

A Cognitive Layer **não pode**:
- Alterar entidades de domínio
- Modificar estado do Runtime
- Alterar competências, XP ou níveis
- Escrever no banco de dados
- Bloquear operações do Runtime
- Sobrescrever decisões do Builder

Toda comunicação entre a Cognitive Layer e o Runtime é governada pelo **SPEC-0005 — Cognitive Protocol**.

### I15 — Observation Determinism

Every observation must produce the same result for the same sequence of events.

The Cognitive Layer may never modify events. It may only observe them.

Events are immutable. Metrics are reproducible. Replay must generate exactly the same results.

### I16 — Observation Append Only

Once an observation is written to the cognitive store, it is never modified, updated, or deleted.

The `observations` table is **append-only**. No `UPDATE` or `DELETE` operations are permitted on observation rows. The only exception is retention pruning, which deletes entire rows (not individual fields) according to a configurable policy — and even then, pruning is logged and auditable.

This invariant guarantees:
- **Replay determinism:** The same session always produces the same timeline, because the same observations are always read in the same order.
- **Audit integrity:** Historical observations are tamper-proof. What was observed at the time is preserved forever.
- **Causal traceability:** Every signal, pattern, and insight can be traced back to its root observation, which will never change.

The only permitted mutations on cognitive data are:
1. **Append**: New observations are written.
2. **Prune**: Entire observation rows are deleted (not updated) by retention policy.
3. **Export & Delete**: The builder can export and then delete all their data (full row deletion, not update).

No `UPDATE` statement may target the `observations`, `signals`, or `events` tables of the cognitive database at any time.

### I17 — Repository Integrity

The repository must never be left in an inconsistent state.

Every logical unit of work must end with:
- All tests passing
- Documentation synchronized
- Commit completed
- Working tree clean (`git status` → `nothing to commit, working tree clean`)

**Rules:**

1. **No implementation continues while uncommitted code exists.** If `git status` is dirty, fix it first.
2. **`git status` must return `working tree clean` before starting any new feature.**
3. **Never accumulate more than 10 files changed OR 500 lines without a commit.** Whichever limit is reached first triggers a mandatory commit.
4. **Every AI agent must run `git status` before starting and before finishing any task.**
5. **Under no circumstances may the working tree contain 200+ uncommitted files.** This is a constitutional violation requiring immediate invocation of RECOVERY_PROTOCOL.md.
6. **Every commit must be small and focused.** One commit = one logical change.

**Failure to comply with I17 triggers mandatory RECOVERY_PROTOCOL.md execution.** Repeated violations may result in loss of commit privileges.

### I18 — Cognitive Pipeline Determinism

Every stage of the Cognitive Pipeline must be a deterministic, pure function of its input.

**Pipeline stages:**

```
ObservationCollection → Normalization → SignalExtraction → PatternDetection → InsightGeneration → Recommendation
```

Each stage must satisfy:
1. **Same input → same output.** Given the same sequence of events, every stage produces identical output regardless of environment, time, or execution count.
2. **No randomness.** No stage may use random number generation, sampling, or probabilistic algorithms in deterministic mode.
3. **No AI.** No stage may invoke AI models, LLMs, or non-deterministic external services.
4. **No external state.** No stage may depend on mutable global state, wall-clock time (except timestamps from the input event), or environment-specific configuration.
5. **Lineage preservation.** Every output must carry references to its source inputs, enabling full traceability through the pipeline.

**Rationale:** Determinism is what makes the Cognitive Layer testable, auditable, and replayable. If a Pattern Detector produces different results for the same signals on different runs, the system cannot be validated. AI augmentation is permitted ONLY at a separate, explicitly marked post-processing layer that sits outside the deterministic pipeline — and even then, the deterministic pipeline output must be preserved unmodified alongside any AI-enhanced output.

**Enforcement:**
- Every stage implementation must be a `Protocol` with a pure function signature
- Unit tests must verify determinism by running each stage twice with identical inputs and asserting identical outputs
- The CI pipeline (`ascend doctor --workflow`) will flag any stage that imports `random`, `numpy.random`, LLM SDKs, or HTTP clients

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 7.0 | 2026-07-21 | Chief Architect | Added I18 — Cognitive Pipeline Determinism (OPERAÇÃO ORACLE II) |
| 6.0 | 2026-07-21 | Chief Architect | Added I17 — Repository Integrity (OPERAÇÃO HERMES II) |
| 5.0 | 2026-07-21 | Chief Architect | Added I16 — Observation Append Only (OPERAÇÃO PROMETHEUS) |
| 4.0 | 2026-07-20 | Chief Architect | Added I15 — Observation Determinism (OPERAÇÃO OLYMPUS) |
| 3.0 | 2026-07-20 | Chief Architect | Added I14 — Cognitive Independence (OPERAÇÃO ATHENA — The Cognitive Constitution) |
| 2.0 | 2026-07-20 | Chief Architect | Added I13 — Canonical Language (references `@ascend/contracts`) |
| 1.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO APOLLO |

## Violações

Se um Pull Request violar qualquer invariante:

1. Marcar como `blocked: architectural-invariant`
2. Notificar o Chief Architect
3. Não mergear até resolução

## Status

**DOC-0009 — Architectural Invariants**

- Estado: ✅ Approved
- Próximo: Archieve como referência para code review
