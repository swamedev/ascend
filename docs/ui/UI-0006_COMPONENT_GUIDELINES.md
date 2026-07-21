# UI-0006 — Component Guidelines

| Field | Value |
|-------|-------|
| **ID** | UI-0006 |
| **Name** | Component Guidelines |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | UI/UX |
| **Derived from** | UI-0001, UI-0005, ARCH-0022, ARCH-0023 |

---

## 1. Purpose

Define the standard for every component in ASCEND. All components must follow this document. No component is exempt.

---

## 2. Component Anatomy

Every component has three layers:

```
Contract (types)
    │
    ▼
Component (tsx)
    │
    ▼
Styles (tailwind)
```

### 2.1 Contract Layer

```typescript
// ComponentName.ts (types only)
interface ButtonProps {
  // Required
  children?: React.ReactNode

  // Variants
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'

  // States
  disabled?: boolean
  loading?: boolean

  // Events
  onClick?: (e: React.MouseEvent) => void
  onKeyDown?: (e: React.KeyboardEvent) => void

  // Extras
  className?: string
  'aria-label'?: string
}
```

### 2.2 Component Layer

```tsx
function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  className,
  ...props
}: ButtonProps) {
  const { reducedMotion } = useMotion()
  // ...
}
```

### 2.3 Styles Layer

Uses Tailwind with ASCEND tokens. Never hardcoded values.

```tsx
const variants = {
  primary: 'bg-primary text-primary-foreground hover:bg-primary/90',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
}
```

---

## 3. Naming Convention

| Element | Convention | Example |
|---------|------------|---------|
| Component | `PascalCase` | `MissionCard` |
| Props interface | `{Name}Props` | `MissionCardProps` |
| Variant type | `{Name}Variant` | `ButtonVariant` |
| Size type | `{Name}Size` | `ButtonSize` |
| State enum | String union | `'loading' \| 'error' \| 'empty'` |
| File (component) | `kebab-case.tsx` | `mission-card.tsx` |
| File (types) | `kebab-case.ts` | `mission-card.ts` |
| File (test) | `kebab-case.test.tsx` | `mission-card.test.tsx` |

---

## 4. Required States

Every interactive component must handle:

| State | Implementation |
|-------|----------------|
| **Default** | Base variant rendering |
| **Hover** | `hover:` Tailwind variant |
| **Active** | `active:` Tailwind variant or `scale(0.98)` |
| **Focus** | `focus-visible:ring-2 focus-visible:ring-ring` |
| **Disabled** | `opacity-50 cursor-not-allowed`, `aria-disabled` |
| **Loading** | Spinner icon + disabled interactions |
| **Error** | `border-destructive`, error message |
| **Empty** | Placeholder or skeleton |

---

## 5. Accessibility

| Requirement | Implementation |
|-------------|----------------|
| **ARIA labels** | `aria-label` on all interactive elements |
| **Role** | Correct role (button, dialog, navigation, etc.) |
| **Keyboard** | Tab order, Enter/Space for activation, Escape for dismiss |
| **Focus trap** | Modals and drawers must trap focus |
| **Screen reader** | `aria-hidden` on decorative icons, `sr-only` for context |
| **Focus visible** | Never remove outline without replacing it |
| **Reduced motion** | Respect `prefers-reduced-motion` via MotionProvider |

---

## 6. Motion

| Rule | Description |
|------|-------------|
| **M1** | All durations from `useMotion()` — never hardcoded |
| **M2** | Entrances: `fadeIn` or `slideUp` from MotionProvider |
| **M3** | Exits: `fadeIn` exit variant |
| **M4** | `prefers-reduced-motion` disables all animations |
| **M5** | Micro-interactions (hover, active): CSS transitions only |
| **M6** | Layout animations: Framer Motion `layout` prop |

---

## 7. Responsiveness

| Rule | Description |
|------|-------------|
| **R1** | Components adapt via `useBreakpoint()`, never `window.innerWidth` |
| **R2** | Mobile: full-width inputs, stacked layouts, bottom sheets |
| **R3** | Tablet: collapsible panels, condensed tables |
| **R4** | Desktop: multi-column, side panels, tooltips |
| **R5** | Touch targets: minimum 44x44px |

---

## 8. Composition Rules

| Rule | Description |
|------|-------------|
| **C1** | Components receive data via props. No direct store access in primitive components |
| **C2** | Layout components may read LayoutStore. Domain components never read LayoutStore |
| **C3** | Components never import from features (missions, journeys, etc.) |
| **C4** | ASCEND components (Tier 3) receive mock data via props until Runtime is connected |
| **C5** | No component makes HTTP calls |
| **C6** | No component accesses the Runtime directly |

---

## 9. Forbidden Patterns

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| `any` in props | Type safety | Define explicit union or interface |
| Inline hex colors | Token violation | Use `var(--ascend-*)` |
| Inline `transition` | Motion violation | Use `useMotion()` |
| `window.innerWidth` | Break violation | Use `useBreakpoint()` |
| `@apply` directives | Tailwind JIT issues | Use plain `className` |
| `!important` | Specificity hack | Restructure selectors |
| Default exports | Import consistency | Named exports only |
| `any` cast | Type safety | Proper type narrowing |

---

## 10. Component Tiers

| Tier | Category | Location | Examples |
|------|----------|----------|----------|
| 1 | Primitive | `components/ui/` | Button, Input, Card, Modal |
| 2 | Layout | `components/layout/` | Sidebar, TopBar, Breadcrumb |
| 3 | ASCEND | `components/shared/` | AscensionRing, XPBar, JourneyCard |
| 4 | Feedback | `components/ui/` | Toast, Alert, EmptyState |

---

## 11. Testing Expectations

| Test type | Coverage |
|-----------|----------|
| Render | Component renders without crashing |
| Variants | All variants render correctly |
| States | Loading, disabled, error, empty |
| Events | Click, keydown, change handlers |
| Accessibility | ARIA attributes, keyboard nav |
| Responsive | Layout adapts (if applicable) |

---

## 12. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Implementation Engineer | Initial version |
