# UI-0005 — Design Token Reference

| Field | Value |
|-------|-------|
| **ID** | UI-0005 |
| **Name** | Design Token Reference |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | UI/UX |
| **Derived from** | UI-0001, ARCH-0022 |
| **Source of truth** | `packages/tokens/` |

---

## 1. Purpose

This document is the **single source of truth** for every design token in ASCEND. No token exists outside this document. No implementation should use a value that is not documented here.

---

## 2. Token Categories

```
TOKENS
├── Primitive       → Base values (spacing, radius, color, font)
├── Semantic        → Purpose-based aliases (background, success, border)
├── Brand           → ASCEND identity colors
├── Component       → Component-specific tokens (button, card, sidebar)
└── Motion          → Animation and transition tokens
```

---

## 3. Naming Convention

```
--ascend-{category}-{variant}-{state}
```

| Part | Description | Example |
|------|-------------|---------|
| `--ascend` | Prefix — all ASCEND tokens | `--ascend` |
| `{category}` | Token category | `space`, `brand`, `text` |
| `{variant}` | Specific variant | `4`, `500`, `sm` |
| `{state}` | Optional state modifier | `hover`, `focus` |

**Examples:**
- `--ascend-space-4` — 16px spacing
- `--ascend-brand-500` — Primary blue
- `--ascend-text-sm` — Small text
- `--ascend-button-radius` — Button border radius

**Forbidden patterns:**
- ❌ `--ascend-blue` — use `--ascend-brand-500` instead
- ❌ `--ascend-margin` — use `--ascend-space-{n}` instead
- ❌ `--primary-color` — use `--ascend-brand-500` instead
- ❌ Inline hex values in components — always reference a token

---

## 4. Primitive Tokens

### 4.1 Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--ascend-space-0` | 0 | No spacing |
| `--ascend-space-1` | 0.25rem (4px) | Micro spacing |
| `--ascend-space-2` | 0.5rem (8px) | Tight spacing |
| `--ascend-space-3` | 0.75rem (12px) | Small gap |
| `--ascend-space-4` | 1rem (16px) | **Standard gap** |
| `--ascend-space-5` | 1.25rem (20px) | Medium |
| `--ascend-space-6` | 1.5rem (24px) | Section gap |
| `--ascend-space-8` | 2rem (32px) | Large gap |
| `--ascend-space-10` | 2.5rem (40px) | XL |
| `--ascend-space-12` | 3rem (48px) | Section separator |
| `--ascend-space-16` | 4rem (64px) | Page section |
| `--ascend-space-20` | 5rem (80px) | Page section large |
| `--ascend-space-24` | 6rem (96px) | Hero section |

### 4.2 Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| `--ascend-radius-none` | 0 | Tables, inputs |
| `--ascend-radius-sm` | 0.25rem (4px) | Small elements |
| `--ascend-radius-md` | 0.5rem (8px) | **Cards, modals** |
| `--ascend-radius-lg` | 0.75rem (12px) | Large cards |
| `--ascend-radius-xl` | 1rem (16px) | Dialogs |
| `--ascend-radius-full` | 9999px | Badges, avatars |

### 4.3 Typography

| Token | Value | Weight | Usage |
|-------|-------|--------|-------|
| `--ascend-text-xs` | 0.75rem (12px) | 400 | Caption, metadata |
| `--ascend-text-sm` | 0.875rem (14px) | 400 | Body small |
| `--ascend-text-base` | 1rem (16px) | 400 | **Body** |
| `--ascend-text-lg` | 1.125rem (18px) | 500 | Lead, subtitles |
| `--ascend-text-xl` | 1.25rem (20px) | 600 | Section titles |
| `--ascend-text-2xl` | 1.5rem (24px) | 600 | Page titles |
| `--ascend-text-3xl` | 1.875rem (30px) | 700 | Hero titles |
| `--ascend-text-4xl` | 2.25rem (36px) | 700 | Display large |
| `--ascend-text-5xl` | 3rem (48px) | 800 | Display hero |

**Font families:**
| Token | Value |
|-------|-------|
| `--ascend-font-sans` | `'Inter', system-ui, sans-serif` |
| `--ascend-font-mono` | `'JetBrains Mono', monospace` |

**Font weights:**
| Token | Value |
|-------|-------|
| `--ascend-font-weight-regular` | 400 |
| `--ascend-font-weight-medium` | 500 |
| `--ascend-font-weight-semibold` | 600 |
| `--ascend-font-weight-bold` | 700 |
| `--ascend-font-weight-extrabold` | 800 |

### 4.4 Duration & Easing

| Token | Value | Usage |
|-------|-------|-------|
| `--ascend-dur-instant` | 0ms | State changes |
| `--ascend-dur-fast` | 100ms | Hover, micro-interactions |
| `--ascend-dur-normal` | 200ms | **Standard transitions** |
| `--ascend-dur-slow` | 300ms | Page transitions |
| `--ascend-dur-celebrate` | 500ms | Level up, achievements |
| `--ascend-ease-default` | `ease` | Default |
| `--ascend-ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Entrance |
| `--ascend-ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Exit |
| `--ascend-ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | In-out |
| `--ascend-ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Celebrations |

### 4.5 Opacity

| Token | Value | Usage |
|-------|-------|-------|
| `--ascend-opacity-0` | 0 | Hidden |
| `--ascend-opacity-5` | 0.05 | Subtle |
| `--ascend-opacity-10` | 0.1 | Very faint |
| `--ascend-opacity-20` | 0.2 | Faint |
| `--ascend-opacity-30` | 0.3 | Light overlay |
| `--ascend-opacity-40` | 0.4 | Medium overlay |
| `--ascend-opacity-50` | 0.5 | **Disabled state** |
| `--ascend-opacity-60` | 0.6 | Muted |
| `--ascend-opacity-70` | 0.7 | Subtle emphasis |
| `--ascend-opacity-80` | 0.8 | Emphasis |
| `--ascend-opacity-90` | 0.9 | Strong emphasis |
| `--ascend-opacity-100` | 1 | Full visibility |

### 4.6 Z-Index

| Token | Value | Usage |
|-------|-------|-------|
| `--ascend-z-base` | 0 | Base |
| `--ascend-z-dropdown` | 100 | Dropdown menus |
| `--ascend-z-sticky` | 200 | Sticky elements |
| `--ascend-z-navbar` | 300 | Navigation bar |
| `--ascend-z-modal` | 400 | Modals |
| `--ascend-z-toast` | 500 | Toasts |
| `--ascend-z-tooltip` | 600 | Tooltips |
| `--ascend-z-overlay` | 700 | Overlays |
| `--ascend-z-max` | 9999 | Maximum |

### 4.7 Shadows

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | `0 1px 2px rgba(0,0,0,0.3)` | Subtle |
| `--ascend-shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | `0 4px 6px rgba(0,0,0,0.4)` | Cards |
| `--ascend-shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | `0 10px 15px rgba(0,0,0,0.5)` | Modals |
| `--ascend-shadow-xl` | `0 20px 25px rgba(0,0,0,0.12)` | `0 20px 25px rgba(0,0,0,0.6)` | Dropdowns |
| `--ascend-shadow-glow` | `0 0 20px rgba(51,102,255,0.15)` | `0 0 20px rgba(102,153,255,0.2)` | Brand glow |

---

## 5. Semantic Tokens

### 5.1 Surface & Background

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-background` | `#F8FAFC` | `#0F1115` | Page background |
| `--ascend-surface` | `#FFFFFF` | `#1A1D23` | Card, panel surface |
| `--ascend-surface-elevated` | `#FFFFFF` | `#262A33` | Modal, popover |
| `--ascend-muted` | `#F1F5F9` | `#1A1D23` | Muted background |

### 5.2 Text

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-foreground` | `#0F172A` | `#E1E5EB` | Primary text |
| `--ascend-foreground-muted` | `#64748B` | `#838996` | Secondary text |
| `--ascend-foreground-subtle` | `#94A3B8` | `#4A4F5C` | Placeholder, caption |

### 5.3 Border

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-border` | `#E2E8F0` | `#262A33` | Default border |
| `--ascend-border-strong` | `#CBD5E1` | `#333842` | Active border |

### 5.4 Accent

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-accent` | `#D6E4FF` | `#1A2744` | Accent background |
| `--ascend-accent-foreground` | `#1F3D99` | `#99C0FF` | Accent text |

### 5.5 Feedback

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-success` | `#22C55E` | `#4ADE80` | Success icon/text |
| `--ascend-success-bg` | `#F0FFF4` | `#052E16` | Success background |
| `--ascend-warning` | `#F59E0B` | `#FBBF24` | Warning icon/text |
| `--ascend-warning-bg` | `#FFFBEB` | `#422006` | Warning background |
| `--ascend-danger` | `#EF4444` | `#F87171` | Danger icon/text |
| `--ascend-danger-bg` | `#FFF5F5` | `#450A0A` | Danger background |
| `--ascend-info` | `#3B82F6` | `#60A5FA` | Info icon/text |
| `--ascend-info-bg` | `#EFF6FF` | `#0C1F3F` | Info background |

---

## 6. Brand Tokens

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `--ascend-brand-50` | `#F0F4FF` | `#0D1428` | Lightest brand |
| `--ascend-brand-100` | `#D6E4FF` | `#1A2744` | Hover background |
| `--ascend-brand-200` | `#ADC8FF` | `#2A3F66` | Subtle border |
| `--ascend-brand-300` | `#84A9FF` | `#3D5A8C` | Active border |
| `--ascend-brand-400` | `#5B8AFF` | `#5375AD` | Icon brand |
| `--ascend-brand-500` | `#3366FF` | `#6699FF` | **Primary — Builder Blue** |
| `--ascend-brand-600` | `#2952CC` | `#80ADFF` | Hover primary |
| `--ascend-brand-700` | `#1F3D99` | `#99C0FF` | Active primary |
| `--ascend-brand-800` | `#142966` | `#B3D4FF` | Text on dark |
| `--ascend-brand-900` | `#0A1433` | `#CCE5FF` | Deep brand |

---

## 7. Component Tokens

### 7.1 Button

| Token | Value |
|-------|-------|
| `--ascend-button-radius` | `var(--ascend-radius-md)` |
| `--ascend-button-padding-x` | `var(--ascend-space-4)` |
| `--ascend-button-padding-y` | `var(--ascend-space-2)` |
| `--ascend-button-font` | `var(--ascend-font-weight-medium)` |
| `--ascend-button-gap` | `var(--ascend-space-2)` |

### 7.2 Card

| Token | Value |
|-------|-------|
| `--ascend-card-radius` | `var(--ascend-radius-lg)` |
| `--ascend-card-padding` | `var(--ascend-space-6)` |
| `--ascend-card-shadow` | `var(--ascend-shadow-sm)` |
| `--ascend-card-gap` | `var(--ascend-space-4)` |

### 7.3 Panel

| Token | Value |
|-------|-------|
| `--ascend-panel-radius` | `var(--ascend-radius-md)` |
| `--ascend-panel-padding` | `var(--ascend-space-4)` |
| `--ascend-panel-bg` | `var(--ascend-surface)` |
| `--ascend-panel-border` | `var(--ascend-border)` |

### 7.4 Sidebar

| Token | Value |
|-------|-------|
| `--ascend-sidebar-width` | `240px` |
| `--ascend-sidebar-width-collapsed` | `64px` |
| `--ascend-sidebar-bg` | `var(--ascend-surface)` |
| `--ascend-sidebar-border` | `var(--ascend-border)` |
| `--ascend-sidebar-item-radius` | `var(--ascend-radius-md)` |
| `--ascend-sidebar-item-padding` | `var(--ascend-space-3)` |

### 7.5 Input

| Token | Value |
|-------|-------|
| `--ascend-input-radius` | `var(--ascend-radius-md)` |
| `--ascend-input-padding-x` | `var(--ascend-space-3)` |
| `--ascend-input-padding-y` | `var(--ascend-space-2)` |
| `--ascend-input-border` | `var(--ascend-border)` |
| `--ascend-input-border-focus` | `var(--ascend-brand-500)` |

### 7.6 Badge

| Token | Value |
|-------|-------|
| `--ascend-badge-radius` | `var(--ascend-radius-full)` |
| `--ascend-badge-padding-x` | `var(--ascend-space-2)` |
| `--ascend-badge-padding-y` | `0.125rem` |
| `--ascend-badge-font` | `var(--ascend-text-xs)` |
| `--ascend-badge-dot-size` | `8px` |

---

## 8. Motion Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--ascend-motion-instant` | `var(--ascend-dur-instant)` | No animation |
| `--ascend-motion-fast` | `var(--ascend-dur-fast)` | Hover, micro |
| `--ascend-motion-normal` | `var(--ascend-dur-normal)` | Standard |
| `--ascend-motion-slow` | `var(--ascend-dur-slow)` | Page transitions |
| `--ascend-motion-hero` | `var(--ascend-dur-celebrate)` | Celebrations |
| `--ascend-motion-spring` | `var(--ascend-ease-spring)` | Spring effect |

### Transition Shorthands

| Token | Value |
|-------|-------|
| `--ascend-transition-default` | `all var(--ascend-dur-normal) var(--ascend-ease-out)` |
| `--ascend-transition-color` | `background-color var(--ascend-dur-normal) var(--ascend-ease-out), color var(--ascend-dur-normal) var(--ascend-ease-out)` |
| `--ascend-transition-transform` | `transform var(--ascend-dur-normal) var(--ascend-ease-out)` |
| `--ascend-transition-opacity` | `opacity var(--ascend-dur-normal) var(--ascend-ease-out)` |

### Animation References

| Token | Value |
|-------|-------|
| `--ascend-key-fade-in` | `fade-in var(--ascend-dur-normal) var(--ascend-ease-out)` |
| `--ascend-key-slide-up` | `slide-up var(--ascend-dur-slow) var(--ascend-ease-out)` |
| `--ascend-key-scale-in` | `scale-in var(--ascend-dur-normal) var(--ascend-ease-out)` |
| `--ascend-key-shimmer` | `shimmer 1.5s linear infinite` |

---

## 9. Forbidden Tokens

The following tokens are **prohibited** and must not appear in any ASCEND code:

| Token | Reason |
|-------|--------|
| Any hardcoded hex color | Must reference an ASCEND token |
| Any hardcoded `px` value for spacing | Must use `--ascend-space-{n}` |
| Any `z-index` value directly | Must use `--ascend-z-{name}` |
| Any inline `transition` | Must use `--ascend-transition-{name}` |
| Any `box-shadow` value directly | Must use `--ascend-shadow-{name}` |
| `--ascend-blue`, `--ascend-red`, etc. | Generic names not allowed |
| `--primary-color`, `--secondary-color` | Must use semantic tokens |

---

## 10. How to Add a New Token

1. Add to the TypeScript definition in `packages/tokens/src/`
2. Add to the CSS output in `packages/tokens/src/generated/tokens.css`
3. Add to this document (UI-0005)
4. Update the Tailwind config if the token should be available as a utility class
5. Submit an RFC if the token changes existing values

---

## 11. Source of Truth Hierarchy

```
1. UI-0005 (this document)      → Canonical reference
2. packages/tokens/src/          → TypeScript definitions
3. packages/tokens/generated/    → CSS custom properties
4. apps/web/tailwind.config.ts   → Tailwind utility mappings
5. apps/web/globals.css          → shadcn/ui variable mapping
```

A change in level 1 **must** propagate to all levels below. A change in level 5 alone (without updating levels 1-3) is a protocol violation.

---

## 12. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Implementation Engineer | Initial version |
