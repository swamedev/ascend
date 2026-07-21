// Core
export { AscendSDK, SDK_VERSION } from './core/ascend-sdk'
export type { SDKConfig, SDKOptions, AscendSDKInstance } from './core/types'

// Contracts
export type {
  Transport,
  TransportStatus,
  RequestConfig,
  TransportResponse,
  TransportHealth,
  RetryConfig,
  CacheEntry,
  CachePolicy,
  CacheStore,
  Logger,
  LogLevel,
  EventBus,
  EventHandler,
  Clock,
} from './contracts'

// Errors
export {
  AscendError,
  ValidationError,
  NetworkError,
  AuthenticationError,
  ConflictError,
  OfflineError,
} from './errors'

// Events
export { SimpleEventBus, SDKEvents } from './events'
export type {
  SDKEventName,
  SDKInitializingPayload,
  SDKInitializedPayload,
  SDKInitializationFailedPayload,
  SDKShuttingDownPayload,
  SDKShutdownPayload,
  TransportChangedPayload,
  TransportFailedPayload,
  TransportRecoveredPayload,
  StateChangedPayload,
  CacheClearedPayload,
  CacheMissPayload,
  CacheHitPayload,
} from './events'

// Logger
export { ConsoleLogger, SilentLogger } from './logger'

// Clock
export { SystemClock } from './clock'

// Lifecycle
export { Lifecycle, SDKStates } from './lifecycle'
export type { SDKState, StateChangeEvent, StateChangeHandler } from './lifecycle'

// Registry
export { TransportRegistry } from './registry'

// Cache
export { InMemoryCacheStore, DEFAULT_CACHE_POLICY, createCacheKey } from './cache'

// Transports
export { MockTransport } from './transports'
export type { MockTransportOptions } from './transports'

// Health
export type { SDKHealthReport, TransportHealthInfo } from './health'
