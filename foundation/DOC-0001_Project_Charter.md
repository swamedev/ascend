# DOC-0001 — Project Charter

**Status:** Aprovado  
**Versão:** 1.0  
**Data:** 2026-07-19  
**Classificação:** Documento Canônico — Fundação

---

## 1. Mission

Criar um framework de desenvolvimento de competências que transforme a maneira como habilidades são adquiridas, medidas e validadas — substituindo métricas superficiais por evidência demonstrável de maestria.

## 2. Vision

Um mundo onde cada profissional tem um mapa claro de suas competências reais, onde organizações podem confiar nas habilidades declaradas, e onde o aprendizado é uma jornada contínua guiada por dados, não por suposições.

## 3. Problem Statement

### O Problema

O ecossistema atual de desenvolvimento profissional está fundamentalmente quebrado:

- **Certificações sem profundidade:** Diplomas e certificados medem presença e memorização, não competência real.
- **Auto-avaliação enviesada:** O efeito Dunning-Kruger é sistêmico — quem menos sabe, mais confiança tem.
- **Feedback genérico:** Sistemas atuais oferecem "parabéns, você completou o módulo" em vez de análise granular de gaps.
- **Progressão baseada em tempo:** "3 anos de experiência" não indica nível de competência. Indica apenas que o tempo passou.
- **Desconexão com a prática:** A maioria dos sistemas avalia conhecimento teórico, não capacidade de aplicação.

### A Oportunidade

Inteligência Artificial generativa e técnicas avançadas de avaliação adaptativa permitem, pela primeira vez, criar um sistema que:

- Avalia competência em contexto real, não em questões de múltipla escolha.
- Adapta-se ao nível do aprendiz em tempo real.
- Fornece feedback que é simultaneamente diagnóstico e formativo.
- Gera evidência verificável de maestria.

## 4. Scope

### In Scope (Sprint 0 — Fundação)
- Documentação fundacional (North Star, Charter, Manifesto)
- Definição do modelo de competências (taxonomia, níveis, critérios)
- Arquitetura conceitual da Engine de avaliação
- Especificação dos Knowledge Packages (formato, estrutura, versionamento)
- Design do Agent System (avaliador, tutor, gerador de cenários)

### In Scope (Sprints Futuros)
- Implementação da Engine de avaliação adaptativa
- Desenvolvimento dos agentes de IA
- Criação dos primeiros Knowledge Packages (Python, Engenharia de Software)
- Interface do aprendiz (dashboard, progressão, evidências)
- API para integração com sistemas externos

### Out of Scope
- Plataforma de e-commerce ou marketplace de cursos
- Sistema de gestão acadêmica (LMS tradicional)
- Certificação formal / acreditação institucional (fase inicial)
- Gamificação superficial (badges sem substância)

## 5. Stakeholders

| Papel | Descrição |
|-------|-----------|
| **Aprendiz** | Profissional que busca desenvolver e validar competências |
| **Organizações** | Empresas que precisam avaliar e desenvolver talentos |
| **Criadores de Conteúdo** | Especialistas que contribuem com Knowledge Packages |
| **Mantenedores** | Equipe técnica que evolui o framework |

## 6. Success Criteria

| Critério | Métrica | Meta (MVP) |
|----------|---------|------------|
| Precisão da avaliação | Correlação com performance real | > 0.8 |
| Engajamento do aprendiz | Taxa de retorno semanal | > 60% |
| Qualidade do feedback | Acionabilidade (avaliada pelo aprendiz) | > 4.0/5.0 |
| Cobertura de competências | Knowledge Packages disponíveis | ≥ 3 domínios |
| Confiança externa | Organizações que aceitam evidências CDF | ≥ 2 pilotos |

## 7. Constraints

- **Soberania de dados:** Dados do aprendiz pertencem ao aprendiz. Sem venda de dados, sem lock-in.
- **Open Source Core:** O motor principal do CDF será open source. Modelos proprietários podem ser usados como plugins, nunca como dependência central.
- **Hardware-aware:** O sistema deve funcionar em hardware modesto (perfil definido em `.arsenal/hardware_profile.yaml`).
- **Privacidade by Design:** Conformidade com LGPD/GDPR desde a concepção.

## 8. Risks

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Avaliação imprecisa gera desconfiança | Média | Alto | Calibração contínua + validação humana nos estágios iniciais |
| Complexidade técnica subestimada | Alta | Médio | Sprints curtos + MVPs incrementais |
| Escopo creep | Alta | Alto | Charter como contrato + revisão a cada Sprint |
| Dependência de APIs externas de LLM | Média | Alto | Abstração de providers + fallback local |

## 9. Timeline (High-Level)

| Fase | Período | Entregáveis |
|------|---------|-------------|
| **Sprint 0 — Fundação** | Atual | Docs fundacionais, arquitetura conceitual |
| **Sprint 1 — Esqueleto** | +2 semanas | Estrutura de código, primeiros testes |
| **Sprint 2 — Motor** | +4 semanas | Engine de avaliação (v0.1) |
| **Sprint 3 — Agentes** | +6 semanas | Primeiro agente funcional |
| **Sprint 4 — Integração** | +8 semanas | MVP integrado |

---

*Este documento é o contrato social do projeto. Toda decisão arquitetural deve ser rastreável até um princípio aqui declarado.*
