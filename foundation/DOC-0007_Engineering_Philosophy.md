# DOC-0007 — Engineering Philosophy

| Campo | Valor |
|-------|-------|
| **ID** | DOC-0007 |
| **Nome** | Engineering Philosophy |
| **Versão** | 1.0 |
| **Status** | Approved |
| **Categoria** | Foundation |
| **Owner** | Chief Architect |
| **Derivado de** | DOC-0003 First Principles, DOC-0000 North Star |
| **Referenciado por** | Platform Architecture, Agent Specifications, todos os documentos ARCH-* |

---

## ENGINEERING PHILOSOPHY

---

## 1. Arquitetura antes de código

Nenhuma implementação começa sem compreensão do problema.

> Entender o *porquê* antes de escrever o *como*.

---

## 2. Simplicidade antes de sofisticação

Tecnologia complexa só existe quando necessária.

> A solução mais simples que resolve o problema é a solução correta.

---

## 3. Modularidade como princípio

Cada componente deve possuir:

- **responsabilidade clara** — faz uma coisa e faz bem;
- **baixo acoplamento** — pode evoluir sem quebrar vizinhos;
- **possibilidade de evolução** — substituível, extensível, testável.

---

## 4. Dados separados de comportamento

Conteúdo não pertence à Engine.

- A **Engine** executa.
- Os **Packages** definem conhecimento.

> Separação fundamental: lógica de avaliação ≠ conteúdo avaliado.

---

## 5. AI-Native, não AI-Dependent

A plataforma deve **funcionar sem IA**.

A IA **melhora**. Não **sustenta**.

> Se removermos todos os agentes de IA, o sistema deve continuar operacional — com menor qualidade de experiência, mas funcional.

---

## 6. Open Source First

Código deve ser:

- **legível** — outro engenheiro entende sem guia;
- **documentado** — decisões explicadas, não apenas implementadas;
- **contribuível** — qualquer pessoa pode propor melhorias.

---

## 7. Evidence Driven Development

Toda funcionalidade deve produzir **valor observável**.

> Não implementamos features porque são interessantes. Implementamos porque resolvem um problema validado.

---

## Arquitetura Conceitual

```
              FOUNDATION
                   │
                   ▼
        Competency Framework
                   │
                   ▼
               ENGINE
        ┌──────────┼──────────┐
        │          │          │
       AI      Missions   Evidence
        │          │          │
     Agents    Packages   Portfolio
```

### Camadas

| Camada | Responsabilidade |
|--------|-----------------|
| **Foundation** | Princípios, identidade, filosofia — não muda com frequência |
| **Competency Framework** | Modelo de competências, taxonomia, níveis — evolui por versão |
| **Engine** | Motor de avaliação, orquestração, progressão — código vivo |
| **AI / Agents** | Mentor, Avaliador, Gerador — inteligência acoplável |
| **Missions / Packages** | Conteúdo estruturado, desafios, cenários — contribuição aberta |
| **Evidence / Portfolio** | Artefatos produzidos pelo Builder — propriedade do usuário |

---

## Declaração Final

> *"Engenharia não é escrever código. É resolver problemas com disciplina, clareza e responsabilidade."*
