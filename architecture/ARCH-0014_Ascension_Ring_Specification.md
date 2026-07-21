# ARCH-0014 — Ascension Ring Specification

| Field | Value |
|-------|-------|
| **ID** | ARCH-0014 |
| **Name** | Ascension Ring Specification |
| **Versão** | 1.0 |
| **Status** | Draft |
| **Categoria** | Architecture |
| **Owner** | Chief Architect |
| **Derivado de** | ARCH-0011 Experience Layer, ARCH-0013 Product Behavior Architecture, UI-0001 Design System, UI-0002 Builder Journey |
| **Será utilizado por** | Frontend Implementation, UI-0004 Component Library |

---

## 1. Purpose

The **Ascension Ring** is the signature visual component of ASCEND.

It is a living circle that communicates the Builder's complete state in a single glance: level, XP, competencies, streak, and achievements.

This document defines its mathematics, animations, colors, states, accessibility, component API, and future evolution.

---

## 2. Concept

```
                    ┌────────────────────┐
                    │   OUTER RING       │
                    │  Achievement glow  │
                    │  (golden pulse)    │
                    │                    │
              ┌─────┴────────────────────┴─────┐
              │   STREAK RING                  │
              │   🔥 Active streak indicator   │
              │   (orange glow when active)    │
              │                                │
              │   ┌────────────────────────┐   │
              │   │  COMPETENCY RING        │   │
              │   │  Small icons orbiting   │   │
              │   │  Active competencies    │   │
              │   │                        │   │
              │   │   ┌────────────────┐   │   │
              │   │   │   LEVEL CORE   │   │   │
              │   │   │    Number      │   │   │
              │   │   │   "Level 5"    │   │   │
              │   │   └────────────────┘   │   │
              │   │                        │   │
              │   │   ┌────────────────┐   │   │
              │   │   │   XP METER     │   │   │
              │   │   │   450 / 800    │   │   │
              │   │   │   ▓▓▓▓▓▓░░░   │   │   │
              │   │   └────────────────┘   │   │
              │   └────────────────────────┘   │
              └────────────────────────────────┘
```

---

## 3. Layer Architecture

| Layer | Z-index | Content | Visual |
|-------|---------|---------|--------|
| **L0 — Core** | 0 | Level number + XP text | Center text, bold |
| **L1 — XP Arc** | 1 | Circular progress bar | SVG arc, purple gradient |
| **L2 — Competency Orbit** | 2 | Competency icons (2–6) | Small icons in orbit |
| **L3 — Streak Ring** | 3 | Streak indicator | Orange ring segment |
| **L4 — Achievement Glow** | 4 | Achievement border glow | Golden radial gradient |

---

## 4. Mathematics

### 4.1 Sizes

| Variant | Diameter (px) | Core size | Arc width | Icon size |
|---------|---------------|-----------|-----------|-----------|
| `xs` | 48 | 16px text | 3px | — |
| `sm` | 80 | 24px text | 4px | 12px |
| `md` | 120 | 36px text | 6px | 16px |
| `lg` | 180 | 52px text | 8px | 20px |
| `xl` | 240 | 72px text | 10px | 24px |

### 4.2 XP Arc Calculation

```
Circumference = 2 * π * radius
Arc length = Circumference * (xp_current / xp_max)
Stroke-dasharray = arc_length, circumference
Rotation = -90deg (start from top)
```

### 4.3 Competency Orbit Positions

Competency icons are positioned evenly around the ring:

```
angle(i) = (360 / count) * i
x(i) = center_x + orbit_radius * cos(angle(i))
y(i) = center_y + orbit_radius * sin(angle(i))
```

Where `orbit_radius = ring_diameter * 0.35`.

Max 6 competencies shown. If more exist, show the 6 most active.

### 4.4 Streak Ring Segment

```
streak_angle = min(streak_days / 365 * 360, 360)
```

Full circle = 365-day streak. Partial = current progress.

---

## 5. Colors

### 5.1 Default Palette

| Element | Light | Dark | Gradient |
|---------|-------|------|----------|
| XP Arc fill | `#3366FF` | `#6699FF` | `linear-gradient(90deg, #3366FF, #A855F7)` |
| XP Arc background | `#E2E8F0` | `#333842` | Solid |
| Level number | `#0F172A` | `#E1E5EB` | Solid |
| XP text | `#64748B` | `#646A78` | Solid |
| Streak inactive | `#CBD5E1` | `#4A4F5C` | Solid |
| Streak active | `#F59E0B` | `#FBBF24` | `radial-gradient(#F59E0B, #EF4444)` |
| Streak fire | `#EF4444` | `#F87171` | Solid |
| Achievement glow | `rgba(245, 158, 11, 0.15)` | `rgba(251, 191, 36, 0.2)` | Radial |
| Competency dot | `#3366FF` | `#6699FF` | Solid |

### 5.2 State Colors

| State | XP Arc | Glow |
|-------|--------|------|
| Idle | Brand | None |
| XP gained | Bright purple pulse | Soft purple glow |
| Level up | Gold → brand transition | Golden burst |
| Streak milestone | Orange pulse | Orange glow |
| Achievement | Brand | Golden glow pulse |

---

## 6. Animations

### 6.1 Animation Registry

| ID | Name | Trigger | Duration | Easing | Description |
|----|------|---------|----------|--------|-------------|
| `A1` | `ring-idle` | Always (when visible) | 3s loop | ease-in-out | Subtle breathing: scale 1→1.02→1, opacity 1→0.95→1 |
| `A2` | `xp-fill` | XP earned | 600ms | ease-out | Arc fills from current to new value, counter increments |
| `A3` | `level-up` | Level threshold | 800ms | ease-spring | Ring expands 1→1.15→1, number scale-up, golden burst |
| `A4` | `streak-pulse` | Streak milestone | 400ms | ease-out | Streak arc pulses 3 times |
| `A5` | `achievement-glow` | New badge | 500ms | ease-out | Golden glow fades in, holds 2s, fades to idle |
| `A6` | `competency-enter` | New competency | 500ms | ease-spring | Icon slides into orbit with pop |
| `A7` | `ring-enter` | Component mount | 400ms | ease-out | Ring scales 0→1, arc draws clockwise |
| `A8` | `streak-fire` | Streak active | 1s loop | ease-in-out | Flame icon flickers (opacity 0.8→1) |

### 6.2 Animation Constraints

| Constraint | Rule |
|------------|------|
| **Reduced motion** | All animations disabled, instant state transition |
| **Concurrent animations** | Max 2 animations running simultaneously |
| **Priority** | Level up > Achievement > XP > Streak > Idle |
| **Queue** | If multiple triggers: queue and play sequentially |

---

## 7. States

### 7.1 Complete State Matrix

| State | XP Arc | Level | Streak | Competency | Glow |
|-------|--------|-------|--------|------------|------|
| **Empty** (new user) | 0%, gray | "1" | Hidden | Hidden | None |
| **Idle** | Current % | Current | Static dots | Icons visible | None |
| **XP gained** | Animated fill | Same | Static | Static | Soft purple |
| **Level up** | Full, gold | Animated +1 | Static | Static | Golden burst |
| **Streak day** | Same | Same | +1 dot, pulse | Same | Orange flicker |
| **Achievement** | Same | Same | Same | Same | Golden glow 2s |
| **Streak lost** | Same | Same | Reset, dim | Same | None |
| **Error** | 0%, red | "?" | Hidden | Hidden | Red glow |

### 7.2 Empty State (New Builder)

```
          ┌────┐
          │  1 │   Level 1, no XP, no streak, no competencies
          │  0 │
          └────┘
```

### 7.3 Active State (Regular Builder)

```
          ┌──────────┐
          │ 🔥       │   7-day streak active
          │  ┌────┐  │
          │  │  5 │  │   Level 5
          │  └────┘  │
          │ 450/800  │   450 XP of 800 needed
          │ ▓▓▓▓▓░░░│
          └──────────┘
```

### 7.4 Level Up State (Celebration)

```
          ╔══════════╗
          ║  ✦ ✦ ✦  ║   Golden burst effect
          ║  ┌────┐  ║
          ║  │  6 │  ║   Level increased from 5 to 6
          ║  └────┘  ║
          ║  LEVEL UP ║   Text appears briefly
          ╚══════════╝
```

---

## 8. Accessibility

### 8.1 Screen Reader

```html
<div
  role="progressbar"
  aria-label="Ascension Ring"
  aria-valuenow="450"
  aria-valuemin="0"
  aria-valuemax="800"
  aria-valuetext="Level 5, 450 of 800 XP, 7 day streak"
>
```

### 8.2 Keyboard

| Key | Action |
|-----|--------|
| `Tab` | Focus the ring |
| `Enter` | Open profile detail |
| `Escape` | Close detail (if open) |

### 8.3 Reduced Motion

When `prefers-reduced-motion: reduce` is active:

- All animations disabled
- States change instantly
- Level up shows as static badge (no burst)
- XP fill shows as instant bar update

### 8.4 Color Blindness

- XP arc uses pattern (dots/dashes) in addition to color
- Streak indicator uses icon (🔥) plus position, not just color
- All states have text labels alongside visual indicators

---

## 9. Component API

### 9.1 Props

```typescript
interface AscensionRingProps {
  // Core data
  level: number;
  xpCurrent: number;
  xpMax: number;

  // Streak
  streakDays?: number;       // default: 0

  // Competencies (max 6)
  competencies?: CompetencySummary[];

  // Achievement state
  hasNewAchievement?: boolean;  // default: false
  isLevelUp?: boolean;          // default: false

  // Appearance
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';  // default: 'md'
  variant?: 'default' | 'compact' | 'celebrate';  // default: 'default'
  className?: string;

  // Events
  onClick?: () => void;
  onLevelUpComplete?: () => void;

  // Accessibility
  ariaLabel?: string;
}

interface CompetencySummary {
  id: string;
  name: string;
  level: number;       // 0-5
  icon: string;        // Lucide icon name
  color?: string;      // Optional override
}
```

### 9.2 Events

```typescript
// Custom events emitted by the component
'AscensionRing:xpUpdate'    — Fired when XP animation completes
'AscensionRing:levelUp'     — Fired when level-up animation completes
'AscensionRing:ringClick'   — Fired when user clicks the ring
```

### 9.3 Usage Example

```tsx
<AscensionRing
  level={5}
  xpCurrent={450}
  xpMax={800}
  streakDays={7}
  competencies={[
    { id: 'file-mgmt', name: 'File Management', level: 3, icon: 'FolderTree' },
    { id: 'user-admin', name: 'User Admin', level: 2, icon: 'Users' },
  ]}
  size="md"
  onClick={() => router.push('/profile')}
/>
```

---

## 10. Responsive Behavior

| Breakpoint | Size | Position |
|------------|------|----------|
| Desktop (>=1024px) | `md` (120px) | Sidebar footer |
| Tablet (768-1023px) | `sm` (80px) | Header |
| Mobile (<768px) | `sm` (80px) | Header center |

---

## 11. Future Evolution

### 11.1 V1 (Current)

- Static SVG-based ring
- XP arc animation
- Basic competency dots
- Level display

### 11.2 V2 (Planned)

- Canvas-based rendering for performance
- Particle effects for level up
- Custom competency icon upload
- Ring theme customization

### 11.3 V3 (Vision)

- Animated competency icons (micro-lottie)
- Interactive ring (hover competency to see detail)
- Ring as navigation (click competency → go to tree)
- Shareable ring (export as image for social)

---

## 12. Implementation Notes

| Note | Detail |
|------|--------|
| **Rendering** | SVG for simplicity, canvas if performance becomes an issue |
| **Framework** | React component with Framer Motion |
| **Color tokens** | Use CSS custom properties from UI-0001 |
| **Testing** | Storybook for visual states, jest for math logic |
| **Bundle size** | Target < 5KB (gzipped) for the component |

---

## 13. Definition of Done

ARCH-0014 aprovado quando:

- [ ] Layer architecture defined (5 layers)
- [ ] Mathematics documented (sizes, arc calc, orbit positions, streak angle)
- [ ] Colors specified (default palette + state colors)
- [ ] Animation registry complete (8 animations)
- [ ] Animation constraints defined
- [ ] State matrix complete (7 states)
- [ ] Visuals for empty, active, and level-up states
- [ ] Accessibility covered (screen reader, keyboard, reduced motion, color blindness)
- [ ] Component API defined (props, events, usage example)
- [ ] Responsive behavior specified
- [ ] Future evolution roadmap documented
- [ ] Implementation notes provided

---

## 14. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
