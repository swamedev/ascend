# ASCEND PROJECT — Manifest

**ARCHITECTURE_MODE:** foundation  
**PROJECT:** Competency Development Framework (CDF)  
**CREATED:** 2026-07-19  
**LAST_UPDATED:** 2026-07-19T01:43:00-03:00  
**PHASE:** Phase 1 Complete → Ready for Implementation (Sprint 1)
**ARCH-0006_STATUS:** Approved
**DOC-0008_STATUS:** Draft  

---

## Architecture Decision Records (ADR)

### ADR-001: Project Structure — Foundation + Platform Split
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O projeto CDF precisa de uma separação clara entre documentação canônica (princípios, visão, manifesto) e implementação técnica (engine, agentes, pacotes).
- **Decision:** Criar duas pastas raiz: `foundation/` para documentos canônicos e `platform/` para código e infraestrutura técnica.
- **Consequences:** Permite evolução independente de documentação e código. Facilita onboarding — novos contribuidores leem `foundation/` antes de tocar em `platform/`.
- **Hash:** `adr001-foundation-platform-split-20260719`

### ADR-002: Document Naming Convention
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Documentos fundacionais precisam de identificação clara e ordenação lógica.
- **Decision:** Usar formato `DOC-XXXX_Nome_Do_Documento.md` com numeração sequencial de 4 dígitos.
- **Consequences:** Garante ordenação natural no filesystem. Permite referência cruzada por ID.
- **Hash:** `adr002-doc-naming-convention-20260719`

### ADR-003: Governance Toolkit Installation
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O protocolo Ascended exige rastreabilidade via shadow ledger, rotação de manifesto e replay.
- **Decision:** Instalar `tools/` com `manifest_rotator.py`, `shadow_ledger_validator.py` e `replay_manifest.py` desde o Sprint 0.
- **Consequences:** Toda ADR futura será automaticamente validada. Integridade do manifesto é verificável a qualquer momento.
- **Hash:** `adr003-governance-toolkit-20260719`

### ADR-004: Canonical Document Hierarchy
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Os documentos fundacionais precisam de uma hierarquia de derivação clara — cada documento deve saber de onde vem e para onde aponta.
- **Decision:** Estabelecer a cadeia canônica: `DOC-0000 North Star` → `DOC-0002 Manifesto` → `DOC-0003 First Principles` → `DOC-0004 Identity Architecture` → `DOC-0005 Brand Architecture` → `DOC-0006 Lexicon` → `DOC-0007 Engineering Philosophy`. North Star define o PORQUÊ, First Principles define as LEIS, Manifesto define a FILOSOFIA.
- **Consequences:** Toda decisão arquitetural é rastreável até um princípio, que é rastreável até a North Star. Cadeia de custódia filosófica completa.
- **Hash:** `adr004-canonical-doc-hierarchy-20260719`

### ADR-005: First Principles as Constitutional Law
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O ecossistema precisa de leis fundamentais que governem todas as decisões — técnicas, de produto, de design e de estratégia.
- **Decision:** Criar DOC-0003 com exatamente 7 princípios constitucionais: (1) Competência exige evidência, (2) Construção supera consumo, (3) IA amplifica humanos, (4) Autonomia é o objetivo, (5) Complexidade precisa ser justificada, (6) Conhecimento aberto evolui, (7) Verdade técnica supera aparência. Regra: se uma decisão contradiz um First Principle, a decisão está errada — mesmo que tecnicamente possível, comercialmente interessante ou mais rápida.
- **Consequences:** Todo agente, módulo, feature e pacote futuro deve passar pelo teste de alinhamento com os 7 princípios. Poder de veto constitucional.
- **Hash:** `adr005-first-principles-constitutional-20260719`

### ADR-006: Identity Architecture
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O ecossistema precisa de uma definição clara de identidade — quem somos, nossa essência, personalidade, voz, valores e o que nunca seremos.
- **Decision:** Criar DOC-0004 definindo: essência em 5 palavras (Construir, Demonstrar, Evoluir, Compartilhar, Dominar), personalidade como "O Mentor Experiente", arquétipo principal como "The Builder". Declaração: "Nós não criamos pessoas que sabem mais. Criamos pessoas capazes de fazer mais."
- **Consequences:** Toda comunicação, UI e interação de agentes deve refletir esta identidade. O Builder é o centro do ecossistema.
- **Hash:** `adr006-identity-architecture-20260719`

### ADR-007: Brand Architecture
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O projeto precisa de posicionamento claro no mercado e relação definida com os usuários.
- **Decision:** Criar DOC-0005 estabelecendo: nova categoria "Competency Development Ecosystem" (não concorremos com cursos online), promessa central "Transforme conhecimento em competência comprovada", diferencial baseado em "O que você consegue demonstrar?" vs. "Quanto conteúdo consumiu?". Usuário = Builder.
- **Consequences:** Marketing, onboarding e toda comunicação externa seguem este posicionamento.
- **Hash:** `adr007-brand-architecture-20260719`

### ADR-008: Canonical Lexicon
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A linguagem cria cultura. Termos genéricos (curso, aula, aluno, prova) contradizem a identidade e os princípios do ecossistema.
- **Decision:** Criar DOC-0006 como Living Document definindo: termos oficiais (Learning Path, Mission, Challenge, Boss Fight, Evidence, Builder, Mentor Agent, Competency Map, Journey), termos proibidos ("aprenda rápido", "certificado garantido", "sem esforço", etc.) e linguagem padrão.
- **Consequences:** Todo código, UI, documentação e comunicação deve usar exclusivamente o vocabulário canônico.
- **Hash:** `adr008-canonical-lexicon-20260719`

### ADR-009: Engineering Philosophy
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Antes de qualquer linha de código, a filosofia de engenharia precisa estar cristalizada.
- **Decision:** Criar DOC-0007 com 7 princípios de engenharia: (1) Arquitetura antes de código, (2) Simplicidade antes de sofisticação, (3) Modularidade como princípio, (4) Dados separados de comportamento, (5) AI-Native não AI-Dependent, (6) Open Source First, (7) Evidence Driven Development. Arquitetura conceitual em camadas: Foundation → Competency Framework → Engine → (AI + Missions + Evidence).
- **Consequences:** Todo PR, toda decisão técnica e toda arquitetura de sistema deve derivar destes princípios. AI-Dependent é proibido.
- **Hash:** `adr009-engineering-philosophy-20260719`

### ADR-010: Foundation Phase Complete
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Todos os 8 documentos fundacionais foram produzidos e aprovados: North Star, Project Charter, Manifesto, First Principles, Identity Architecture, Brand Architecture, Lexicon, Engineering Philosophy.
- **Decision:** Declarar Foundation v1.0 como completa. Próxima fase: PHASE 1 — SYSTEM ARCHITECTURE com documentos ARCH-0001 a ARCH-0006 (System Architecture Overview, Domain Model, Core Engine Specification, Agent Architecture, Data Model, MVP Technical Specification). Nenhum código será escrito antes da conclusão dos documentos ARCH.
- **Consequences:** A fundação está selada. Alterações nos DOCs fundacionais exigem revisão formal. A fase de arquitetura técnica pode iniciar.
- **Hash:** `adr010-foundation-complete-20260719`

### ADR-011: CLI-First MVP Strategy
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O MVP precisa validar a Engine sem a distração de UI, autenticação, banco de dados web e deploy. O valor inicial está na lógica de competências, não na interface.
- **Decision:** O MVP será CLI-First. Comandos como `ascend init`, `ascend mission start`, `ascend mission submit`, `ascend review`, `ascend progress`. Uma CLI valida a lógica, é rápida de construir, ensina engenharia real, funciona no GitHub e combina com público técnico inicial. Aplicação web será Fase 2.
- **Consequences:** Foco total na Engine e no modelo de domínio. Sem frontend, sem deploy web na Fase 1. Scalability strategy: CLI → Web → Ecossistema.
- **Hash:** `adr011-cli-first-mvp-20260719`

### ADR-012: Four Core Architectural Principles
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A arquitetura do sistema precisa de princípios técnicos claros que traduzam os First Principles (DOC-0003) em decisões de engenharia.
- **Decision:** Estabelecer 4 princípios arquiteturais core: (1) **Engine First** — Engine é o núcleo, agnosética a domínio; (2) **Content as Data** — conteúdo como pacotes independentes, Engine apenas interpreta; (3) **AI as Layer** — IA é camada substituível, não dependência central; (4) **Evidence Driven** — evidência é a unidade mais importante, não o conteúdo.
- **Consequences:** Toda decisão de design deve aderir a estes 4 princípios. Violação exige revisão formal.
- **Hash:** `adr012-four-core-arch-principles-20260719`

### ADR-013: ARCH-0001 System Architecture Overview
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Primeiro documento arquitetural do sistema, definindo visão macro, componentes, data flow, extensões, segurança e escalabilidade.
- **Decision:** Aprovar ARCH-0001 com: 6 componentes maiores (Core Engine, Mission System, Evidence System, Progress System, Agent Layer, Package System), 4 princípios core, 3 fases de escalabilidade, modelo de extensão em 4 dimensões e technology independence.
- **Consequences:** Todos os documentos ARCH subsequentes derivam desta visão. Alterações no ARCH-0001 exigem cascata de revisão.
- **Hash:** `adr013-arch0001-approved-20260719`

### ADR-014: Architecture Directory Structure
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Documentos de arquitetura técnica precisam de um diretório separado da fundação filosófica.
- **Decision:** Criar `architecture/` como diretório de documentos ARCH-*, separado de `foundation/` (DOCs filosóficos) e `platform/` (código futuro).
- **Consequences:** Estrutura clara: `foundation/` = porquê, `architecture/` = como (design), `platform/` = como (código).
- **Hash:** `adr014-architecture-directory-20260719`

### ADR-015: ARCH-0002 Domain Model Design
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O Competency Development Framework (CDF) necessita de uma modelagem de domínio unificada baseada em Domain-Driven Design (DDD) para estruturar a lógica da Engine.
- **Decision:** Aprovar ARCH-0002 dividindo o domínio em três Bounded Contexts (Competency, Journey e Execution Domains), identificando os Aggregates fundamentais (Competency Registry, Learning Journey, Builder Profile) e suas respectivas entidades/Value Objects, Domain Events e Domain Invariants.
- **Consequences:** Garante consistência em toda a implementação técnica, mapeamento de termos do Lexicon para código e rastreabilidade total de evidências e avaliações.
- **Hash:** `adr015-arch0002-domain-model-20260719`

### ADR-016: ARCH-0003 Core Engine Specification
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** É necessária uma especificação rigorosa da Core Engine para detalhar o funcionamento lógico das transições de aprendizado.
- **Decision:** Aprovar ARCH-0003 definindo a especificação dos 5 subsistemas fundamentais da Engine: Mission Engine (ciclo de vida das missões), Evidence Engine (validação estrutural de artefatos), Evaluation Engine (orquestração e timeouts de avaliações), Progress Engine (cálculo de nível e XP), e Portfolio Engine (assinaturas criptográficas e livro-razão imutável de evidências).
- **Consequences:** Estabelece o comportamento comportamental que o código do MVP deverá implementar estritamente, sem acoplamento a infraestrutura externa.
- **Hash:** `adr016-arch0003-core-engine-spec-20260719`

### ADR-017: ARCH-0004 Agent Architecture Design
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A integração de inteligência artificial deve seguir a orientação de não-dependência de fornecedores de modelos específicos e alinhamento aos princípios éticos do CDF.
- **Decision:** Aprovar ARCH-0004 especificando a Agent Architecture composta por 3 agentes focados (Mentor, Reviewer e Interviewer Agents), delimitando seus prompts de sistema, escopo de ferramentas, limites operacionais, mecanismos de memória e testes automáticos de conformidade (evitando geração direta de respostas).
- **Consequences:** Define as regras de comportamento dos agentes cognitivos do ecossistema, garantindo que o Builder mantenha o controle e protagonismo de seu próprio aprendizado.
- **Hash:** `adr017-arch0004-agent-architecture-20260719`

### ADR-018: ARCH-0005 Data Model Design
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** A persistência de dados do CDF no MVP CLI-First deve ser eficiente, local e estruturada sem a complexidade de bancos de dados em nuvem.
- **Decision:** Aprovar ARCH-0005 definindo o armazenamento em disco usando arquivos JSON estruturados organizados na pasta local `.ascend/` do workspace, contendo esquemas JSON robustos para o perfil do Builder (`profile.json`) e livro-razão de evidências (`portfolio.json`), além de implementar um fluxo de transações atômicas de escrita contra arquivos temporários.
- **Consequences:** Garante simplicidade técnica para o MVP, isolamento absoluto dos dados (Local First) e mitigação contra corrupção de dados decorrente de falhas no CLI.
- **Hash:** `adr018-arch0005-data-model-20260719`

### ADR-019: ARCH-0006 MVP Technical Specification
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** O desenvolvimento inicial do MVP requer uma stack tecnológica definida, uma estrutura modular de diretórios clara em `platform/` e comandos CLI mapeados de ponta a ponta.
- **Decision:** Aprovar ARCH-0006 adotando Python 3.10+, utilizando o pacote nativo `argparse` para a CLI para evitar dependências excessivas, definindo o leiaute exato de diretórios sob `platform/`, mapeando os comandos fundamentais (`init`, `status`, `mission start`, `mission submit`, `review`) e definindo a Definition of Done (DoD).
- **Consequences:** Provê as especificações concretas de engenharia para que o código comece a ser implementado de maneira limpa, testável e sem complexidades artificiais.
- **Hash:** `adr019-arch0006-mvp-tech-spec-20260719`

### ADR-020: System Architecture Phase Complete
- **Date:** 2026-07-19
- **Status:** Accepted
- **Context:** Todos os 6 documentos arquiteturais da Phase 1 foram criados, revisados e aprovados: ARCH-0001 (Overview), ARCH-0002 (Domain Model), ARCH-0003 (Core Engine Spec), ARCH-0004 (Agent Architecture), ARCH-0005 (Data Model) e ARCH-0006 (MVP Tech Spec).
- **Decision:** Selar a Phase 1 como concluída e habilitar o início do desenvolvimento de código do MVP (Sprint 1). A governança do projeto exige a verificação imediata da integridade do Shadow Ledger.
- **Consequences:** Bloqueia a edição direta dos blueprints da arquitetura sem nova submissão de ADRs e autoriza o início da codificação do ecossistema.
- **Hash:** `adr020-system-architecture-complete-20260719`

---

## Changelog

| Data | ADR | Ação |
|------|-----|------|
| 2026-07-19 | ADR-001 | Criação — Foundation + Platform split |
| 2026-07-19 | ADR-002 | Criação — Document naming convention |
| 2026-07-19 | ADR-003 | Criação — Governance toolkit |
| 2026-07-19 | ADR-004 | Criação — Canonical document hierarchy |
| 2026-07-19 | ADR-005 | Criação — First Principles como lei constitucional |
| 2026-07-19 | ADR-006 | Criação — Identity Architecture |
| 2026-07-19 | ADR-007 | Criação — Brand Architecture |
| 2026-07-19 | ADR-008 | Criação — Canonical Lexicon (Living Document) |
| 2026-07-19 | ADR-009 | Criação — Engineering Philosophy |
| 2026-07-19 | ADR-010 | **MILESTONE** — Foundation Phase v1.0 Complete |
| 2026-07-19 | ADR-011 | Criação — CLI-First MVP Strategy |
| 2026-07-19 | ADR-012 | Criação — Four Core Architectural Principles |
| 2026-07-19 | ADR-013 | Criação — ARCH-0001 System Architecture Overview |
| 2026-07-19 | ADR-014 | Criação — Architecture directory structure |
| 2026-07-19 | ADR-015 | Criação — ARCH-0002 Domain Model |
| 2026-07-19 | ADR-016 | Criação — ARCH-0003 Core Engine Specification |
| 2026-07-19 | ADR-017 | Criação — ARCH-0004 Agent Architecture |
| 2026-07-19 | ADR-018 | Criação — ARCH-0005 Data Model |
| 2026-07-19 | ADR-019 | Criação — ARCH-0006 MVP Technical Specification |
| 2026-07-19 | ADR-020 | **MILESTONE** — System Architecture Phase Complete |
| 2026-07-19 | ADR-021 | Criação — DOC-0008 Project Continuity Protocol |
| 2026-07-19 | ADR-022 | Criação — ARCH-0005 Data Model Specification (Revisão detalhada) |
| 2026-07-19 | ADR-023 | Criação — ARCH-0006 MVP Technical Specification (Revisão detalhada) |
| 2026-07-19 | ADR-024 | Criação — BUILD-0001 Implementation Roadmap |
| 2026-07-19 | ADR-025 | Criação — AGENT-0001 DeepSeek Implementation Profile |
| 2026-07-19 | ADR-026 | Criação — Python Version Support (>=3.11) |





