# WF-0006 — Evidence Center

| Campo | Valor |
|-------|-------|
| **ID** | WF-0006 |
| **Nome** | Evidence Center |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, ARCH-0003, UI-0001, UI-0003 |
| **Será utilizado por** | Frontend Sprint 3 |

---

## 1. Propósito

O Evidence Center é o repositório central de todas as evidências que o Builder já submeteu.

Aqui ele pode:

- Ver todas as evidências em um só lugar
- Acompanhar status de cada submissão
- Ler feedback de revisões
- Re-enviar evidências rejeitadas
- Acessar anexos e histórico completo

---

## 2. Wireframe Desktop

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Evidence                             👤 Level 5  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │ 🔍 Search evidence...                                │ │
│ │      │                                                      │ │
│ │      │ [All] [Pending] [Approved] [Rejected] [+ Filter]     │ │
│ │      │                                                      │ │
│ │      │ ┌──────────────────────────────────────────────────┐ │ │
│ │      │ │ 📁 Evidence #24 — Linux #4: User Management      │ │ │
│ │      │ │ 🟡 Pending Review · Submitted 2h ago             │ │ │
│ │      │ │ 📎 commands.log  report.md  screenshot.png       │ │ │
│ │      │ │ 📝 "Created 3 users with specific permissions..." │ │ │
│ │      │ └──────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │ ┌──────────────────────────────────────────────────┐ │ │
│ │      │ │ 📁 Evidence #23 — Linux #3: File Permissions     │ │ │
│ │      │ │ 🟢 Approved · Reviewed 1d ago · Score: 92/100    │ │ │
│ │      │ │ 📎 script.sh  output.txt                         │ │ │
│ │      │ │ 📝 "Permissions configured correctly..."         │ │ │
│ │      │ │ 💬 "Good work! Consider adding sticky bit."      │ │ │
│ │      │ └──────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │ ┌──────────────────────────────────────────────────┐ │ │
│ │      │ │ 📁 Evidence #22 — Linux #2: File Management      │ │ │
│ │      │ │ 🔴 Rejected · Reviewed 2d ago                    │ │ │
│ │      │ │ 📎 commands.log                                  │ │ │
│ │      │ │ 💬 "Missing explanation of commands used."       │ │ │
│ │      │ │ [🔄 Resubmit]                                    │ │ │
│ │      │ └──────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │ ┌──────────────────────────────────────────────────┐ │ │
│ │      │ │ 📁 Evidence #21 — Linux #1: Terminal Navigation  │ │ │
│ │      │ │ 🟢 Approved · Reviewed 5d ago · Score: 88/100    │ │ │
│ │      │ │ 📎 terminal.log  notes.md                        │ │ │
│ │      │ │ 💬 "Navigation commands correct. Well done!"     │ │ │
│ │      │ └──────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │ [← Previous]  Page 1 of 4  [Next →]                 │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Evidence Card Anatomy

```
┌──────────────────────────────────────────────────────────────────┐
│ 📁 Evidence #24 — Linux #4: User Management                     │
│ 🟡 Pending Review · Submitted 2h ago                            │
│                                                                  │
│ 📎 Attachments (3):                                              │
│   [📄 commands.log]  [📄 report.md]  [🖼️ screenshot.png]       │
│                                                                  │
│ 📝 Description:                                                  │
│ "Created 3 users with specific permissions using useradd        │
│  and usermod. Developer user granted sudo access.               │
│  Guest user restricted to /sbin/nologin."                       │
│                                                                  │
│ Score: — (pending review)                                       │
│ Feedback: —                                                     │
│                                                                  │
│ [📋 View Full]                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Evidence Detail View (clique em "View Full")

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Evidence  >  Evidence #24                         │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │  ← Back to Evidence Center                           │ │
│ │      │                                                      │ │
│ │      │  📁 Evidence #24 — Linux #4                          │ │
│ │      │  Status: 🟡 Pending Review                           │ │
│ │      │                                                      │ │
│ │      │  ┌─ Submission Details ────────────────────────────┐ │ │
│ │      │  │ Mission: Linux #4 — User Management             │ │ │
│ │      │  │ Submitted: 2 hours ago                          │ │ │
│ │      │  │ Journey: Linux System Administration             │ │ │
│ │      │  │ Format: Mixed (code + document)                  │ │ │
│ │      │  └────────────────────────────────────────────────┘ │ │
│ │      │                                                      │ │
│ │      │  ┌─ Description ──────────────────────────────────┐  │ │
│ │      │  │ Created 3 users with specific permissions      │  │ │
│ │      │  │ using useradd and usermod...                    │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  ┌─ Attachments ──────────────────────────────────┐  │ │
│ │      │  │ 📄 commands.log          [Preview] [Download]  │  │ │
│ │      │  │ 📄 report.md             [Preview] [Download]  │  │ │
│ │      │  │ 🖼️ screenshot.png        [View]   [Download]  │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  ┌─ Review (when available) ──────────────────────┐  │ │
│ │      │  │ Status: Pending                                 │  │ │
│ │      │  │ Estimated: ~5 minutes                           │  │ │
│ │      │  └────────────────────────────────────────────────┘  │ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 5. Evidence Status & Colors

| Status | Icon | Color | Ação do Builder |
|--------|------|-------|-----------------|
| **Pending** | 🟡 | Amber | Aguardar |
| **Under Review** | 🔄 | Blue | (automático) |
| **Approved** | 🟢 | Green | Seguir para próxima missão |
| **Rejected** | 🔴 | Red | [Resubmit] com base no feedback |
| **Draft** | ⚪ | Gray | [Continue editing] |

---

## 6. Feedback Display

### 6.1 Approved Feedback

```
💬 Review Feedback
Score: 92/100

✅ Accuracy: 95% — Commands are precise and correct
✅ User creation: 100% — All users created correctly
✅ Documentation: 85% — Clear, could add more edge cases
✅ Explanation: 90% — Good reasoning

"Excellent work. Your command usage is precise. 
Consider adding notes about troubleshooting next time."
```

### 6.2 Rejected Feedback

```
💬 Review Feedback
Score: 45/100

❌ Accuracy: 40% — Some commands have syntax errors
❌ Documentation: 30% — Missing explanations
❌ Evidence incomplete: Missing screenshots

"Please review the command syntax and add 
documentation explaining each step. 
Resubmit when ready."
```

---

## 7. Wireframe Tablet (768px)

```
┌──────────────────────────────────────────────────┐
│ 🔷 Evidence                                      │
│ ┌──────────────────────────────────────────────┐ │
│ │ 🔍 Search...                                 │ │
│ │ [All] [Pending] [Approved] [Rejected]        │ │
│ └──────────────────────────────────────────────┘ │
│                                                   │
│ ┌──────────────────────────────────────────────┐ │
│ │ 📁 #24 — Linux #4            🟡 Pending 2h  │ │
│ │ 📎 commands.log report.md screenshot.png    │ │
│ └──────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────┐ │
│ │ 📁 #23 — Linux #3            🟢 Approved 1d │ │
│ │ Score: 92/100  📎 script.sh output.txt      │ │
│ └──────────────────────────────────────────────┘ │
│ ┌──────────────────────────────────────────────┐ │
│ │ 📁 #22 — Linux #2            🔴 Rejected 2d │ │
│ │ 💬 "Missing explanation..." [Resubmit]       │ │
│ └──────────────────────────────────────────────┘ │
│                                                   │
│ Page 1 of 4 [→]                                  │
│                                                   │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️                                 │
└──────────────────────────────────────────────────┘
```

---

## 8. Wireframe Mobile (<768px)

```
┌──────────────────────────┐
│ 🔷 Evidence              │
│ 🔍 Search...             │
│                          │
│ [All] [Pending] [Approved]│
│                          │
│ ┌──────────────────────┐ │
│ │ 📁 #24 — Linux #4    │ │
│ │ 🟡 Pending · 2h ago  │ │
│ │ 3 files attached     │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 📁 #23 — Linux #3    │ │
│ │ 🟢 Approved · 92%    │ │
│ │ 2 files              │ │
│ └──────────────────────┘ │
│ ┌──────────────────────┐ │
│ │ 📁 #22 — Linux #2    │ │
│ │ 🔴 Rejected          │ │
│ │ [Resubmit]           │ │
│ └──────────────────────┘ │
│                          │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️       │
└──────────────────────────┘
```

---

## 9. States

| State | Visual |
|-------|--------|
| **Loading** | Skeleton cards (5 items, shimmer) |
| **Empty (no evidence)** | "No evidence yet. Start a mission to submit your first evidence." + [Explore Missions] |
| **Empty (filtered)** | "No evidence matching your filters." + [Clear Filters] |
| **Error** | "Could not load evidence." + [Retry] |

---

## 10. Motion Timeline

| Component | Animation | Duration | Delay |
|-----------|-----------|----------|-------|
| Page enter | `fade-in` | 200ms | 0 |
| Filter pills | `slide-down` | 200ms | 100ms |
| Evidence cards | `slide-up` stagger | 250ms each | 200ms |
| Status badge | `scale-in` | 200ms | 300ms per card |
| Detail view | `slide-right` | 300ms | 0 |
| Resubmit button | `pulse` (if rejected) | infinite | 1s loop |

---

## 11. Definition of Done

WF-0006 aprovado quando:

- [ ] Wireframe Desktop completo
- [ ] Evidence Card anatomy definida
- [ ] Evidence Detail View especificada
- [ ] Status e cores documentados
- [ ] Feedback display (approved/rejected) especificado
- [ ] Wireframe Tablet completo
- [ ] Wireframe Mobile completo
- [ ] Estados (loading, empty, filtered, error) documentados
- [ ] Motion timeline completa

---

## Status

**WF-0006 — Evidence Center**

- Estado: ✅ Completo
- Próximo: WF-0007 — Achievement Gallery
