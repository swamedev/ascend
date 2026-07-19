# DOC-0009 — Architectural Invariants

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0009 |
| **Nome** | Architectural Invariants |
| **Versão** | 1.0 |
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

## Violações

Se um Pull Request violar qualquer invariante:

1. Marcar como `blocked: architectural-invariant`
2. Notificar o Chief Architect
3. Não mergear até resolução

## Status

**DOC-0009 — Architectural Invariants**

- Estado: ✅ Approved
- Próximo: Archieve como referência para code review
