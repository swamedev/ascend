# WF-0001 — Dashboard

| Campo | Valor |
|-------|-------|
| **ID** | WF-0001 |
| **Nome** | Dashboard |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, UI-0001, UI-0002, UI-0003 |
| **Será utilizado por** | Frontend Sprint 1 |

---

## 1. Propósito

O Dashboard é a primeira tela que o Builder vê ao acessar o ASCEND.

Sua missão é responder instantaneamente a quatro perguntas:

1. **Onde eu parei?** — Missão ativa, progresso
2. **O que fazer agora?** — Próxima ação recomendada
3.**Como estou evoluindo?** — XP, nível, streak
4. **O que está acontecendo?** — Atividade recente, notificações

---

## 2. Wireframe Desktop

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND                                          🔥7 📬 👤    │
│                                                    Level 5      │
│                                                     450/800 XP  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │                                                      │ │
│ │  ■   │  ┌────────────────────────────────────────────────┐  │ │
│ │  🗡️  │  │  🗡️ CONTINUE YOUR MISSION                        │  │ │
│ │  ◆   │  │                                                │  │ │
│ │  🧠  │  │  Linux Basics — Mission 4                       │  │ │
│ │  🏅  │  │  "Configurar usuários e permissões Linux"       │  │ │
│ │  📁  │  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  65%                   │  │ │
│ │  ⚗️  │  │  [▶️ Resume]        [📁 Submit Evidence]       │  │ │
│ │  🤖  │  └────────────────────────────────────────────────┘  │ │
│ │  🌐  │                                                      │ │
│ │  🛒  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ │
│ │  ⚙️  │  │ 🎯 Total     │ │ 🧠 Compet.   │ │ 🏅 Achieve.  │ │ │
│ │      │  │ Missions     │ │ Earned       │ │ Unlocked     │ │ │
│ │      │  │     24       │ │      6       │ │     12       │ │ │
│ │      │  └──────────────┘ └──────────────┘ └──────────────┘ │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────┐ ┌──────────────────────────┐   │ │
│ │      │  │ 🔥 7-Day Streak  │ │ 🏆 Next Achievement      │   │ │
│ │      │  │ ▓▓▓▓▓▓▓░░ 7/7   │ │ "Consistent" — 3 more    │   │ │
│ │      │  └──────────────────┘ │ ▓▓▓▓▓░░░░░░  50%         │   │ │
│ │      │                       └──────────────────────────┘   │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │ 📢 Activity Feed                              │    │ │
│ │      │  │ ● Today                                       │    │ │
│ │      │  │   🗡️ Mission completed: Linux #4        +100XP│    │ │
│ │      │  │   📁 Evidence approved: Linux #3              │    │ │
│ │      │  │   🏅 Badge earned: "File Manager"             │    │ │
│ │      │  │ ● Yesterday                                   │    │ │
│ │      │  │   🤖 Mentor: new suggestion available         │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │ 💡 Mentor Suggestion                           │    │ │
│ │      │  │ "Baseado no seu progresso, você está pronto   │    │ │
│ │      │  │  para avançar para configuração de rede."     │    │ │
│ │      │  │ [View Mission]                                │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Wireframe Tablet (768px)

```
┌──────────────────────────────────────────────────┐
│ 🔷 ASCEND                   🔥7 📬 👤 Level 5   │
│                                                     │
│ ┌────────────────────────────────────────────────┐ │
│ │  🗡️ CONTINUE YOUR MISSION                        │ │
│ │  Linux Basics — Mission 4                       │ │
│ │  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░  65%                   │ │
│ │  [▶️ Resume]        [📁 Submit]                │ │
│ └────────────────────────────────────────────────┘ │
│                                                     │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ 🎯 Missions  │ │ 🧠 Compet.   │ │ 🏅 Achieve.  │ │
│ │     24       │ │      6       │ │     12       │ │
│ └──────────────┘ └──────────────┘ └──────────────┘ │
│                                                     │
│ ┌──────────────────┐ ┌──────────────────────────┐   │
│ │ 🔥 7-Day Streak  │ │ 🏆 Next Achievement      │   │
│ │ ▓▓▓▓▓▓▓░░ 7/7   │ │ "Consistent" — 50%       │   │
│ └──────────────────┘ └──────────────────────────┘   │
│                                                     │
│ ┌──────────────────────────────────────────────┐    │
│ │ 📢 Activity Feed                              │    │
│ │ ● Today: 🗡️ Mission +100XP 🏅 Badge          │    │
│ │ ● Yesterday: 🤖 Mentor suggestion             │    │
│ └──────────────────────────────────────────────┘    │
│                                                     │
│ ┌──────────────────────────────────────────────┐    │
│ │ 💡 Mentor Suggestion                           │    │
│ │ "Você está pronto para configuração de rede." │    │
│ │ [View Mission]                                │    │
│ └──────────────────────────────────────────────┘    │
│                                                     │
│ ┌───┬───┬───┬───┬───┬───┐                          │
│ │ 🏠 │ 🗡️ │ 🧠 │ 🤖 │ 🌐 │ ⚙️ │                    │
│ └───┴───┴───┴───┴───┴───┘                          │
└──────────────────────────────────────────────────┘
```

---

## 4. Wireframe Mobile (<768px)

```
┌──────────────────────────┐
│ 🔷 ASCEND     🔥7 📬 👤  │
│ Level 5 — 450/800 XP    │
├──────────────────────────┤
│                          │
│ 🗡️ CONTINUE MISSION      │
│ Linux Basics — Mission 4 │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░  65%  │
│                          │
│ [▶️ Resume]              │
│                          │
├──────────────────────────┤
│ 🎯 24  🧠 6  🏅 12     │
│ Missions Compet. Achiev. │
├──────────────────────────┤
│ 🔥 7-Day Streak          │
│ ▓▓▓▓▓▓▓░░ 7/7           │
├──────────────────────────┤
│ 🏆 Next: "Consistent"    │
│ ▓▓▓▓▓░░░░  50%           │
├──────────────────────────┤
│ 📢 Activity              │
│ 🗡️ Mission +100XP        │
│ 🏅 Badge earned          │
├──────────────────────────┤
│ 💡 "Pronto para rede"   │
├──────────────────────────┤
│                          │
├──────────────────────────┤
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️       │
└──────────────────────────┘
```

---

## 5. Hierarquia Visual

```
Priority 1 (Maior atenção)
  ┌────────────────────────────────────────────┐
  │  🗡️ CONTINUE YOUR MISSION                   │
  │  Card principal, maior, cor brand, CTA      │
  └────────────────────────────────────────────┘

Priority 2
  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
  │ Quick Stats  │ │ Quick Stats  │ │ Quick Stats  │
  └──────────────┘ └──────────────┘ └──────────────┘

Priority 3
  ┌──────────────────┐ ┌──────────────────────────┐
  │ Streak + Next    │ │ Achievement Progress      │
  └──────────────────┘ └──────────────────────────┘

Priority 4
  ┌──────────────────────────────────────────────┐
  │ Activity Feed                                 │
  └──────────────────────────────────────────────┘

Priority 5
  ┌──────────────────────────────────────────────┐
  │ Mentor Suggestion                             │
  └──────────────────────────────────────────────┘
```

---

## 6. Heatmap de Atenção

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                                                   ░░░░░          │
│                                                     ░░░         │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░████████████████████████████████████████████░░░░░░░░░░░░░░░░   │
│ ░░████████████████████████████████████████████░░░░░░░░░░░░░░░░   │
│ ░░████████████████████████████████████████████░░░░░░░░░░░░░░░░   │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                                                  │
│ ░░░░░░░░████░░░░░░░░████░░░░░░░░░░████░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░░░░░░░████░░░░░░░░████░░░░░░░░░░████░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                                                  │
│ ░░░░░░████████░░░░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░░░░░████████░░░░░░░████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                                                  │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │
│                                                                  │
│ ██ = máxima atenção                                              │
│ ░░ = média/baixa atenção                                         │
└──────────────────────────────────────────────────────────────────┘
```

---

## 7. Fluxo de Navegação

```
Dashboard
  │
  ├── [▶️ Resume] → Mission Workspace (WF-0003)
  │
  ├── [📁 Submit Evidence] → Evidence Center (WF-0006)
  │
  ├── Quick Stats (Missions) → Mission Explorer (WF-0002)
  │
  ├── Quick Stats (Competencies) → Competency Tree (WF-0004)
  │
  ├── Quick Stats (Achievements) → Achievement Gallery (WF-0007)
  │
  ├── Streak Card → Builder Profile (WF-0005)
  │
  ├── Next Achievement → Achievement Gallery (WF-0007)
  │
  ├── Activity Feed → Activity Feed Detail
  │
  ├── Mentor Suggestion → AI Mentor Panel (WF-0008)
  │
  └── Sidebar → All sections
```

---

## 8. Estados

### 8.1 Novo Usuário (First Access)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND                                          👤            │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │                                              │    │ │
│ │      │  │         🗡️ Welcome to ASCEND                  │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  "Toda competência reivindicada deve ser     │    │ │
│ │      │  │   uma competência comprovada."               │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  Sua jornada começa com uma única missão.    │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  ┌────────────────────────────────────────┐  │    │ │
│ │      │  │  │ 🗡️ Your First Mission                    │  │    │ │
│ │      │  │  │ "Configurar ambiente de aprendizagem"  │  │    │ │
│ │      │  │  │ ⏱️ 15 min · 🎯 Beginner                 │  │    │ │
│ │      │  │  │                                        │  │    │ │
│ │      │  │  │ [▶️ Start Mission]                      │  │    │ │
│ │      │  │  └────────────────────────────────────────┘  │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  Stats:                                      │    │ │
│ │      │  │  🎯 0 🧠 0 🏅 0 🔥 0                        │    │ │
│ │      │  │                                              │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ │      │                                                      │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 8.2 Builder Ativo

(O wireframe Desktop na seção 2 representa este estado.)

### 8.3 Builder Avançado

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND                                          🔥34 📬 👤   │
│                                                    Level 12     │
│                                                     12450/15000 │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │  ┌────────────────────────────────────────────────┐  │ │
│ │      │  │  📊 Your Week in Review                         │  │ │
│ │      │  │  12 missions · 3 competencies · 4500 XP        │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │ │
│ │      │  │ 🎯 156      │ │ 🧠 18        │ │ 🏅 47        │ │ │
│ │      │  │ Missions    │ │ Competencies │ │ Achievements  │ │ │
│ │      │  └──────────────┘ └──────────────┘ └──────────────┘ │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │  🗡️ Active Missions (3)                        │    │ │
│ │      │  │  ├ Linux #7 — Configuring Firewall      ▓▓▓  │    │ │
│ │      │  │  ├ Security #2 — Pentesting Basics      ▓░░  │    │ │
│ │      │  │  └ Cloud #1 — AWS Setup                 ░░░  │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────┐ ┌──────────────────────────┐   │ │
│ │      │  │ 🔥 34-Day Streak │ │ 🏆 "Mentor" — 80%       │   │ │
│ │      │  └──────────────────┘ └──────────────────────────┘   │ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │ 📢 Activity — Global                          │    │ │
│ │      │  │ 🌐 CyberPro completed "Advanced Network"     │    │ │
│ │      │  │ 🌐 DataMaster reached Level 15               │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 8.4 Skeleton Loading

```
┌──────────────────────────────────────────────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │ ▓▓▓▓ │  ┌────────────────────────────────────────────────┐  │ │
│ │ ▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  │ │
│ │ ▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  │ │
│ │ ▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  │ │
│ │ ▓▓▓▓ │  └────────────────────────────────────────────────┘  │ │
│ │ ▓▓▓▓ │                                                      │ │
│ │ ▓▓▓▓ │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │ │
│ │ ▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓ │ │ ▓▓▓▓▓▓▓▓ │ │ ▓▓▓▓▓▓▓▓ │            │ │
│ │ ▓▓▓▓ │  └──────────┘ └──────────┘ └──────────┘            │ │
│ │ ▓▓▓▓ │                                                      │ │
│ │ ▓▓▓▓ │  ┌──────────────────────────────────────────────┐    │ │
│ │ ▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │    │ │
│ │ ▓▓▓▓ │  │ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │    │ │
│ │ ▓▓▓▓ │  └──────────────────────────────────────────────┘    │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
│                                                                  │
│ Shimmer animation: gradient sweep 1.5s infinite                  │
└──────────────────────────────────────────────────────────────────┘
```

### 8.5 Empty State (After Onboarding, No Active Mission)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND                                          🔥0 📬 👤    │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │                                              │    │ │
│ │      │  │              📭 No Active Mission             │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  You've completed all available missions.    │    │ │
│ │      │  │  Ready for the next challenge?               │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  ┌────────────────────────────────────────┐  │    │ │
│ │      │  │  │  🗡️ Suggested Next:                     │  │    │ │
│ │      │  │  │  "Linux Network Configuration"          │  │    │ │
│ │      │  │  │  ⏱️ 45 min · 🎯 Medium                  │  │    │ │
│ │      │  │  │  [Explore Journeys]                     │  │    │ │
│ │      │  │  └────────────────────────────────────────┘  │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

### 8.6 Error State

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND                                          🔥7 📬 👤    │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │                                                      │ │
│ │      │  ┌──────────────────────────────────────────────┐    │ │
│ │      │  │                                              │    │ │
│ │      │  │        ⚠️ Something went wrong                │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  We couldn't load your dashboard.            │    │ │
│ │      │  │  This is usually temporary.                  │    │ │
│ │      │  │                                              │    │ │
│ │      │  │  [🔄 Retry]    [📞 Contact Support]          │    │ │
│ │      │  │                                              │    │ │
│ │      │  └──────────────────────────────────────────────┘    │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 9. Motion Timeline (Entrada dos Componentes)

### 9.1 Sequence

```
Timeline: 0ms → 800ms

0ms      ├── Page transition (fade in, 200ms)
100ms    ├── Sidebar slides in from left (300ms, ease-out)
150ms    ├── Header fades in (200ms)
200ms    ├── Continue Mission card slides up (300ms, ease-out)
300ms    ├── Quick Stats cards stagger in (each 100ms delay)
│        │   ├── Missions card
│        │   ├── Competencies card
│        │   └── Achievements card
400ms    ├── Streak + Next Achievement fade in (200ms)
500ms    ├── Activity Feed slides up (300ms)
600ms    └── Mentor Suggestion fades in (200ms)
```

### 9.2 Motion Specs

| Component | Animation | Duration | Easing | Delay |
|-----------|-----------|----------|--------|-------|
| Page transition | `fade-in` | 200ms | ease-out | 0 |
| Sidebar | `slide-left` | 300ms | ease-out | 100ms |
| Header | `fade-in` | 200ms | ease-out | 150ms |
| Mission card | `slide-up` | 300ms | ease-out | 200ms |
| Stats (each) | `scale-in` | 200ms | ease-spring | 300ms+stagger |
| Streak card | `fade-in` | 200ms | ease-out | 400ms |
| Activity feed | `slide-up` | 300ms | ease-out | 500ms |
| Mentor card | `fade-in` | 200ms | ease-out | 600ms |

### 9.3 Reduced Motion

When `prefers-reduced-motion` is active:
- All animations disabled
- Instant appear (opacity 0→1, no movement)

---

## 10. Ascension Ring Integration (Dashboard)

The Dashboard features the **Ascension Ring** as the primary identity element in the sidebar footer.

```
┌──────┐
│      │      ┌──────────┐
│      │      │  Level 5 │
│ Side │      │   ┌───┐  │
│ Bar  │      │   │450│  │◄── XP counter
│      │      │   └───┘  │
│      │      │ ┌──────┐ │
│      │      │ │800 XP│ │◄── Progress to next
│      │      │ └──────┘ │
│      │      │  ┌────┐  │
│      │      │  │7🔥 │  │◄── Streak
│      │      │  └────┘  │
│──────│      └──────────┘
│ 👤   │
└──────┘
```

See WF-0005 for full Ascension Ring specification.

---

## 11. Definition of Done

WF-0001 aprovado quando:

- [ ] Wireframe Desktop completo
- [ ] Wireframe Tablet completo
- [ ] Wireframe Mobile completo
- [ ] Hierarquia visual documentada
- [ ] Prioridade de informação definida
- [ ] Heatmap de atenção gerado
- [ ] Fluxo de navegação mapeado
- [ ] Estado Novo Usuário documentado
- [ ] Estado Builder Ativo documentado
- [ ] Estado Builder Avançado documentado
- [ ] Skeleton Loading especificado
- [ ] Empty State especificado
- [ ] Error State especificado
- [ ] Motion timeline completa
- [ ] Reduced motion coberto

---

## Status

**WF-0001 — Dashboard**

- Estado: ✅ Completo
- Próximo: WF-0002 — Journey Explorer
