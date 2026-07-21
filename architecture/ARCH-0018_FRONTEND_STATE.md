# ARCH-0018 — Frontend State Management

| Field | Value |
|-------|-------|
| **ID** | ARCH-0018 |
| **Name** | Frontend State Management |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | ARCH-0011, ARCH-0016, ARCH-0017 |
| **Referenced by** | ARCH-0019, ARCH-0022 |

---

## 1. Purpose

Define what state lives where, who owns it, and how it flows through the frontend.

---

## 2. State Ownership Table

| State Type | Tool | Location | Persistence | Scope |
|------------|------|----------|-------------|-------|
| **Server State** | React Query | Cache layer | Memory (stale-while-revalidate) | Global |
| **UI State** | Zustand | Store | Memory (browser session) | Global |
| **URL State** | Next.js Router | URL | Browser URL bar | Page-scoped |
| **Offline State** | IndexedDB | Browser DB | Disk (persistent) | Global |
| **Session State** | Zustand + Secure Storage | Memory + encrypted store | Memory + cookie/localStorage | Global |
| **Form State** | React Hook Form | Component | Memory (unmounts) | Component-scoped |
| **Local Component State** | `useState` | Component | Memory (unmounts) | Component-scoped |

---

## 3. State Layer Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    URL STATE (Next.js Router)                    │
│  /missions/active  │  page=2  │  filter=status:eq:active        │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SERVER STATE (React Query)                    │
│  ['missions', 'list', { status: 'active' }] → MissionListResponse│
│  ['missions', 'detail', 'm4']              → MissionResponse    │
│  ['builder', 'me']                          → BuilderResponse    │
│                                                                  │
│  Cache: 5s default TTL │ Stale-while-revalidate │ Auto-refetch   │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    UI STATE (Zustand)                            │
│  sidebarOpen: boolean                                            │
│  theme: 'light' | 'dark'                                        │
│  currentMissionId: string | null                                 │
│  focusMode: boolean                                              │
│  notifications: Notification[]                                   │
│  toastQueue: Toast[]                                             │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SESSION STATE (Zustand + Secure)               │
│  authToken: string | null (memory)                               │
│  refreshToken: string (encrypted)                                │
│  localUuid: string (IndexedDB)                                   │
│  sessionStatus: 'anonymous' | 'authenticated' | 'expired'       │
└─────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OFFLINE STATE (IndexedDB)                      │
│  pendingQueue: OfflineAction[]   (evidence submissions, etc.)    │
│  cachedMissions: Mission[]       (for offline reading)           │
│  cachedCompetencies: Competency[]                                │
│  localProgress: Progress                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. What Goes Where

### 4.1 React Query (Server State)

```typescript
// All API data lives here
const { data, isLoading, error } = useQuery({
  queryKey: ['missions', 'list', filters],
  queryFn: () => client.missions.list(filters),
  staleTime: 5000,        // 5s
  gcTime: 5 * 60 * 1000, // 5min garbage collection
})

// Mutations
const mutation = useMutation({
  mutationFn: (id: string) => client.missions.start(id),
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['missions'] })
  }
})
```

**Stores:** All data returned from the API. Never duplicated in Zustand.

### 4.2 Zustand (UI State)

```typescript
interface UIState {
  // Navigation
  sidebarOpen: boolean
  currentView: string

  // Theme
  theme: 'light' | 'dark'

  // Mission context
  focusMode: boolean
  activeMissionId: string | null

  // Feedback
  toasts: Toast[]
  notifications: Notification[]

  // Actions
  toggleSidebar: () => void
  setTheme: (theme: 'light' | 'dark') => void
  enterFocusMode: () => void
  exitFocusMode: () => void
  addToast: (toast: Toast) => void
  removeToast: (id: string) => void
}
```

**Stores:** UI-only state that doesn't come from the server.

### 4.3 URL State (Router)

```typescript
// Page, filters, sort, pagination
// Example: /missions?status=active&page=2&sort=-created_at
const searchParams = useSearchParams()
const router = useRouter()
```

**Stores:** Shareable, bookmarkable, back-button-friendly state.

### 4.4 IndexedDB (Offline)

```typescript
interface OfflineStore {
  pendingQueue: OfflineAction[]
  missionCache: Map<string, Mission>
  competencyCache: Map<string, Competency>
  localProgress: LocalProgress
}
```

**Stores:** Data needed when offline. Synced when connection restores.

### 4.5 Session (Auth)

```typescript
interface SessionState {
  status: 'anonymous' | 'authenticated' | 'expired'
  localUuid: string
  accessToken: string | null  // memory only
  builder: BuilderSummary | null
}
```

**Stores:** Authentication state. Access token never touches localStorage.

---

## 5. State Flow Rules

| Rule | Description |
|------|-------------|
| **No duplicate server state** | Never copy server data into Zustand. Query it from React Query. |
| **UI state is ephemeral** | Zustand resets on session end. Persistent preferences use IndexedDB. |
| **URL is the source of truth for navigation** | Page, filters, pagination live in the URL. |
| **Offline mutations queue** | Write to IndexedDB + queue for sync. Never block the UI. |
| **Session is secure** | Access token lives in memory. Refresh token is encrypted. |

---

## 6. Zustand Store Structure

```
store/
├── index.ts              # Combined store
├── ui-store.ts           # Theme, sidebar, toasts
├── session-store.ts      # Auth state, tokens
├── mission-store.ts      # Active mission context
└── preferences-store.ts  # User preferences (persisted)
```

---

## 7. State Access Patterns

```typescript
// Component: Read server data
function ActiveMission() {
  const { data: mission, isLoading } = useQuery({
    queryKey: ['missions', 'active'],
    queryFn: () => client.missions.list({ status: 'active' }),
  })

  const { focusMode, enterFocusMode } = useUIStore()

  if (isLoading) return <Skeleton />
  return <MissionCard mission={mission} />
}

// Component: Read URL state
function MissionList() {
  const searchParams = useSearchParams()
  const status = searchParams.get('status') ?? 'active'
  const page = parseInt(searchParams.get('page') ?? '1')
}
```

---

## 8. Definition of Done

ARCH-0018 aprovado quando:

- [ ] State ownership table complete (6 state types)
- [ ] State layer diagram documented
- [ ] React Query scope defined
- [ ] Zustand scope defined
- [ ] URL state scope defined
- [ ] IndexedDB offline state defined
- [ ] Session state defined
- [ ] State flow rules established (5 rules)
- [ ] Zustand store structure defined
- [ ] State access patterns demonstrated

---

## 9. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
