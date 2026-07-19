# PROTOCOL-0005 — Capability Protocol

| Campo | Valor |
|-------|-------|
| **ID** | PROTOCOL-0005 |
| **Nome** | Capability Protocol |
| **Versão** | 1.0 |
| **Status** | Stable |
| **Categoria** | Protocol |
| **Owner** | Chief Architect |
| **Derivado de** | Constituição, ARCH-0001, ARCH-0006, SPEC-0001 (APS), SPEC-0004 (AAP) |
| **Linguagem** | Independente |

---

## 1. Propósito

Este protocolo define o **sistema de capabilities** do ASCEND.

Capabilities são características declarativas que um componente (Runtime, Package, Agent) possui. Elas permitem descoberta, negociação, compatibilidade e fallback entre componentes.

---

## 2. Capabilities

### 2.1 Definição

Uma **Capability** é uma capacidade declarativa que um componente possui.

```
Capability = (name: string, version: string, parameters: dict)
```

### 2.2 Catálogo de Capabilities

| Capability | Descrição | Valores Possíveis |
|------------|-----------|-------------------|
| `persistence` | Suporte a persistência de dados | `true`, `false` |
| `event_store` | Suporte a event store | `true`, `false` |
| `ai_runtime` | Suporte a agentes de IA | `true`, `false` |
| `plugin_sdk` | Suporte a plugins | `true`, `false` |
| `evidence` | Suporte a evidência | `true`, `false` |
| `ai` | Suporte a agentes de IA | `true`, `false` |
| `plugin` | Suporte a plugins | `true`, `false` |
| `async` | Suporte a execução assíncrona | `true`, `false` |
| `network` | Suporte a operações de rede | `true`, `false` |
| `sync` | Suporte a sincronização remota | `true`, `false` |
| `offline` | Suporte a operação offline | `true`, `false` |
| `multi_builder` | Suporte a múltiplos builders | `true`, `false` |
| `multi_package` | Suporte a múltiplos pacotes simultâneos | `true`, `false` |
| `custom_hooks` | Suporte a hooks personalizados | `true`, `false` |
| `custom_policies` | Suporte a políticas personalizadas | `true`, `false` |
| `audit_trail` | Suporte a audit trail completo | `true`, `false` |
| `encryption` | Suporte a criptografia de dados | `true`, `false` |
| `signing` | Suporte a assinatura de pacotes | `true`, `false` |

### 2.3 Declaração de Capabilities

**Em Packages (APS):**
```yaml
metadata:
  id: pkg:cyber-foundations
  version: 1.0.0
capabilities:
  - evidence: true
  - ai: false
  - plugin: false
  - async: false
```

**Em Runtime (Settings):**
```python
@dataclass
class Settings:
    db_path: str = ":memory:"
    debug: bool = False
    capabilities: dict = {
        "persistence": True,
        "event_store": True,
        "ai_runtime": False,
        "plugin_sdk": False,
    }
```

**Em Agent (AAP):**
```yaml
agent:
  id: agent:reviewer-v1
  capabilities:
    - assessment: true
    - feedback: true
    - scoring: true
    - language: pt-BR
```

---

## 3. Negotiation

### 3.1 O que é Negotiation

Negotiation é o processo pelo qual o Runtime determina se um componente (Package, Agent) é compatível com suas capabilities.

### 3.2 Fluxo de Negotiation

```
1. Runtime declara suas capabilities (Settings.capabilities)
2. Package declara suas capabilities (package.yaml)
3. Runtime compara:
     a. Package requer capability que Runtime não tem? → WARNING ou BLOCK
     b. Runtime tem capability que Package não requer? → OK (sobra)
     c. Ambos têm a capability? → OK
4. Resultado da negotiation:
     a. COMPATIBLE → prossegue
     b. INCOMPATIBLE → bloqueia com diagnóstico
     c. PARTIAL → prossegue com warnings
```

### 3.2 Regras de Negotiation

| Runtime | Package | Resultado |
|---------|---------|-----------|
| Tem a capability | Requer a capability | ✅ COMPATIBLE |
| Tem a capability | Não requer | ✅ COMPATIBLE (sobra) |
| Não tem | Requer | ❌ INCOMPATIBLE |
| Não tem | Não requer | ✅ COMPATIBLE |

### 3.3 Exemplo de Negotiation

```python
def negotiate(runtime_caps: dict, package_caps: dict) -> NegotiationResult:
    missing = []
    warnings = []
    
    for cap, required in package_caps.items():
        if required and not runtime_caps.get(cap, False):
            missing.append(cap)
        elif required and runtime_caps.get(cap, False):
            pass  # OK
        elif not required:
            pass  # OK, sobra
    
    if missing:
        return NegotiationResult(
            status="INCOMPATIBLE",
            missing_capabilities=missing,
            message=f"Runtime não suporta: {', '.join(missing)}"
        )
    
    return NegotiationResult(
        status="COMPATIBLE",
        missing_capabilities=[],
        message="Runtime e Package são compatíveis"
    )
```

---

## 4. Discovery

### 4.1 O que é Discovery

Discovery é o processo pelo qual um componente descobre as capabilities de outro componente.

### 4.2 Discovery Methods

| Método | Descrição | Quando usar |
|--------|-----------|-------------|
| **Static Declaration** | Capabilities declaradas em YAML/JSON | Packages, Agents |
| **Runtime Inspection** | Runtime expõe capabilities via API | Runtime Settings |
| **Protocol Negotiation** | Componentes trocam capabilities em tempo de execução | Agent ↔ Runtime |

### 4.3 Discovery Flow

```
1. Runtime inicia
2. Runtime lê Settings.capabilities
3. Runtime carrega Package
4. Runtime lê Package.capabilities
5. Runtime compara (Negotiation)
6. Se COMPATIBLE → executa
7. Se INCOMPATIBLE → reporta erro
```

---

## 5. Compatibility

### 5.1 Matriz de Compatibilidade

| Capability | Runtime v1.0 | Runtime v1.1 | Runtime v2.0 |
|------------|-------------|-------------|-------------|
| `persistence` | ✅ | ✅ | ✅ |
| `event_store` | ✅ | ✅ | ✅ |
| `ai_runtime` | ❌ | ✅ | ✅ |
| `plugin_sdk` | ❌ | ❌ | ✅ |
| `evidence` | ✅ | ✅ | ✅ |
| `async` | ❌ | ❌ | ✅ |
| `network` | ❌ | ❌ | ✅ |
| `offline` | ✅ | ✅ | ✅ |

### 5.2 Regras de Compatibilidade

| Regra | Descrição |
|-------|-----------|
| C1 | Runtime deve suportar todas as capabilities que o Package REQUER |
| C2 | Runtime pode ter capabilities que o Package não requer (sobra) |
| C3 | Se Runtime não suporta capability requerida → INCOMPATIBLE |
| C4 | Se capability tem versão, a versão do Runtime deve ser >= versão requerida |
| C5 | Capabilities não declaradas são consideradas `false` |

---

## 6. Fallback

### 6.1 O que é Fallback

Fallback é o comportamento quando uma capability requerida não está disponível.

### 6.2 Estratégias de Fallback

| Estratégia | Descrição | Exemplo |
|------------|-----------|---------|
| **Skip** | Ignora a funcionalidade que requer a capability | Package com `ai: true` → Runtime sem IA → pula avaliação por IA |
| **Degrade** | Usa implementação alternativa | Package com `async: true` → Runtime síncrono → executa sequencial |
| **Warn** | Avisa o usuário e continua | Package com `plugin: true` → Runtime sem plugin → warning |
| **Block** | Bloqueia a execução | Package com `encryption: true` → Runtime sem → bloqueia |

### 6.3 Regras de Fallback

| Capability Requerida | Runtime Tem? | Fallback |
|---------------------|--------------|----------|
| `ai` | Não | Degrade: usa AssessmentPipeline built-in |
| `plugin` | Não | Warn: plugins não serão executados |
| `async` | Não | Degrade: execução síncrona |
| `network` | Não | Block: se package requer rede |
| `encryption` | Não | Block: se package requer criptografia |
| `evidence` | Sim | OK |
| `persistence` | Sim | OK |

---

## 6. Versionamento

### 6.1 Versionamento de Capabilities

Capabilities seguem SemVer:

| Versão | Mudança | Exemplo |
|--------|---------|---------|
| MAJOR | Capability removida ou comportamento incompatível | `ai_runtime` v1 → v2 (API diferente) |
| MINOR | Nova capability adicionada | `plugin_sdk` adicionada |
| PATCH | Correção sem mudança de comportamento | Documentação, bug fix |

### 6.2 Declaração de Versão

```yaml
capabilities:
  evidence: { version: "1.0.0", required: true }
  ai: { version: "2.0.0", required: false }
  plugin: { version: "1.0.0", required: false }
```

### 6.3 Regras de Versionamento

| Regra | Descrição |
|-------|-----------|
| V1 | Runtime com versão MAJOR N aceita capabilities MAJOR N |
| V2 | Runtime com versão MAJOR N rejeita capabilities MAJOR N+1 |
| V3 | Runtime com versão MAJOR N aceita capabilities MINOR/PATCH superiores |
| V4 | Capability não versionada = MAJOR 1 |

---

## 7. Compliance com a Constituição

| Elemento | Constituição | ARCH | SPEC |
|----------|-------------|------|------|
| Capabilities | — | ARCH-0006 | SPEC-0001 (APS) |
| Negotiation | — | ARCH-0001 | — |
| Discovery | — | ARCH-0001 | — |
| Compatibility | — | ARCH-0006 | — |
| Fallback | P3 (IA substituível) | ARCH-0004 | SPEC-0004 (AAP) |
| Versionamento | — | — | SPEC-0001 |

---

## 8. Declaração Final

> **PROTOCOL-0005 define como os componentes do ASCEND descobrem, negociam e verificam compatibilidade.**
>
> Capabilities permitem que o Runtime, Packages e Agents declarem o que sabem fazer.
>
> Negotiation garante que componentes incompatíveis nunca interajam.
>
> Fallback garante que o sistema degrade graciosamente quando capabilities estão ausentes.
>
> Versionamento garante que a evolução das capabilities não quebre o ecossistema.
