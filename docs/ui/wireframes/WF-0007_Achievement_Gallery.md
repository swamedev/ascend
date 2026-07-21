# WF-0007 — Achievement Gallery

| Campo | Valor |
|-------|-------|
| **ID** | WF-0007 |
| **Nome** | Achievement Gallery |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, UI-0001, UI-0002 |
| **Será utilizado por** | Frontend Sprint 2 |

---

## 1. Propósito

A Achievement Gallery não é uma lista de badges.

É um **museu de conquistas** — um espaço que o Builder visita para sentir orgulho do que construiu.

Cada badge é uma história. Cada nível é um capítulo. Cada certificado é um livro fechado.

---

## 2. Wireframe Desktop

```
┌──────────────────────────────────────────────────────────────────┐
│ 🔷 ASCEND  >  Achievements                         👤 Level 5  │
│ ┌──────┬──────────────────────────────────────────────────────┐ │
│ │      │                                                      │ │
│ │      │  🏅 Badges    📜 Certificates    📊 Level History    │ │
│ │      │                                                      │ │
│ │      │  ┌─ Featured Collection ──────────────────────────┐  │ │
│ │      │  │                                                 │  │ │
│ │      │  │   ┌────────────┐   ┌────────────┐              │  │ │
│ │      │  │   │   🔥       │   │    🗡️      │              │  │ │
│ │      │  │   │ "Consistent"│   │ "Explorer" │   +5 more   │  │ │
│ │      │  │   │  30-day    │   │ First      │   recent     │  │ │
│ │      │  │   │  streak    │   │ mission    │   badges...  │  │ │
│ │      │  │   │   🥇 Gold  │   │   🥈 Silver│              │  │ │
│ │      │  │   └────────────┘   └────────────┘              │  │ │
│ │      │  └─────────────────────────────────────────────────┘  │ │
│ │      │                                                      │ │
│ │      │  ┌─ All Badges ───────────────────────────────────┐  │ │
│ │      │  │                                                   │ │
│ │      │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │ │
│ │      │  │  │ 🌟   │ │ 🔥   │ │ ⚡   │ │ 🛡️   │ │ 📚   │  │ │
│ │      │  │  │ First │ │Consis│ │Speed │ │Securi│ │Schola│  │ │
│ │      │  │  │Steps  │ │tent  │ │Demon │ │ty    │ │r     │  │ │
│ │      │  │  ├──────┤ ├──────┤ ├──────┤ ├──────┤ ├──────┤  │ │
│ │      │  │  │Common│ │Rare  │ │Rare  │ │Epic  │ │Common│  │ │
│ │      │  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │ │
│ │      │  │                                                   │ │
│ │      │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │ │
│ │      │  │  │ 🏆   │ │ 🧠   │ │ 🤖   │ │ 🌐   │ │ 🔒   │  │ │
│ │      │  │  │Expert │ │Mentee │ │Mentor │ │Social│ │Locked│  │ │
│ │      │  │  ├──────┤ ├──────┤ ├──────┤ ├──────┤ ├──────┤  │ │
│ │      │  │  │Epic  │ │Rare  │ │Legend│ │Common│ │🔒    │  │ │
│ │      │  │  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │ │
│ │      │  │                                                   │ │
│ │      │  │  [← Previous]  Page 1 of 3  [Next →]             │ │
│ │      │  └───────────────────────────────────────────────────┘ │
│ │      │                                                      │ │
│ │      │  ┌─ Badge Detail (clique em um badge) ─────────────┐ │ │
│ │      │  │ ┌──────────────────────────────────────────────┐ │ │
│ │      │  │ │                                              │ │ │
│ │      │  │ │           ⚡ "Speed Demon"                    │ │ │
│ │      │  │ │                                              │ │ │
│ │      │  │ │  Completed a mission in under 15 minutes     │ │ │
│ │      │  │ │                                              │ │ │
│ │      │  │ │  🏅 Rarity: Rare                             │ │ │
│ │      │  │ │  📅 Earned: 15 Jul 2026                      │ │ │
│ │      │  │ │  🗡️ Mission: Linux #3 — File Permissions    │ │ │
│ │      │  │ │  📊 5% of builders have this badge           │ │ │
│ │      │  │ │                                              │ │ │
│ │      │  │ │  [Share]  [View Mission]                     │ │ │
│ │      │  │ └──────────────────────────────────────────────┘ │ │
│ │      │  └──────────────────────────────────────────────────┘ │
│ └──────┴──────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. Badge Rarity System

| Rarity | Color | Glow | Border | Label |
|--------|-------|------|--------|-------|
| **Common** | Cinza | Sem glow | Simples | 🟤 Common |
| **Rare** | Azul | Glow sutil | Brand | 🔵 Rare |
| **Epic** | Roxo | Glow médio | Purple | 🟣 Epic |
| **Legendary** | Dourado | Glow intenso | Gold | 🟡 Legendary |
| **Mythic** | Platina | Aurora | Prism | 🤍 Mythic |

---

## 4. Badge States

| State | Visual |
|-------|--------|
| **Earned** | Cor cheia, glow ativo, brilho |
| **Locked** | Silhueta cinza, "🔒" overlay |
| **Hidden** | Silhueta com "?" , "Complete requirements to reveal" |
| **New** | Como earned + pulsing glow + "NEW" tag |
| **Featured** | Tamanho maior, posição de destaque |

---

## 5. Certificates Section

```
┌─ Certificates ──────────────────────────────────────────────┐
│                                                               │
│ ┌────────────────────────────────────────────────────────┐    │
│ │                  📜 CERTIFICATE                         │    │
│ │                  ───────────                            │    │
│ │                                                        │    │
│ │           ASCEND CDF — Competency Certificate           │    │
│ │                                                        │    │
│ │              Linux System Administration                │    │
│ │                    Level: Proficient                    │    │
│ │                                                        │    │
│ │                BuilderName                              │    │
│ │                                                        │    │
│ │    🔗 ascend.dev/cert/a1b2c3          📅 Jul 2026      │    │
│ │                                                        │    │
│ │    [Download PDF]  [Share on LinkedIn]  [Verify]       │    │
│ └────────────────────────────────────────────────────────┘    │
│                                                               │
│ [← Previous]  Page 1 of 1  [Next →]                          │
└───────────────────────────────────────────────────────────────┘
```

---

## 6. Level History Section

```
┌─ Level History ───────────────────────────────────────────┐
│                                                             │
│  Level Timeline                                             │
│                                                             │
│  L5  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  Current           │
│  L4  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  15 Jul 2026       │
│  L3  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        10 Jul 2026       │
│  L2  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓               05 Jul 2026       │
│  L1  ▓▓▓▓▓▓▓▓▓▓▓▓                        01 Jul 2026       │
│                                                             │
│  XP Milestones:                                             │
│  🥉 L1: 100 XP     🥈 L3: 1,000 XP                        │
│  🥇 L5: 5,000 XP  💎 L10: 25,000 XP                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Wireframe Tablet (768px)

```
┌──────────────────────────────────────────────────┐
│ 🔷 Achievements                                   │
│ [Badges] [Certificates] [Level History]           │
│                                                   │
│ ┌─ Featured ───────────────────────────────────┐ │
│ │ [🔥 Consistent]  [🗡️ Explorer]  [+5 more]   │ │
│ └──────────────────────────────────────────────┘ │
│                                                   │
│ ┌─ All Badges ────────────────────────────────┐  │
│ │ [🌟][🔥][⚡][🛡️][📚]                         │  │
│ │ [🏆][🧠][🤖][🌐][🔒]                         │  │
│ └──────────────────────────────────────────────┘  │
│                                                   │
│ Page 1 of 3 [→]                                  │
│                                                   │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️                                 │
└──────────────────────────────────────────────────┘
```

---

## 8. Wireframe Mobile (<768px)

```
┌──────────────────────────┐
│ 🔷 Achievements          │
│                          │
│ [Badges] [Certs] [Levels]│
│                          │
│ ┌─ Featured ──────────┐  │
│ │ 🔥 Consistent       │  │
│ │ 🗡️ Explorer         │  │
│ └─────────────────────┘  │
│                          │
│ ┌─ Badges ────────────┐  │
│ │ 🌟 First Steps      │  │
│ │ 🔥 Consistent       │  │
│ │ ⚡ Speed Demon      │  │
│ │ 🔒 Locked           │  │
│ │ ...                 │  │
│ └─────────────────────┘  │
│                          │
│ 🏠 🗡️ 🧠 🤖 🌐 ⚙️       │
└──────────────────────────┘
```

---

## 9. Badge Unlock Animation

Quando um novo badge é conquistado:

```
0ms      ├── Screen dims slightly
200ms    ├── Badge appears center-screen (scale 0 → 1)
         │   ┌────────────────────┐
         │   │                    │
300ms    │   │   ⚡ Speed Demon   │ ← Glow pulse
         │   │   Earned!          │
         │   │                    │
         │   └────────────────────┘
400ms    ├── Badge glow intensifies
600ms    ├── Rarity border animates in
800ms    ├── Confetti particles (8–12 particles)
1000ms   ├── Text appears: "5% of builders have this"
1200ms   ├── [Share] [Continue] buttons fade in
┌────────┴─────────────────────────────────┐
│ User can dismiss or share                │
└──────────────────────────────────────────┘
```

---

## 10. States

| State | Visual |
|-------|--------|
| **Loading** | Skeleton grid (6 badge placeholders) |
| **Empty** | "No achievements yet. Your first badge awaits!" + [Start Mission] |
| **Error** | "Could not load achievements" + [Retry] |

---

## 11. Motion Timeline

| Component | Animation | Duration | Delay |
|-----------|-----------|----------|-------|
| Gallery enter | `fade-in` | 300ms | 0 |
| Featured badges | `slide-up` | 400ms | 100ms |
| Badge grid | `scale-in` stagger | 200ms each | 300ms |
| Badge detail | `slide-up` + `scale-in` | 300ms | 0 |
| Certificate | `fade-in` + `scale` | 400ms | 100ms |
| Level timeline | `draw` (SVG animate) | 600ms | 200ms |

---

## 12. Definition of Done

WF-0007 aprovado quando:

- [ ] Wireframe Desktop completo com museu/conceito de galeria
- [ ] Badge Rarity System definido
- [ ] Badge States (earned, locked, hidden, new, featured)
- [ ] Certificates section especificada
- [ ] Level History section especificada
- [ ] Badge Unlock Animation especificada
- [ ] Wireframe Tablet completo
- [ ] Wireframe Mobile completo
- [ ] Estados (loading, empty, error) documentados
- [ ] Motion timeline completa

---

## Status

**WF-0007 — Achievement Gallery**

- Estado: ✅ Completo
- Próximo: WF-0008 — AI Mentor
