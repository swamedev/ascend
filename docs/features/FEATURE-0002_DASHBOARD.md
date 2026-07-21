# FEATURE-0002 — Dashboard

> **Status:** Draft  
> **Author:** Chief Architect  
> **Date:** 2026-07-20  
> **Phase:** F  
> **Depends on:** FEATURE-0001 (Authentication), Experience Freeze v1.0

---

## 1. Objective

Deliver the post-login home screen: at-a-glance overview of the user's ascension progress, active journeys, recent activity, and quick actions.

---

## 2. Scope

- Welcome section with user greeting + level + XP
- Ascension Ring with current level and progress
- Active journeys summary (up to 3, with progress bars)
- Recent activity feed (up to 5 items)
- Quick action buttons (Start Journey, View Profile, etc.)
- Empty states when no journeys or activity exist

---

## 3. Out of Scope

- Customizable widgets / dashboard layout
- Detailed analytics or charts
- Leaderboards or social feed
- Notification center — *deferred to post-MVP*
- Inline journey starting — *click navigates to Journey Explorer*

---

## 4. User Flows

### Flow A — First Visit (No Journeys)

```
User logs in for the first time
  → Dashboard loads
  → Shows Ascension Ring (level 1, 0% progress)
  → Shows "No journeys yet" empty state
  → Shows empty activity feed
  → Shows "Begin Your Journey" CTA button
```

### Flow B — Returning User (Active Journeys)

```
User logs in
  → Dashboard loads
  → Shows Ascension Ring with current level + XP progress bar
  → Shows up to 3 active journey cards with progress
  → Shows recent activity (XP earned, missions completed)
  → Shows "Continue Journey" quick actions
```

### Flow C — All Journeys Complete

```
User has completed all journeys
  → Dashboard shows max-level Ascension Ring
  → "All journeys complete" message
  → Call-to-action for new content or profile review
```

---

## 5. Components Used

| Component | Usage |
|-----------|-------|
| `PageContainer` | Dashboard layout wrapper |
| `AscensionRing` | Level + progress visualization |
| `XPBar` | XP progress toward next level |
| `LevelBadge` | Current level number |
| `JourneyCard` | Active journey summary |
| `ProgressIndicator` | Per-journey progress bars |
| `MissionStatus` | Journey status badges |
| `EvidenceBadge` | Evidence count per journey |
| `AchievementBadge` | Recent achievements |
| `Card`, `CardHeader`, `CardContent` | Widget containers |
| `Button` | Quick action CTA |
| `EmptyState` | No-journeys / no-activity states |
| `LoadingState` | Initial data fetch |
| `ErrorState` | Failed data load |
| `Divider` | Section separators |
| `TopBar` (via AppShell) | User menu + breadcrumb |

---

## 6. States

| State | Visual |
|-------|--------|
| `loading` | `LoadingState` in content area |
| `loaded` | Full dashboard with all widgets |
| `empty_journeys` | No journeys — empty state with CTA |
| `empty_activity` | No activity — muted "No recent activity" message |
| `error` | `ErrorState` with retry button |
| `all_complete` | All journeys at 100% — congratulatory message |

---

## 7. Events

| Event | Trigger | Effect |
|-------|---------|--------|
| `dashboard:load` | Page mount | Fetch user progress, journeys, activity |
| `dashboard:loaded` | Data received | Render all widgets |
| `dashboard:error` | API failure | Show ErrorState |
| `dashboard:cta:click` | User clicks quick action | Navigate to target route |

---

## 8. Required Data

```typescript
interface DashboardData {
  user: UserProfile
  ascension: {
    level: number
    currentXp: number
    maxXp: number
    progressPercent: number
  }
  activeJourneys: JourneySummary[]  // max 3
  recentActivity: ActivityItem[]    // max 5
}

interface JourneySummary {
  id: string
  title: string
  description: string
  progressPercent: number
  status: 'pending' | 'active' | 'completed' | 'locked'
  evidenceCount: number
  xpReward: number
}

interface ActivityItem {
  id: string
  type: 'xp_earned' | 'mission_completed' | 'level_up' | 'journey_completed' | 'achievement'
  label: string
  timestamp: string
  xp?: number
}
```

---

## 9. API Contracts (Mocked)

### GET /api/dashboard

```
Request:  Authorization: Bearer <token>
Success:  { data: DashboardData }
Error:    { error: string }
Status:   200 | 401 | 500
```

---

## 10. Acceptance Criteria

- [ ] Dashboard loads and displays user greeting with level
- [ ] Ascension Ring shows current level and accurate progress
- [ ] Active journeys render with correct progress bars
- [ ] Empty journey state shows when no journeys exist
- [ ] Recent activity shows up to 5 items with correct icons
- [ ] Quick action buttons navigate to correct routes
- [ ] Loading state shown during data fetch
- [ ] Error state shown on API failure
- [ ] Data refreshes on page navigation (not cached stale)
- [ ] Works in light and dark mode
- [ ] All content is keyboard navigable

---

## 11. Error Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| API returns 401 | Redirect to /login |
| API timeout | ErrorState with "Could not load dashboard" + Retry |
| Partial data (journeys loaded, activity failed) | Show journeys, skip activity section |

---

## 12. Expected Tests

```
dashboard/
  DashboardPage.test.tsx
    - renders welcome message with user name
    - shows AscensionRing with correct level
    - displays active journeys
    - shows EmptyState when no journeys
    - shows LoadingState during fetch
    - shows ErrorState on failure
  
  DashboardWidgets.test.tsx
    - renders recent activity list
    - renders quick action buttons
    - shows correct progress in XPBar
```
