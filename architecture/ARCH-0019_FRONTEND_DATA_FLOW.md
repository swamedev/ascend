# ARCH-0019 — Frontend Data Flow

| Field | Value |
|-------|-------|
| **ID** | ARCH-0019 |
| **Name** | Frontend Data Flow |
| **Version** | 1.0 |
| **Status** | Draft |
| **Category** | Architecture |
| **Owner** | Chief Architect |
| **Derived from** | ARCH-0011, ARCH-0015, ARCH-0016, ARCH-0018 |
| **Referenced by** | ARCH-0020, ARCH-0021 |

---

## 1. Purpose

This is the most important document for understanding how data moves through the entire ASCEND system.

Every flow is mapped: from the UI component all the way down to SQLite and back.

---

## 2. Canonical Data Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                        PRESENTATION                              │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │ Component │───▶│   Hook   │───▶│   SDK    │                   │
│  └──────────┘    └──────────┘    └─────┬────┘                   │
│        ▲                               │                         │
│        │                               │                         │
│        └─────────── Data ──────────────┘                         │
├──────────────────────────────────────────────────────────────────┤
│                        API LAYER                                 │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │  Router  │───▶│  Auth    │───▶│  Controller│                 │
│  └──────────┘    └──────────┘    └─────┬────┘                   │
│                                        │                         │
├────────────────────────────────────────┼─────────────────────────┤
│                        APPLICATION     │                         │
│                                        │                         │
│  ┌─────────────────────────────────────┴──────────────┐          │
│  │                 Use Case                             │         │
│  │  Validates → Authorizes → Orchestrates              │         │
│  └─────────────────────────────────────────────────────┘         │
│                                        │                         │
├────────────────────────────────────────┼─────────────────────────┤
│                        DOMAIN          │                         │
│                                        ▼                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Runtime / Core Engine                      │ │
│  │  State Machine → Business Rules → Domain Events              │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                        │                         │
├────────────────────────────────────────┼─────────────────────────┤
│                        INFRASTRUCTURE  │                         │
│                                        ▼                         │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Repository → SQLite / File System / Event Store            │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. All Flows

### 3.1 Read Flow: List Missions

```
Component: <MissionList />
    │
    ▼
Hook: useMissions(filters)
    │  Manages: loading, error, data, refetch
    │  Returns: { missions, isLoading, error, refetch }
    ▼
React Query: useQuery(['missions', 'list', filters], ...)
    │  Checks cache → staleness → refetch if stale
    ▼
SDK: client.missions.list(filters)
    │  Attaches auth token
    │  Applies retry policy
    │  Checks offline cache (if no connection)
    ▼
HTTP: GET /api/v1/missions?status=active&page=1
    │  Rate limited → auth verified → routed
    ▼
Controller: MissionsController.list(filters)
    │  Validates input → calls use case
    ▼
Use Case: ListMissionsUseCase.execute(filters)
    │  Authorizes → calls repository protocol
    ▼
Repository: MissionRepository.find_by_status('active')
    │  Protocol interface → SQLite implementation
    ▼
SQLite: SELECT * FROM missions WHERE status = 'active' ...
    │
    ▼
Return path (reverse):
    SQLite → Repository → Use Case → Controller → HTTP Response
    → SDK parses → React Query caches → Hook transforms → Component renders
```

### 3.2 Write Flow: Start Mission

```
Component: <StartMissionButton />
    │
    ▼
Hook: useStartMission()
    │  useMutation with optimistic update
    ▼
SDK: client.missions.start('m4')
    │  Optimistic: update local cache immediately
    │  POST /api/v1/missions/m4/start
    ▼
Controller: MissionsController.start('m4')
    │  Validates → Check auth → Calls use case
    ▼
Use Case: StartMissionUseCase.execute('m4')
    │  Loads mission → Validates state → Calls Runtime
    ▼
Runtime: MissionEngine.start('m4')
    │  State machine: AVAILABLE → ACTIVE
    │  Emits: MissionStarted event
    ▼
Repository: MissionRepository.save(mission)
    │  SQLite: UPDATE missions SET status = 'active'
    ▼
Event Store: Store MissionStarted event
    │
    ▼
Return path:
    SQLite → Repository → Runtime → Use Case → Controller → 200 OK
    → SDK receives response → React Query invalidates cache
    → Hook triggers re-render → Component shows active state

If error:
    SDK rolls back optimistic update
    Hook returns error state
    Component shows error toast
```

### 3.3 Write Flow: Submit Evidence

```
Component: <EvidenceUploader />
    │
    ▼
Hook: useSubmitEvidence()
    │  Manages: files, description, upload progress
    ▼
SDK: client.missions.submitEvidence('m4', { files, description })
    │  Offline: if no connection, queue for later
    │  Online: POST /api/v1/missions/m4/evidence
    │  Multipart upload with progress tracking
    ▼
Controller: EvidenceController.submit('m4', data)
    │  Validate files (type, size) → Store files → Call use case
    ▼
Use Case: SubmitEvidenceUseCase.execute('m4', evidence)
    │  Validate evidence → Call Evidence Engine
    ▼
EvidenceEngine: submit(evidence)
    │  Validate format → Store metadata → Emit event
    ▼
Repository: EvidenceRepository.save(evidence)
    │  SQLite: INSERT INTO evidence
    ▼
File Storage: Save files to disk
    │
    ▼
Event: EvidenceSubmitted → SSE push to client
    │
    ▼
Return path:
    → 201 Created
    → React Query invalidates ['missions', 'm4'] and ['evidence']
    → Component shows "Submitted, awaiting review"
```

### 3.4 SSE Event Flow: Achievement Unlocked

```
Server:
    Domain Event: AchievementUnlocked
        │
        ▼
    SSE Stream: event: achievement
                data: { badge_id: 'speed-demon', name: 'Speed Demon' }
        │
        ▼
Client:
    SDK: events.subscribe('achievement', handler)
        │
        ▼
    Hook: useAchievementEvents()
        │  Listens for new achievements
        ▼
    Zustand: addNotification({ type: 'achievement', data })
        │
        ▼
    Component: <AchievementToast />
        │  Shows celebration overlay
        ▼
    React Query: invalidateQueries(['achievements'])
        │  Refreshes achievement list
        ▼
    Component: <AchievementGallery />
        │  Re-renders with new badge
```

### 3.5 Offline Flow: Evidence Queue

```
Component: <EvidenceUploader />
    │
    ▼
SDK: client.missions.submitEvidence('m4', data)
    │
    ├── Online: proceed normally
    │
    └── Offline:
         │
         ▼
    Store in IndexedDB: pendingQueue.push({
        id: 'offline_001',
        action: 'submit_evidence',
        payload: { missionId: 'm4', files, description },
        createdAt: timestamp
    })
         │
         ▼
    Show UI: "Saved offline. Will sync when connected."
         │
         ▼
    ── Connection restores ──
         │
         ▼
    SDK: offlineQueue.sync()
         │  Process queue in order
         │  On success: remove from queue
         │  On conflict: notify user
         ▼
    React Query: invalidateQueries(['missions', 'evidence'])
```

### 3.6 Auth Flow: Login

```
Component: <LoginForm />
    │
    ▼
SDK: client.auth.login({ email, password })
    │
    ▼
API: POST /api/v1/auth/login
    │
    ▼
Use Case: LoginUseCase.execute(email, password)
    │  Verify credentials → Generate JWT
    ▼
Return: { access_token, refresh_token, builder }
    │
    ▼
Zustand session-store: setSession({ status: 'authenticated', ... })
    │  access_token → memory (only)
    │  refresh_token → encrypted storage
    ▼
React Query: setQueryData(['builder', 'me'], builder)
    │
    ▼
Router: redirect to /dashboard
```

---

## 4. Data Flow Diagram (Complete)

```mermaid
graph TB
    subgraph "Frontend"
        COMP["React Component"]
        HOOK["Custom Hook"]
        RQ["React Query"]
        ZU["Zustand Store"]
        SDK["Platform SDK"]
        IDB["IndexedDB
             Offline Queue"]
    end

    subgraph "API"
        CTRL["Controller"]
        AUTH["Auth Middleware"]
        VALID["Validation"]
    end

    subgraph "Application"
        UC["Use Case"]
    end

    subgraph "Domain"
        RT["Runtime"]
        ENG["Core Engine"]
        EVT["Domain Events"]
    end

    subgraph "Infrastructure"
        REPO["Repository"]
        DB[("SQLite")]
        FS["File Storage"]
        ES["Event Store"]
    end

    subgraph "SSE"
        SSE["SSE Stream"]
    end

    %% Read Flow
    COMP -->|action| HOOK
    HOOK -->|query| RQ
    RQ -->|fetch| SDK
    SDK -->|HTTP| CTRL
    SDK -->|offline fallback| IDB
    CTRL --> AUTH
    AUTH --> VALID
    VALID --> UC
    UC --> RT
    RT --> ENG
    ENG --> REPO
    REPO --> DB

    %% Return
    DB --> REPO --> ENG --> RT --> UC --> CTRL --> SDK
    SDK --> RQ --> HOOK --> COMP

    %% Write Flow
    COMP -->|mutation| HOOK
    HOOK -->|mutate| SDK
    SDK -->|optimistic| RQ
    SDK -->|POST| CTRL
    CTRL --> UC --> RT --> REPO --> DB
    UC --> FS

    %% SSE Flow
    EVT --> SSE
    SSE -.->|push| SDK
    SDK -->|event| HOOK
    HOOK -->|update| ZU
    HOOK -->|invalidate| RQ

    %% Offline Flow
    SDK -.->|queue| IDB
    IDB -.->|sync| SDK
```

---

## 5. Flow Catalog

| # | Flow | Type | Criticality |
|---|------|------|-------------|
| F1 | List journeys | Read | High |
| F2 | Get journey detail | Read | High |
| F3 | List missions | Read | High |
| F4 | Get mission detail | Read | High |
| F5 | Start mission | Write | High |
| F6 | Submit evidence | Write | Critical |
| F7 | Get feedback | Read | High |
| F8 | Get competency tree | Read | High |
| F9 | Get competency detail | Read | Medium |
| F10 | List evidence | Read | Medium |
| F11 | Get evidence detail | Read | Medium |
| F12 | List achievements | Read | Medium |
| F13 | Get achievement detail | Read | Low |
| F14 | Ask mentor | Write | Medium |
| F15 | Get mentor suggestions | Read | Low |
| F16 | Login | Write | Critical |
| F17 | Register | Write | Medium |
| F18 | SSE event stream | Read (push) | High |
| F19 | Offline evidence queue | Write (deferred) | High |
| F20 | Analytics summary | Read | Medium |

---

## 6. Definition of Done

ARCH-0019 aprovado quando:

- [ ] Canonical data flow diagram complete
- [ ] Read flow (list missions) fully mapped
- [ ] Write flow (start mission) fully mapped
- [ ] Write flow (submit evidence) fully mapped
- [ ] SSE event flow (achievement) fully mapped
- [ ] Offline flow (evidence queue) fully mapped
- [ ] Auth flow (login) fully mapped
- [ ] Complete data flow Mermaid diagram
- [ ] Flow catalog with all 20 flows

---

## 7. Change History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-07-20 | Chief Architect | Initial version |
