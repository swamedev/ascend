# ARCH-0007 — Persistence Architecture

| Campo | Valor |
|-------|-------|
| **ID** | ARCH-0007 |
| **Nome** | Persistence Architecture |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | ARCH-0005 Data Model, DOC-0009 Architectural Invariants |

## 1. Philosophy

A infraestrutura de persistência segue três princípios:

1. **Repository Pattern** — Application nunca fala com SQL
2. **Unit of Work** — Cada caso de uso é uma transação
3. **Event Store** — Eventos são imutáveis e auditáveis

## 2. Layered Repository Design

```
Application (Use Case)
    │
    ▼
Repository Protocol (Interface)
    │
    ▼
Repository Base (Abstração concreta)
    │
    ▼
SQLiteRepository (Implementação)
```

A pirâmide de construção será:

```
1. Connection Manager
2. Repository Base
3. Unit of Work
4. BuilderRepository
5. MissionRepository
6. EvidenceRepository
7. Event Store
```

## 3. Connection Manager

Responsabilidade única: gerenciar a conexão SQLite.

```python
class ConnectionManager:
    def get_connection() -> sqlite3.Connection
    def close() -> None
```

- Singleton por aplicação
- Suporta `:memory:` para testes
- Suporta `foreign_keys = ON`

## 4. Repository Base

Classe base que todo repositório SQLite estende.

```python
class SQLiteRepository:
    conn: ConnectionManager
    table_name: str
    schema: dict
```

Fornece:
- `_execute(query, params)`
- `_fetch_one(query, params)`
- `_fetch_all(query, params)`

## 5. Unit of Work

Gerencia transações.

```python
class UnitOfWork:
    def begin()
    def commit()
    def rollback()
```

Cada Use Case na Application Layer cria um escopo transacional:

```python
with uow:
    builder_repo.save(builder)
    mission_repo.save(mission)
    uow.commit()
```

## 6. Event Store

Tabela separada para eventos — nunca misturada com entidades.

```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    aggregate_id TEXT NOT NULL,
    aggregate_type TEXT NOT NULL,
    event_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

Funcionalidades:
- Auditoria completa
- Replay de eventos
- Debugging
- Analytics

## 7. Schema Versioning

O schema do banco será versionado com migration scripts.

```sql
CREATE TABLE schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL,
    description TEXT
);
```

Migrações são arquivos numerados:

```
migrations/
    001_create_builders.sql
    002_create_missions.sql
    003_create_events.sql
```

## 8. Transaction Boundary

Cada Use Case no Application Ring representa uma transação.

```
BEGIN TRANSACTION
    load aggregate
    validate
    execute domain logic
    save aggregate
    insert events
COMMIT
```

Se algo falha → ROLLBACK.
Nenhum estado inconsistentes persiste.

## 9. Test Strategy

Para基础设施:

| Teste | O que valida |
|-------|-------------|
| Repository test | save + get + list |
| Unit of Work test | commit persiste, rollback desfaz |
| Event Store test | insert + replay |
| Integration test | Builder completo (criar → persistir → carregar) |

Usar `:memory:` SQLite para testes — zero configuração.

## 10. MVP Database

Primeira versão terá apenas:

| Tabela | Finalidade |
|--------|-----------|
| `builders` | Perfis dos aprendizes |
| `competencies` | Competências do sistema |
| `builder_competencies` | Progresso de cada Builder |
| `missions` | Missões disponíveis |
| `evidence` | Evidências submetidas |
| `assessments` | Avaliações |
| `achievements` | Conquistas |
| `builder_achievements` | Conquistas obtidas |
| `events` | Event Store |

## 11. Dependencies

A infraestrutura DEPENDE de:
- `ascend.domain` — entidades
- `ascend.application.interfaces` — protocolos

A infraestrutura NÃO DEPENDE de:
- `ascend.application.services` — casos de uso
- Nenhum framework web
- Nenhuma biblioteca de IA

## Definition of Done

ARCH-0007 implementado quando:

- [x] Connection Manager criado
- [x] Repository Base criado
- [x] Unit of Work criado
- [x] Repositórios SQLite implementados
- [x] Event Store implementado
- [x] Testes de integração passando
- [x] `ascend.domain` intacto (zero alterações)

## Status

**ARCH-0007 — Persistence Architecture**

- Estado: ✅ Approved
- Próximo: Implementação no Sprint 003 — Infrastructure Foundation
