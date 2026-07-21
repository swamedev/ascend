# WF-0003 — Mission Workspace

| Campo | Valor |
|-------|-------|
| **ID** | WF-0003 |
| **Nome** | Mission Workspace |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, ARCH-0003, UI-0001, UI-0002 |
| **Será utilizado por** | Frontend Sprint 2 |

---

## 1. Propósito

A tela mais importante do ASCEND.

O Mission Workspace é onde o Builder passa a maior parte do tempo. É onde ele:

- Lê o briefing da missão
- Consulta a rubrica de avaliação
- Conversa com o Mentor
- Envia evidências
- Recebe feedback

É também onde o **Focus Mode** transforma a experiência em um estado de fluxo puro.

---

## 2. Wireframe Desktop — Painéis

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Linux Basics  >  Mission 4: User Management       │
│                                                    ⏱️ 35:42     │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─ Painel Esquerdo (Briefing) ────┐ ┌─ Painel Direito (Mentor) ┐│
│ │                                 │ │                           ││
│ │ 🗡️ Configure Linux Users         │ │ 🤖 AI Mentor              ││
│ │                                 │ │                           ││
│ │ Status: 🟡 Active               │ │ ┌─ Conversation ────────┐││
│ │ 🎯 Medium  ·  ⏱️ 45 min         │ │ │ Mentor: Dica rápida   │││
│ │ +150 XP expected                │ │ │                       │││
│ │                                 │ │ │ Você: Como criar um   │││
│ │ ┌─ Objective ───────────────┐   │ │ │ usuário com sudo?    │││
│ │ │ Criar 3 usuários Linux    │   │ │ │                       │││
│ │ │ com permissões            │   │ │ │ Mentor: Use useradd   │││
│ │ │ específicas...            │   │ │ │ -m -G sudo nome       │││
│ │ └───────────────────────────┘   │ │ └───────────────────────┘││
│ │                                 │ │                           ││
│ │ ┌─ Resources ───────────────┐   │ │ ┌─ Quick Actions ──────┐ ││
│ │ │ 📄 Linux Command Ref      │   │ │ │ 💡 Dica para missão  │ ││
│ │ │ 📺 Video: User Mgmt      │   │ │ │ 📚 Material extra    │ ││
│ │ │ 🔗 man useradd            │   │ │ │ 🎯 Próximo passo    │ ││
│ │ └───────────────────────────┘   │ │ └───────────────────────┘││
│ │                                 │ │                           ││
│ └─────────────────────────────────┘ └───────────────────────────┘│
│                                                                  │
│ ┌─ Painel Inferior Esquerdo ──────┐ ┌─ Painel Inferior Direito ┐│
│ │ ┌─ Rubric ────────────────────┐ │ │ ┌─ Evidence ───────────┐ ││
│ │ │ Criteria           Weight   │ │ │ │                      │ ││
│ │ │ ✅ Command accuracy   40%   │ │ │ │ 📁 Drag files here   │ ││
│ │ │ ✅ User creation      30%   │ │ │ │    or click to       │ ││
│ │ │ ✅ Documentation      20%   │ │ │ │    upload            │ ││
│ │ │ ✅ Explanation        10%   │ │ │ │                      │ ││
│ │ └─────────────────────────────┘ │ │ │ Accepted: .md,.pdf   │ ││
│ │                                 │ │ │ Max: 10MB            │ ││
│ │                                 │ │ │                      │ ││
│ │                                 │ │ │ [📤 Submit Evidence] │ ││
│ │                                 │ │ └──────────────────────┘ ││
│ └─────────────────────────────────┘ └───────────────────────────┘│
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ Feedback (aparece após review)                                   │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ ✅ Approved by Reviewer · Score: 85/100                      │ │
│ │ "Good work! Suggestion: add user comments for clarity."      │ │
│ │ +150 XP earned                                              │ │
│ └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Focus Mode

### 3.1 Conceito

Focus Mode é o estado no qual o ASCEND desaparece para que apenas a missão exista.

Quando ativado:

- Sidebar recolhida (ou oculta)
- Header minimizado (apenas timer + sair)
- Mentor vira overlay (aparece apenas quando chamado)
- Fundo pode escurecer levemente
- Apenas briefing + editor/terminal + evidência

### 3.2 Wireframe Focus Mode

```
┌──────────────────────────────────────────────────────────────────┐
│ 🗡️ Configure Linux Users              ⏱️ 35:42     [Exit Focus] │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌─ Objective ──────────────────────────────────────────────────┐│
│ │                                                               ││
│ │ Create 3 Linux users with specific permissions:               ││
│ │ • User1: developer — sudo access                              ││
│ │ • User2: intern  — basic access                               ││
│ │ • User3: guest   — restricted                                 ││
│ │                                                               ││
│ │ Document each step with explanation.                          ││
│ │                                                               ││
│ └───────────────────────────────────────────────────────────────┘│
│                                                                  │
│ ┌─ Reference ───────────────────────────────────────────────────┐│
│ │ 📄 Linux Command Reference   |   🔗 man useradd   |  📺 Video ││
│ └──────────────────────────────────────────────────────────────┘│
│                                                                  │
│ ┌─ Your Work ──────────────────────────────────────────────────┐│
│ │                                                               ││
│ │ ┌───────────────────────────────────────────────────────────┐ ││
│ │ │ # Terminal (ou editor de texto)                           │ ││
│ │ │ $ sudo useradd -m -G sudo developer                       │ ││
│ │ │ $ sudo passwd developer                                   │ ││
│ │ │ $ sudo useradd -m intern                                  │ ││
│ │ │ $ sudo useradd -m guest                                   │ ││
│ │ │ $ sudo usermod -s /sbin/nologin guest                     │ ││
│ │ └───────────────────────────────────────────────────────────┘ ││
│ │                                                               ││
│ │ ┌───────────────────────────────────────────────────────────┐ ││
│ │ │ 📝 Notes / Documentation                                  │ ││
│ │ │ User developer created with sudo access for development.  │ ││
│ │ │ User intern created with basic home directory access.     │ ││
│ │ │ User guest created with restricted shell.                 │ ││
│ │ └───────────────────────────────────────────────────────────┘ ││
│ │                                                               ││
│ └───────────────────────────────────────────────────────────────┘│
│                                                                  │
│ ┌─ Evidence ───────────────────────────────────────────────────┐│
│ │ 📎 commands.log  📎 report.md  📎 screenshot.png             ││
│ │ [Add Files]                                  [📤 Submit]     ││
│ └──────────────────────────────────────────────────────────────┘│
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 🤖 Mentor (aparece como floating button, clique abre overlay)   │
└──────────────────────────────────────────────────────────────────┘
```

### 3.3 Focus Mode — States

| State | Visual |
|-------|--------|
| **Active** | Full-screen workspace, minimal chrome |
| **Mentor call** | Floating bubble → slide-in panel from right |
| **Evidence ready** | Subtle notification "Ready to submit?" |
| **Mission complete** | Celebration overlay (WF-0001 style) |
| **Exit** | Smooth transition back to normal workspace |

### 3.4 Focus Mode — Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+F` | Toggle Focus Mode |
| `Ctrl+M` | Toggle Mentor panel (within focus) |
| `Ctrl+E` | Toggle Evidence panel |
| `Ctrl+Enter` | Submit evidence |
| `Escape` | Exit Focus Mode |

---

## 4. Wireframe Tablet (768px)

```
┌──────────────────────────────────────────────────┐
│ 🗡️ Mission 4: User Management     ⏱️ 35:42       │
├──────────────────────────────────────────────────┤
│                                                   │
│ ┌─ Briefing ───────────────────────────────────┐  │
│ │ Objective: Create 3 Linux users...           │  │
│ │ Status: Active · 🎯 Medium · +150 XP        │  │
│ │ Resources: 📄 📺 🔗                         │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌─ Rubric ─────────────────────────────────────┐  │
│ │ Command accuracy 40% | Users 30%             │  │
│ │ Documentation 20% | Explanation 10%          │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌─ Work Area ──────────────────────────────────┐  │
│ │                                                │  │
│ │ Terminal / Editor / Notes                      │  │
│ │                                                │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ ┌─ Evidence ───────────────────────────────────┐  │
│ │ 📎 commands.log  📎 report.md                │  │
│ │ [Add Files]            [Submit]              │  │
│ └──────────────────────────────────────────────┘  │
│                                                    │
│ 🤖 [Mentor] (floating button)                      │
│                                                    │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️                                  │
└──────────────────────────────────────────────────┘
```

---

## 5. Wireframe Mobile (<768px)

```
┌──────────────────────────┐
│ 🗡️ Mission 4    ⏱️ 35:42 │
├──────────────────────────┤
│                          │
│ 📋 Briefing              │
│ Create 3 users...        │
│                          │
│ ✅ Rubric                │
│ Commands 40% Users 30%  │
│ Docs 20% Explain 10%    │
│                          │
│ ┌─ Work ──────────────┐  │
│ │                      │  │
│ │ Terminal / Notes     │  │
│ │                      │  │
│ └──────────────────────┘  │
│                          │
│ 📁 Evidence              │
│ 2 files ready            │
│ [Upload] [Submit]        │
│                          │
├──────────────────────────┤
│ 🤖 🏠 🗡️ 📁 ⚙️           │
└──────────────────────────┘
```

---

## 6. Hierarquia Visual

```
Priority 1 (Topo — atenção imediata)
  ┌─────────────────────────────────────────────┐
  │ Briefing: Objetivo claro da missão          │
  └─────────────────────────────────────────────┘

Priority 2 (Centro — ação)
  ┌─────────────────────────────────────────────┐
  │ Work Area: Terminal / Editor / Notes        │
  └─────────────────────────────────────────────┘

Priority 3 (Inferior — entrega)
  ┌─────────────────────────────────────────────┐
  │ Evidence: Upload + Submit                   │
  └─────────────────────────────────────────────┘

Priority 4 (Laterais — suporte)
  ┌─────────────┐  ┌───────────────────────────┐
  │ Rubric      │  │ Mentor (optional)         │
  └─────────────┘  └───────────────────────────┘
```

---

## 7. Estados

### 7.1 Active Mission (Normal)

Wireframe Desktop seção 2.

### 7.2 Focus Mode

Wireframe seção 3.

### 7.3 Submitted (Aguardando Review)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🗡️ Configure Linux Users           Status: ⏳ Under Review      │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │  Evidence submitted successfully!                            │ │
│ │                                                              │ │
│ │  📎 commands.log      ✅ Uploaded                            │ │
│ │  📎 report.md         ✅ Uploaded                            │ │
│ │  📎 screenshot.png    ✅ Uploaded                            │ │
│ │                                                              │ │
│ │  Your mission is under review. You'll be notified when       │ │
│ │  feedback is available.                                      │ │
│ │                                                              │ │
│ │  Estimated review time: ~5 minutes                           │ │
│ │                                                              │ │
│ │  [📊 View Other Missions]                                    │ │
│ └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 7.4 Completed (Com Feedback)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🗡️ Configure Linux Users           Status: ✅ Completed        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │  🎉 Mission Complete!                                        │ │
│ │                                                              │ │
│ │  +150 XP earned                                              │ │
│ │                                                              │ │
│ │  ┌─ Feedback ─────────────────────────────────────────────┐  │ │
│ │  │ Score: 85/100                                          │  │ │
│ │  │                                                        │  │ │
│ │  │ ✅ Command accuracy: 90%  — Excellent                  │  │ │
│ │  │ ✅ User creation: 100%    — Perfect                     │  │ │
│ │  │ ✅ Documentation: 70%    — Good, add comments           │  │ │
│ │  │ ✅ Explanation: 80%      — Clear                        │  │ │
│ │  │                                                        │  │ │
│ │  │ "Good work! Your commands are precise. Consider        │  │ │
│ │  │  adding inline comments to document edge cases."       │  │ │
│ │  └────────────────────────────────────────────────────────┘  │ │
│ │                                                              │ │
│ │  [▶️ Next Mission]  [🔄 Resubmit]  [🏅 View Achievement]   │ │
│ └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 7.5 Loading

```
┌──────────────────────────────────────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
├──────────────────────────────────────────────────────────────────┤
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                                                  │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │
│ └──────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌──────────────────────────────┐ ┌──────────────────────────────┐│
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ││
│ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ││
│ └──────────────────────────────┘ └──────────────────────────────┘│
└──────────────────────────────────────────────────────────────────┘
```

### 7.6 Error State

```
┌──────────────────────────────────────────────────────────────────┐
│ 🗡️ Configure Linux Users                                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌──────────────────────────────────────────────────────────────┐ │
│ │                                                              │ │
│ │  ⚠️ Could not load mission data                              │ │
│ │                                                              │ │
│ │  Something went wrong while loading this mission.            │ │
│ │  Please try again.                                           │ │
│ │                                                              │ │
│ │  [🔄 Retry]  [📞 Support]                                    │ │
│ │                                                              │ │
│ └──────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 8. Motion Timeline

| Component | Animation | Duration | Easing | Delay |
|-----------|-----------|----------|--------|-------|
| Page enter | `fade-in` | 200ms | ease-out | 0 |
| Briefing panel | `slide-up` | 300ms | ease-out | 100ms |
| Mentor panel | `slide-right` | 300ms | ease-out | 200ms |
| Rubric | `fade-in` | 200ms | ease-out | 300ms |
| Work area | `scale-in` | 300ms | ease-out | 400ms |
| Evidence | `slide-up` | 300ms | ease-out | 500ms |
| Focus Mode enter | `full-screen` | 400ms | ease-in-out | — |
| Focus Mode exit | `full-screen reverse` | 300ms | ease-in-out | — |

---

## 9. Feedback After Submission

O feedback é dividido em três níveis:

| Nível | Conteúdo | Timing |
|-------|----------|--------|
| **Instant** | "Evidence received" | Imediato após upload |
| **AI Review** | Score + sugestões | ~1-2 min |
| **Human Review** (futuro) | Avaliação detalhada | ~24h |

---

## 10. Definition of Done

WF-0003 aprovado quando:

- [ ] Wireframe Desktop com 4 painéis completo
- [ ] Focus Mode especificado + wireframe
- [ ] Focus Mode keyboard shortcuts definidos
- [ ] Wireframe Tablet completo
- [ ] Wireframe Mobile completo
- [ ] Hierarquia visual documentada
- [ ] Estado Active Mission documentado
- [ ] Estado Submitted documentado
- [ ] Estado Completed com Feedback documentado
- [ ] Estado Loading documentado
- [ ] Estado Error documentado
- [ ] Motion timeline completa
- [ ] Feedback após submissão especificado

---

## Status

**WF-0003 — Mission Workspace**

- Estado: ✅ Completo
- Próximo: WF-0004 — Competency Tree
