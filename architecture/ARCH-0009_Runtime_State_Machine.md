# ARCH-0009 — Runtime State Machine

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0009 |
| **Nome** | Runtime State Machine |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | ARCH-0001, ARCH-0003, ARCH-0008, SPEC-0002 AEP |
| **Referenciado por** | Runtime Kernel, State Engine, Implementation |

---

## 1. Propósito

Este documento define a **máquina de estados formal do Runtime do ASCEND**.

Enquanto o ARCH-0008 (Competency Lifecycle) define o ciclo de vida no nível de **domínio** (estados de uma missão/competência), este documento define o ciclo de vida no nível de **infraestrutura** (estados do Runtime como sistema executável).

A distinção é fundamental:

| Camada | Documento | O que governa | Exemplo de estados |
|--------|-----------|---------------|-------------------|
| **Domínio** | ARCH-0008 | Missão, evidência, competência | NOT_STARTED, AVAILABLE, COMPLETED |
| **Runtime** | ARCH-0009 | Pipeline de execução | LOADING, EXECUTING, REPORTING |

O Runtime é o **invólucro** que orquestra o ciclo de vida de domínio. Ele próprio possui um ciclo de vida distinto, com estados, transições, eventos, políticas e garantias de determinismo.

---

## 2. Visão Arquitetural: Os Quatro Motores

Este documento reconhece a visão do ASCEND como **quatro motores independentes**:

```
                        ASCEND
                            │
              ┌─────────────┼─────────────┐
              │             │             │
       Runtime Engine  State Engine  Competency  Evidence
                                      Engine     Engine
```

| Motor | Responsabilidade | Dono | Especificado em |
|-------|-----------------|------|-----------------|
| **Runtime Engine** | Orquestra a execução. Gerencia o pipeline: load → validate → convert → execute → report | Kernel | ARCH-0009 (este documento) |
| **State Engine** | Governa as transições válidas. Impede violações de invariantes. Audit trail | State Machine | ARCH-0009 (seção 3–7) |
| **Competency Engine** | Calcula progresso. XP, level, unlock de competências, achievements | `CompetencyEngine` | ARCH-0008 |
| **Evidence Engine** | Valida e consolida evidências. Formato, integridade, armazenamento | `AssessmentPipeline` + `ChallengeRunner` | ARCH-0008 |

> **Nota:** Esta separação não exige refatoração imediata. É uma direção arquitetural. A especificação abaixo já trata o State Engine como conceito formal, mesmo que sua implementação ainda esteja distribuída entre `RuntimeKernel`, `RuntimeOrchestrator` e `MissionRunner`.

---

## 3. State Machine do Runtime

### 3.1 Diagrama Completo

```
                     IDLE
                      │
                   [run() called]
                      ▼
                  LOADING
                      │
              ┌─ [load OK?] ──┐
              │                │
              ▼                ▼
         VALIDATING        FAILED
              │
      ┌─ [valid?] ──┐
      │              │
      ▼              ▼
  CONVERTING      FAILED
      │
      ▼
    READY
      │
      ▼
  EXECUTING
      │
      ├──→ JOURNEY_STARTED
      │       │
      │       ├──→ MISSION_STARTED
      │       │       │
      │       │       ├──→ CHALLENGE_PRESENTED
      │       │       ├──→ EVIDENCE_COLLECTED
      │       │       ├──→ ASSESSING
      │       │       └──→ MISSION_COMPLETED
      │       │
      │       └──→ JOURNEY_COMPLETED
      │
      ▼
  REPORTING
      │
      ▼
  COMPLETED
```

### 3.2 Tabela de Estados

| Estado | Nível | Definição | Duração Máxima | Dono |
|--------|-------|-----------|----------------|------|
| **IDLE** | Runtime | Runtime instanciado, aguardando `run()` | Indeterminada | Kernel |
| **LOADING** | Runtime | Lendo pacote do disco | 5s | PackageLoader |
| **VALIDATING** | Runtime | Validando estrutura do pacote | 5s | PackageValidator |
| **CONVERTING** | Runtime | Convertendo APS → Runtime models | 2s | PackageConverter |
| **READY** | Runtime | Pacote carregado, pronto para executar | 1s | Kernel |
| **EXECUTING** | Runtime | Executando jornadas | Variável | Orchestrator |
| ├ **JOURNEY_STARTED** | Execução | JourneyRunner iniciou journey | Variável | JourneyRunner |
| ├ **MISSION_STARTED** | Execução | MissionRunner iniciou missão | Variável | MissionRunner |
| ├ **CHALLENGE_PRESENTED** | Execução | Desafio apresentado ao builder | Variável | ChallengeRunner |
| ├ **EVIDENCE_COLLECTED** | Execução | Evidência recebida | 2s | ChallengeRunner |
| ├ **ASSESSING** | Execução | Evidência sendo avaliada | 30s | AssessmentPipeline |
| ├ **MISSION_COMPLETED** | Execução | Missão concluída (com ou sem unlock) | 1s | MissionRunner |
| └ **JOURNEY_COMPLETED** | Execução | Jornada concluída | 1s | JourneyRunner |
| **REPORTING** | Runtime | Gerando ExecutionReport | 1s | Orchestrator |
| **COMPLETED** | Runtime | Execução finalizada com sucesso | Terminal | Kernel |
| **FAILED** | Runtime | Execução finalizada com erros | Terminal | Kernel |
| **CANCELLED** | Runtime | Execução cancelada externamente | Terminal | Kernel |

---

## 4. Eventos do Runtime

### 4.1 Catálogo de Eventos

| Evento | Emissor | Estado de Origem | Estado de Destino | Payload |
|--------|---------|-----------------|-------------------|---------|
| **RunRequested** | Cliente (CLI/API) | IDLE | LOADING | `{ package_path, builder_id }` |
| **PackageLoaded** | PackageLoader | LOADING | VALIDATING | `{ package_id, version, file_count }` |
| **PackageLoadFailed** | PackageLoader | LOADING | FAILED | `{ error, path }` |
| **PackageValidated** | PackageValidator | VALIDATING | CONVERTING | `{ valid, warning_count }` |
| **PackageInvalid** | PackageValidator | VALIDATING | FAILED | `{ errors: [...] }` |
| **PackageConverted** | PackageConverter | CONVERTING | READY | `{ journey_count, mission_count }` |
| **ExecutionStarted** | Orchestrator | READY | EXECUTING | `{ builder_id, package_id }` |
| **JourneyStarted** | JourneyRunner | EXECUTING | JOURNEY_STARTED | `{ journey_id, mission_count }` |
| **MissionStarted** | MissionRunner | JOURNEY_STARTED | MISSION_STARTED | `{ mission_id, challenge_type }` |
| **ChallengePresented** | ChallengeRunner | MISSION_STARTED | CHALLENGE_PRESENTED | `{ mission_id, description }` |
| **EvidenceCollected** | ChallengeRunner | CHALLENGE_PRESENTED | EVIDENCE_COLLECTED | `{ evidence_id, evidence_type }` |
| **AssessmentStarted** | AssessmentPipeline | EVIDENCE_COLLECTED | ASSESSING | `{ mission_id, rubric_id }` |
| **AssessmentCompleted** | AssessmentPipeline | ASSESSING | MISSION_COMPLETED | `{ score, percentage, passed }` |
| **MissionCompleted** | MissionRunner | MISSION_COMPLETED | JOURNEY_STARTED | `{ mission_id, xp_gained, unlocked }` |
| **JourneyCompleted** | JourneyRunner | JOURNEY_STARTED | EXECUTING | `{ journey_id, missions_done, missions_total }` |
| **ExecutionFinished** | Orchestrator | EXECUTING | REPORTING | `{ journeys_completed, missions_completed }` |
| **ReportGenerated** | Orchestrator | REPORTING | COMPLETED | `{ duration, total_xp, competencies_unlocked }` |
| **ExecutionCancelled** | Cliente/Admin | EXECUTING | CANCELLED | `{ reason }` |
| **RuntimeError** | Qualquer | Qualquer | FAILED | `{ error, location, recoverable }` |

### 4.2 Ordem Causal dos Eventos

```
RunRequested
    → PackageLoaded | PackageLoadFailed
        → PackageValidated | PackageInvalid
            → PackageConverted
                → ExecutionStarted
                    → JourneyStarted (por journey)
                        → MissionStarted (por missão)
                            → ChallengePresented
                                → EvidenceCollected
                                    → AssessmentStarted
                                        → AssessmentCompleted
                                            → MissionCompleted
                                    ├── AssessmentStarted
                                    └── AssessmentCompleted (rejeitado)
                                → EvidenceCollected (retry)
                            → ChallengePresented (retry)
                        → MissionCompleted (próxima missão)
                        → MissionStarted
                        → ...
                    → JourneyCompleted
                    → JourneyStarted (próxima journey)
                    → ...
                → ExecutionFinished
                    → ReportGenerated
                → RuntimeError
                    → FAILED
```

### 4.3 Schema do Evento de Runtime

```python
@dataclass
class RuntimeEvent:
    event_id: str
    event_type: str
    previous_state: RuntimeState
    current_state: RuntimeState
    payload: dict[str, Any]
    timestamp: datetime
    trace_id: str       # Correlaciona todos os eventos de uma execução
    version: int = 1
```

### 4.4 Diferença entre RuntimeEvent e DomainEvent

| Característica | RuntimeEvent | DomainEvent |
|----------------|-------------|-------------|
| **Nível** | Infraestrutura | Domínio |
| **Quem emite** | Kernel, Loader, Orchestrator, Runners | Builder, Mission, CompetencyEngine |
| **O que rastreia** | Pipeline de execução | Ciclo de vida da competência |
| **Armazenamento** | Runtime log (em memória) | EventStore (SQLite) |
| **Consumidores** | Monitoramento, debugging | Audit trail, projeções |
| **Exemplo** | `PackageLoaded`, `ExecutionStarted` | `CompetencyUnlocked`, `EvidenceSubmitted` |

---

## 5. Transições

### 5.1 Transições Válidas (Primeiro Nível)

| Estado de Origem | Gatilho | Política | Estado de Destino |
|-----------------|---------|----------|-------------------|
| IDLE | `Kernel.run()` chamado | Builder deve existir | LOADING |
| LOADING | `PackageLoader.load()` OK | Arquivo package.yaml existe e é YAML válido | VALIDATING |
| LOADING | `PackageLoader.load()` falha | Exceção FileNotFoundError ou OSError | FAILED |
| VALIDATING | `PackageValidator.validate()` OK | Nenhum erro de validação | CONVERTING |
| VALIDATING | `PackageValidator.validate()` falha | Erros de validação detectados | FAILED |
| CONVERTING | `PackageConverter.convert()` OK | APS models convertidos com sucesso | READY |
| CONVERTING | `PackageConverter.convert()` falha | Erro inesperado na conversão | FAILED |
| READY | `RuntimeOrchestrator.run()` chamado | Contexto montado com sucesso | EXECUTING |
| EXECUTING | Todas as journeys executadas | Nenhum erro fatal | REPORTING |
| EXECUTING | Erro fatal não recuperável | Exceção não capturada pelo orchestrator | FAILED |
| EXECUTING | Cancelamento externo | Sinal de interrupção recebido | CANCELLED |
| REPORTING | `ExecutionReport` gerado | Relatório montado com sucesso | COMPLETED |
| REPORTING | Falha ao gerar relatório | Erro ao consolidar resultados | FAILED |

### 5.2 Transições Válidas (Segundo Nível — Execução)

| Estado de Origem | Gatilho | Política | Estado de Destino |
|-----------------|---------|----------|-------------------|
| EXECUTING | JourneyRunner inicia journey | Package contém journeys | JOURNEY_STARTED |
| JOURNEY_STARTED | MissionRunner inicia missão | Pré-requisitos satisfeitos | MISSION_STARTED |
| JOURNEY_STARTED | Todas as missões processadas | Iteração concluída | EXECUTING |
| MISSION_STARTED | ChallengeRunner.open() | Missão inicializada com sucesso | CHALLENGE_PRESENTED |
| CHALLENGE_PRESENTED | Evidence recebida via contexto | Evidência não vazia | EVIDENCE_COLLECTED |
| CHALLENGE_PRESENTED | evidence_required == false | Missão não exige evidência | MISSION_COMPLETED |
| EVIDENCE_COLLECTED | AssessmentPipeline.run() inicia | Evidência validada estruturalmente | ASSESSING |
| ASSESSING | AssessmentPipeline.run() conclui | Score calculado (aprovado ou não) | MISSION_COMPLETED |
| MISSION_COMPLETED | Próxima missão disponível | Mais missões na journey | MISSION_STARTED |
| MISSION_COMPLETED | Todas as missões da journey feitas | Nenhuma missão restante | JOURNEY_STARTED |

### 5.3 Transições Inválidas (Proibidas pelo State Engine)

| Tentativa | Motivo | Invariante Violado |
|-----------|--------|--------------------|
| IDLE → EXECUTING | Pula LOADING, VALIDATING, CONVERTING | Pipeline incompleto |
| LOADING → READY | Pula VALIDATING e CONVERTING | Pacote não validado |
| VALIDATING → EXECUTING | Pula CONVERTING | Package não convertido |
| READY → FAILED | Falha sem execução | Estado impossível |
| EXECUTING → COMPLETED | Pula REPORTING | Relatório não gerado |
| MISSION_STARTED → ASSESSING | Pula CHALLENGE_PRESENTED, EVIDENCE_COLLECTED | Violação ARCH-0008 CL4 |
| EVIDENCE_COLLECTED → COMPLETED | Pula ASSESSING | Violação ARCH-0008 CL1 |
| CHALLENGE_PRESENTED → MISSION_COMPLETED | Se evidence_required == true | Evidência obrigatória ignorada |
| COMPLETED → EXECUTING | Regressão de estado | Estado terminal |

---

## 6. Políticas de Autorização

Cada transição é autorizada por uma **política** — uma regra que deve ser verdadeira para que a transição ocorra.

| Transição | Política | Implementação |
|-----------|----------|---------------|
| IDLE → LOADING | Caminho do pacote é válido e acessível | `Path.exists()` |
| LOADING → VALIDATING | package.yaml parseável como YAML | `yaml.safe_load()` |
| VALIDATING → CONVERTING | `ValidationResult.valid == True` | `PackageValidator.validate()` |
| CONVERTING → READY | APS→Runtime convertido sem erros | `PackageConverter.convert()` |
| READY → EXECUTING | `RuntimeContext` montado com builder + pacote | `RuntimeContext()` |
| JOURNEY_STARTED → MISSION_STARTED | `Mission.can_start(completed_ids) == True` | `JourneyRunner` verifica pré-requisitos |
| MISSION_STARTED → CHALLENGE_PRESENTED | Missão iniciou corretamente | `MissionRunner` + domain |
| CHALLENGE_PRESENTED → EVIDENCE_COLLECTED | Evidência existe no `RuntimeContext.evidence_input` | `ChallengeRunner.collect_evidence()` |
| EVIDENCE_COLLECTED → ASSESSING | Evidência validada (não vazia, tipo aceito) | `AssessmentPipeline.validate()` |
| ASSESSING → MISSION_COMPLETED | `AssessmentResult` calculado | `AssessmentPipeline.run()` |
| EXECUTING → REPORTING | Todas as journeys processadas | `RuntimeOrchestrator.run()` |
| REPORTING → COMPLETED | `ExecutionReport` montado | Construtor do report |

---

## 7. Ações Executadas em Cada Transição

| Transição | Ações | Efeitos Colaterais |
|-----------|-------|--------------------|
| IDLE → LOADING | Iniciar temporizador. Resolver caminho absoluto. | Nenhum |
| LOADING → VALIDATING | Ler package.yaml. Parsear YAML. | Arquivo lido do disco |
| VALIDATING → CONVERTING | Executar 13 regras de validação. | Nenhum |
| CONVERTING → READY | Instanciar RuntimePackage, RuntimeJourney, RuntimeMission. | Models em memória |
| READY → EXECUTING | Criar RuntimeContext. Instanciar DomainEventCollector. | Contexto alocado |
| EXECUTING → JOURNEY_STARTED | Disparar hook `before_journey`. | Hook executado |
| JOURNEY_STARTED → MISSION_STARTED | Disparar hook `before_mission`. | Hook executado |
| MISSION_STARTED → CHALLENGE_PRESENTED | Emitir `MissionStarted`. Executar `ChallengeRunner.open()`. | Evento gerado |
| CHALLENGE_PRESENTED → EVIDENCE_COLLECTED | Emitir `EvidenceSubmitted`. | Evento gerado |
| EVIDENCE_COLLECTED → ASSESSING | Emitir `AssessmentStarted`. Disparar hook `before_assessment`. | Evento gerado |
| ASSESSING → MISSION_COMPLETED | Emitir `AssessmentCompleted`. Disparar hook `after_assessment`. Executar `CompetencyEngine.process()`. Atualizar Builder (XP, level, competencies). | Builder modificado |
| MISSION_COMPLETED → JOURNEY_STARTED | Disparar hook `after_mission`. | Hook executado |
| JOURNEY_STARTED → EXECUTING | Disparar hook `after_journey`. Consolidar resultados parciais. | Hook executado |
| EXECUTING → REPORTING | Coletar todos os JourneyResult. Calcular totais. | Nenhum |
| REPORTING → COMPLETED | Calcular duração. Limpar collector. | Collector drain |
| EXECUTING → FAILED | Capturar exceção. Registrar erro no report. | Report com success=false |
| EXECUTING → CANCELLED | Interromper execução. Marcador de cancelamento. | Estado terminal |

---

## 8. Garantias de Determinismo

### 8.1 O Runtime é Determinístico?

**Sim, para o mesmo input, o mesmo Runtime produz o mesmo output.**

### 8.2 Condições para Determinismo

| Condição | Garantia | Dependência |
|----------|----------|-------------|
| Mesmo pacote YAML | ✅ Idêntico | PackageLoader não depende de rede |
| Mesma evidência | ✅ Idêntico | AssessmentPipeline é puro (sem IO) |
| Mesmo builder | ✅ Idêntico | Builder mutado apenas pelo Runtime |
| Mesmo clock | ✅ Idêntico | Clock injetado (FakeClock em testes) |
| Mesmos hooks | ✅ Idêntico | Hooks síncronos, sem efeitos colaterais |
| Sem agentes IA | ✅ Idêntico | Pipeline built-in sem randomness |
| Com agentes IA | ❌ Não determinístico | LLMs produzem outputs diferentes |

### 8.3 Fontes de Não-Determinismo

| Fonte | Impacto | Mitigação |
|-------|---------|-----------|
| `datetime.now()` direto | Alto | Usar `Clock` injetado (já implementado) |
| `uuid4()` / `md5()` | Baixo | IDs únicos,不影响 lógica |
| Ordem de iteração de dict | Médio | Python 3.7+ preserva ordem de inserção |
| Agentes de IA externos | Alto | AAP define contrato, mas output varia |
| Exceções assíncronas | Médio | Kernel é síncrono por definição (AEP) |

### 8.4 Provas de Determinismo

**Prova 1:** Dado um pacote APS válido e uma evidência fixa, `AssessmentPipeline.run()` retorna o mesmo `AssessmentResult` em todas as execuções.

**Prova 2:** Dado um `AssessmentResult` fixo, `CompetencyEngine.process()` retorna o mesmo `CompetencyUpdate` para o mesmo builder state.

**Prova 3:** Dado um `RuntimeKernel` com `FakeClock` e `NoopHooks`, `run()` retorna o mesmo `ExecutionReport` para o mesmo input.

### 8.5 Garantias do State Engine

| Garantia | Descrição |
|----------|-----------|
| **Unicidade de estado** | Runtime está em exatamente um estado por vez |
| **Transições atômicas** | Cada transição completa ou falha como um todo |
| **Não regressão** | Nenhuma transição retorna a um estado anterior no mesmo eixo |
| **Eventos imutáveis** | Eventos são append-only, nunca alterados |
| **Rastreabilidade** | Toda transição deixa um RuntimeEvent rastreável |
| **Recuperabilidade** | Estados FAILED e CANCELLED são terminais com diagnóstico |

---

## 9. Mapeamento para a Implementação Atual

### 9.1 Onde cada estado vive hoje

| Estado ARCH-0009 | Local na Implementação Atual | Status |
|------------------|------------------------------|--------|
| IDLE | `RuntimeKernel.__init__()` — após construção | ✅ Implícito |
| LOADING | `RuntimeKernel.run()` linha 35: `PackageLoader.load()` | ✅ Existe, sem estado explícito |
| VALIDATING | `RuntimeKernel.run()` linha 50: `validation.valid` | ✅ Existe, sem estado explícito |
| CONVERTING | `RuntimeKernel.run()` linha 65: `PackageConverter.convert()` | ✅ Existe, sem estado explícito |
| READY | `RuntimeKernel.run()` linha 68–75: criação do `RuntimeContext` | ✅ Implícito |
| EXECUTING | `RuntimeKernel.run()` linha 78: `Orchestrator.run()` | ✅ Existe |
| JOURNEY_STARTED | `JourneyRunner.run()` | ✅ Existe |
| MISSION_STARTED | `MissionRunner.run()` | ✅ Existe |
| CHALLENGE_PRESENTED | `ChallengeRunner.open()` | ✅ Existe |
| EVIDENCE_COLLECTED | `ChallengeRunner.collect_evidence()` | ✅ Existe |
| ASSESSING | `AssessmentPipeline.run()` | ✅ Existe |
| MISSION_COMPLETED | `MissionRunner.run()` — retorno | ✅ Existe |
| JOURNEY_COMPLETED | `JourneyRunner.run()` — retorno | ✅ Existe |
| REPORTING | `RuntimeKernel.run()` linha 79–82 | ⚠️ Inline, sem estado explícito |
| COMPLETED | `RuntimeKernel.run()` — retorno do report | ✅ Implícito |
| FAILED | `RuntimeKernel.run()` — retorno com erros | ✅ Implícito |
| CANCELLED | **Não implementado** | ❌ Inexistente |

### 9.2 Lacunas

| Lacuna | Descrição | Prioridade |
|--------|-----------|------------|
| Nenhum estado é explícito no Runtime | Runtime não expõe `current_state` | Alta |
| CANCELLED não existe | Não há suporte a interrupção de execução | Média |
| REPORTING é inline | Misturado com a lógica de finalização | Média |
| Eventos de Runtime não são emitidos | Só existem DomainEvents | Alta |
| Sem trace_id entre eventos | Eventos não correlacionáveis | Média |

### 9.3 Recomendações

1. **Adicionar `RuntimeState` enum** em `runtime/models.py`
2. **Expor `current_state` no `RuntimeContext`** para hooks e debugging
3. **Criar `RuntimeEventCollector`** (separado do `DomainEventCollector`)
4. **Implementar `CANCELLED`** com suporte a signal handlers
5. **Extrair `StateEngine`** como componente independente na próxima versão

---

## 10. Relação com os Quatro Motores

### 10.1 Como o State Engine se relaciona com os demais

```
                  Runtime Engine (Kernel)
                        │
                        │  delega para
                        ▼
┌─────────────────────────────────────────────┐
│              State Engine                    │
│                                              │
│  • Guarda o estado atual                     │
│  • Valida cada transição contra a máquina    │
│  • Rejeita transições inválidas              │
│  • Emite RuntimeEvent para cada transição    │
│  • Garante determinismo                     │
└─────────────────────────────────────────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
   Competency        Evidence      Package
     Engine           Engine        Loader
```

### 10.2 Contrato do State Engine

```python
class StateEngine(Protocol):
    def current(self) -> RuntimeState: ...
    def can_transition(self, target: RuntimeState) -> bool: ...
    def transition(self, target: RuntimeState, payload: dict) -> RuntimeEvent: ...
    def allowed_transitions(self) -> list[RuntimeState]: ...
    def reset(self) -> None: ...
```

### 10.3 Visão de Evolução

| Versão | State Engine | Implementação |
|--------|-------------|---------------|
| v1.0 (atual) | Inexistente | Estados implícitos no fluxo do Kernel |
| v1.1 | Enum + validação | `RuntimeState` enum, `can_transition()` |
| v2.0 | Componente independente | `StateEngine` class com máquina formal |

---

## 11. Failure Modes do Runtime

| Modo de Falha | Estado | Gatilho | Resposta Atual | Resposta Desejada |
|--------------|--------|---------|----------------|-------------------|
| Pacote não encontrado | LOADING | Path inexistente | `FileNotFoundError` capturado → FAILED | ✅ Adequado |
| YAML mal formatado | LOADING | Arquivo corrompido | Exceção não capturada → FAILED | ⚠️ Melhorar mensagem |
| Validação falha | VALIDATING | Regra de validação quebrada | `ValidationResult.valid=False` → FAILED | ✅ Adequado |
| Conversão falha | CONVERTING | Erro inesperado | Exceção não capturada → FAILED | ⚠️ Capturar no Kernel |
| Erro em uma journey | EXECUTING | Exceção no JourneyRunner | Capturado, continua próxima journey | ✅ Adequado |
| Erro em todas as journeys | EXECUTING | Exceção no Orchestrator | Report com errors | ✅ Adequado |
| Timeout de execução | EXECUTING | Missão nunca completa | Não implementado | ❌ Adicionar timeout |
| Cancelamento pelo usuário | EXECUTING | Ctrl+C / signal | Não tratado | ❌ Adicionar CANCELLED |
| Falha ao gerar relatório | REPORTING | Erro ao consolidar | Não implementado | ❌ Tratar como FAILED |

---

## 12. Exemplo de Execução Completa

### 12.1 Cenário: Builder executa pacote cyber-foundations

```
Linha do Tempo               Estado            Evento
──────────────────────────────────────────────────────────────────
t=0s    Runtime instanciado   IDLE
t=0s    run() chamado         LOADING           RunRequested
t=0.1s  package.yaml lido     VALIDATING        PackageLoaded
t=0.2s  Válido                CONVERTING        PackageValidated
t=0.3s  Convertido            READY             PackageConverted
t=0.3s  Iniciando orquestrador EXECUTING        ExecutionStarted
t=0.3s  Journey "fundamentos" JOURNEY_STARTED   JourneyStarted
t=0.3s  Missão "html"         MISSION_STARTED   MissionStarted
t=0.3s  Desafio apresentado   CHALLENGE_PRESENTED ChallengePresented
t=0.3s  Evidence coletada     EVIDENCE_COLLECTED EvidenceCollected
t=0.3s  Avaliando             ASSESSING         AssessmentStarted
t=0.4s  Aprovado (85%)        MISSION_COMPLETED AssessmentCompleted
t=0.4s  Missão "css"          MISSION_STARTED   MissionStarted
t=0.4s  Desafio apresentado   CHALLENGE_PRESENTED ChallengePresented
t=0.4s  Evidence coletada     EVIDENCE_COLLECTED EvidenceCollected
t=0.4s  Avaliando             ASSESSING         AssessmentStarted
t=0.5s  Aprovado (90%)        MISSION_COMPLETED AssessmentCompleted
t=0.5s  Journey completa      JOURNEY_COMPLETED JourneyCompleted
t=0.5s  Journey "lógica"      JOURNEY_STARTED   JourneyStarted
t=0.5s  Missão "python"       MISSION_STARTED   MissionStarted
t=0.5s  Desafio apresentado   CHALLENGE_PRESENTED ChallengePresented
t=0.5s  Sem evidência         EVIDENCE_COLLECTED
t=0.5s  Avaliando             ASSESSING
t=0.6s  Aprovado (baseline)   MISSION_COMPLETED
t=0.6s  Journey completa      JOURNEY_COMPLETED JourneyCompleted
t=0.6s  Gerando relatório     REPORTING         ExecutionFinished
t=0.7s  Report pronto         COMPLETED         ReportGenerated
```

---

## 13. Glossário

| Termo | Definição |
|-------|-----------|
| **RuntimeState** | Enum que representa o estado atual do Runtime |
| **RuntimeEvent** | Evento emitido a cada transição de estado do Runtime |
| **State Engine** | Componente que governa as transições válidas do Runtime |
| **Trace ID** | Identificador único que correlaciona todos os eventos de uma execução |
| **Transição** | Mudança de um estado para outro, autorizada por uma política |
| **Política** | Regra que deve ser verdadeira para que uma transição ocorra |
| **Determinismo** | Propriedade de produzir o mesmo output para o mesmo input |
| **Pipeline** | Sequência de estados que o Runtime percorre: IDLE → LOADING → VALIDATING → CONVERTING → READY → EXECUTING → REPORTING → COMPLETED |

---

## 14. Declaração Final

> **O Runtime do ASCEND não é um script que executa missões.**
>
> É um **sistema de estados** que orquestra um pipeline determinístico.
>
> A máquina de estados aqui especificada garante que:
>
> 1. O pipeline nunca pula etapas
> 2. Toda transição é autorizada por uma política
> 3. Toda transição é registrada como evento
> 4. O estado é sempre conhecido e verificável
> 5. Falhas são estados, não exceções
> 6. O sistema é determinístico para o mesmo input
>
> A separação futura em quatro motores (Runtime, State, Competency, Evidence)
> fortalecerá ainda mais essas garantias — mas o contrato já está definido aqui.

---

---

## Stability Declaration

> **The Runtime is frozen.**

Starting from v1.0 Standard Edition, the Runtime Kernel (`ascend.runtime`) is considered **stable and frozen**. No changes may be made to it without:
1. An approved RFC (see `docs/rfc/RFC_TEMPLATE.md`)
2. Approval from the Technical Steering Committee (TSC)
3. An Architecture Decision Record (ADR) documenting the rationale

All platform development happens **around** the Runtime — through the Application Layer, API, and SDK — never inside it.

---

## Appendix A: Comparação Runtime vs Domain State Machines

| Dimensão | ARCH-0008 (Domain) | ARCH-0009 (Runtime) |
|----------|-------------------|---------------------|
| **O que modela** | Ciclo de vida da competência | Pipeline de execução do sistema |
| **Estados** | NOT_STARTED → ACHIEVEMENT_GRANTED | IDLE → COMPLETED/FAILED/CANCELLED |
| **Eventos** | DomainEvents (8) | RuntimeEvents (19) |
| **Persistência** | EventStore (SQLite) | Em memória (log) |
| **Determinismo** | Sim (sem IA) | Sim (clock + hooks injetados) |
| **Responsável** | Domain + Runners | Kernel + State Engine |
| **Audit trail** | EventStore | RuntimeEventCollector |
| **Duração** | Longa (dias) | Curta (segundos) |
