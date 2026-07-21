# UI-0001 — ASCEND Design System

| Campo | Valor |
|-------|-------|
| **ID** | UI-0001 |
| **Nome** | ASCEND Design System |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | UI/UX |
| **Derivado de** | ARCH-0011 Experience Layer, DOC-0004 Identity Architecture, DOC-0005 Brand Architecture |
| **Será utilizado por** | UI-0004 Component Library, Frontend Implementation |

---

## 1. Design System Philosophy

O ASCEND Design System não é uma coleção de componentes bonitos.

É uma **linguagem visual** que comunica os princípios do projeto:

- **Clareza** — interfaces que não precisam de explicação
- **Progresso** — cada pixel celebra evolução
- **Confiança** — solidez visual que reflete solidez arquitetural

### Tom

| Eixo | Posição |
|------|---------|
| Formal ↔ Casual | **Casual profissional** |
| Sério ↔ Divertido | **Sério com momentos de celebração** |
| Simples ↔ Complexo | **Simples nos detalhes, rico na profundidade** |
| Escuro ↔ Claro | **Both — Light/Dark mode** |

---

## 2. Color Palette

### 2.1 Brand Colors

| Token | Light | Dark | Uso |
|-------|-------|------|-----|
| `--ascend-brand-50` | #F0F4FF | #0D1428 | Background brand sutil |
| `--ascend-brand-100` | #D6E4FF | #1A2744 | Hover background |
| `--ascend-brand-200` | #ADC8FF | #2A3F66 | Border sutil |
| `--ascend-brand-300` | #84A9FF | #3D5A8C | Border ativo |
| `--ascend-brand-400` | #5B8AFF | #5375AD | Ícone brand |
| `--ascend-brand-500` | #3366FF | #6699FF | **Primary** |
| `--ascend-brand-600` | #2952CC | #80ADFF | Hover primary |
| `--ascend-brand-700` | #1F3D99 | #99C0FF | Active primary |
| `--ascend-brand-800` | #142966 | #B3D4FF | Text on dark |
| `--ascend-brand-900` | #0A1433 | #CCE5FF | Text on dark |

### 2.2 Neutral Colors

| Token | Light | Dark | Uso |
|-------|-------|------|-----|
| `--ascend-neutral-50` | #F8FAFC | #0F1115 | Background |
| `--ascend-neutral-100` | #F1F5F9 | #1A1D23 | Card background |
| `--ascend-neutral-200` | #E2E8F0 | #262A33 | Border sutil |
| `--ascend-neutral-300` | #CBD5E1 | #333842 | Border |
| `--ascend-neutral-400` | #94A3B8 | #4A4F5C | Placeholder |
| `--ascend-neutral-500` | #64748B | #646A78 | Secondary text |
| `--ascend-neutral-600` | #475569 | #838996 | Text muted |
| `--ascend-neutral-700` | #334155 | #A1A6B2 | Text |
| `--ascend-neutral-800` | #1E293B | #C1C6D0 | Heading |
| `--ascend-neutral-900` | #0F172A | #E1E5EB | Strong heading |

### 2.3 Semantic Colors

| Token | Light | Dark | Uso |
|-------|-------|------|-----|
| `--ascend-success` | #22C55E | #4ADE80 | Concluído, XP gained |
| `--ascend-warning` | #F59E0B | #FBBF24 | Atenção, pending |
| `--ascend-error` | #EF4444 | #F87171 | Erro, bloqueado |
| `--ascend-info` | #3B82F6 | #60A5FA | Informação, dica |
| `--ascend-xp` | #A855F7 | #C084FC | XP color, purple accent |

### 2.4 Gamification Colors

| Token | Light | Dark | Uso |
|-------|-------|------|-----|
| `--ascend-gold` | #F59E0B | #FCD34D | Achievements, badges |
| `--ascend-silver` | #9CA3AF | #D1D5DB | Level medals |
| `--ascend-bronze` | #D97706 | #FBBF24 | Starter badges |
| `--ascend-platinum` | #6EE7B7 | #A7F3D0 | Elite achievements |

---

## 3. Typography

### 3.1 Font Family

| Uso | Font | Fallback |
|-----|------|----------|
| Display/Headings | `Inter` | `system-ui, sans-serif` |
| Body | `Inter` | `system-ui, sans-serif` |
| Code/Monospace | `JetBrains Mono` | `monospace` |

### 3.2 Type Scale

| Token | Size | Weight | Line Height | Uso |
|-------|------|--------|-------------|-----|
| `--text-xs` | 0.75rem (12px) | 400 | 1.5 | Caption, metadata |
| `--text-sm` | 0.875rem (14px) | 400 | 1.5 | Body small, secondary |
| `--text-base` | 1rem (16px) | 400 | 1.5 | Body |
| `--text-lg` | 1.125rem (18px) | 500 | 1.4 | Lead, subtitles |
| `--text-xl` | 1.25rem (20px) | 600 | 1.3 | Section titles |
| `--text-2xl` | 1.5rem (24px) | 600 | 1.3 | Page titles |
| `--text-3xl` | 1.875rem (30px) | 700 | 1.2 | Hero titles |
| `--text-4xl` | 2.25rem (36px) | 700 | 1.2 | Display large |
| `--text-5xl` | 3rem (48px) | 800 | 1.1 | Display hero |

### 3.3 Font Weights

| Weight | Variable | Uso |
|--------|----------|-----|
| 400 | Regular | Body text |
| 500 | Medium | Navigation, buttons |
| 600 | Semibold | Subtitles, emphasis |
| 700 | Bold | Headings |
| 800 | ExtraBold | Display text |

---

## 4. Spacing System

Base unit: **4px** (0.25rem)

| Token | Value | Uso |
|-------|-------|-----|
| `--space-0` | 0 | No spacing |
| `--space-1` | 0.25rem (4px) | Micro spacing |
| `--space-2` | 0.5rem (8px) | Tight spacing |
| `--space-3` | 0.75rem (12px) | Small gap |
| `--space-4` | 1rem (16px) | Standard gap |
| `--space-5` | 1.25rem (20px) | Medium |
| `--space-6` | 1.5rem (24px) | Section gap |
| `--space-8` | 2rem (32px) | Large gap |
| `--space-10` | 2.5rem (40px) | XL |
| `--space-12` | 3rem (48px) | Section separator |
| `--space-16` | 4rem (64px) | Page section |
| `--space-20` | 5rem (80px) | Page section large |
| `--space-24` | 6rem (96px) | Hero section |

---

## 5. Grid System

### 5.1 Layout Grid

| Propriedade | Valor |
|-------------|-------|
| Columns | 12 |
| Gutter | `--space-6` (24px) |
| Max width | 1280px |
| Padding | `--space-6` (mobile: `--space-4`) |

### 5.2 Breakpoints

| Name | Min Width | Target |
|------|-----------|--------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop |
| `xl` | 1280px | Desktop wide |
| `2xl` | 1536px | Large desktop |

---

## 6. Border Radius

| Token | Value | Uso |
|-------|-------|-----|
| `--radius-none` | 0 | Tables, inputs |
| `--radius-sm` | 0.25rem (4px) | Small elements |
| `--radius-md` | 0.5rem (8px) | Cards, modals |
| `--radius-lg` | 0.75rem (12px) | Large cards |
| `--radius-xl` | 1rem (16px) | Dialogs, dropdows |
| `--radius-full` | 9999px | Badges, avatars |

---

## 7. Shadows

| Token | Light | Dark |
|-------|-------|------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | `0 1px 2px rgba(0,0,0,0.3)` |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.07)` | `0 4px 6px rgba(0,0,0,0.4)` |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | `0 10px 15px rgba(0,0,0,0.5)` |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.12)` | `0 20px 25px rgba(0,0,0,0.6)` |
| `--shadow-glow` | `0 0 20px rgba(51,102,255,0.15)` | `0 0 20px rgba(102,153,255,0.2)` |

---

## 8. Icons

### 8.1 Icon Library

**Lucide Icons** é a biblioteca oficial.

### 8.2 Icon Size Tokens

| Token | Size | Uso |
|-------|------|-----|
| `--icon-xs` | 12px | Inline, metadata |
| `--icon-sm` | 16px | Buttons, list items |
| `--icon-md` | 20px | Standard icon |
| `--icon-lg` | 24px | Section icons |
| `--icon-xl` | 32px | Empty states, heroes |
| `--icon-2xl` | 48px | Feature illustrations |

### 8.3 Icon Naming Convention

```
ascend:mission       → Sword
ascend:achievement   → Trophy
ascend:evidence      → FileCheck
ascend:xp            → Zap
ascend:level         → ArrowUpCircle
ascend:mentor        → Bot
ascend:journey       → Map
ascend:builder       → UserCheck
ascend:lab           → FlaskConical
ascend:community     → Users
```

---

## 9. Light / Dark Mode

### 9.1 Strategy

- **System preference first** — respeita `prefers-color-scheme`
- **Manual toggle** — o Builder pode sobrescrever
- **Persistência** — salva em `localStorage` + perfil
- **Transição suave** — `transition: background-color 0.3s, color 0.3s`

### 9.2 Dark Mode Adaptations

| Elemento | Light | Dark |
|----------|-------|------|
| Background | `--ascend-neutral-50` | `--ascend-neutral-50` (dark) |
| Cards | White | `--ascend-neutral-100` (dark) |
| Text | `--ascend-neutral-900` | `--ascend-neutral-900` (dark) |
| Borders | `--ascend-neutral-200` | `--ascend-neutral-200` (dark) |
| Shadows | Black/05 | Black/40+ |
| Brand | `#3366FF` appears | Glows slightly |

---

## 10. States

### 10.1 Interactive States

| State | Descrição | Implementação |
|-------|-----------|---------------|
| **Default** | Estado normal | Variante base |
| **Hover** | Mouse sobre | Brightness/darkness shift |
| **Active** | Click/pressionado | Scale(0.98) + cor mais forte |
| **Focus** | Teclado ativo | Outline 2px brand |
| **Disabled** | Não interativo | Opacity 50%, cursor not-allowed |
| **Loading** | Operação em andamento | Skeleton ou spinner |

### 10.2 Feedback States

| State | Visual | Uso |
|-------|--------|-----|
| **Success** | Green + check icon | Missão concluída, upload OK |
| **Error** | Red + alert icon | Falha, validação |
| **Warning** | Amber + warning icon | Pending, atenção |
| **Info** | Blue + info icon | Dica, tutorial |
| **Empty** | Illustration + text | Nenhum dado ainda |
| **Progress** | Progress bar / spinner | Operação em andamento |

### 10.3 Skeleton Loading

```
┌─────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓         │  ← Shimmer animation
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   │
│ ▓▓▓▓▓▓▓▓                │
└─────────────────────────┘

Animation: shimmer (gradient sweep)
Duration: 1.5s
Direction: left → right
```

---

## 11. Motion Guidelines

### 11.1 Principles

- **Rápido** — animações nunca atrapalham o fluxo
- **Suave** — easing natural, sem movimentos bruscos
- **Significativo** — cada movimento comunica algo
- **Moderado** — sem exageros, sem enjoo

### 11.2 Duration Tokens

| Token | Duration | Uso |
|-------|----------|-----|
| `--dur-instant` | 0ms | Mudanças de estado |
| `--dur-fast` | 100ms | Hover, micro-interações |
| `--dur-normal` | 200ms | Transições padrão |
| `--dur-slow` | 300ms | Page transitions |
| `--dur-celebrate` | 500ms | Level up, achievements |

### 11.3 Easing Tokens

| Token | Value | Uso |
|-------|-------|-----|
| `--ease-default` | `ease` | Padrão |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Entrada |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Saída |
| `--ease-in-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Entrada e saída |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Celebração |

### 11.4 Key Animations

| Animation | Descrição | Duration | Easing |
|-----------|-----------|----------|--------|
| `fade-in` | Aparecer | 200ms | ease-out |
| `slide-up` | Subir (cards, modais) | 300ms | ease-out |
| `slide-down` | Descer (dropdowns) | 200ms | ease-out |
| `scale-in` | Crescer de 0.95 → 1 | 200ms | ease-out |
| `xppulse` | XP counter incrementa | 300ms | ease-out |
| `confetti` | Achievement celebra | 800ms | ease-out |
| `shimmer` | Skeleton loading | 1.5s | linear (infinite) |
| `progress` | Barra de progresso | 600ms | ease-out |

---

## 12. Responsiveness

### 12.1 Adaptive Strategy

| Tela | Estratégia |
|------|------------|
| **Desktop (>=1024px)** | Layout completo, sidebar, multi-pane |
| **Tablet (768-1023px)** | Sidebar colapsável, single pane |
| **Mobile (<768px)** | Bottom nav, stack vertical, sheet modals |

### 12.2 Component Adaptation

| Componente | Desktop | Mobile |
|------------|---------|--------|
| Navigation | Sidebar vertical | Bottom tab bar |
| Modals | Center dialog | Bottom sheet |
| Tables | Full table | Card list |
| Tooltips | Hover tooltip | Tap to show |
| Command Palette | `Cmd+K` overlay | Full screen search |

---

## 13. Accessibility

| Critério | Implementação |
|----------|---------------|
| **Color contrast** | 4.5:1 (AA) mínimo, 7:1 (AAA) ideal |
| **Keyboard navigation** | Tab order lógico, skip links |
| **Focus indicators** | Visible outline 2px brand |
| **Screen readers** | ARIA labels, roles, live regions |
| **Motion** | `prefers-reduced-motion` respeitado |
| **Text scaling** | Suporta aumento de 200% sem quebra |
| **Touch targets** | Mínimo 44x44px |

---

## 14. Design Tokens Structure

```css
/* tokens.css */

:root {
  /* Brand */
  --ascend-brand-500: #3366FF;

  /* Neutrals */
  --ascend-neutral-50: #F8FAFC;
  /* ... */

  /* Semantic */
  --ascend-success: #22C55E;
  --ascend-error: #EF4444;
  --ascend-warning: #F59E0B;
  --ascend-info: #3B82F6;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --text-base: 1rem;
  /* ... */

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  /* ... */

  /* Radius */
  --radius-md: 0.5rem;

  /* Shadows */
  --shadow-md: 0 4px 6px rgba(0,0,0,0.07);

  /* Motion */
  --dur-normal: 200ms;
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
}

[data-theme="dark"] {
  --ascend-neutral-50: #0F1115;
  --ascend-brand-500: #6699FF;
  /* ... */
}
```

---

## 15. Definition of Done

UI-0001 aprovado quando:

- [ ] Paleta de cores completa (brand, neutral, semantic, gamification)
- [ ] Tipografia definida (fontes, scale, weights)
- [ ] Sistema de spacing documentado
- [ ] Grid e breakpoints estabelecidos
- [ ] Border radius e shadows especificados
- [ ] Biblioteca de ícones e tamanhos definidos
- [ ] Design tokens estruturados
- [ ] Light/Dark mode coberto
- [ ] Estados (loading, error, success, empty) documentados
- [ ] Motion guidelines completos
- [ ] Estratégia de responsividade clara
- [ ] Acessibilidade coberta

---

## Status

**UI-0001 — ASCEND Design System**

- Estado: 🟡 Draft técnico
- Resultado: Sistema de design completo — cores, tipografia, grid, spacing, ícones, tokens, modes, estados, motion, responsividade
- Próximo: UI-0002 — Builder Journey
