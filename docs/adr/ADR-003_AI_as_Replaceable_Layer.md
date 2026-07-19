# ADR-003 — AI as Replaceable Layer

| Campo | Valor |
|-------|-------|
| **ID** | ADR-003 |
| **Título** | AI as Replaceable Layer |
| **Status** | Accepted |
| **Data** | 2026-07-19 |
| **Owner** | Chief Architect |
| **Referências** | SPEC-0004 (AAP), ARCH-0004, First Principle 3, I5 (Architectural Invariant) |

---

## Contexto

Inteligência artificial pode ser integrada ao ASCEND de diversas formas: como núcleo do sistema, como camada opcional, ou como funcionalidade embutida. A decisão impacta a dependência tecnológica, a resiliência e a filosofia do projeto.

## Decisão

IA é uma **camada substituível**, não o núcleo do sistema. A plataforma deve funcionar **sem IA**. A IA **melhora** a experiência, mas não **sustenta** a operação.

### Regras:
- O domínio e a application layer não dependem de IA
- Agentes de IA se comunicam via protocolo AAP (SPEC-0004)
- Se todos os agentes de IA forem removidos, o sistema continua operacional
- IA pode: orientar, avaliar, explicar, recomendar
- IA **não pode**: alterar regras de validação, modificar estados críticos, decidir aprovações sem supervisão

### Arquitetura:
```
Core Engine
    ▲
    │
AI Interface Layer (AAP Protocol)
    ▲
    │
Model Providers (OpenAI, Anthropic, local, etc.)
```

## Consequências

**Positivas:**
- Sistema resiliente: funciona offline e sem API keys
- Liberdade de escolha de provedor de IA
- Substituível conforme o mercado evolui
- Alinhado com First Principle 3 (IA amplifica humanos)

**Negativas:**
- Integração de IA requer mais camadas de abstração
- Qualidade da experiência reduzida sem IA
- Avaliação automatizada limitada sem modelos de linguagem

## Status

Decisão aceita. O Invariante I5 protege esta decisão.
