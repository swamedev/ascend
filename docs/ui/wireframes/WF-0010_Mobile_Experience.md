# WF-0010 — Mobile Experience

| Campo | Valor |
|-------|-------|
| **ID** | WF-0010 |
| **Nome** | Mobile Experience |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, UI-0001, UI-0002, UI-0003 |
| **Será utilizado por** | Frontend Sprint 4+ |

---

## 1. Propósito

A Experiência Mobile do ASCEND não é uma adaptação do desktop.

É um **projeto Mobile First** que repensa cada fluxo para a tela pequena.

Enquanto o desktop é o ambiente de trabalho, o mobile é o ambiente de:

- **Micro-learning** — missões curtas de 5-15 min
- **Streak maintenance** — manter o hábito diário
- **Progress check** — ver evolução rapidamente
- **Notifications** — saber quando algo acontece
- **Community** — interagir com outros Builders

---

## 2. Navigation Structure

### 2.1 Bottom Tab Bar

```
┌──────────────────────────────────────┐
│                                      │
│                                      │
│           (Content Area)             │
│                                      │
│                                      │
├──────────────────────────────────────┤
│                                      │
│  🏠    🗡️     🧠     🤖    ☰       │
│ Home  Missions  Comp.  Mentor More   │
└──────────────────────────────────────┘
```

### 2.2 More Sheet

```
┌──────────────────────────────────────┐
│                                      │
│  ☰ More                              │
│                                      │
│  🏅 Achievements                     │
│  📁 Evidence                         │
│  ⚗️ Labs                             │
│  🌐 Community                        │
│  👤 My Profile                       │
│  🛒 Marketplace                      │
│  ⚙️ Settings                         │
│                                      │
│  ─────────────────────────────────   │
│                                      │
│  👤 BuilderName                      │
│  Level 5  •  450/800 XP              │
│                                      │
└──────────────────────────────────────┘
```

---

## 3. Core Flows

### 3.1 Daily Login Flow

```
┌──────────────────────────┐
│ 🔷 ASCEND                │
│                          │
│    ┌───────────┐         │
│    │ Level 5   │         │
│    │ 450/800   │         │
│    │ 🔥 7-day  │         │
│    └───────────┘         │
│                          │
│  🔥 Day 7! Keep going!  │
│                          │
│  ┌────────────────────┐  │
│  │ 🗡️ Continue Mission │  │
│  │ Linux #4 — 65%     │  │
│  │ [▶️ Resume]         │  │
│  └────────────────────┘  │
│                          │
│  ┌────────────────────┐  │
│  │ 💡 Mentor: Dica     │  │
│  │ rápida para hoje   │  │
│  └────────────────────┘  │
│                          │
│  🏠  🗡️  🧠  🤖  ☰    │
└──────────────────────────┘
```

### 3.2 Mission Flow

```
┌──────────────────────────┐    ┌──────────────────────────┐
│ 🗡️ Linux #4              │    │ 🗡️ Mission #4            │
│                          │    │                          │
│ "Configurar usuários     │    │ ┌─ Objective ──────────┐ │
│  Linux"                  │    │ │ Create 3 users...    │ │
│                          │    │ └──────────────────────┘ │
│ ⏱️ 35:42 · 🎯 Medium    │    │                          │
│                          │    │ ┌─ Notes ─────────────┐ │
│ ┌────────────────────┐   │ →  │ │ $ sudo useradd ...  │ │
│ │ ▶️ Start Mission    │   │    │ │                     │ │
│ │ (opens focus mode)  │   │    │ └────────────────────┘ │
│ └────────────────────┘   │    │                          │
│                          │    │ [📁 Add Evidence]        │
│ 🏠  🗡️  🧠  🤖  ☰      │    │                          │
└──────────────────────────┘    │ 🏠  🗡️  🧠  🤖  ☰      │
                                └──────────────────────────┘

        ┌──────────────────────────┐    ┌──────────────────────────┐
        │ 📁 Submit Evidence        │    │ ✅ Mission Complete!     │
        │                          │    │                          │
        │ 📎 commands.log    ✓     │    │ +150 XP                  │
        │ 📎 report.md       ✓     │    │                          │
        │ 📎 screenshot.png  ✓     │    │ Score: 92/100            │
        │                          │    │                          │
        │ 📝 Description:          │    │ "Excellent work!"        │
        │ "Created 3 users..."     │    │                          │
        │                          │    │ [▶️ Next] [🏅 Badges]    │
        │ [📤 Submit]              │    │                          │
        │                          │    │ 🏠  🗡️  🧠  🤖  ☰      │
        │ 🏠  🗡️  🧠  🤖  ☰      │    └──────────────────────────┘
        └──────────────────────────┘
```

### 3.3 Competency Check Flow

```
┌──────────────────────────┐    ┌──────────────────────────┐
│ 🧠 Competencies          │    │ 🖥️ File Management        │
│                          │    │                          │
│ 🧠 Linux Sys Admin      │    │ Level 2 · 85%            │
│                          │    │ ▓▓▓▓▓▓▓▓▓░░              │
│ ┌────────────────────┐   │    │                          │
│ │ 🖥️ File Mgmt  85%  │   │    │ ✅ M1: Navigate         │
│ │ 👥 User Admin 45%  │   │ →  │ ✅ M2: Create files     │
│ │ 🔒 Network     0%  │   │    │ ✅ M3: Permissions      │
│ │ 🔒 Security    0%  │   │    │ ✅ M4: Find             │
│ └────────────────────┘   │    │ 🗡️ M5: Archive          │
│                          │    │                          │
│ 🏠  🗡️  🧠  🤖  ☰      │    │ [▶️ Continue M5]         │
└──────────────────────────┘    │                          │
                                │ 🏠  🗡️  🧠  🤖  ☰      │
                                └──────────────────────────┘
```

### 3.4 Achievement Unlock Flow

```
┌──────────────────────────┐
│                          │
│      ⚡ Speed Demon      │
│                          │
│   ┌────────────────┐    │
│   │   ★  ★  ★      │    │
│   │   ★  ⚡  ★      │    │
│   │   ★  ★  ★      │    │
│   └────────────────┘    │
│                          │
│   New Badge Earned!      │
│                          │
│   "Complete a mission    │
│    in under 15 min"      │
│                          │
│   🔵 Rare · 5% of       │
│   builders have this    │
│                          │
│   [Continue] [Share]     │
│                          │
└──────────────────────────┘
```

---

## 4. Mobile-Specific Features

### 4.1 Quick Mission (5 min)

Missões super curtas para manter streak em dias ocupados.

```
┌──────────────────────────┐
│ ⚡ Quick Mission          │
│                          │
│ "List 3 Linux commands   │
│  you learned this week   │
│  and what they do."      │
│                          │
│ ⏱️ 5 min · +25 XP       │
│                          │
│ ┌────────────────────┐   │
│ │ Type your answer... │   │
│ └────────────────────┘   │
│                          │
│ [Submit Quick Mission]   │
└──────────────────────────┘
```

### 4.2 Push Notifications

| Evento | Notification | Timing |
|--------|-------------|--------|
| Streak reminder | "🔥 Don't lose your 7-day streak!" | Morning (8AM) |
| Review complete | "📁 Evidence #24 has been reviewed" | Instant |
| Achievement | "🏅 New badge: Speed Demon!" | Instant |
| Level up | "🎉 You reached Level 6!" | Instant |
| Mentor tip | "💡 Mentor has a suggestion for you" | Periodic |
| Inactivity | "👋 We miss you! Your progress is waiting" | 24h idle |
| Community | "🌐 BuilderOne completed a new mission" | Periodic |

### 4.3 Offline Mode

| Feature | Offline behavior |
|---------|-----------------|
| Missions | Read cached missions, mark progress offline |
| Evidence | Queue upload, sync when online |
| Competencies | View cached tree |
| Profile | View cached profile |
| Achievements | View cached gallery |
| Mentor | Not available (show "offline" state) |

---

## 5. Mobile Interaction Patterns

### 5.1 Gestures

| Gesture | Action |
|---------|--------|
| Swipe right | Go back / reveal sidebar |
| Swipe left | Next item in list |
| Long press | Context menu |
| Pull down | Refresh |
| Double tap | Scroll to top |
| Pinch | Zoom (competency tree) |

### 5.2 Haptic Feedback

| Event | Haptic |
|-------|--------|
| Mission complete | Success tap |
| Achievement | Notification burst |
| Error | Error tap |
| Navigation | Light tap |
| Submission | Medium tap |

---

## 6. Responsive Breakpoints

| Name | Width | Layout |
|------|-------|--------|
| **Phone narrow** | <400px | Single column, compact |
| **Phone wide** | 400-767px | Single column, normal |
| **Tablet small** | 768-1023px | Two column, tab bar |
| **Tablet large** | 1024-1279px | Two column, sidebar |
| **Desktop** | 1280px+ | Full layout |

---

## 7. Motion Timeline

| Component | Animation | Duration | Easing |
|-----------|-----------|----------|--------|
| Tab switch | cross-fade | 200ms | ease-out |
| Sheet open | slide-up | 300ms | ease-out |
| Sheet close | slide-down | 200ms | ease-in |
| Mission start | scale + slide | 300ms | ease-out |
| Notification | slide-down | 250ms | ease-out |
| Swipe back | follow gesture | dynamic | spring |

---

## 8. Performance Targets

| Metric | Target |
|--------|--------|
| App launch (cold) | < 2s |
| App launch (warm) | < 1s |
| Page transition | < 300ms |
| Mission load | < 1.5s |
| Scroll fps | 60fps |
| Offline sync | < 5s |

---

## 9. Definition of Done

WF-0010 aprovado quando:

- [ ] Bottom tab navigation definida
- [ ] More sheet especificada
- [ ] Daily login flow completo
- [ ] Mission flow completo
- [ ] Competency check flow completo
- [ ] Achievement unlock flow completo
- [ ] Quick Mission feature especificada
- [ ] Push notifications mapeadas
- [ ] Offline mode definido
- [ ] Gestos e haptics especificados
- [ ] Breakpoints responsivos definidos
- [ ] Motion timeline completa
- [ ] Performance targets estabelecidos

---

## Status

**WF-0010 — Mobile Experience**

- Estado: ✅ Completo
- Próximo: Frontend Implementation — Sprint 1
