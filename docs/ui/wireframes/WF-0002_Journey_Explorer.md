# WF-0002 — Journey Explorer

| Campo | Valor |
|-------|-------|
| **ID** | WF-0002 |
| **Nome** | Journey Explorer |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, UI-0001, UI-0003 |
| **Será utilizado por** | Frontend Sprint 1 |

---

## 1. Propósito

O Journey Explorer é o hub de descoberta de jornadas de aprendizado.

O Builder pode navegar, buscar, filtrar e selecionar jornadas em três visualizações distintas.

---

## 2. Visualizações

### 2.1 Visualização em Cards (Padrão)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Journeys                              👤 Level 5  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │ 🔍 Search journeys...    [Cards] [Tree] [Map]        │ │
│ │      │                                                      │ │
│ │      │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
│ │      │ │ 🗡️ Linux      │ │ 🔒 Security  │ │ ☁️ Cloud      │  │ │
│ │      │ │ Sys Admin     │ │              │ │ Engineering   │  │ │
│ │      │ │               │ │ Locked       │ │              │  │ │
│ │      │ │ 12 missões    │ │ Req: Level 3 │ │ 8 missões    │  │ │
│ │      │ │ 4 competências│ │              │ │ 3 competências│  │ │
│ │      │ │ ▓▓▓▓▓▓▓ 75%  │ │ 🔒           │ │ ▓░░░░░░ 20%  │  │ │
│ │      │ │ [Continue]   │ │              │ │ [View]       │  │ │
│ │      │ └──────────────┘ └──────────────┘ └──────────────┘  │ │
│ │      │                                                      │ │
│ │      │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐  │ │
│ │      │ │ 🛡️ Cyber     │ │ 🤖 AI/ML     │ │ 📊 Data      │  │ │
│ │      │ │ Security     │ │              │ │ Engineering   │  │ │
│ │      │ │              │ │              │ │              │  │ │
│ │      │ │ 20 missões   │ │ 15 missões   │ │ 10 missões   │  │ │
│ │      │ │ 6 competências│ │ 5 competências│ │ 4 competências││ │
│ │      │ │ ░░░░░░░ 0%   │ │ ░░░░░░░ 0%   │ │ ░░░░░░░ 0%   │  │ │
│ │      │ │ [Start]      │ │ [Start]      │ │ [Start]      │  │ │
│ │      │ └──────────────┘ └──────────────┘ └──────────────┘  │ │
│ │      │                                                      │ │
│ │      │ ┌────────────────────────────────────────────────┐    │ │
│ │      │ │ Filters: [All] [Active] [Completed] [Locked]   │    │ │
│ │      │ │ Difficulty: [All] [Easy] [Medium] [Hard]       │    │ │
│ │      │ │ Duration: [All] [<1h] [1-3h] [3h+]            │    │ │
│ │      │ └────────────────────────────────────────────────┘    │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

#### Card Anatomy

```
┌──────────────────────────┐
│  🗡️ Journey Icon          │
│                          │
│  Linux System Admin      │  ← Title
│                          │
│  12 missions             │  ← Metadata
│  4 competencies          │
│                          │
│  ▓▓▓▓▓▓▓▓▓░░░  75%      │  ← Progress bar
│                          │
│  Prerequisites:          │
│  • Basic terminal        │  ← Requirements
│  • Linux installed       │
│                          │
│  🎯 Medium · ⏱️ 8h total │  ← Tags
│  +1200 XP expected       │  ← Reward
│                          │
│  [▶️ Continue]            │  ← CTA
└──────────────────────────┘
```

---

### 2.2 Visualização em Árvore

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Journeys  >  Tree View                👤 Level 5  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │ 🔍 Search journeys...    [Cards] [Tree✓] [Map]       │ │
│ │      │                                                      │ │
│ │      │  🗡️ Linux System Administration                      │ │
│ │      │  ├── 📁 Linux Basics                                 │ │
│ │      │  │   ├── ✅ Mission 1: Terminal Navigation            │ │
│ │      │  │   ├── ✅ Mission 2: File Management                │ │
│ │      │  │   ├── ✅ Mission 3: Package Manager               │ │
│ │      │  │   ├── 🗡️ Mission 4: User Management (Active)      │ │
│ │      │  │   ├── 🔒 Mission 5: Permissions                   │ │
│ │      │  │   └── 🔒 Mission 6: Process Management            │ │
│ │      │  ├── 📁 Network Configuration                        │ │
│ │      │  │   ├── 🔒 Mission 7: Interface Config              │ │
│ │      │  │   ├── 🔒 Mission 8: Firewall Basics               │ │
│ │      │  │   └── 🔒 Mission 9: DNS Setup                    │ │
│ │      │  ├── 📁 Security Hardening                           │ │
│ │      │  │   ├── 🔒 Mission 10: User Security                │ │
│ │      │  │   ├── 🔒 Mission 11: File Integrity               │ │
│ │      │  │   └── 🔒 Mission 12: Audit Logs                  │ │
│ │      │  └── 📁 Advanced Topics                              │ │
│ │      │      └── 🔒 Boss Fight: Full Sys Admin Setup         │ │
│ │      │                                                      │ │
│ │      │  Legend: ✅ Completed  🗡️ Active  🔒 Locked         │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

#### Tree Interaction

| Ação | Comportamento |
|------|---------------|
| Click pasta | Expande/recolhe sub-árvore |
| Click missão | Navega para Mission Workspace |
| Hover missão | Tooltip: nome, duração, XP |
| Drag folder | Reordena (personal view) |
| Right-click | Menu: "Start", "View Details" |

---

### 2.3 Visualização em Mapa

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Journeys  >  Map View                 👤 Level 5  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │ 🔍 Search journeys...    [Cards] [Tree] [Map✓]       │ │
│ │      │                                            [+][−]🔍 │ │
│ │      │                                                      │ │
│ │      │     ┌───────┐                                       │ │
│ │      │     │ START │  ← First node (always completed)      │ │
│ │      │     └───┬───┘                                       │ │
│ │      │         │                                           │ │
│ │      │    ┌────┴────┐                                      │ │
│ │      │    │Terminal │                                      │ │
│ │      │    │  Nav    │  ← Completed nodes (green)           │ │
│ │      │    └────┬────┘                                      │ │
│ │      │         │                                           │ │
│ │      │    ┌────┴────┐        ┌──────────┐                 │ │
│ │      │    │  File   │────────│Package   │                 │ │
│ │      │    │ Mgmt    │        │Manager   │  ← Connected    │ │
│ │      │    └────┬────┘        └────┬─────┘    nodes        │ │
│ │      │         │                 │                         │ │
│ │      │    ┌────┴────┐     ┌──────┴──────┐                 │ │
│ │      │    │  User   │─────│Permissions  │  ← Active path  │ │
│ │      │    │ Admin   │     │             │                  │ │
│ │      │    └────┬────┘     └──────┬──────┘                 │ │
│ │      │         │                 │                         │ │
│ │      │    ┌────┴────┐     ┌──────┴──────┐                 │ │
│ │      │    │ Process │─────│   Network   │  ← Locked nodes │ │
│ │      │    │ Mgmt    │     │   Config    │    (gray)       │ │
│ │      │    └─────────┘     └─────────────┘                 │ │
│ │      │                                                      │ │
│ │      │         ┌──────────────────┐                         │ │
│ │      │         │  🏆 Boss Fight   │  ← Final node (gold)   │ │
│ │      │         │  Full Sys Admin  │                         │ │
│ │      │         └──────────────────┘                         │ │
│ │      │                                                      │ │
│ │      │  Legend: 🟢 Completed  🟡 Active  ⚪ Available       │ │
│ │      │          🔒 Locked  🏆 Boss  🔗 Prerequisite        │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

#### Map Interaction

| Ação | Comportamento |
|------|---------------|
| Click node | Tooltip com detalhes + [Start] |
| Drag canvas | Pan (movimento livre) |
| Scroll | Zoom in/out |
| Double-click node | Navega para Mission Workspace |
| Lines | Show prerequisite connections |

---

## 3. Busca e Filtros

### 3.1 Search Bar

```
┌──────────────────────────────────────────────────────────────┐
│ 🔍 Search journeys, skills, or keywords...              [↵]  │
└──────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- Busca em tempo real (debounce 300ms)
- Resultados filtram cards/tree/map instantaneamente
- Highlight do termo buscado nos resultados

### 3.2 Filter Panel

```
Filters:
  ┌────────────────────────────────────────────┐
  │ Status:     [All] [Active] [Completed] [Locked]   │
  │ Difficulty: [All] [Easy] [Medium] [Hard]          │
  │ Duration:   [All] [<1h] [1-3h] [3h+] [10h+]     │
  │ XP Range:   [Min] ────────────── [Max]           │
  │                                                    │
  │ Tags:  #linux  #security  #cloud  #dev  #ai        │
  │                                                    │
  │ [Clear All]  [Apply]                               │
  └────────────────────────────────────────────────────┘
```

---

## 4. Journey Detail (Clique em um Card)

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Journeys  >  Linux System Administration          │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │  Back to Journeys                    [Cards] [Tree]  │ │
│ │      │                                                      │ │
│ │      │  🗡️ Linux System Administration                       │ │
│ │      │                                                      │ │
│ │      │  ┌─ Overview ─────────────────────────────────────┐  │ │
│ │      │  │ 12 missions · 4 competencies · ~8 hours        │  │ │
│ │      │  │ 🎯 Medium · +1200 XP total                     │  │ │
│ │      │  │                                                │  │ │
│ │      │  │ Prerequisites:                                 │  │ │
│ │      │  │ ✅ Basic terminal knowledge                     │  │ │
│ │      │  │ ✅ Linux installed (VM or WSL)                  │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  ┌─ Competencies Unlocked ────────────────────────┐  │ │
│ │      │  │ 🧠 Linux File Management — Level 2             │  │ │
│ │      │  │ 🧠 User Administration — Level 1 (in progress) │  │ │
│ │      │  │ 🔒 Network Configuration                       │  │ │
│ │      │  │ 🔒 Security Hardening                          │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  ┌─ Missions ─────────────────────────────────────┐  │ │
│ │      │  │ ✅ M1: Terminal Navigation             +100 XP  │  │ │
│ │      │  │ ✅ M2: File Management                +100 XP   │  │ │
│ │      │  │ ✅ M3: Package Manager                +100 XP   │  │ │
│ │      │  │ 🗡️ M4: User Management                +150 XP   │  │ │
│ │      │  │ 🔒 M5: Permissions                    +150 XP   │  │ │
│ │      │  │ 🔒 M6: Process Management             +150 XP   │  │ │
│ │      │  │ 🔒 ...                                            │  │ │
│ │      │  │ 🔒 🏆 Boss Fight: Full Setup          +500 XP   │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  [▶️ Continue Mission]  [📊 View Progress]           │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Estados

| Estado | Comportamento Visual |
|--------|---------------------|
| **Loading** | Skeleton cards (6 placeholders com shimmer) |
| **Empty** | "No journeys found matching your filters" + [Clear Filters] |
| **Error** | "Could not load journeys" + [Retry] |
| **No results** | "No journeys found for 'search term'" + suggestions |

---

## 6. Mobile Adaptation

```
┌──────────────────────────┐
│ 🔷 ASCEND  >  Journeys   │
│ ┌────────────────────────┐│
│ │ 🔍 Search...           ││
│ └────────────────────────┘│
│ [Cards] [Tree] [Map]     │
│                           │
│ ┌────────────────────┐   │
│ │ 🗡️ Linux Sys Admin │   │
│ │ 12 missões · 75%   │   │
│ │ ▓▓▓▓▓▓▓▓▓░░░      │   │
│ │ [Continue]         │   │
│ └────────────────────┘   │
│ ┌────────────────────┐   │
│ │ 🔒 Security        │   │
│ │ Req: Level 3       │   │
│ └────────────────────┘   │
│ ┌────────────────────┐   │
│ │ ☁️ Cloud Engineer  │   │
│ │ 8 missões · 20%    │   │
│ │ [View]             │   │
│ └────────────────────┘   │
│                           │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️       │
└──────────────────────────┘
```

---

## 7. Definition of Done

WF-0002 aprovado quando:

- [ ] Visualização em Cards documentada
- [ ] Visualização em Árvore documentada
- [ ] Visualização em Mapa documentada
- [ ] Card anatomy definida
- [ ] Busca e filtros especificados
- [ ] Pré-requisitos visíveis
- [ ] Dificuldade, tempo, XP, competências visíveis
- [ ] Journey Detail view documentada
- [ ] Estados (loading, empty, error, no results) cobertos
- [ ] Mobile adaptation documentada

---

## Status

**WF-0002 — Journey Explorer**

- Estado: ✅ Completo
- Próximo: WF-0003 — Mission Workspace
