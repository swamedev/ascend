# ADR-004 — Local-First with SQLite

| Campo | Valor |
|-------|-------|
| **ID** | ADR-004 |
| **Título** | Local-First with SQLite |
| **Status** | Accepted |
| **Data** | 2026-07-19 |
| **Owner** | Chief Architect |
| **Referências** | ARCH-0006, I6, I8 (Architectural Invariants) |

---

## Contexto

O ASCEND precisa armazenar estado do sistema (builders, missões, evidências, eventos). As opções incluem: banco de dados remoto (PostgreSQL, MySQL), banco local incorporado (SQLite), ou armazenamento em arquivo (JSON, YAML).

## Decisão

O ASCEND adota **arquitetura local-first** com **SQLite** como mecanismo de persistência primário.

### O que isso significa:
- Banco de dados SQLite embutido no processo Python
- Suporte a `:memory:` para testes e `:file:` para produção
- Dados pertencem ao usuário — sem sincronização obrigatória
- Sem telemetria obrigatória
- Sem lock-in de nuvem

### Camada de abstração:
```
Application (Protocols)
    ▲
    │
SQLiteRepository (implements Protocol)
    ▲
    │
ConnectionManager (thread-safe)
```

### Tabelas:
builders, competencies, builder_competencies, missions, builder_missions, evidence, assessments, achievements, builder_achievements, events, journeys, schema_version

## Consequências

**Positivas:**
- Zero configuração para o usuário final
- Portabilidade: único arquivo .db
- Testes com `:memory:` são rápidos e isolados
- Invariante I6 (offline) e I8 (dados do usuário) respeitados
- Migrações versionadas via MigrationEngine

**Negativas:**
- Sem concorrência multi-processo
- Escalabilidade limitada para cenários enterprise
- Futura sincronização com cloud exigirá adaptação

## Status

Decisão aceita para v1. A camada de protocolos (I10) permite substituir SQLite por PostgreSQL no futuro sem alterar application/domain.
