# ADR-001 — Engine-First Architecture

| Campo | Valor |
|-------|-------|
| **ID** | ADR-001 |
| **Título** | Engine-First Architecture |
| **Status** | Accepted (Frozen) |
| **Data** | 2026-07-19 |
| **Owner** | Chief Architect |
| **Referências** | ARCH-0001, ARCH-0003, DOC-0007 |

---

## Contexto

O ASCEND precisa definir como o núcleo do sistema se relaciona com o conteúdo que ele processa. Existem duas abordagens possíveis: construir um motor genérico que interpreta conteúdo, ou construir motores especializados para cada domínio de conhecimento (cyber, programação, cloud, etc.).

## Decisão

A Engine será **agnóstica a domínio**. Ela não sabe o que está executando — apenas como executar.

### O que a Engine sabe fazer:
- Gerenciar competências
- Executar missões
- Validar evidências
- Acompanhar evolução
- Orquestrar agentes

### O que a Engine NÃO sabe:
- Ensinar Cyber
- Ensinar Programação
- Ensinar Cloud
- Conhecer domínios específicos

## Consequências

**Positivas:**
- A Engine pode ser reutilizada para qualquer domínio de conhecimento
- A separação permite que comunidade crie pacotes sem modificar o núcleo
- A Engine permanece estável enquanto os pacotes evoluem
- Testes da Engine são independentes de conteúdo

**Negativas:**
- A Engine precisa de um formato de pacote bem definido (APS)
- Não é possível otimizar a Engine para domínios específicos
- Pacotes precisam ser autossuficientes em termos de regras e critérios

## Status

Esta decisão está **congelada** para a v1. Qualquer proposta de mudança requer aprovação do TSC.
