# EXPERIENCE FREEZE v1.0

> **Status:** Ratified  
> **Date:** 2026-07-20  
> **Authority:** Chief Architect (OPERAÇÃO AURORA / GATE 4)  
> **Domain:** Experience Layer (Frontend)  
> **Change Control:** Any modification requires an RFC per `docs/rfc/RFC_TEMPLATE.md`

---

## 1. Purpose

Freeze the ASCEND Experience Layer — the complete set of official components, layouts, tokens, motion presets, providers, hooks, contexts, slots, and public APIs — so that all feature development (Phase D onward) builds on a stable, known surface.

No component, token, hook, or layout may be added, removed, or altered without an approved RFC.

---

## 2. Official Component Registry

### 2.1 Tier 1 — Primitives (`@/components/ui/`)

| Component | Props Interface | Variants | States | Source |
|-----------|---------------|----------|--------|--------|
| `Button` | `ButtonProps` | `primary`, `secondary`, `ghost`, `danger` | `loading`, `disabled`, `icon` | `button.tsx` |
| `IconButton` | `IconButtonProps` | — | `loading`, `disabled` | `icon-button.tsx` |
| `Badge` | `BadgeProps` | `default`, `primary`, `success`, `warning`, `danger`, `info`, `xp` | `dot`, `size` | `badge.tsx` |
| `Avatar` | `AvatarProps` | — | `src`, `initials` | `avatar.tsx` |
| `Divider` | `DividerProps` | `horizontal`, `vertical`, `label` | — | `divider.tsx` |
| `Spinner` | `SpinnerProps` | — | `size` | `spinner.tsx` |
| `Skeleton` | `SkeletonProps` | `text`, `circular`, `rectangular` | `width`, `height` | `skeleton.tsx` |
| `Label` | `LabelProps` | — | `required` | `label.tsx` |
| `Input` | `InputProps` | — | `error`, `icon`, `disabled` | `input.tsx` |
| `Textarea` | `TextareaProps` | — | `error`, `disabled` | `textarea.tsx` |
| `Tooltip` | `TooltipProps` | `top`, `bottom`, `left`, `right` | `delay` | `tooltip.tsx` |
| `ScrollArea` | `ScrollAreaProps` | `vertical`, `horizontal`, `both` | — | `scroll-area.tsx` |
| `Card` | `CardProps` | `default`, `elevated`, `bordered` | `padding` | `card.tsx` |
| `CardHeader` | `CardHeaderProps` | — | `title`, `description`, `action` | `card.tsx` |
| `CardContent` | `CardContentProps` | — | `padding` | `card.tsx` |
| `CardFooter` | `CardFooterProps` | — | — | `card.tsx` |
| `Modal` | `ModalProps` | `sm`, `md`, `lg`, `xl`, `full` | `open`, `onClose` | `modal.tsx` |
| `Drawer` | `DrawerProps` | `left`, `right`, `bottom` | `open`, `onClose` | `drawer.tsx` |

### 2.2 Tier 4 — Feedback (`@/components/ui/`)

| Component | Props Interface | Variants | States | Source |
|-----------|---------------|----------|--------|--------|
| `ToastContainer` | `ToastContainerProps` | — | renders `ToastData[]` | `toast.tsx` |
| `Alert` | `AlertProps` | `success`, `error`, `warning`, `info` | `onDismiss` | `alert.tsx` |
| `EmptyState` | `EmptyStateProps` | — | `icon`, `action` | `empty-state.tsx` |
| `LoadingState` | `LoadingStateProps` | — | `label` | `state-components.tsx` |
| `ErrorState` | `ErrorStateProps` | — | `action` | `state-components.tsx` |
| `SuccessState` | `SuccessStateProps` | — | `action` | `state-components.tsx` |

### 2.3 Tier 2 — Layout (`@/components/layout/`)

| Component | Props Interface | Variants | Notes | Source |
|-----------|---------------|----------|-------|--------|
| `AppShell` | `AppShellSlots` | — | Slot-based container | `app-shell.tsx` |
| `Sidebar` | `SidebarProps` | — | Consumes layout store | `sidebar.tsx` |
| `SidebarItem` | `SidebarItemProps` | — | Supports nested items | `sidebar.tsx` |
| `TopBar` | `TopBarProps` | — | 3-zone layout (left, center, right) | `topbar.tsx` |
| `TopBarAction` | `TopBarActionProps` | — | Icon button with badge | `topbar.tsx` |
| `Breadcrumb` | `BreadcrumbProps` | — | Consumes layout store | `breadcrumb.tsx` |
| `PageContainer` | `PageContainerProps` | `sm`, `md`, `lg`, `xl`, `full` | Max-width wrapper | `page-container.tsx` |
| `BottomNavigation` | `BottomNavigationProps` | — | Mobile nav bar | `bottom-navigation.tsx` |
| `Panel` | `PanelProps` | — | Flexible side panel | `panel.tsx` |
| `PanelHeader` | `PanelHeaderProps` | — | Title + description + action | `panel.tsx` |
| `Workspace` | `WorkspaceProps` | — | Scrollable main area | `workspace.tsx` |

### 2.4 Tier 3 — ASCEND Domain (`@/components/shared/`)

| Component | Props Interface | Variants | Source |
|-----------|---------------|----------|--------|
| `AscensionRing` | `AscensionRingProps` | — | `ascension-ring.tsx` |
| `XPBar` | `XPBarProps` | `sm`, `md`, `lg` | `xp-bar.tsx` |
| `LevelBadge` | `LevelBadgeProps` | `sm`, `md`, `lg` | `level-badge.tsx` |
| `CompetencyBadge` | `CompetencyBadgeProps` | — | `competency-badge.tsx` |
| `MissionStatus` | `MissionStatusProps` | `pending`, `active`, `completed`, `failed`, `locked` | `mission-status.tsx` |
| `JourneyCard` | `JourneyCardProps` | — | `journey-card.tsx` |
| `ProgressIndicator` | `ProgressIndicatorProps` | `default`, `xp`, `success`, `warning` | `progress-indicator.tsx` |
| `EvidenceBadge` | `EvidenceBadgeProps` | — | `evidence-badge.tsx` |
| `AchievementBadge` | `AchievementBadgeProps` | — | `achievement-badge.tsx` |

### 2.5 Component Gallery (Dev Only)

- **Route:** `/dev/gallery`
- **Location:** `apps/web/src/app/dev/gallery/page.tsx`
- **Purpose:** Visual review of every component and every variant
- **Access:** Developer-only; never exposed in production

---

## 3. Official Layout Registry

| Layout | Slots | File |
|--------|-------|------|
| `AppShell` | `topbar`, `sidebar`, `workspace` *(required)*, `rightPanel`, `overlay` | `layout/app-shell.tsx` |
| Sidebar + Workspace | Sidebar groups feed into `sidebar` slot | `layout/sidebar.tsx` |
| TopBar + Content | TopBar zones feed into `topbar` slot | `layout/topbar.tsx` |
| Bottom Navigation | Mobile-only layout mode | `layout/bottom-navigation.tsx` |
| Right Panel (Drawer) | Injected via `rightPanel` / `Drawer` component | `ui/drawer.tsx` |

### Layout Invariance (ARCH-0023)

Layout components **must never**:
- Import domain logic, Runtime, or feature-specific code
- Access API or SDK modules
- Contain business logic or domain types
- Depend on `components/shared/` or feature components

---

## 4. Official Token Registry

### 4.1 Primitive Tokens

```
--ascend-space-{0..24}     Spacing scale (12 steps)
--ascend-radius-{none|sm|md|lg|xl|full}
--ascend-font-{sans|mono}
--ascend-text-{xs..5xl}    Type scale
--ascend-font-weight-{regular..extrabold}
--ascend-dur-{instant|fast|normal|slow|celebrate}
--ascend-ease-{default|in|out|in-out|spring}
--ascend-opacity-{0..100}  (11 steps)
--ascend-z-{base|dropdown|sticky|navbar|modal|toast|tooltip|overlay|max}
--ascend-shadow-{sm|md|lg|xl|glow}
```

### 4.2 Semantic Tokens

```
--ascend-background
--ascend-surface / --ascend-surface-elevated
--ascend-foreground / --ascend-foreground-muted / --ascend-foreground-subtle
--ascend-border / --ascend-border-strong
--ascend-muted / --ascend-accent / --ascend-accent-foreground
--ascend-{success|warning|danger|info}
--ascend-{success|warning|danger|info}-bg
```

### 4.3 Brand Tokens

```
--ascend-brand-{50..900}   Builder Blue (dark and light variants)
```

### 4.4 Component Tokens

```
--ascend-button-{radius|padding-x|padding-y|font|gap}
--ascend-card-{radius|padding|shadow|gap}
--ascend-panel-{radius|padding|bg|border}
--ascend-sidebar-{width|width-collapsed|bg|border|item-radius|item-padding}
--ascend-input-{radius|padding-x|padding-y|border|border-focus}
--ascend-badge-{radius|padding-x|padding-y|font|dot-size}
```

### 4.5 Motion Tokens

```
--ascend-motion-{instant|fast|normal|slow|hero}
--ascend-motion-spring
--ascend-transition-{default|color|transform|opacity}
--ascend-key-{fade-in|slide-up|scale-in|shimmer}
```

### 4.6 Icons

- **Library:** `lucide-react` v0.460+
- **Official icon registry:** All Lucide icons are available
- **Rule:** Icons must be imported from `lucide-react` only

**Source:** `packages/tokens/src/generated/tokens.css` (208 lines)

---

## 5. Official Motion Presets

| Preset | Duration | Ease | Usage |
|--------|----------|------|-------|
| `instant` | 0ms | — | Disabled animations |
| `fast` | 100ms | `[0, 0, 0.2, 1]` | Micro-interactions (hover, tap) |
| `normal` | 200ms | `[0, 0, 0.2, 1]` | Default transitions |
| `slow` | 300ms | `[0, 0, 0.2, 1]` | Panel slides, accordions |
| `hero` | 500ms | `[0, 0, 0.2, 1]` | Celebratory, entrance animations |

### Framer Motion Variants (from `MotionProvider`)

| Variant | Initial | Animate | Exit |
|---------|---------|---------|------|
| `fadeIn` | `{ opacity: 0 }` | `{ opacity: 1 }` | `{ opacity: 0 }` |
| `slideUp` | `{ opacity: 0, y: 10 }` | `{ opacity: 1, y: 0 }` | `{ opacity: 0, y: -10 }` |
| `slideDown` | `{ opacity: 0, y: -10 }` | `{ opacity: 1, y: 0 }` | `{ opacity: 0, y: 10 }` |
| `scaleIn` | `{ opacity: 0, scale: 0.95 }` | `{ opacity: 1, scale: 1 }` | `{ opacity: 0, scale: 0.95 }` |
| `shimmer` | `{ backgroundPosition: '-200% 0' }` | Looping 1.5s linear | — |

### Reduced Motion

- All components respect `prefers-reduced-motion: reduce`
- Duration becomes `0` when reduced motion is active
- No animation should play without a motion check

**Source:** `motion/motion-provider.tsx`

---

## 6. Official Provider Registry

| Provider | Props | Responsibility | File |
|----------|-------|---------------|------|
| `MotionProvider` | `speed?: MotionSpeed` | Centralized Framer Motion config, reduced-motion detection | `motion/motion-provider.tsx` |
| `ThemeProvider` | *(from next-themes)* | Light/Dark/System theme switching | *(external)* |
| `LayoutProvider` | `children` | Breakpoint init, Motion wrapper, layout orchestration | `layout/layout-provider.tsx` |

---

## 7. Official Hook Registry

| Hook | Returns | Consumes | File |
|------|---------|----------|------|
| `useMotion()` | `{ speed, reducedMotion, pageTransition, modalTransition, springPreset, variants }` | MotionContext | `motion/motion-provider.tsx` |
| `useBreakpoint()` | `LayoutMode` | LayoutStore | `hooks/use-breakpoint.ts` |
| `useBreakpointInit()` | *(side-effect)* | LayoutStore | `hooks/use-breakpoint.ts` |
| `useViewport()` | `{ width, height, scrollY }` | Window events | `hooks/use-viewport.ts` |

---

## 8. Official Context Registry

| Context | Provided By | Value |
|---------|------------|-------|
| `MotionContext` | `MotionProvider` | `MotionContextValue` (speed, reducedMotion, variants, transitions) |

No other React Contexts are approved for the Experience Layer v1.0.

---

## 9. Official Store Registry

| Store | Library | Key | File |
|-------|---------|-----|------|
| `layoutStore` | Zustand v5 | `sidebar`, `topbar`, `workspace`, `rightPanel`, `breadcrumbs`, `layoutMode`, `reducedMotion` | `store/layout-store.ts` |

### LayoutStore Public API

```typescript
// State
sidebar: { open: boolean; collapsed: boolean; pinned: boolean }
topbar: { transparent: boolean; hidden: boolean }
workspace: { fullscreen: boolean; focusMode: boolean }
rightPanel: { open: boolean; width: number }
breadcrumbs: Breadcrumb[]
layoutMode: LayoutMode  // 'ultrawide' | 'desktop' | 'tablet' | 'mobile'
reducedMotion: boolean

// Actions
toggleSidebar(), setSidebarOpen(open), setSidebarCollapsed(collapsed), setSidebarPinned(pinned)
setTopbarTransparent(transparent), setTopbarHidden(hidden)
setFullscreen(fullscreen), setFocusMode(focusMode)
toggleRightPanel(), setRightPanelOpen(open), setRightPanelWidth(width)
setBreadcrumbs(breadcrumbs), setLayoutMode(mode), setReducedMotion(reduced)
reset()
```

---

## 10. Official Slot Registry

| Slot | Parent | Type | Required |
|------|--------|------|----------|
| `topbar` | `AppShell` | `ReactNode` | No |
| `sidebar` | `AppShell` | `ReactNode` | No |
| `workspace` | `AppShell` | `ReactNode` | **Yes** |
| `rightPanel` | `AppShell` | `ReactNode` | No |
| `overlay` | `AppShell` | `ReactNode` | No |

---

## 11. Official Type Registry

| Type | Definition | File |
|------|-----------|------|
| `NavigationItem` | `{ id, icon, label, href, permissions?, badge?, hidden?, children? }` | `types/navigation.ts` |
| `NavigationGroup` | `{ id, label?, items: NavigationItem[] }` | `types/navigation.ts` |
| `NavigationRegistry` | `NavigationGroup[]` | `types/navigation.ts` |
| `Breadcrumb` | `{ label, href? }` | `store/layout-store.ts` |
| `LayoutMode` | `'ultrawide' \| 'desktop' \| 'tablet' \| 'mobile'` | `store/layout-store.ts` |
| `MotionSpeed` | `'instant' \| 'fast' \| 'normal' \| 'slow' \| 'hero'` | `motion/motion-provider.tsx` |
| `ToastData` | `{ id, message, variant?, duration? }` | `ui/toast.tsx` |
| `ToastVariant` | `'success' \| 'error' \| 'warning' \| 'info'` | `ui/toast.tsx` |

---

## 12. Component Import Paths

```
@/components/ui/*          → Tier 1 + Tier 4
@/components/layout/*      → Tier 2
@/components/shared/*      → Tier 3
@/components/motion/*      → Motion (provider + hooks)
@/store/*                  → State stores
@/hooks/*                  → Custom hooks
@/types/*                  → Type definitions
@/lib/utils                → cn() utility
```

---

## 13. Forbidden Components & Patterns

The following are **explicitly forbidden** in the Experience Layer v1.0:

### Forbidden Components
- No third-party component libraries (Material UI, Chakra, Ant Design, etc.)
- No page-level components in `components/` directories
- No direct Runtime imports in any component
- No SDK imports in Tier 1, Tier 2, or Tier 4 components

### Forbidden Patterns
- **Direct Runtime access:** Components must never call or import Runtime modules
- **Inline styles:** Must use CSS custom properties (tokens) or Tailwind classes
- **Component-specific CSS files:** Use Tailwind + tokens only
- **Circular dependencies:** Tier 1 must not import Tier 2+; Tier 2 must not import Tier 3+; Layout must not import Domain
- **Business logic in UI:** All business logic belongs in features, services, or SDK
- **Redundant state:** If state exists in LayoutStore, do not duplicate it in component-local state
- **Uncontrolled motion:** Every animation must respect `reducedMotion` from `useMotion()`

---

## 14. Process for Adding New Components

Any addition to the Experience Layer requires:

1. **RFC:** File a proposal at `docs/rfc/RFC_TEMPLATE.md` following the standard format
2. **Review:** Peer review by at least one other developer
3. **Approval:** Sign-off by the Chief Architect or TSC
4. **Implementation:** Must follow UI-0006 Component Guidelines
5. **Requirements:**
   - Typed Props interface with JSDoc
   - All states (loading, disabled, empty, error where applicable)
   - Keyboard navigation and ARIA attributes
   - Dark mode via CSS variables
   - Reduced-motion support via `useMotion()`
   - Responsive behavior where applicable
   - Barrel export in `index.ts`
   - Entry in Component Gallery (`/dev/gallery`)
6. **CI Gate:** Build, lint, typecheck must pass at zero
7. **Documentation:** Update `EXPERIENCE_FREEZE_v1.md` with the new entry

---

## 15. Versioning

| Version | Date | Author | Change |
|---------|------|--------|--------|
| v1.0 | 2026-07-20 | Chief Architect | Initial freeze after GATE 4 |

---

*This document is the single source of truth for the ASCEND Experience Layer. Any discrepancy between this document and the codebase should be resolved by updating this document via RFC.*
