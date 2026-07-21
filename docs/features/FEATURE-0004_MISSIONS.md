# FEATURE-0004 — Missions

> **Status:** Draft  
> **Author:** Chief Architect  
> **Date:** 2026-07-20  
> **Phase:** H  
> **Depends on:** FEATURE-0003 (Journeys), Experience Freeze v1.0

---

## 1. Objective

Deliver the mission workspace — the core interaction surface where users complete missions, submit evidence, receive assessments, and track their progress within a journey.

---

## 2. Scope

- Mission Workspace (full-screen focus mode for active mission)
- Mission overview (title, description, objectives, XP reward)
- Evidence submission (text + file upload areas)
- Assessment display (pass/fail/score with feedback)
- Focus Mode (hides sidebar, expands workspace)
- Objective checklist (track sub-task completion)
- Mission status transitions (pending → active → submitted → assessed)

---

## 3. Out of Scope

- Real-time collaboration on missions
- Peer review / social assessment
- AI-powered evaluation (AI is a layer — post-MVP)
- Mission creation / editing (admin feature)
- Gamification animations (post-MVP)

---

## 4. User Flows

### Flow A — Start Mission

```
User is on Journey Detail
  → Clicks "Start Mission" on a pending mission
  → Mission Workspace opens in Focus Mode
  → Sidebar collapses
  → TopBar shows mission title + close button
  → Mission objectives displayed
  → Evidence submission area ready
```

### Flow B — Submit Evidence

```
User completes mission work
  → Writes reflection/notes in text area
  → Uploads supporting files (optional, 1-3 files)
  → Clicks "Submit for Assessment"
  → [Loading] submission in progress
  → [Success] mission status → "submitted", waiting for assessment
  → [Error] inline error, retry option
```

### Flow C — View Assessment

```
User returns to a mission with "submitted" status
  → Mission Workspace shows:
    - Assessment result (pass/fail) with score
    - Assessor feedback text
    - XP earned (if passed)
  → If passed: confetti/celebration visual
  → "Continue" button → back to Journey Detail
```

### Flow D — Focus Mode Navigation

```
User is in Mission Workspace
  → Sidebar hidden, workspace expanded
  → TopBar minimized: only mission title + close button
  → Clicks "Close" → exits Focus Mode
  → Returns to Journey Detail
  → If mission is "active", progress preserved
```

---

## 5. Components Used

| Component | Usage |
|-----------|-------|
| `PageContainer` | Workspace layout |
| `Card`, `CardHeader`, `CardContent`, `CardFooter` | Mission sections |
| `Button` | Start, Submit, Continue |
| `IconButton` | Close focus mode |
| `Textarea` | Evidence reflection input |
| `Input` | File label / optional fields |
| `Badge` | XP reward, status indicators |
| `ProgressIndicator` | Objective checklist progress |
| `MissionStatus` | Status display |
| `EvidenceBadge` | Attached evidence count |
| `LoadingState` | Mission fetch / submission |
| `ErrorState` | Fetch / submission error |
| `SuccessState` | Assessment passed |
| `Alert` | Submission feedback / warnings |
| `Divider` | Section separation |
| `Tooltip` | Objective clarification |
| `Workspace` (via AppShell) | Scrollable mission content |
| `TopBar` (via AppShell) | Title bar + close in focus mode |
| `Drawer` | Evidence file list sidebar |

### Focus Mode Integration

- Uses `useLayoutStore().setFocusMode(true/false)`
- Uses `useLayoutStore().setFullscreen(true/false)`
- AppShell automatically hides sidebar and collapses TopBar

---

## 6. States

| State | Visual |
|-------|--------|
| `loading` | Skeleton + spinner |
| `active` | Full workspace: objectives + evidence form |
| `submitting` | Button shows spinner, form disabled |
| `submitted` | "Awaiting assessment" message |
| `assessed_pass` | SuccessState with XP + confetti |
| `assessed_fail` | Feedback displayed, retry option |
| `error` | ErrorState with retry |
| `focus_mode` | Sidebar hidden, workspace expanded |

---

## 7. Events

| Event | Trigger | Effect |
|-------|---------|--------|
| `mission:start` | User clicks "Start Mission" | Mission status → active, open workspace in focus mode |
| `mission:submit` | User clicks "Submit" | Evidence payload sent, button → loading |
| `mission:submitted` | API confirms | Status → submitted, show confirmation |
| `mission:assessed` | Assessment received | Show result (pass/fail), XP earned |
| `mission:focus:enter` | Workspace opens | Focus mode on, sidebar hidden |
| `mission:focus:exit` | User clicks close | Focus mode off, return to journey |
| `mission:objective:check` | User toggles objective | Update progress indicator |

---

## 8. Required Data

```typescript
interface Mission {
  id: string
  journeyId: string
  title: string
  description: string
  objectives: Objective[]
  status: 'pending' | 'active' | 'submitted' | 'assessed' | 'failed' | 'locked'
  xpReward: number
  evidence?: EvidenceSubmission
  assessment?: Assessment
}

interface Objective {
  id: string
  label: string
  completed: boolean
}

interface EvidenceSubmission {
  text: string
  files: FileAttachment[]
  submittedAt: string
}

interface FileAttachment {
  id: string
  name: string
  size: number
  type: string
  url: string
}

interface Assessment {
  passed: boolean
  score: number
  maxScore: number
  feedback: string
  assessedBy: string
  assessedAt: string
  xpAwarded: number
}
```

---

## 9. API Contracts (Mocked)

### GET /api/missions/:id

```
Request:  Authorization: Bearer <token>
Success:  { data: Mission }
Error:    { error: string }
Status:   200 | 401 | 404
```

### POST /api/missions/:id/start

```
Request:  Authorization: Bearer <token>
Success:  { data: Mission }  // status → active
Error:    { error: string }
Status:   200 | 400 | 401
```

### POST /api/missions/:id/submit

```
Request:  Authorization: Bearer <token>
Body:     { text: string, files?: File[] }
Success:  { data: Mission }  // status → submitted
Error:    { error: string }
Status:   200 | 400 | 401
```

### GET /api/missions/:id/assessment

```
Request:  Authorization: Bearer <token>
Success:  { data: Assessment }
Error:    { error: string }
Status:   200 | 404 | 401
```

---

## 10. Acceptance Criteria

- [ ] User can start a pending mission → Focus Mode opens
- [ ] Mission workspace shows title, description, objectives
- [ ] Objective checklist updates progress indicator
- [ ] User can write evidence text
- [ ] User can attach files (1-3, type validation)
- [ ] Submit button sends data, shows loading, then confirmation
- [ ] Submitted mission shows "Awaiting assessment"
- [ ] Assessed mission shows pass/fail with feedback
- [ ] XP rewarded shown on pass
- [ ] Focus Mode hides sidebar, workspace expands
- [ ] Close button exits Focus Mode, returns to Journey Detail
- [ ] All states rendered (loading, submitting, assessed, error)
- [ ] Works in light and dark mode

---

## 11. Error Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Submit with empty text | Inline validation: "Please provide evidence" |
| File too large | Alert: "File exceeds 10MB limit" |
| Wrong file type | Alert: "Accepted formats: PDF, DOC, ZIP, PNG, JPG" |
| Network failure on submit | ErrorState + "Retry" button |
| Mission not found (404) | ErrorState + return to Journey Detail |
| Max files exceeded (3) | Alert: "Maximum 3 files allowed" |

---

## 12. Expected Tests

```
missions/
  MissionWorkspace.test.tsx
    - renders mission title and description
    - shows objectives checklist
    - toggles objectives, updates progress
  
  EvidenceSubmission.test.tsx
    - renders text area for evidence
    - validates empty submission
    - file upload with type/size validation
    - submit button shows loading state
    - shows success state on submission
  
  FocusMode.test.tsx
    - opens in focus mode
    - sidebar hidden
    - close button exits focus mode
    - mission state preserved after exit
  
  Assessment.test.tsx
    - shows pass/fail result
    - displays feedback text
    - shows XP awarded
    - shows retry option on fail
```
