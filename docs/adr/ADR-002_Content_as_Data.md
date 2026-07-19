# ADR-002 — Content as Data

| Campo | Valor |
|-------|-------|
| **ID** | ADR-002 |
| **Título** | Content as Data |
| **Status** | Accepted (Frozen) |
| **Data** | 2026-07-19 |
| **Owner** | Chief Architect |
| **Referências** | SPEC-0001 (APS), ARCH-0001, I4 (Architectural Invariant) |

---

## Contexto

O conteúdo educacional do ASCEND (missões, desafios, avaliações, rubricas) precisa ser armazenado e processado. As abordagens possíveis incluem: conteúdo como código Python executável, conteúdo como banco de dados relacional, ou conteúdo como dados declarativos (YAML/JSON).

## Decisão

Conteúdo é **dado, nunca código**. Pacotes, missões, desafios e avaliações são arquivos YAML. A Engine interpreta — nunca compila ou importa — conteúdo.

### O que isso significa:
- Todo pacote segue o formato APS (SPEC-0001)
- A Engine lê YAML do disco e converte para modelos internos
- Qualquer pessoa pode criar pacotes sem escrever Python
- Pacotes podem ser versionados, assinados e distribuídos independentemente

### O que fica proibido:
- Código Python dentro de pacotes
- Import dinâmico de módulos de pacotes
- Execução de código fornecido pelo pacote

## Consequências

**Positivas:**
- Segurança: pacotes não executam código arbitrário
- Portabilidade: pacotes podem ser escritos em qualquer linguagem
- Versionamento: SemVer aplicável a pacotes
- Comunidade: barreira de entrada reduzida

**Negativas:**
- Complexidade de expressão limitada a YAML
- Necessidade de um parser e validador robustos
- Impossibilidade de lógica condicional complexa nos pacotes

## Status

Esta decisão está **congelada** para a v1. É também o Invariante Arquitetural I4.
