# WF-0009 — Command Palette

| Campo | Valor |
|-------|-------|
| **ID** | WF-0009 |
| **Nome** | Command Palette |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | Wireframe |
| **Derivado de** | ARCH-0011, UI-0001, UI-0003 |
| **Será utilizado por** | Frontend Sprint 1 |

---

## 1. Propósito

A Command Palette é o mecanismo de navegação e ação universal do ASCEND.

Inspirada no Raycast e no Spotlight do macOS, ela permite que o Builder:

- Navegue para qualquer página instantaneamente
- Execute ações sem usar o mouse
- Busque missões, competências, configurações
- Descubra funcionalidades que não conhecia

---

## 2. Atalho

| Plataforma | Atalho |
|------------|--------|
| macOS | `Cmd + K` |
| Windows/Linux | `Ctrl + K` |

Disponível de **qualquer tela** do ASCEND.

---

## 3. Wireframe Desktop

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│                                                                  │
│                  ┌─────────────────────────────────────┐         │
│                  │  🔍  Search commands, pages...       │         │
│                  │  ⌨️  Ctrl+K to open                  │         │
│                  └─────────────────────────────────────┘         │
│                                                                  │
│                  ┌─────────────────────────────────────┐         │
│                  │  Pages                               │         │
│                  │  ┌─────────────────────────────────┐ │         │
│                  │  │ 🏠  Dashboard                  │ │         │
│                  │  │ 🗡️  Missions  >  Active         │ │         │
│                  │  │ 🧠  Competencies  >  Linux      │ │         │
│                  │  │ 📁  Evidence                    │ │         │
│                  │  │ 🤖  AI Mentor                   │ │         │
│                  │  │ 🌐  Community                   │ │         │
│                  │  │ ⚙️  Settings                    │ │         │
│                  │  └─────────────────────────────────┘ │         │
│                  │                                         │         │
│                  │  Quick Actions                          │         │
│                  │  ┌─────────────────────────────────┐ │         │
│                  │  │ 🗡️  Start next mission          │ │         │
│                  │  │ 📁  Submit evidence             │ │         │
│                  │  │ 💬  Ask the Mentor              │ │         │
│                  │  │ 🔄  Continue last mission        │ │         │
│                  │  │ 📊  View my progress             │ │         │
│                  │  └─────────────────────────────────┘ │         │
│                  │                                         │         │
│                  │  Recent                                │         │
│                  │  ┌─────────────────────────────────┐ │         │
│                  │  │ 🗡️  Linux #4  (continue)        │ │         │
│                  │  │ 📁  Evidence #23  (view result)  │ │         │
│                  │  │ 🏅  Badge: "Consistent"         │ │         │
│                  │  └─────────────────────────────────┘ │         │
│                  │                                         │         │
│                  │  Tips                                   │         │
│                  │  Tip: Type "?" to see all commands      │         │
│                  └─────────────────────────────────────┘         │
│                                                                  │
│                                                                  │
│          ←── Overlay escurece o fundo em 60% ──→                │
└──────────────────────────────────────────────────────────────────┘
```

---

## 4. Search Behavior

### 4.1 Default State

Ao abrir, mostra as ações mais comuns e recentes.

### 4.2 Typing

```
Input: "lin"

Results:
  ┌──────────────────────────────────────┐
  │ 🗡️  Linux Basics  (Journey)          │
  │ 🗡️  Linux #4: User Management        │
  │ 🧠  Linux System Administration      │
  │ ⚙️  Settings > Preferences > Language│
  └──────────────────────────────────────┘
```

### 4.3 Fuzzy Search

A busca usa fuzzy matching: "linadm" encontra "Linux Administration".

### 4.4 No Results

```
  ┌──────────────────────────────────────────────┐
  │  No results found for "xyz"                  │
  │                                              │
  │  Suggestions:                                │
  │  • Check the spelling                        │
  │  • Try a broader term                        │
  │  • Browse Missions instead                   │
  └──────────────────────────────────────────────┘
```

---

## 5. Command Types

| Type | Icon | Description | Example |
|------|------|-------------|---------|
| **Page** | 🏠 | Navigate to a page | "Dashboard" |
| **Mission** | 🗡️ | Open a specific mission | "Linux #4" |
| **Action** | ⚡ | Execute an action | "Submit evidence" |
| **Search** | 🔍 | Search within a section | "Find Linux missions" |
| **Setting** | ⚙️ | Open a settings page | "Change theme" |
| **Mentor** | 🤖 | Ask the mentor | "Ask: how to use grep" |

---

## 6. Keyboard Navigation

| Key | Action |
|-----|--------|
| `Ctrl+K` | Open/Close palette |
| `↑` / `↓` | Navigate results |
| `Enter` | Select result |
| `Tab` | Next section |
| `Escape` | Close palette |
| `Backspace` | (empty input) close palette |
| `?` | Show all available commands |
| `>` | Command mode (type commands directly) |

### 6.1 Power User Shortcuts

| Shortcut | Action |
|----------|--------|
| `> mentor What is X` | Ask mentor directly |
| `> mission start` | Start next available mission |
| `> evidence submit` | Open evidence upload |
| `> theme dark` | Switch to dark mode |
| `> goto settings` | Navigate to settings |

---

## 7. Sections

### 7.1 Pages

Lista completa de todas as páginas navegáveis do ASCEND.

### 7.2 Quick Actions

Ações frequentes que o Builder pode executar.

### 7.3 Recent

Últimos itens acessados pelo Builder.

### 7.4 Search Results

Resultados dinâmicos conforme o Builder digita.

### 7.5 Tips

Dicas contextuais de uso da palette.

---

## 8. States

| State | Visual |
|-------|--------|
| **Closed** | Overlay invisível |
| **Open (default)** | Overlay 60%, input focused, recent items |
| **Typing** | Results update in real-time (debounce 100ms) |
| **Loading results** | Spinner no input + "Searching..." |
| **No results** | "No results found" + suggestions |
| **Error** | "Search unavailable" + [Retry] |

---

## 9. Mobile Adaptation

No mobile, a Command Palette abre como tela cheia.

```
┌──────────────────────────┐
│ ← 🔍  Search...          │
│                          │
│ Pages                    │
│ 🏠 Dashboard             │
│ 🗡️ Missions              │
│ 🧠 Competencies          │
│                          │
│ Quick Actions            │
│ 🗡️ Start next mission    │
│ 📁 Submit evidence       │
│                          │
│ Keyboard: Search opens   │
│ native keyboard          │
└──────────────────────────┘
```

---

## 10. Motion Timeline

| Component | Animation | Duration | Easing |
|-----------|-----------|----------|--------|
| Overlay appear | fade-in | 150ms | ease-out |
| Palette enter | scale(0.95→1) + slide-down | 200ms | ease-out |
| Results change | cross-fade | 100ms | ease-out |
| Highlight row | background-color | 50ms | ease-out |
| Palette exit | fade-out + scale(1→0.95) | 100ms | ease-in |

---

## 11. Responsividade

| Tela | Comportamento |
|------|---------------|
| Desktop (>1024px) | Overlay centralizado, 640px width |
| Tablet (768-1023px) | Overlay centralizado, 90% width |
| Mobile (<768px) | Tela cheia, busca com teclado nativo |

---

## 12. Definition of Done

WF-0009 aprovado quando:

- [ ] Wireframe Desktop completo
- [ ] Search behavior documentado (default, typing, fuzzy, no results)
- [ ] Command types definidos
- [ ] Keyboard navigation completo
- [ ] Power user shortcuts documentados
- [ ] Sections (pages, actions, recent, tips) especificadas
- [ ] Estados (closed, open, typing, loading, no results, error)
- [ ] Mobile adaptation documentada
- [ ] Motion timeline completa
- [ ] Responsividade definida

---

## Status

**WF-0009 — Command Palette**

- Estado: ✅ Completo
- Próximo: WF-0010 — Mobile Experience
