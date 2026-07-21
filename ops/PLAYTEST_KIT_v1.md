# ⚜️ OPERAÇÃO AURORA — Sprint 4: Playtest Kit

| Field | Value |
|-------|-------|
| **Document** | PLAYTEST_KIT_v1.md |
| **Operation** | OPERAÇÃO AURORA — Sprint 4 |
| **Status** | Ready |
| **Date** | 2026-07-20 |

---

> *"Assista. Não explique. Anote. Corrija. Repita."*

---

## 1. Pré-requisitos

Antes de convidar qualquer participante:

- [ ] `npm run build` no frontend — zero erros, zero warnings
- [ ] Backend rodando em `localhost:8000` (ou deploy de preview)
- [ ] Ambiente limpo — sem dados de teste no banco
- [ ] Computador/configuração que o participante usará (não o seu)
- [ ] Gravador de tela pronto (OBS, Loom, ou similar — com permissão)
- [ ] Timer visível (monitorar TTFC)
- [ ] Checklist impresso ou em segunda tela
- [ ] Navegador limpo (sem cache, sem sessão)

### Ambiente recomendado

```bash
# Terminal 1: Backend
cd /d "D:\ASCEND PROJECT"
set ASCEND_DB_PATH=:memory:
uvicorn ascend.api.app:create_app --reload --port 8000

# Terminal 2: Frontend (se for build estático, usar preview)
cd /d "D:\ASCEND PROJECT\apps\web"
npm run build && npm run start
```

---

## 2. Recrutamento

### Perfil ideal (10 pessoas)

| Perfil | Quantidade | Por quê |
|--------|------------|---------|
| **Não-técnico** | 4 | Testa clareza da proposta de valor + onboarding |
| **Estudante (qualquer área)** | 3 | Público-alvo primário |
| **Profissional de tecnologia** | 2 | Testa se o valor é claro mesmo para quem entende de sistemas |
| **Educador/instrutor** | 1 | Perspectiva de quem cria conteúdo |

### Critérios de exclusão

- Pessoa que já viu o ASCEND antes (viés)
- Pessoa que participou do desenvolvimento
- Pessoa que não tem familiaridade básica com navegador web

### Como convidar

> *"Estou testando um produto de aprendizado e gostaria da sua opinião sincera. Não precisa saber nada de tecnologia. É só usar por alguns minutos e me dizer o que achou. Leva no máximo 15 minutos."*

**Não diga:**
- "É um framework de competências"
- "É baseado em evidências"
- "Tem uma engine de runtime"
- "Usa Python + Next.js"

**Diga apenas:**
- "É uma ferramenta de aprendizado"
- "Você vai fazer uma atividade rápida"
- "Me diga o que você entendeu"

---

## 3. Roteiro de Observação

### 3.1 Instrução única

Leia em voz alta, exatamente como está abaixo:

> *"Esta é uma ferramenta de aprendizado. Por favor, abra o site e explore como achar melhor. Não vou responder perguntas durante o teste. Quando terminar — ou se quiser parar — é só avisar. Não tem resposta certa ou errada. Quero entender o que faz sentido para você."*

### 3.2 Timeline de observação

| Momento | O que observar | Anotar |
|---------|----------------|--------|
| **T = 0** | Abre o site | Expressão facial inicial |
| **T + 5s** | Primeiro olhar | O que ele lê primeiro? |
| **T + 10s** | Primeira ação | Clica em quê? |
| **T + 30s** | Navegação inicial | Já entendeu o propósito? |
| **T + 1min** | Primeira interação | Começou uma jornada? Criou conta? |
| **T + 2min** | Fluxo de missão | Leu o briefing? Entendeu o que fazer? |
| **T + 5min** | Evidência | Escreveu algo? Ficou travado? |
| **T + 8min** | Completa? | Conseguiu terminar? |
| **T + 10min** | Resultado | Viu a competência? Entendeu? |
| **T + 15min** | Fim | Para por vontade própria? |

### 3.3 Checklist por página

#### Home Page (`/`)
- [ ] Entendeu o propósito do site?
- [ ] Leu o título e subtítulo?
- [ ] Clicou em "Começar Agora" ou "Experimentar Demo"?
- [ ] Hesitou (> 3s sem clicar)?
- [ ] Tentou clicar em elemento não-clicável?

#### Auth Page (`/auth`) (se não for demo)
- [ ] Entendeu que precisa criar conta?
- [ ] Reclamou de criar conta?
- [ ] Digitou username rapidamente?
- [ ] Errou? Teve feedback?

#### Dashboard (`/dashboard`)
- [ ] Entendeu os números?
- [ ] Percebeu o Ascension Ring?
- [ ] Clicou em "Start Your First Journey"?
- [ ] Ficou confuso com algum termo?

#### Journey Explorer (`/journeys`)
- [ ] Entendeu que são trilhas de aprendizado?
- [ ] Clicou em uma jornada?
- [ ] Entendeu que precisa clicar em "Start"?
- [ ] Ficou confuso com "pré-requisitos"?

#### Mission Workspace (`/missions/{id}`)
- [ ] Leu o briefing?
- [ ] Entendeu o que precisa fazer?
- [ ] Ficou travado no que escrever?
- [ ] Usou o Focus Mode? Gostou?
- [ ] Conseguiu submeter evidência?

#### Assessment Result (`/missions/{id}/result`)
- [ ] Entendeu que passou?
- [ ] Percebeu a competência desbloqueada?
- [ ] Percebeu o XP/level-up?
- [ ] Clicou em "Back to Dashboard" ou "Continue"?
- [ ] Sorriu? (sério — anote)

---

## 4. Pós-teste: Entrevista (5 min)

Após o participante terminar (ou desistir), faça estas perguntas. **Não conduza.** Deixe a pessoa responder livremente.

### Perguntas abertas

1. **"O que você entendeu que o produto faz?"**
   - Se a resposta for muito diferente do propósito real, o onboarding falhou.

2. **"O que te frustrou?"**
   - Escute sem justificar. Anote tudo.

3. **"O que você mais gostou?"**
   - Isso é o que você deve proteger a qualquer custo.

4. **"Teve algum momento em que você não soube o que fazer?"**
   - Se sim, onde? Isso é um ponto de atrito.

5. **"Você usaria isso de novo? Por quê?"**
   - Se sim: o que te faria voltar?
   - Se não: o que precisa mudar?

6. **"Se você pudesse mudar uma coisa no produto, o que seria?"**
   - A primeira resposta geralmente é a mais honesta.

### Escala NPS

> *"Em uma escala de 0 a 10, o quanto você recomendaria esta ferramenta para um amigo que quer aprender uma habilidade nova?"*

| Nota | Classificação |
|------|---------------|
| 9-10 | Promotores |
| 7-8 | Neutros |
| 0-6 | Detratores |

---

## 5. Métricas a Coletar

### Automáticas (instrumentação)

```typescript
// Adicione ao demo-store.ts ou crie um hook usePlaytestMetrics
interface PlaytestMetrics {
  ttfc_start: number           // Timestamp when page loaded
  ttfc_first_click: number     // First interaction
  ttfc_builder_created: number // Auth completed or demo started
  ttfc_mission_started: number // First mission started
  ttfc_evidence_submitted: number // First evidence submitted
  ttfc_competency_unlocked: number // First competency received
  // Computed
  ttfc: number                 // competency_unlocked - page_load (ms)
}
```

### Manuais

| Métrica | Coleta | Target |
|---------|--------|--------|
| TTFC (real) | Timer | < 5 min |
| TTFC (demo) | Timer | < 2 min |
| Clicks to first mission | Observação | ≤ 3 |
| Abandonos antes de completar | Contagem | 0 |
| Expressões de frustração | Contagem | ≤ 2 |
| Sorrisos/reações positivas | Contagem | ≥ 3 |
| "Não entendi" | Contagem | ≤ 2 |
| Ajuda solicitada | Contagem | 0 |
| NPS | Entrevista | ≥ 7 |
| "Usaria de novo?" | Entrevista | ≥ 7/10 |

---

## 6. Sessão de Debrief (pós-playtest)

Após cada participante, reserve 10 minutos para:

### 6.1 Consolidar observações

```
Participante #: ___
Perfil: ___________
Data: _____________

TTFC: _____ minutos
Missões completadas: ___/___
Abandonou? [ ] Sim [ ] Não
NPS: ___/10
Usaria de novo? [ ] Sim [ ] Não

Top 3 frustrações:
1. _______________________________
2. _______________________________
3. _______________________________

Top 3 acertos:
1. _______________________________
2. _______________________________
3. _______________________________

Citações literais:
"________________________________"
"________________________________"
"________________________________"
```

### 6.2 Priorizar problemas

Após cada 5 participantes, compile uma matriz:

| Problema | Frequência | Impacto | Prioridade |
|----------|------------|---------|------------|
| (ex) Não entendeu o que é competência | 3/5 | Alto | 🔴 P1 |
| (ex) Demorou a achar o botão de iniciar | 4/5 | Médio | 🟠 P2 |

### 6.3 Ciclo de correção

```
Playtest (3 pessoas)
  ↓
Consolidar
  ↓
Corrigir top 5 problemas
  ↓
Playtest (mais 3 pessoas)
  ↓
Consolidar
  ↓
Corrigir
  ↓
Playtest (4 pessoas)
  ↓
Review final → v1.1 Stable
```

---

## 7. Critérios para v1.1 Stable

O playtest é aprovado quando:

- [ ] **8/10** participantes completam uma missão sem ajuda
- [ ] **7/10** dizem que usariam novamente
- [ ] **Zero** participantes desistem por frustração
- [ ] **TTFC médio** < 5 min (modo normal) e < 2 min (demo)
- [ ] **NPS médio** ≥ 7
- [ ] **Zero** "não entendi o que fazer" no fluxo demo
- [ ] **Top 5 problemas** identificados e corrigidos

---

## 8. Pós v1.1: Próximos Passos

Após aprovação no playtest:

```
v1.1 Stable
  │
  ├── Release público (GitHub Release + anúncio)
  │
  ├── Milestone F — Intelligence
  │   ├── AI Mentor (LLM integration)
  │   ├── Reviewer Agent
  │   └── Personalization
  │
  ├── Milestone G — Ecosystem
  │   ├── Package Registry
  │   ├── Marketplace
  │   └── Community
  │
  └── Milestone H — Sovereign Learning Network
      ├── Portable Identity
      ├── Decentralized Evidence
      └── Cross-Platform
```

### O que NÃO fazer antes do playtest

- ❌ JWT / autenticação real
- ❌ AI Mentor / LLM
- ❌ Marketplace
- ❌ Multiplayer / ranking
- ❌ Gamificação adicional
- ❌ Analytics / tracking
- ❌ Cloud sync
- ❌ Plugins / SDK

A única pergunta que importa agora:

> **Uma pessoa aprende melhor usando o ASCEND do que estudando da forma tradicional?**

Playtest responde essa pergunta. Todo o resto é distração.

---

## Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial playtest kit |
