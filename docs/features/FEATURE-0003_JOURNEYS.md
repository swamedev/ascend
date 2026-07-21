# FEATURE-0003 — Journeys

> **Status:** Draft  
> **Author:** Chief Architect  
> **Date:** 2026-07-20  
> **Phase:** G  
> **Depends on:** FEATURE-0001 (Authentication), Experience Freeze v1.0

---

## 1. Objective

Deliver the full journey experience: browse available journeys, view journey details with missions, search and filter, and track overall journey progress.

---

## 2. Scope

- Journey Explorer (grid/list of all available journeys)
- Journey Detail page (overview, missions list, progress, rewards)
- Search bar (by journey title)
- Filter (by status: All, Active, Completed, Locked)
- Journey progress (aggregate of mission progress)
- Empty state (no journeys match filters)
- Navigation: Dashboard → Journey Explorer → Journey Detail

---

## 3. Out of Scope

- Starting a journey (requires Mission Experience — Phase H)
- Journey creation / editing (admin feature, post-MVP)
- Journey sharing or social features
- Recommended journeys (ML-powered, post-MVP)

---

## 4. User Flows

### Flow A — Browse Journeys

```
User clicks "Journeys" in sidebar
  → Journey Explorer loads
  → Shows grid of JourneyCards
  → Each card shows: title, description, progress, status, XP reward
  → Search bar at top
  → Filter tabs (All / Active / Completed / Locked)
```

### Flow B — Search + Filter

```
User types "React" in search bar
  → Grid filters to matching journeys
User clicks "Active" filter tab
  → Grid filters to only active journeys
User clears search
  → Full grid restored
User selects filter with no matches
  → EmptyState: "No journeys match your criteria"
```

### Flow C — Journey Detail

```
User clicks a JourneyCard
  → Navigate to /journeys/:id
  → Shows: title, full description, progress bar, XP reward
  → Shows missions list (grouped by status)
  → Shows evidence count per mission
  → "Start Mission" button on first incomplete mission
  → Breadcrumb: Dashboard > Journeys > Journey Name
```

---

## 5. Components Used

| Component | Usage |
|-----------|-------|
| `PageContainer` | Explorer and Detail wrappers |
| `JourneyCard` | Journey grid items |
| `ProgressIndicator` | Per-journey and detail progress |
| `MissionStatus` | Status badges on cards and detail |
| `EvidenceBadge` | Evidence count on JourneyCard |
| `Badge` | XP reward badges |
| `Card`, `CardHeader`, `CardContent` | Detail page sections |
| `Tooltip` | Long-name truncation |
| `Input` | Search bar |
| `Button` | "Start Mission" CTAs |
| `EmptyState` | No-results state |
| `LoadingState` | Data fetching |
| `ErrorState` | API failure |
| `Breadcrumb` | Navigation breadcrumb |
| `Divider` | Section separation |
| `Sidebar` (via AppShell) | Journey navigation item |

---

## 6. States

| State | Visual |
|-------|--------|
| `loading` | Grid of Skeleton cards |
| `loaded` | Full grid of JourneyCards |
| `empty` | "No journeys available" EmptyState |
| `filtered_empty` | "No journeys match your criteria" |
| `detail_loading` | Skeleton detail layout |
| `detail_loaded` | Full journey detail |
| `detail_error` | ErrorState with retry |

---

## 7. Events

| Event | Trigger | Effect |
|-------|---------|--------|
| `journeys:load` | Explorer mount | Fetch all journeys |
| `journeys:search` | User types in search | Filter client-side |
| `journeys:filter` | User clicks filter tab | Filter by status |
| `journeys:select` | User clicks JourneyCard | Navigate to /journeys/:id |
| `journeys:detail:load` | Detail page mount | Fetch journey detail + missions |

---

## 8. Required Data

```typescript
interface Journey {
  id: string
  title: string
  description: string
  longDescription?: string
  progressPercent: number
  status: 'pending' | 'active' | 'completed' | 'locked'
  xpReward: number
  evidenceCount: number
  missionCount: number
  completedMissionCount: number
  category?: string
  prerequisites?: string[]
}

interface JourneyDetail extends Journey {
  missions: MissionSummary[]
  competencies: { name: string; score: number; maxScore: number }[]
  achievements?: { icon: string; label: string; unlocked: boolean }[]
}

interface MissionSummary {
  id: string
  title: string
  description: string
  status: 'pending' | 'active' | 'completed' | 'failed' | 'locked'
  xpReward: number
  evidenceCount: number
}
```

---

## 9. API Contracts (Mocked)

### GET /api/journeys

```
Request:  Authorization: Bearer <token>
Query:    ?search=&status=all|active|completed|locked
Success:  { data: Journey[] }
Error:    { error: string }
Status:   200 | 401
```

### GET /api/journeys/:id

```
Request:  Authorization: Bearer <token>
Success:  { data: JourneyDetail }
Error:    { error: string }
Status:   200 | 401 | 404
```

---

## 10. Acceptance Criteria

- [ ] Journey Explorer shows all available journeys
- [ ] Each JourneyCard shows correct title, progress, status, XP
- [ ] Search filters journeys by title in real-time
- [ ] Status filter tabs work correctly (All/Active/Completed/Locked)
- [ ] Combined search + filter works correctly
- [ ] Empty state shown when no journeys match filters
- [ ] Clicking a card navigates to /journeys/:id
- [ ] Journey Detail shows full description, progress, missions
- [ ] Missions list shows correct status and evidence count
- [ ] Breadcrumb updates correctly for detail page
- [ ] Loading/Error states handled on both pages
- [ ] Works in light and dark mode

---

## 11. Error Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Journey not found (404) | ErrorState: "Journey not found" + Back button |
| Search with no results | EmptyState: "No journeys match" |
| Network failure on explorer | ErrorState + Retry |
| Network failure on detail | ErrorState + Back button |

---

## 12. Expected Tests

```
journeys/
  JourneyExplorer.test.tsx
    - renders journey grid
    - search filters correctly
    - filter tabs switch correctly
    - combined search + filter works
    - shows EmptyState for no results
    - shows LoadingState during fetch
  
  JourneyDetail.test.tsx
    - renders journey info
    - shows missions list
    - breadcrumb matches journey name
    - shows ErrorState on 404
  
  JourneyCard.test.tsx
    - renders all journey fields
    - click navigates to detail
    - shows correct progress
```
