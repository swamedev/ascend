# WF-0004 — Competency Tree

| Campo | Valor |
|-------|-------|
| **ID** | WF-0004 |
| **Nome** | Competency Tree |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, ARCH-0003, UI-0001 |
| **Será utilizado por** | Frontend Sprint 2 |

---

## 1. Propósito

A Competency Tree é a representação visual do progresso do Builder em cada área de conhecimento.

Inspirada em árvores de habilidade de RPGs (Path of Exile, Final Fantasy), ela transforma habilidades abstratas em um mapa navegável de evolução.

---

## 2. Wireframe Desktop

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Competencies                         👤 Level 5  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │ 🔍 Search competencies...            [+][−] 🔄 Fit  │ │
│ │      │                                                      │ │
│ │      │                 🧠 Linux System Administration       │ │
│ │      │                        Level 2                       │ │
│ │      │                        ▓▓▓▓▓▓▒░░                    │ │
│ │      │                                                      │ │
│ │      │         ┌──────────────┐                             │ │
│ │      │         │   🖥️ File    │                             │ │
│ │      │         │  Management  │─── L2 ▓▓▓▓▓▓▓▓▓▓▓▓▓░░ 85% │ │
│ │      │         └──────┬───────┘                             │ │
│ │      │                │                                     │ │
│ │      │    ┌───────────┴───────────┐                         │ │
│ │      │    │                       │                         │ │
│ │      │ ┌──┴────────┐       ┌──────┴──────┐                  │ │
│ │      │ │    👥     │       │    🔒       │                  │ │
│ │      │ │   User    │       │ Networking  │                  │ │
│ │      │ │ Admin     │─── L1 │ Basics      │─── L0            │ │
│ │      │ │ ▓▓▓▓░░ 45%│       │ ░░░░░░░  0% │                  │ │
│ │      │ └───────────┘       └─────────────┘                  │ │
│ │      │       │                    │                          │ │
│ │      │       │                    │                          │ │
│ │      │ ┌─────┴─────┐      ┌──────┴──────┐                   │ │
│ │      │ │    🔒     │      │    🔒        │                   │ │
│ │      │ │ Process   │      │ Firewall     │                   │ │
│ │      │ │ Mgmt      │─── L0│ Basics       │─── L0             │ │
│ │      │ │ ░░░░░  0% │      │ ░░░░░░░   0% │                   │ │
│ │      │ └───────────┘      └─────────────┘                   │ │
│ │      │                                                      │ │
│ │      │               ┌──────────────────────┐               │ │
│ │      │               │      🔒 Security     │               │ │
│ │      │               │     Hardening        │               │ │
│ │      │               │      ░░░░░░░  0%     │               │ │
│ │      │               │   Requires: L2 in    │               │ │
│ │      │               │   File + User + Net  │               │ │
│ │      │               └──────────────────────┘               │ │
│ │      │                                                      │ │
│ │      │  Legend:                                             │ │
│ │      │  🟢 Dominated (Level 2+)                             │ │
│ │      │  🟡 In Progress                                      │ │
│ │      │  ⚪ Available (prerequisites met)                    │ │
│ │      │  🔒 Locked (prerequisites not met)                   │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Node Anatomy

Cada nó da árvore segue esta estrutura:

```
┌──────────────────┐
│  🖥️ File         │  ← Icon + Name
│  Management      │
│                  │
│  Level 2         │  ← Current level
│  ▓▓▓▓▓▓▓▓▓░░ 85%│  ← Progress to next
│                  │
│  4/5 missions    │  ← Evidence count
│  +450 XP earned  │  ← Total XP
└──────────────────┘
```

---

## 4. Node States

| State | Visual | Descrição |
|-------|--------|-----------|
| **Locked** | 🔒 Cinza, sem brilho, conectores pontilhados | Pré-requisitos não atendidos |
| **Available** | ⚪ Contorno sutil, brilho suave, conector sólido | Pode iniciar |
| **In Progress** | 🟡 Borda brand, glow amarelo, parcialmente preenchido | Missões ativas |
| **Dominated** | 🟢 Brilho verde, preenchimento completo, badge de nível | Nível máximo atingido |

### 4.1 Locked Node

```
┌──────────────────┐
│  🔒              │
│  Networking      │
│  Basics          │
│                  │
│  Requires:       │
│  File Mgmt L1    │
│  User Admin L1   │
│  ░░░░░░░░░  0%   │
│                  │
│  🔒 Locked       │
└──────────────────┘
```

### 4.2 Available Node

```
┌──────────────────┐
│  ⚪              │
│  Process Mgmt    │
│                  │
│  ░░░░░░░░░  0%   │
│                  │
│  [▶️ Start]      │
└──────────────────┘
```

### 4.3 In Progress Node

```
┌──────────────────┐
│  🟡              │
│  User Admin      │
│                  │
│  Level 1         │
│  ▓▓▓▓░░░░  45%   │
│                  │
│  2/5 missions    │
│  +200 XP         │
│                  │
│  [▶️ Continue]   │
└──────────────────┘
```

### 4.4 Dominated Node

```
┌──────────────────┐
│  🟢 🏆           │
│  File            │
│  Management      │
│                  │
│  Level 3         │
│  MAXED ▓▓▓▓ 100% │
│                  │
│  5/5 missions    │
│  +750 XP         │
│                  │
│  Dominated       │
└──────────────────┘
```

---

## 5. Node Transitions (Animações)

| Transition | Animação | Duration | Trigger |
|------------|----------|----------|---------|
| Locked → Available | Glow pulse, conector solidifica | 500ms | Prerequisite complete |
| Available → In Progress | Scale bounce + brand fill | 400ms | First mission started |
| In Progress → Dominated | Celebration burst + green fill | 600ms | Last mission complete |
| Level up (within Progress) | XP bar fills, number increments | 300ms | Sufficient XP |

### 5.1 Node Connection Lines

| State | Visual | Animação |
|-------|--------|----------|
| Locked | `┄┄┄` (dashed, gray) | Static |
| Available | `───` (solid, dim) | Static |
| In Progress | `═══` (solid, brand) | Pulse glow |
| Dominated | `═══` (solid, green) | Static glow |

---

## 6. Interaction

| Ação | Comportamento |
|------|---------------|
| **Click node** | Select + show detail sidebar |
| **Hover node** | Tooltip: nome, level, progress, XP |
| **Double-click node** | Open competencies detail view |
| **Drag canvas** | Pan movement |
| **Scroll** | Zoom in/out (0.5x–2x) |
| **Ctrl+Click** | Multi-select for comparison |
| **Right-click** | Context menu: "Start mission", "View evidence" |

### 6.1 Detail Sidebar (ao clicar no nó)

```
┌────────────────────────────────┐
│ 🖥️ File Management             │
│                                │
│ Level 2 · ▓▓▓▓▓▓▓▓▓░░  85%   │
│                                │
│ ┌─ Progress ────────────────┐  │
│ │ ✅ M1: Navigate file sys  │  │
│ │ ✅ M2: Create/edit files  │  │
│ │ ✅ M3: Permissions        │  │
│ │ ✅ M4: Find/grep          │  │
│ │ 🗡️ M5: File archiving     │  │
│ └────────────────────────────┘  │
│                                │
│ ┌─ Evidence ────────────────┐  │
│ │ 📄 report-m1.md  ✅      │  │
│ │ 📄 evidence-m2.log ✅    │  │
│ │ 📄 m3-script.sh   ✅     │  │
│ │ 📄 m4-output.txt  ✅     │  │
│ └────────────────────────────┘  │
│                                │
│ ⏱️ 4h total  ·  +750 XP       │
│                                │
│ [▶️ Continue Mission]          │
└────────────────────────────────┘
```

---

## 7. Wireframe Tablet (768px)

```
┌──────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Competencies                       │
│ ┌────────────────────────────────────────────────┐│
│ │ 🔍 Search...                        [+][−]   ││
│ └────────────────────────────────────────────────┘│
│                                                    │
│ 🧠 Linux System Administration — Level 2           │
│                                                    │
│ ┌────────────────────────────────────────────────┐ │
│ │ 🖥️ File Mgmt    ─── 👥 User Admin              │ │
│ │ L2 ▓▓▓▓▓ 85%    │    L1 ▓▓▓▓  45%              │ │
│ │                  │                              │ │
│ │ 🔒 Networking   │    🔒 Process Mgmt           │ │
│ │ L0 ░░░░░  0%    │    L0 ░░░░░  0%              │ │
│ │                  │                              │ │
│ │ 🔒 Firewall     │    🔒 Security Hardening     │ │
│ │ L0 ░░░░░  0%   │    L0 ░░░░░  0%              │ │
│ └────────────────────────────────────────────────┘ │
│                                                    │
│ Legend: 🟢 🟡 ⚪ 🔒                                │
│                                                    │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️                                  │
└──────────────────────────────────────────────────┘
```

---

## 8. Wireframe Mobile (<768px)

```
┌──────────────────────────┐
│ 🔷 Competencies          │
│ ┌────────────────────────┐│
│ │ 🔍 Search...          ││
│ └────────────────────────┘│
│                           │
│ 🧠 Linux Sys Admin L2    │
│                           │
│ ┌────────────────────────┐│
│ │ 🖥️ File Mgmt   L2 85%││
│ │ 👥 User Admin  L1 45%││
│ │ 🔒 Networking   L0 0%││
│ │ 🔒 Process Mgmt L0 0%││
│ │ 🔒 Firewall     L0 0%││
│ │ 🔒 Security     L0 0%││
│ └────────────────────────┘│
│                           │
│ 🟢 🟡 ⚪ 🔒              │
│                           │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️       │
└──────────────────────────┘
```

Mobile: árvore simplificada para lista vertical com indicadores de progresso.

---

## 9. Heatmap de Atenção

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                              🧠                                  │
│                          █████████                               │
│                                                                  │
│       █████████                ███████████                       │
│       █████████                ███████████                       │
│            ██                       ██                           │
│       █████████                ███████████                       │
│       █████████                ███████████                       │
│            ██                       ██                           │
│            ██                       ██                           │
│       █████████                ███████████                       │
│       █████████                ███████████                       │
│                                                                  │
│               █████████████████████████                          │
│               █████████████████████████                          │
│                                                                  │
│                                                                  │
│  ██ = Maximum attention (center nodes, in-progress)             │
│  ░░ = Peripheral attention (locked nodes)                       │
└──────────────────────────────────────────────────────────────────┘
```

---

## 10. Motion Timeline

| Component | Animation | Duration | Easing | Delay |
|-----------|-----------|----------|--------|-------|
| Tree background | `fade-in` | 300ms | ease-out | 0 |
| Nodes | `scale-in` stagger | 200ms each | ease-spring | 100ms |
| Connections | `draw-line` | 400ms | ease-out | 200ms |
| Node hover | `scale(1.05)` + glow | 150ms | ease-out | 0 |
| Node select | `scale(1.1)` + detail slide | 300ms | ease-out | 0 |
| Node complete | burst + fill | 600ms | ease-spring | — |
| Zoom | smooth transform | 200ms | ease-out | 0 |

---

## 11. Definition of Done

WF-0004 aprovado quando:

- [ ] Wireframe Desktop completo com árvore navegável
- [ ] Node anatomy definida
- [ ] 4 estados de nó (locked, available, in progress, dominated)
- [ ] Visual de cada estado especificado
- [ ] Node transitions (animações) documentadas
- [ ] Connection line states documentados
- [ ] Interações (click, hover, drag, zoom) definidas
- [ ] Detail sidebar especificada
- [ ] Wireframe Tablet completo
- [ ] Wireframe Mobile completo
- [ ] Heatmap de atenção gerado
- [ ] Motion timeline completa

---

## Status

**WF-0004 — Competency Tree**

- Estado: ✅ Completo
- Próximo: WF-0005 — Builder Profile
