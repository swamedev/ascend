# ASCEND Quality Standard v1.0

> Padrões de qualidade para código, testes, documentação e arquitetura.

---

## 1. Code Quality

### 1.1 Python Standards

| Regra | Padrão | Exceções |
|-------|--------|----------|
| Python version | >= 3.11 | N/A |
| Type hints | Obrigatório em todas as funções/métodos públicos | Testes, scripts temporários |
| Dataclasses | Preferir sobre classes manuais | Quando comportamento complexo é necessário |
| Protocols | Usar `Protocol` para interfaces (não ABC) | Quando herança de implementação é necessária |
| NewTypes | Usar para IDs de domínio (BuilderId, MissionId, etc.) | N/A |
| Result pattern | Usar `Result[T, E]` para operações que podem falhar | Quando exceção é mais semântica (BuilderNotFound) |

### 1.2 Naming Conventions

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Classes | PascalCase | `RuntimeKernel`, `AssessmentPipeline` |
| Funções/métodos | snake_case | `start_mission()`, `submit_evidence()` |
| Constantes | UPPER_SNAKE_CASE | `_BASELINE_SCORE`, `MAX_XP_PER_MISSION` |
| Arquivos | snake_case.py | `mission_runner.py`, `competency_engine.py` |
| IDs (domínio) | kebab-case | `html-foundations`, `comp-linux-admin` |
| IDs (código) | prefixo + hash | `ev-abc123`, `ach-linux-builder` |
| Pacotes | kebab-case | `linux-foundations`, `git-foundations` |

### 1.3 Module Structure

```
module/
├── __init__.py    # Public API exports
├── core.py        # Lógica principal
├── models.py      # Modelos de dados (dataclasses)
├── service.py     # Casos de uso (application layer)
└── runner.py      # Orquestração (runtime layer)
```

### 1.4 Proibições

- ❌ `import *` — exceto em `__init__.py` com `__all__` definido
- ❌ Módulos com mais de 500 linhas
- ❌ Funções com mais de 80 linhas (sem justificativa documentada)
- ❌ Globals mutáveis — usar `RuntimeContext` ou injeção de dependências
- ❌ Exceções para controle de fluxo — usar `Result` pattern ou `ExecutionReport.errors`
- ❌ Strings mágicas — definir como constantes nomeadas
- ❌ Dependency cycle entre módulos do mesmo pacote

---

## 2. Testing Standards

### 2.1 Coverage Requirements

| Camada | Cobertura Mínima |
|--------|------------------|
| Domain | 95% |
| Application | 90% |
| Runtime | 85% |
| Infrastructure | 85% |
| Package Engine | 90% |
| API | 85% |
| CLI | 70% (testado via subprocess) |
| **Geral** | **85%** |

### 2.2 Test Structure

```
tests/
├── test_domain.py           # Testes de domínio (unitários)
├── test_application.py      # Testes de application layer (com in-memory repos)
├── test_runtime.py          # Testes de runtime (kernel, runners, assessment)
├── test_infrastructure.py   # Testes de infra (SQLite, event bus, UoW)
├── test_package_engine.py   # Testes de package engine (parser, validator, loader)
├── test_api.py              # Testes de API facade + CLI (subprocess)
└── test_bootstrap.py        # Teste de bootstrap/import
```

### 2.3 Test Naming

```
class Test<ComponentName>:
    def test_<scenario>_<expected_behavior>:
```

### 2.4 Test Patterns

| Padrão | Quando usar |
|--------|-------------|
| InMemoryRepository | Testes de application layer |
| `:memory:` SQLite | Testes de infrastructure |
| FakeClock | Testes que dependem de tempo |
| Fixtures com escopo `function` | Estado isolado por teste |
| Subprocess | Testes de CLI |

### 2.5 Regras Obrigatórias

- ✅ Toda entidade de domínio deve ter teste de criação e estado inicial
- ✅ Toda transição de state machine deve ser testada (válida e inválida)
- ✅ Toda exceção de domínio deve ser testada
- ✅ Toda interface (Protocol) deve ter pelo menos uma implementação testada
- ✅ Toda regra de validação do PackageValidator deve ter teste positivo e negativo
- ✅ Testes não podem depender de rede, arquivos externos ou variáveis de ambiente

---

## 3. Documentation Standards

### 3.1 Document Hierarchy

```
foundation/     → Princípios imutáveis (North Star, First Principles, etc.)
architecture/  → Decisões arquiteturais (ARCH docs)
docs/spec/     → Especificações formais (APS, AEP, ARP, AAP)
docs/adr/      → Architecture Decision Records
docs/build/    → Planos de implementação
```

### 3.2 Docstring Standards

```python
def function_name(param: str) -> bool:
    """Descrição curta do que a função faz.
    
    Args:
        param: Descrição do parâmetro.
    
    Returns:
        Descrição do retorno.
    
    Raises:
        ValueError: Quando ocorre X.
    """
```

### 3.3 README Standards

Todo pacote de conteúdo (packages/) deve ter:
- `package.yaml` com metadados completos
- `README.md` com descrição em linguagem natural
- Competências, missões e rubricas documentadas

### 3.4 ADR Standards

Todo ADR deve conter:
- Contexto (problema/oportunidade)
- Decisão (o que foi decidido)
- Consequências (positivas e negativas)
- Status (Proposed, Accepted, Deprecated, Superseded)

---

## 4. Architecture Standards

### 4.1 Layer Rules

```
CLI / API
    ↓
Application (Services, Commands, DTOs)
    ↓
Domain (Entities, Events, Value Objects)
    ↓
Infrastructure (SQLite, EventBus, UoW)
```

- Domain NUNCA importa Infrastructure
- Application conhece apenas Protocols (não implementações concretas)
- Runtime pode importar Domain (para execução)
- API pode importar Runtime e Domain (facade pública)

### 4.2 Invariants Checklist (Code Review)

| Invariant | Verificar |
|-----------|-----------|
| I1 | Domain imports apenas domain e shared |
| I2 | UnlockCompetency valida evidência |
| I3 | Toda mutação de estado gera DomainEvent |
| I4 | Packages são YAML, nunca Python |
| I5 | IA nunca modifica regras de negócio |
| I6 | Domain e Application operam offline |
| I7 | Toda funcionalidade testável via CLI |
| I8 | Sem telemetria obrigatória |
| I9 | Camadas comunicam-se apenas para dentro |
| I10 | Application usa Protocols, Infrastructure implementa |

### 4.3 Revisão de Código

| Critério | Obrigatório | Recomendado |
|----------|-------------|--------------|
| Testes acompanham código | ✅ | — |
| Invariantes respeitados | ✅ | — |
| Type hints completos | ✅ | — |
| Docstrings em métodos públicos | — | ✅ |
| Nomenclatura consistente | ✅ | — |
| Sem dead code | ✅ | — |
| Cobertura >= 85% | ✅ | — |

---

## 5. Dependency Standards

### 5.1 Dependências de Produção

| Dependência | Versão Mínima | Justificativa |
|-------------|---------------|---------------|
| Python | >= 3.11 | Type hints, dataclasses, pattern matching |
| PyYAML | >= 6.0 | Parsing de pacotes APS |

### 5.2 Dependências de Desenvolvimento

| Dependência | Versão Mínima | Justificativa |
|-------------|---------------|---------------|
| pytest | >= 7.0 | Framework de testes |
| pytest-cov | >= 4.0 | Cobertura de código |

### 5.3 Non-Dependencies

As seguintes tecnologias NÃO devem ser adicionadas sem aprovação do Chief Architect:
- Frameworks web (Django, Flask, FastAPI) — fase 2
- ORMs (SQLAlchemy) — SQLite direto é suficiente
- Async frameworks — kernel é síncrono por definição (AEP)
- Tipagem externa (mypy, pyright) — opcional por enquanto

---

## 6. Versioning

| Artefato | Esquema | Exemplo |
|----------|---------|---------|
| ASCEND Runtime | SemVer | 0.1.0 → 0.2.0 → 1.0.0 |
| APS packages | SemVer | 1.0.0 → 1.1.0 → 2.0.0 |
| Documentos fundacionais | Versão manual | 1.0 → 1.1 → 2.0 |
| ADRs | Sequencial | ADR-001, ADR-002 |
| Specs | SemVer | 1.0.0, 1.1.0 |

---

## 7. Commit Standards

```
<type>(<scope>): <description>

tipos: feat, fix, refactor, test, docs, chore
scope: domain, runtime, app, infra, pkg, cli, docs
```

Exemplos:
- `feat(domain): add Mission state machine`
- `test(runtime): add kernel integration tests`
- `docs(adr): add ADR-001 Engine-First Architecture`

---

## 8. Enforcement

| Padrão | Como verificar | Ferramenta |
|--------|----------------|------------|
| Cobertura | `pytest --cov=src/ascend --cov-fail-under=85` | pytest-cov |
| Testes | `pytest tests/ -q` | pytest |
| Invariantes | Code review + checklist | Manual |
| Naming | Code review | Manual |
| Docstrings | Code review | Manual |
| Architecture | `ascend doctor` (métricas automatizadas) | built-in |

---

*Documento gerado em 2026-07-19. v1.0.*
*Revisão: quando houver mudança nos padrões acordados pelo time.*
