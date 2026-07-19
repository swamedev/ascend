# Protocol Governance

| Campo | Valor |
|-------|-------|
| **ID** | PROTOCOL-GOV |
| **Nome** | Protocol Governance |
| **Versão** | 1.0 |
| **Status** | Stable |
| **Categoria** | Governance |
| **Owner** | Chief Architect |
| **Derivado de** | Constituição, CONTRIBUTING.md, GOVERNANCE.md |

---

## 1. Propósito

Este documento define as regras de **evolução, versionamento, compatibilidade, depreciação e governança** de todos os protocolos do ASCEND.

---

## 2. Ciclo de Evolução dos Protocolos

### 2.1 Estágios

Cada protocolo passa por estágios definidos:

```
DRAFT → PROPOSED → STABLE → DEPRECATED → RETIRED
```

| Estágio | Significado | Pode mudar? | Uso em produção |
|---------|-------------|-------------|-----------------|
| **DRAFT** | Em desenvolvimento inicial | Sim, qualquer mudança | Não recomendado |
| **PROPOSED** | Proposto para revisão | Sim, mudanças controladas | Experimental |
| **STABLE** | Aprovado e congelado | Apenas PATCH | Permitido |
| **DEPRECATED** | Substituído, mas ainda funcional | Não | Permitido com warnings |
| **RETIRED** | Removido do ecossistema | Não | Proibido |

### 2.2 Transições entre Estágios

| De | Para | Requisitos | Aprovação |
|----|------|------------|-----------|
| DRAFT | PROPOSED | Revisão técnica completa | Chief Architect |
| PROPOSED | STABLE | 2 semanas sem objeções, testes implementados | TSC |
| STABLE | DEPRECATED | Protocolo substituto em STABLE | TSC |
| DEPRECATED | RETIRED | 6 meses após depreciação | TSC |

---

## 3. Versionamento

### 3.1 Esquema

Todos os protocolos seguem **SemVer** estrito:

```
MAJOR.MINOR.PATCH
```

| Componente | Quando incrementar | Exemplo |
|------------|--------------------|---------|
| **MAJOR** | Mudança incompatível | Remoção de campo obrigatório, alteração de comportamento |
| **MINOR** | Adição compatível | Novo campo opcional, novo evento |
| **PATCH** | Correção compatível | Esclarecimento de texto, correção de schema |

### 3.2 Versão dos Protocolos

| Protocolo | Versão Atual | Estágio |
|-----------|-------------|---------|
| PROTOCOL-0001 (Core) | 1.0.0 | STABLE |
| PROTOCOL-0002 (Event) | 1.0.0 | STABLE |
| PROTOCOL-0003 (State) | 1.0.0 | STABLE |
| PROTOCOL-0004 (Policy) | 1.0.0 | STABLE |
| PROTOCOL-0005 (Capability) | 1.0.0 | STABLE |

---

## 4. Compatibilidade Retroativa

### 4.1 Regras

| Tipo de Mudança | Compatibilidade | Exigência |
|-----------------|----------------|-----------|
| Adição de campo opcional no payload | Retroativa | MINOR |
| Adição de novo evento | Retroativa | MINOR |
| Adição de novo estado | Retroativa | MINOR |
| Adição de nova policy | Retroativa | MINOR |
| Remoção de campo obrigatório | **Breaking** | MAJOR + RFC |
| Alteração de tipo de campo | **Breaking** | MAJOR + RFC |
| Remoção de evento | **Breaking** | MAJOR + RFC |
| Remoção de estado | **Breaking** | MAJOR + RFC |
| Alteração de comportamento de policy | **Breaking** | MAJOR + RFC |

### 4.2 Garantias

| Garantia | Descrição |
|----------|-----------|
| **STABLE não quebra** | Nenhuma mudança MAJOR em protocolo STABLE sem RFC |
| **12 meses de aviso** | Protocolos DEPRECATED ficam 12 meses antes de RETIRED |
| **Migration guide** | Toda mudança MAJOR inclui guia de migração |
| **Compatibilidade de leitura** | Consumidores conseguem ler versões anteriores |
| **Compatibilidade de escrita** | Produtores conseguem escrever no formato atual |

---

## 5. Processo de Depreciação

### 5.1 Passos

```
1. Proposta de depreciação (RFC)
2. Aprovação do TSC
3. Anúncio público (12 meses de aviso)
4. Protocolo marcado como DEPRECATED
5. Migration guide publicado
6. Após 12 meses: protocolo marcado como RETIRED
7. Implementação de referência atualizada
```

### 5.2 Critérios para Depreciação

| Critério | Descrição |
|----------|-----------|
| Substituição funcional | Novo protocolo cobre todos os casos de uso |
| Complexidade excessiva | Protocolo atual é mais complexo que o necessário |
| Inconsistência arquitetural | Protocolo contradiz a Constituição |
| Baixa adoção | Protocolo não é usado por nenhum componente |

---

## 6. RFC Obrigatória

### 6.1 Quando uma RFC é obrigatória

| Mudança | RFC Obrigatória? |
|---------|------------------|
| Mudança MAJOR em protocolo STABLE | ✅ Sim |
| Mudança MAJOR em protocolo PROPOSED | ✅ Sim |
| Mudança MINOR em protocolo STABLE | ❌ Não (apenas PR review) |
| Mudança PATCH em protocolo STABLE | ❌ Não (apenas PR) |
| Novo protocolo | ✅ Sim |
| Depreciação de protocolo | ✅ Sim |
| Remoção de protocolo | ✅ Sim |

### 6.2 Estrutura da RFC

```
Título: [PROTOCOL] <título descritivo>
Autor: <nome>
Data: <data>
Tipo: Nova funcionalidade | Mudança | Depreciação | Remoção

1. Resumo Executivo
2. Motivação
3. Especificação Técnica
4. Exemplos
5. Compatibilidade
6. Migration Guide (se aplicável)
7. Riscos
8. Decisão (aprovado/rejeitado/pendente)
```

---

## 6. Critérios para Declarar um Protocolo "Stable"

Um protocolo pode ser declarado **STABLE** quando:

| Critério | Descrição | Verificação |
|----------|-----------|-------------|
| **Implementação de referência** | Existe implementação funcional em Python | Código em `src/ascend/` |
| **Testes** | Cobertura >= 90% para o protocolo | `pytest --cov` |
| **Documentação completa** | Todos os campos, eventos, estados documentados | Revisão |
| **Sem objeções** | 2 semanas sem objeções do TSC | Ata de reunião |
| **Consistência** | Não contradiz a Constituição | Revisão arquitetural |
| **Exemplos** | Pelo menos 1 exemplo de uso | Documentação |
| **Casos de borda** | Failure modes documentados | ARCH-0010 seção 8 |

---

## 7. Compliance com a Constituição

| Regra de Governança | Constituição | Alinhamento |
|---------------------|-------------|-------------|
| Estágios DRAFT → STABLE → RETIRED | DOC-0007 (Spec first, code second) | ✅ |
| SemVer para protocolos | DOC-0007 | ✅ |
| RFC obrigatória para breaking changes | DOC-0007 | ✅ |
| 12 meses de aviso para depreciação | DOC-0007 | ✅ |
| Migration guide obrigatório | DOC-0007 | ✅ |
| TSC aprova mudanças MAJOR | GOVERNANCE.md | ✅ |

---

## 7. Declaração Final

> **PROTOCOL_GOVERNANCE define as regras do jogo para a evolução dos protocolos do ASCEND.**
>
> Protocolos são contratos. Contratos não podem ser quebrados sem aviso, sem acordo, sem migração.
>
> A estabilidade dos protocolos é a base para a confiança no ecossistema.
>
> Toda mudança MAJOR exige RFC. Toda depreciação exige aviso. Toda remoção exige migração.
>
> O ASCEND cresce sem quebrar o que já funciona.
