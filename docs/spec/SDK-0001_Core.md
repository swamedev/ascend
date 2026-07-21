# SDK-0001 — ASCEND Frontend SDK Core

**Status:** Draft  
**Version:** 1.0.0  
**Obsoletes:** None  
**License:** MIT  

---

## 1. Abstract

SDK-0001 defines the **core interface** of the ASCEND Frontend SDK: the `AscendSDK` class. Every consumer — Web, Desktop, Mobile — interacts with the platform through this single entry point. No consumer ever instantiates a transport, client, or cache directly.

---

## 2. Scope

This specification covers:

- `AscendSDK` interface and lifecycle
- Configuration object
- Initialization sequence
- Shutdown protocol
- Health and version contracts
- Transport switching

It does **not** cover:

- Client contracts (see SDK-0002)
- Transport contracts (see SDK-0003)
- Mock Engine (see SDK-0004)

---

## 3. AscendSDK Interface

```typescript
interface AscendSDK {
  // ─── Lifecycle ─────────────────────────────────────

  initialize(config: SDKConfig): Promise<InitializeResult>
  shutdown(): Promise<void>

  // ─── Status ────────────────────────────────────────

  health(): Promise<HealthReport>
  version(): SDKVersion

  // ─── Transport ─────────────────────────────────────

  switchTransport(type: TransportType): Promise<void>

  // ─── Clients ──────────────────────────────────────

  builder: BuilderClient
  journey: JourneyClient
  mission: MissionClient
  assessment: AssessmentClient
  achievement: AchievementClient
  profile: ProfileClient

  // ─── Events ───────────────────────────────────────

  events: EventBus

  // ─── Internal ─────────────────────────────────────

  readonly transport: Transport
  readonly cache: CacheStore
  readonly status: SDKStatus
}
```

---

## 4. Configuration

```typescript
interface SDKConfig {
  // Transport
  transport: TransportType | TransportConfig

  // Cache defaults
  cache?: {
    defaultTTL?: number           // ms, default 30000
    maxEntries?: number           // default 500
    persistKey?: string           // for IndexedDB persistence
  }

  // Mock Engine (only when transport = 'mock')
  mock?: {
    seed?: SeedPreset             // 'empty' | 'demo' | 'comprehensive'
    latency?: number              // simulated ms, default 0
    failureRate?: number          // 0-1, default 0
  }

  // REST (only when transport = 'rest')
  rest?: {
    baseUrl: string
    authToken?: string
    timeout?: number              // ms, default 10000
    retryCount?: number           // default 3
  }

  // Offline
  offline?: {
    syncInterval?: number         // ms, default 30000
    conflictStrategy?: 'lww' | 'manual'
  }

  // Events
  events?: {
    enableLogging?: boolean
  }
}

type TransportType = 'mock' | 'rest' | 'offline' | 'realtime'
```

---

## 5. Initialization Sequence

```
AscendSDK.initialize(config)
    │
    ├── 1. Validate config
    │     └── Throw AscendError if invalid
    │
    ├── 2. Create Transport
    │     ├── mock  → MockTransport(seed)
    │     ├── rest  → RESTTransport(baseUrl, auth)
    │     ├── offline → OfflineTransport(wrap REST)
    │     └── realtime → RealtimeTransport(wrap REST)
    │
    ├── 3. Create CacheStore
    │     └── with config.cache defaults
    │
    ├── 4. Create EventBus
    │
    ├── 5. Create Clients
    │     ├── BuilderClient(transport, cache, events)
    │     ├── JourneyClient(transport, cache, events)
    │     ├── MissionClient(transport, cache, events)
    │     ├── AssessmentClient(transport, cache, events)
    │     ├── AchievementClient(transport, cache, events)
    │     └── ProfileClient(transport, cache, events)
    │
    ├── 6. Connect Transport
    │     └── transport.connect()
    │
    └── 7. Return InitializeResult
          └── { success: true, version, transport, status }
```

### 5.1 Initialization Rules

| Rule | Description |
|------|-------------|
| **I1** | `initialize()` must be called exactly once before any client method |
| **I2** | Calling `initialize()` on an already initialized SDK throws `AscendError` |
| **I3** | Every transport must support `connect()` synchronously or with timeout |
| **I4** | MockTransport must never fail to initialize |
| **I5** | Config validation must catch unknown transport types |

---

## 6. Shutdown Protocol

```
AscendSDK.shutdown()
    │
    ├── 1. EventBus.drain()
    ├── 2. CacheStore.clear()
    ├── 3. transport.disconnect()
    └── 4. Mark status as 'shutdown'
```

### 6.1 Shutdown Rules

| Rule | Description |
|------|-------------|
| **S1** | `shutdown()` must be idempotent (calling twice is safe) |
| **S2** | After shutdown, client methods throw `AscendError` |
| **S3** | Ongoing requests are cancelled (if transport supports it) |

---

## 7. Health Contract

```typescript
interface HealthReport {
  status: 'healthy' | 'degraded' | 'unhealthy'
  transport: {
    name: string
    status: TransportStatus
    latency: number             // ms
  }
  cache: {
    size: number
    hitRate: number
  }
  uptime: number                // ms since initialize
  version: string
}
```

---

## 8. Version Contract

```typescript
interface SDKVersion {
  major: number
  minor: number
  patch: number
  label?: string                // 'alpha', 'beta', 'rc.1'
}
```

The SDK follows **Semantic Versioning 2.0**. A major version change in the SDK implies a breaking change in at least one client contract.

---

## 9. Transport Switching

Transport switching is a development-only feature:

```typescript
AscendSDK.switchTransport(type: TransportType): Promise<void>
```

### 9.1 Switch Rules

| Rule | Description |
|------|-------------|
| **T1** | Calling `switchTransport` in production logs a warning |
| **T2** | Old transport disconnects, new transport connects |
| **T3** | Cache is **not** invalidated on switch (shared keyspace) |
| **T4** | Clients remain the same instance (proxy pattern) |

---

## 10. Error Contract

All SDK methods throw or return typed errors:

| Error | When |
|-------|------|
| `AscendError` | Base error for all SDK errors |
| `ValidationError` | Invalid config or input |
| `NetworkError` | Transport connection failure |
| `AuthenticationError` | Auth token missing/expired |
| `ConflictError` | Version conflict on write |
| `OfflineError` | Operation requires network |

```typescript
class AscendError extends Error {
  code: string
  statusCode: number
  details?: unknown
  timestamp: number
  retryable: boolean
}
```

---

## 11. TypeScript Configuration

All SDK types must be exported from a single barrel:

```typescript
// packages/sdk/index.ts
export { AscendSDK } from './core/ascend-sdk'
export type { SDKConfig, HealthReport, SDKVersion, SDKStatus } from './core/types'
export { AscendError, ValidationError, NetworkError } from './errors'
export { TransportType, TransportStatus } from './transport/transport.interface'
```

---

## 12. Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO TITAN |
