import type { Transport } from '../contracts/transport'
import type { CacheStore, CachePolicy } from '../contracts/cache'
import type { Logger, LogLevel } from '../contracts/logger'
import type { EventBus } from '../contracts/event-bus'
import type { Clock } from '../contracts/clock'
import type { TransportRegistry } from '../registry/transport-registry'

export interface SDKConfig {
  transport: string
  logger?: Logger
  logLevel?: LogLevel
  clock?: Clock
  cache?: Partial<CachePolicy>
  mock?: {
    latency?: number
    failureRate?: number
  }
}

export interface SDKOptions {
  transport: Transport
  cache: CacheStore
  logger: Logger
  eventBus: EventBus
  clock: Clock
}

export interface AscendSDKInstance {
  readonly transport: Transport
  readonly cache: CacheStore
  readonly logger: Logger
  readonly events: EventBus
  readonly clock: Clock
  readonly registry: TransportRegistry

  initialize(config: SDKConfig): Promise<void>
  shutdown(): Promise<void>
  health(): Promise<import('../health/health-report').SDKHealthReport>
  version(): string
  switchTransport(name: string): Promise<void>
}
