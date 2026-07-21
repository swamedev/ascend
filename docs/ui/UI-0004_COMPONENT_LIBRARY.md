# UI-0004 — Component Library

| Campo | Valor |
|-------|-------|
| **ID** | UI-0004 |
| **Nome** | Component Library |
| **Versão** | 1.0-DRAFT |
| **Status** | Draft |
| **Categoria** | UI/UX |
| **Derivado de** | ARCH-0011 Experience Layer, UI-0001 Design System, UI-0003 Information Architecture |
| **Será utilizado por** | Frontend Implementation |

---

## 1. Component Philosophy

Todo componente no ASCEND deve responder positivamente a quatro perguntas:

1. **Ela melhora a aprendizagem do Builder?**
2. **Ela respeita a Constituição e os Protocolos?**
3. **Ela pode ser sustentada pela arquitetura existente sem criar acoplamentos desnecessários?**
4. **Ela mantém a experiência simples e intuitiva?**

Componentes que não passam por essas quatro perguntas não entram.

### Taxonomy

| Categoria | Descrição | Quantidade |
|-----------|-----------|------------|
| **Primitives** | Elementos base (botão, input, card) | ~15 |
| **Domain** | Componentes de domínio (BuilderCard, MissionCard) | ~25 |
| **Composite** | Combinações de componentes (Dashboard, Timeline) | ~10 |
| **Layout** | Estrutura da página (Sidebar, Header) | ~8 |
| **Feedback** | Estados e notificações (Toast, Skeleton) | ~8 |
| **Navigation** | Navegação (Tabs, Breadcrumb, CommandPalette) | ~6 |

---

## 2. Component Catalog

### 2.1 Primitives

Baseados em shadcn/ui com customizações do ASCEND Design System.

| Componente | Descrição | Props principais | Estados |
|------------|-----------|-----------------|---------|
| **Button** | Ação primária | `variant: primary|secondary|ghost|danger|link`, `size: sm|md|lg`, `loading` | default, hover, active, focus, disabled, loading |
| **Input** | Entrada de texto | `type: text|email|password|search`, `error`, `hint` | default, focus, error, disabled |
| **Textarea** | Entrada multi-linha | `rows`, `maxLength`, `error` | default, focus, error |
| **Select** | Seleção de opções | `options`, `placeholder`, `searchable` | default, open, selected, disabled |
| **Checkbox** | Seleção múltipla | `checked`, `indeterminate` | unchecked, checked, indeterminate |
| **Toggle** | On/off | `checked` | off, on |
| **Radio** | Seleção única | `options`, `value` | unchecked, checked |
| **Card** | Container de conteúdo | `variant: default|interactive`, `padding`, `onClick` | default, hover (if interactive) |
| **Badge** | Tag/categoria | `variant: default|success|warning|error|info|xp|gold`, `size` | default |
| **Avatar** | Foto do Builder | `src`, `fallback`, `size`, `status` | default, online, offline, busy |
| **Tooltip** | Informação contextual | `content`, `side: top|bottom|left|right` | hidden, visible |
| **Dialog** | Modal de confirmação | `title`, `description`, `actions` | open, closed |
| **Sheet** | Painel lateral | `side: left|right`, `size` | open, closed, closing |
| **Dropdown** | Menu suspenso | `items`, `align` | closed, open, item-hover |
| **Progress** | Barra de progresso | `value: 0-100`, `variant`, `size`, `animated` | empty, partial, complete, animated |

---

### 2.2 Domain Components

#### BuilderCard

**Descrição:** Card de perfil do Builder. Usado em sidebar, community, leaderboard.

```
┌──────────────────────────────┐
│  👤 BuilderName              │
│  Level 5 — Apprentice        │
│  ▓▓▓▓▓▓▓▓▓░░░  450/800 XP   │
│                              │
│  🔥 7-day streak             │
│  🏅 12 achievements          │
└──────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `builder` | `Builder` | Dados do Builder |
| `variant` | `compact | full` | Layout |
| `showStreak` | `boolean` | Mostrar streak |
| `showAchievements` | `boolean` | Mostrar achievements |

**Estados:** default, loading (skeleton), offline

---

#### MissionCard

**Descrição:** Card de missão. Usado em grids e listas.

```
┌──────────────────────────────┐
│  🗡️ Linux Basics — Mission 4│
│  "Configurar usuários Linux" │
│                              │
│  🎯 Medium  |  ⏱️ 45 min    │
│                              │
│  ▓▓▓▓▓░░░░░░  45%           │
│                              │
│  [Continuar]                 │
└──────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `mission` | `Mission` | Dados da missão |
| `variant` | `available | active | completed` | Estado |
| `progress` | `number` | 0-100 |
| `onStart` | `() => void` | Callback |
| `onContinue` | `() => void` | Callback |

**Estados:** available, active, completed, locked, loading

---

#### JourneyCard

**Descrição:** Card de jornada. Usado em catálogos.

```
┌──────────────────────────────┐
│  🗡️ Linux System Admin       │
│                              │
│  12 missões · 4 competências │
│                              │
│  ▓▓▓▓▓▓▓▓▓░░░  75%          │
│                              │
│  🏅 3/12 achievements        │
│                              │
│  [Continuar]                 │
└──────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `journey` | `Journey` | Dados da jornada |
| `progress` | `number` | 0-100 |
| `onClick` | `() => void` | Callback |

**Estados:** available, active, completed, locked

---

#### CompetencyTree

**Descrição:** Visualização interativa da árvore de competências.

```
         Linux System Admin
         │
    ┌────┼────┐
    │         │
  File     User      Network
  Mgmt    Admin      Basics
    │         │         │
  L1─L4    L1─L4     L1─L4
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `competencies` | `Competency[]` | Dados |
| `activeId` | `string` | Competência selecionada |
| `onNodeClick` | `(id) => void` | Callback |
| `zoomable` | `boolean` | Zoom in/out |
| `draggable` | `boolean` | Pan |

**Estados:** loading, empty, populated, zoom-level indicator

---

#### ProgressRing

**Descrição:** Anel de progresso circular. Usado para competências e achievements.

```
      ╭─────────╮
      │   75%   │
      │  ◉━━━━━╮│
      │  ┃     ┃│
      │  ╰━━━━━╯│
      ╰─────────╯
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `value` | `number` | 0-100 |
| `size` | `sm | md | lg` | Tamanho |
| `variant` | `default | xp | achievement | competency` | Cor |
| `animate` | `boolean` | Animação ao montar |
| `label` | `string` | Texto central |

**Estados:** empty (0%), partial, complete (100%), animated

---

#### XPBar

**Descrição:** Barra de XP do nível. Presente no header e sidebar.

```
  Level 5
  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░  450 / 800 XP
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `current` | `number` | XP atual |
| `max` | `number` | XP para próximo nível |
| `level` | `number` | Nível atual |
| `animate` | `boolean` | Animação de incremento |
| `size` | `sm | md` | Tamanho |

**Estados:** normal, level-up (animação de conclusão)

---

#### AchievementBadge

**Descrição:** Badge de conquista. Usado em grid de achievements.

```
┌──────────┐
│          │
│   🏆     │
│          │
│ Explorer │
│          │
└──────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `achievement` | `Achievement` | Dados |
| `variant` | `earned | locked | hidden` | Estado |
| `size` | `sm | md | lg` | Tamanho |
| `onClick` | `() => void` | Callback |

**Estados:** earned (colorido + glow), locked (cinza), hidden (silhueta), new (pulsing)

---

#### Timeline

**Descrição:** Timeline de atividades. Usado no dashboard e comunidad.

```
  ┌──────────────────────────────────┐
  │ ● Hoje                           │
  │ ├ 🗡️ Missão concluída: Linux #4  │  +100 XP
  │ ├ 📁 Evidência aprovada          │
  │ └ 🏅 Badge conquistado: Steps    │
  │                                  │
  │ ● Ontem                          │
  │ ├ 🗡️ Missão iniciada: Linux #5  │
  │ └ 🤖 Mentor: dica disponível     │
  └──────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `events` | `TimelineEvent[]` | Eventos |
| `variant` | `builder | community` | Escopo |
| `limit` | `number` | Máx de eventos |

**Estados:** loading, empty, populated

---

#### CommandPalette

**Descrição:** Busca e ações rápidas. Acessível via `Cmd+K`.

```
┌──────────────────────────────────────┐
│  🔍 Buscar no ASCEND...              │
│                                      │
│  Páginas                             │
│  ├ Dashboard                         │
│  ├ Missions > Active                  │
│  └ Competencies > Linux              │
│                                      │
│  Ações                               │
│  ├ 🗡️ Iniciar próxima missão          │
│  ├ 📁 Submeter evidência             │
│  └ 🤖 Falar com Mentor               │
└──────────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `open` | `boolean` | Visível |
| `onClose` | `() => void` | Fechar |
| `sections` | `CommandSection[]` | Seções de resultado |
| `placeholder` | `string` | Placeholder |

**Estados:** closed, open (with/without results), loading, empty

---

#### EvidenceUploader

**Descrição:** Área de upload de evidências.

```
┌──────────────────────────────────────┐
│  📁 Upload de Evidência              │
│                                      │
│  ┌────────────────────────────────┐  │
│  │                                │  │
│  │    Arraste arquivos ou clique  │  │
│  │    para fazer upload           │  │
│  │                                │  │
│  │    Formatos: .md, .pdf, .png, │  │
│  │    .zip até 10MB               │  │
│  │                                │  │
│  └────────────────────────────────┘  │
│                                      │
│  Arquivos selecionados:              │
│  ├ 📄 report.md                      │
│  └ 🖼️ screenshot.png                 │
│                                      │
│  Descrição:                          │
│  ┌────────────────────────────────┐  │
│  │ Descreva o que foi feito...    │  │
│  └────────────────────────────────┘  │
│                                      │
│  [Submeter para Revisão]             │
└──────────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `missionId` | `string` | Missão vinculada |
| `accept` | `string[]` | Formatos aceitos |
| `maxSize` | `number` | Tamanho máximo (MB) |
| `multiple` | `boolean` | Multiplos arquivos |
| `onSubmit` | `(files, description) => void` | Callback |

**Estados:** empty, dragging (highlight), uploading (progress), uploaded (success), error

---

#### MissionViewer

**Descrição:** Visualização completa de uma missão.

```
┌──────────────────────────────────────┐
│  Back to Missions                    │
│                                      │
│  🗡️ Linux Basics — Mission 4         │
│  "Configurar usuários Linux"         │
│                                      │
│  Status: Active | 🎯 Medium | ⏱️ 45m│
│                                      │
│  ┌─ Briefing ──────────────────────┐ │
│  │ Objetivo:                       │ │
│  │ Criar 3 usuários Linux com      │ │
│  │ permissões específicas...       │ │
│  │                                 │ │
│  │ Critérios:                      │ │
│  │ • Usuários criados corretamente │ │
│  │ • Permissões configuradas       │ │
│  │ • Documentação do processo      │ │
│  │                                 │ │
│  │ Dicas:                          │ │
│  │ • Use useradd e usermod         │ │
│  └─────────────────────────────────┘ │
│                                      │
│  ┌─ Recursos ─────────────────────┐  │
│  │ 📄 Linux Command Reference     │  │
│  │ 📺 Video: User Management     │  │
│  └────────────────────────────────┘  │
│                                      │
│  [Submeter Evidência]                │
└──────────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `mission` | `Mission` | Dados completos |
| `onStart` | `() => void` | Callback |
| `onEvidence` | `() => void` | Callback |

**Estados:** loading, briefing, active (with progress), submitted, reviewed (with feedback)

---

#### AI MentorPanel

**Descrição:** Painel de conversa com o Mentor Agent.

```
┌──────────────────────────────────────┐
│  🤖 AI Mentor                        │
│                                      │
│  ┌─ Messages ──────────────────────┐ │
│  │ Mentor: Olá! Como posso ajudar  │ │
│  │         com sua jornada hoje?   │ │
│  │                                 │ │
│  │ Você: Qual a próxima missão     │ │
│  │       recomendada para Linux?   │ │
│  │                                 │ │
│  │ Mentor: Baseado no seu          │ │
│  │         progresso, recomendo    │ │
│  │         "Mission 5 — Network    │ │
│  │         Configuration"          │ │
│  └─────────────────────────────────┘ │
│                                      │
│  ┌─ Suggestions ──────────────────┐  │
│  │ 💡 "Quer uma dica para         │  │
│  │      a missão atual?"          │  │
│  │ 💡 "Veja seu career path"      │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────┐      │
│  │ Digite sua mensagem...    ➤ │      │
│  └────────────────────────────┘      │
└──────────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `messages` | `Message[]` | Histórico |
| `suggestions` | `Suggestion[]` | Sugestões |
| `onSend` | `(text) => void` | Callback |
| `loading` | `boolean` | Mentora pensando |

**Estados:** empty (welcome message), conversation, loading (typing indicator), error

---

#### Leaderboard

**Descrição:** Ranking da comunidad.

```
┌──────────────────────────────────────┐
│  🌐 Leaderboard                      │
│  [Weekly] [Monthly] [All Time]       │
│                                      │
│  #1  🥇 BuilderOne     Level 12     │
│  #2  🥈 CyberNinja     Level 10     │
│  #3  🥉 DataMaster     Level 9      │
│  #4  YourName          Level 8  ←   │
│  #5  CloudDev          Level 8      │
└──────────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `entries` | `LeaderboardEntry[]` | Rankings |
| `period` | `weekly | monthly | alltime` | Período |
| `currentUserId` | `string` | Destacar usuário |
| `limit` | `number` | Itens visíveis |

**Estados:** loading, empty, populated, highlight-current

---

#### ActivityFeed

**Descrição:** Feed de atividades globais ou do Builder.

```
┌──────────────────────────────────────┐
│  📢 Atividade Recente                │
│                                      │
│  🗡️ BuilderOne completou Mission 4   │  2m ago
│  🏅 CyberNinja desbloqueou "Expert"  │  5m ago
│  📁 DataMaster submeteu evidência    │  12m ago
│  🤖 Mentor respondeu CloudDev        │  18m ago
│  🎉 BuilderOne level up!             │  30m ago
└──────────────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `events` | `FeedEvent[]` | Eventos |
| `variant` | `builder | community` | Escopo |
| `onLoadMore` | `() => void` | Paginação |

**Estados:** loading, empty (CTA), populated

---

### 2.3 Composite Components

#### DashboardOverview

**Descrição:** Composite que monta a página inicial.

**Composto por:** `BuilderCard` (compact), `MissionCard` (active), `Timeline`, `AchievementBadge` (next), `XPBar`, `AI MentorPanel` (suggestions only)

---

#### JourneyDetailPage

**Descrição:** Página de detalhe da jornada.

**Composto por:** `JourneyCard` (large), `ProgressRing`, `MissionCard[]`, `CompetencyTree` (mini)

---

#### MissionDetailPage

**Descrição:** Página de detalhe da missão.

**Composto por:** `MissionViewer`, `EvidenceUploader`, `Timeline` (mission history)

---

#### CompetencyDetailPage

**Descrição:** Página de detalhe da competência.

**Composto por:** `CompetencyTree` (zoom), `ProgressRing`, `Timeline`, `AchievementBadge[]`

---

#### BuilderProfilePage

**Descrição:** Perfil do Builder.

**Composto por:** `BuilderCard` (full), `XPBar`, `AchievementBadge[]`, `Timeline`, `ProgressRing[]`, `CompetencyTree` (mini)

---

### 2.4 Layout Components

#### AppShell

**Descrição:** Estrutura base de todas as páginas.

```
┌──────────────────────────────────┐
│  Header                          │
├──────┬───────────────────────────┤
│      │                            │
│ Side │    Main Content            │
│ Bar  │    (children)             │
│      │                            │
│      │                            │
└──────┴───────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `sidebar` | `ReactNode` | Sidebar content |
| `header` | `ReactNode` | Header content |
| `children` | `ReactNode` | Main content |

**Estados:** desktop (sidebar visible), mobile (sidebar hidden, bottom nav)

---

#### Sidebar

**Descrição:** Navegação lateral primária.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `items` | `NavItem[]` | Links |
| `collapsed` | `boolean` | Estado recolhido |
| `builder` | `Builder` | Perfil no footer |

**Estados:** expanded, collapsed, mobile (hidden)

---

#### Header

**Descrição:** Topo da página.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `breadcrumb` | `BreadcrumbItem[]` | Navegação |
| `title` | `string` | Título da página |
| `actions` | `ReactNode` | Ações contextuais |
| `builder` | `Builder` | Avatar + level |

**Estados:** default, scroll (shadow)

---

#### PageContainer

**Descrição:** Container de conteúdo com padding e largura máxima.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `maxWidth` | `sm | md | lg | xl | full` | Largura máxima |
| `padding` | `boolean` | Padding padrão |

---

### 2.5 Feedback Components

#### Toast

**Descrição:** Notificação temporária.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `variant` | `success | error | warning | info` | Tipo |
| `title` | `string` | Título |
| `description` | `string` | Descrição |
| `duration` | `number` | ms (default: 4000) |
| `action` | `{ label, onClick }` | Ação opcional |

**Estados:** entering, visible, exiting

---

#### Skeleton

**Descrição:** Placeholder de loading.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `variant` | `text | card | avatar | circle` | Forma |
| `width` | `string` | Largura |
| `height` | `string` | Altura |
| `count` | `number` | Repetições |

---

#### EmptyState

**Descrição:** Estado vazio com ilustração.

```
┌──────────────────────────────┐
│                              │
│       🎯 (Ilustração)        │
│                              │
│   Nenhuma missão ativa       │
│                              │
│   Comece explorando as       │
│   jornadas disponíveis       │
│                              │
│   [Explorar Jornadas]        │
│                              │
└──────────────────────────────┘
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `icon` | `string` | Lucide icon name |
| `title` | `string` | Título |
| `description` | `string` | Descrição |
| `action` | `{ label, onClick }` | CTA |

---

#### CelebrationOverlay

**Descrição:** Overlay de celebração (level up, achievement).

```
╔══════════════════════════════╗
║                              ║
║         ▲ ▲ ▲               ║
║        LEVEL UP!             ║
║                              ║
║     Builder → Apprentice     ║
║                              ║
║   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  5    ║
║                              ║
║   Desbloqueado:              ║
║   • Mentor Agent             ║
║   • Advanced Missions        ║
║                              ║
║   [Continuar]                ║
╚══════════════════════════════╝
```

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `variant` | `levelup | achievement | certificate` | Tipo |
| `data` | `object` | Dados do evento |
| `onClose` | `() => void` | Fechar |
| `autoClose` | `number` | Auto-fechar (ms) |

**Estados:** entering (confetti animation), visible, exiting

---

### 2.6 Navigation Components

#### Tabs

**Descrição:** Navegação por abas.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `tabs` | `Tab[]` | Abas |
| `activeTab` | `string` | Aba ativa |
| `onChange` | `(tab) => void` | Callback |
| `variant` | `underline | pills` | Estilo |

---

#### Breadcrumb

**Descrição:** Navegação hierárquica.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `items` | `{ label, href }[]` | Caminho |

---

#### Pagination

**Descrição:** Navegação paginada.

| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| `current` | `number` | Página atual |
| `total` | `number` | Total de páginas |
| `onChange` | `(page) => void` | Callback |

---

## 3. Component Hierarchy (Import Tree)

```
AppShell
├── Sidebar
│   ├── Logo
│   ├── NavItem[]
│   └── BuilderCard (compact)
├── Header
│   ├── Breadcrumb
│   ├── StreakIndicator
│   ├── NotificationBell → Dropdown
│   └── Avatar
└── PageContainer
    ├── Tabs
    ├── [Page-specific content]
    └── Toast (portal)

DashboardOverview
├── BuilderCard
├── MissionCard (active)
├── XPBar
├── ProgressRing[]
├── Timeline
├── AchievementBadge (next)
└── ActivityFeed (mini)

JourneyDetailPage
├── JourneyCard (large)
├── ProgressRing
├── MissionCard[]
└── CompetencyTree (mini)

MissionDetailPage
├── MissionViewer
├── EvidenceUploader
└── Timeline

CompetencyDetailPage
├── CompetencyTree
├── ProgressRing
├── Timeline
└── AchievementBadge[]

BuilderProfilePage
├── BuilderCard (full)
├── XPBar
├── AchievementBadge[]
├── Timeline
├── ProgressRing[]
└── CompetencyTree (mini)
```

---

## 4. Component States Matrix

| Componente | Loading | Empty | Default | Hover | Active | Focus | Disabled | Error | Success |
|------------|---------|-------|---------|-------|--------|-------|----------|-------|---------|
| Button | ✅ | — | ✅ | ✅ | ✅ | ✅ | ✅ | — | — |
| Input | — | ✅ placeholder | ✅ | — | — | ✅ | ✅ | ✅ | ✅ |
| Card | ✅ skeleton | — | ✅ | ✅ | — | — | — | — | — |
| MissionCard | ✅ skeleton | — | ✅ | ✅ | ✅ | — | ✅ locked | — | — |
| JourneyCard | ✅ skeleton | — | ✅ | ✅ | ✅ | — | ✅ locked | — | — |
| ProgressRing | ✅ | ✅ 0% | ✅ | — | — | — | — | — | ✅ 100% |
| XPBar | ✅ | ✅ 0 | ✅ | — | — | — | — | — | ✅ level-up |
| AchievementBadge | ✅ skeleton | — | ✅ | ✅ | — | — | ✅ locked | — | — |
| Timeline | ✅ skeleton | ✅ | ✅ | — | — | — | — | — | — |
| EvidenceUploader | — | ✅ | ✅ | ✅ dragging | — | ✅ | ✅ uploading | ✅ | ✅ |
| Leaderboard | ✅ skeleton | ✅ | ✅ | — | — | — | — | — | — |
| AI MentorPanel | ✅ | ✅ welcome | ✅ | — | — | ✅ | — | ✅ | — |

---

## 5. Responsive Behavior

| Componente | Desktop (>=1024px) | Tablet (768-1023px) | Mobile (<768px) |
|------------|-------------------|--------------------|-----------------|
| **AppShell** | Sidebar visible | Sidebar collapsible | Bottom nav |
| **Sidebar** | Fixed, 260px | Overlay drawer | Hidden |
| **Header** | Full | Compact | Icon only |
| **MissionCard** | Grid 3-col | Grid 2-col | Stack |
| **JourneyCard** | Grid 3-col | Grid 2-col | Stack |
| **CompetencyTree** | Full interativo | Scroll horizontal | Simplified list |
| **Timeline** | Full | Full | Compact |
| **AI MentorPanel** | Side panel | Full page | Full page |
| **Leaderboard** | Table | Table | List |
| **EvidenceUploader** | Inline | Inline | Full width |
| **CommandPalette** | Overlay | Overlay | Full screen |

---

## 6. Accessibility Requirements

| Componente | ARIA | Keyboard | Screen Reader |
|------------|------|----------|---------------|
| **Button** | `role="button"`, `aria-label` | Enter/Space | "Button, label" |
| **Card (interactive)** | `role="button"`, `tabindex="0"` | Enter | "Card, title, clickable" |
| **ProgressRing** | `role="progressbar"`, `aria-valuenow` | — | "75 percent complete" |
| **XPBar** | `role="progressbar"`, `aria-valuenow` | — | "450 of 800 XP" |
| **AchievementBadge** | `aria-label` | Enter (if clickable) | "Badge: Explorer, earned" |
| **Timeline** | `aria-label="Activity timeline"` | — | "Timeline, event list" |
| **CommandPalette** | `role="dialog"`, `aria-label` | Arrow, Enter, Esc | "Command palette, search" |
| **Tabs** | `role="tablist"`, `aria-selected` | Arrow keys | "Tab, label, selected" |
| **Toast** | `role="alert"`, `aria-live="polite"` | — | "Alert, message" |

---

## 7. Component Naming Convention

```
[Domain][Component][Variant]
```

**Exemplos:**
- `MissionCardActive`
- `AchievementBadgeEarned`
- `ProgressRingXp`
- `BuilderCardCompact`

**File structure:**
```
components/
  primitives/
    button.tsx
    input.tsx
    card.tsx
    ...
  domain/
    mission/
      mission-card.tsx
      mission-viewer.tsx
      evidence-uploader.tsx
    achievement/
      achievement-badge.tsx
    competency/
      competency-tree.tsx
    builder/
      builder-card.tsx
    mentor/
      ai-mentor-panel.tsx
    ...
  composite/
    dashboard-overview.tsx
    journey-detail-page.tsx
    ...
  layout/
    app-shell.tsx
    sidebar.tsx
    header.tsx
    page-container.tsx
  feedback/
    toast.tsx
    skeleton.tsx
    empty-state.tsx
    celebration-overlay.tsx
  navigation/
    tabs.tsx
    breadcrumb.tsx
    command-palette.tsx
    pagination.tsx
```

---

## 8. Definition of Done

UI-0004 aprovado quando:

- [ ] Primitives catalogados (~15 componentes)
- [ ] Domain components catalogados (~12 componentes)
- [ ] Composite components listados (~5 componentes)
- [ ] Layout components definidos (~4 componentes)
- [ ] Feedback components especificados (~4 componentes)
- [ ] Navigation components listados (~4 componentes)
- [ ] Cada componente tem descrição, props, estados
- [ ] Component hierarchy (import tree) documentada
- [ ] Component states matrix completa
- [ ] Responsive behavior por componente mapeado
- [ ] Accessibility requirements por componente
- [ ] Naming convention e file structure definidos

---

## Status

**UI-0004 — Component Library**

- Estado: 🟡 Draft técnico
- Resultado: Catálogo completo de componentes — ~45 componentes em 6 categorias, props, estados, responsividade, acessibilidade
- Próximo: Frontend Implementation — Sprint 1
