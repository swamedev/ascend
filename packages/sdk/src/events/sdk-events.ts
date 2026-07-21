import type { SDKHealthReport } from '../health/health-report'
import type { SDKState } from '../lifecycle/lifecycle'

export const SDKEvents = {
  SDKInitializing: 'sdk:initializing' as const,
  SDKInitialized: 'sdk:initialized' as const,
  SDKInitializationFailed: 'sdk:initialization:failed' as const,
  SDKShuttingDown: 'sdk:shutting-down' as const,
  SDKShutdown: 'sdk:shutdown' as const,
  TransportChanged: 'sdk:transport:changed' as const,
  TransportFailed: 'sdk:transport:failed' as const,
  TransportRecovered: 'sdk:transport:recovered' as const,
  StateChanged: 'sdk:state:changed' as const,
  CacheCleared: 'sdk:cache:cleared' as const,
  CacheMiss: 'sdk:cache:miss' as const,
  CacheHit: 'sdk:cache:hit' as const,
} as const

export type SDKEventName = (typeof SDKEvents)[keyof typeof SDKEvents]

export interface SDKInitializingPayload {
  config: Record<string, unknown>
}

export interface SDKInitializedPayload {
  health: SDKHealthReport
}

export interface SDKInitializationFailedPayload {
  error: Error
}

export interface SDKShuttingDownPayload {
  reason?: string
}

export interface SDKShutdownPayload {
  uptime: number
}

export interface TransportChangedPayload {
  from: string
  to: string
}

export interface TransportFailedPayload {
  transport: string
  error: Error
}

export interface TransportRecoveredPayload {
  transport: string
}

export interface StateChangedPayload {
  from: SDKState
  to: SDKState
  reason?: string
}

export interface CacheClearedPayload {
  entries: number
}

export interface CacheMissPayload {
  key: string
}

export interface CacheHitPayload {
  key: string
  ttl: number
}
