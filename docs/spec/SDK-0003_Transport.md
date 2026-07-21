# SDK-0003 — ASCEND Frontend SDK Transport

**Status:** Draft  
**Version:** 1.0.0  
**Obsoletes:** None  
**License:** MIT  

---

## 1. Abstract

SDK-0003 defines the **transport contract** of the ASCEND Frontend SDK. The transport layer is the only part of the SDK that knows how to communicate with the outside world. It is fully swappable: Mock, REST, Offline, or Realtime — the SDK clients never know which one they are using.

---

## 2. Scope

This specification covers:

- Transport interface contract
- All 4 transport implementations (Mock, REST, Offline, Realtime)
- Transport factory
- Request/response pipeline
- Error mapping
- Retry and timeout policies

It does **not** cover:

- SDK Core lifecycle (see SDK-0001)
- Client contracts (see SDK-0002)
- Mock Engine (see SDK-0004)

---

## 3. Transport Interface

```typescript
interface Transport {
  readonly name: string
  readonly status: TransportStatus

  // ─── Lifecycle ───────────────────────────────────

  connect(): Promise<void>
  disconnect(): Promise<void>

  // ─── Request ─────────────────────────────────────

  request<T>(config: RequestConfig): Promise<TransportResponse<T>>

  // ─── Health ──────────────────────────────────────

  health(): Promise<TransportHealth>

  // ─── Events ──────────────────────────────────────

  onStatusChange(handler: (status: TransportStatus) => void): () => void
}

type TransportStatus = 'disconnected' | 'connecting' | 'connected' | 'error'

interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  path: string
  body?: unknown
  params?: Record<string, string>
  headers?: Record<string, string>
  timeout?: number
  retry?: RetryConfig
}

interface TransportResponse<T> {
  data: T
  status: number
  headers: Record<string, string>
  timestamp: number
}

interface TransportHealth {
  status: 'healthy' | 'degraded' | 'unhealthy'
  latency: number
  message?: string
}

interface RetryConfig {
  maxRetries: number
  baseDelay: number
  maxDelay: number
  retryableStatuses: number[]
}
```

---

## 4. Transport Implementations

### 4.1 MockTransport

```typescript
class MockTransport implements Transport {
  name = 'mock'
  status: TransportStatus = 'disconnected'

  constructor(engine: MockEngine, options?: MockTransportOptions)

  connect(): Promise<void>
  disconnect(): Promise<void>
  request<T>(config: RequestConfig): Promise<TransportResponse<T>>
  health(): Promise<TransportHealth>
  onStatusChange(handler: (status: TransportStatus) => void): () => void
}
```

| Property | Behavior |
|----------|----------|
| **Data source** | MockEngine (in-memory) |
| **Latency** | Configurable (default 0ms) |
| **Failure rate** | Configurable (default 0) |
| **Connection** | Always succeeds |
| **Persistence** | None (in-memory only) |

#### MockTransportOptions

```typescript
interface MockTransportOptions {
  latency?: number       // simulated latency in ms
  failureRate?: number   // 0-1, fraction of requests that fail
  failureStatuses?: number[] // which HTTP statuses to simulate
}
```

### 4.2 RESTTransport

```typescript
class RESTTransport implements Transport {
  name = 'rest'
  status: TransportStatus = 'disconnected'

  constructor(config: RESTTransportConfig)

  connect(): Promise<void>
  disconnect(): Promise<void>
  request<T>(config: RequestConfig): Promise<TransportResponse<T>>
  health(): Promise<TransportHealth>
  onStatusChange(handler: (status: TransportStatus) => void): () => void
}
```

| Property | Behavior |
|----------|----------|
| **Data source** | HTTP API server |
| **Auth** | Bearer token (auto-attach) |
| **Timeout** | Configurable (default 10000ms) |
| **Retry** | Configurable (default 3 retries, exponential backoff) |
| **Connection** | Health check on `connect()` |

#### RESTTransportConfig

```typescript
interface RESTTransportConfig {
  baseUrl: string
  authToken?: string
  timeout?: number
  retry?: RetryConfig
  headers?: Record<string, string>
}
```

### 4.3 OfflineTransport

```typescript
class OfflineTransport implements Transport {
  name = 'offline'
  status: TransportStatus = 'disconnected'

  constructor(wrapped: Transport, options?: OfflineTransportOptions)

  connect(): Promise<void>
  disconnect(): Promise<void>
  request<T>(config: RequestConfig): Promise<TransportResponse<T>>
  health(): Promise<TransportHealth>
  onStatusChange(handler: (status: TransportStatus) => void): () => void
}
```

| Property | Behavior |
|----------|----------|
| **Data source** | Wraps another transport (usually REST) |
| **Offline mode** | Queues mutating requests in IndexedDB |
| **Sync** | Replays queue when back online |
| **Conflict resolution** | Last-writer-wins (configurable) |

#### OfflineTransportOptions

```typescript
interface OfflineTransportOptions {
  storage: OfflineStorage       // IndexedDB adapter
  syncInterval?: number         // ms, default 30000
  conflictStrategy?: 'lww' | 'manual'
  maxQueueSize?: number         // default 1000
}

interface OfflineStorage {
  getItem(key: string): Promise<unknown>
  setItem(key: string, value: unknown): Promise<void>
  removeItem(key: string): Promise<void>
  clear(): Promise<void>
}
```

### 4.4 RealtimeTransport

```typescript
class RealtimeTransport implements Transport {
  name = 'realtime'
  status: TransportStatus = 'disconnected'

  constructor(wrapped: Transport, options?: RealtimeTransportOptions)

  connect(): Promise<void>
  disconnect(): Promise<void>
  request<T>(config: RequestConfig): Promise<TransportResponse<T>>
  health(): Promise<TransportHealth>
  onStatusChange(handler: (status: TransportStatus) => void): () => void

  // Realtime-specific
  subscribe<T>(event: string, handler: (data: T) => void): () => void
  unsubscribe(event: string): void
}
```

| Property | Behavior |
|----------|----------|
| **Data source** | Wraps RESTTransport + SSE/WS |
| **Live updates** | Server-sent events for streaming data |
| **Fallback** | Falls back to wrapped transport when disconnected |
| **Reconnect** | Automatic reconnection with backoff |

#### RealtimeTransportOptions

```typescript
interface RealtimeTransportOptions {
  sseUrl: string
  wsUrl?: string
  reconnectDelay?: number       // ms, default 1000
  maxReconnectAttempts?: number  // default 10
}
```

---

## 5. Transport Factory

```typescript
function createTransport(config: SDKConfig): Transport {
  switch (config.transport) {
    case 'mock':
      return new MockTransport(config.mock?.engine, config.mock)
    case 'rest':
      return new RESTTransport(config.rest!)
    case 'offline':
      return new OfflineTransport(
        new RESTTransport(config.rest!),
        config.offline
      )
    case 'realtime':
      return new RealtimeTransport(
        new RESTTransport(config.rest!),
        config.realtime
      )
    default:
      throw new ValidationError(`Unknown transport type: ${config.transport}`)
  }
}
```

---

## 6. Error Mapping

Each transport maps its native errors to SDK errors:

| Transport Error | SDK Error |
|----------------|-----------|
| Network timeout | `NetworkError` |
| HTTP 401/403 | `AuthenticationError` |
| HTTP 409 | `ConflictError` |
| HTTP 422 | `ValidationError` |
| HTTP 5xx | `NetworkError` (retryable) |
| Offline queue full | `OfflineError` |
| No network | `OfflineError` |

```typescript
abstract class TransportErrorMapper {
  abstract map(error: unknown, config: RequestConfig): AscendError
}
```

---

## 7. Retry Policy

```typescript
interface RetryPolicy {
  maxRetries: number
  baseDelay: number
  maxDelay: number
  retryableStatuses: number[]

  // Exponential backoff with jitter
  calculateDelay(attempt: number): number
}
```

Default retry policy:

| Property | Default |
|----------|---------|
| `maxRetries` | 3 |
| `baseDelay` | 1000ms |
| `maxDelay` | 10000ms |
| `retryableStatuses` | [408, 429, 500, 502, 503, 504] |

### 7.1 Retry Rules

| Rule | Description |
|------|-------------|
| **R1** | GET requests are always retryable |
| **R2** | Mutations (POST/PUT/PATCH/DELETE) are retryable only if idempotent |
| **R3** | OfflineTransport retries on reconnect, not on delay |
| **R4** | MockTransport never retries |

---

## 8. Timeout Policy

| Transport | Default Timeout | Configurable |
|-----------|----------------|--------------|
| MockTransport | N/A | N/A |
| RESTTransport | 10000ms | Yes |
| OfflineTransport | Inherits wrapped | — |
| RealtimeTransport | 10000ms | Yes |

---

## 9. Transport Rules

| Rule | Description |
|------|-------------|
| **T1** | No transport holds domain state (stateless between requests) |
| **T2** | Transport must never throw non-Ascend errors |
| **T3** | `connect()` is idempotent |
| **T4** | `disconnect()` must be safe to call multiple times |
| **T5** | Transport names are unique and lowercase |
| **T6** | All timestamps are Unix milliseconds |
| **T7** | Transport must not access the DOM or React APIs |

---

## 10. Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Chief Architect | Initial version — OPERAÇÃO TITAN |
