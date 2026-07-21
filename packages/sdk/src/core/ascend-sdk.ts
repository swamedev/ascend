import type { Transport } from '../contracts/transport'
import type { CacheStore } from '../contracts/cache'
import type { Logger } from '../contracts/logger'
import type { EventBus } from '../contracts/event-bus'
import type { Clock } from '../contracts/clock'
import { InMemoryCacheStore } from '../cache/cache-store'
import { ConsoleLogger } from '../logger/console-logger'
import { SimpleEventBus } from '../events/event-bus'
import { SystemClock } from '../clock/system-clock'
import { TransportRegistry } from '../registry/transport-registry'
import { Lifecycle } from '../lifecycle/lifecycle'
import { MockTransport } from '../transports/mock-transport'
import { AscendError } from '../errors/ascend.error'
import { ValidationError } from '../errors/validation.error'
import { SDKEvents } from '../events/sdk-events'
import type { SDKHealthReport } from '../health/health-report'
import type { SDKConfig, SDKOptions } from './types'

export const SDK_VERSION = '0.1.0'

const VALID_TRANSPORTS_FOR_SWITCH = ['READY', 'DEGRADED'] as const

export class AscendSDK {
  readonly registry: TransportRegistry
  readonly events: EventBus
  readonly logger: Logger
  readonly clock: Clock
  readonly cache: CacheStore

  private _lifecycle: Lifecycle
  private _transport: Transport

  constructor(options?: Partial<SDKOptions>) {
    this.logger = options?.logger ?? new ConsoleLogger()
    this.events = options?.eventBus ?? new SimpleEventBus()
    this.clock = options?.clock ?? new SystemClock()
    this.registry = new TransportRegistry()
    this.cache = options?.cache ?? new InMemoryCacheStore(this.events)
    this._lifecycle = new Lifecycle(this.logger, this.events)
    this._transport = options?.transport ?? new MockTransport()
  }

  get transport(): Transport {
    return this._transport
  }

  get state(): string {
    return this._lifecycle.state
  }

  async initialize(config?: SDKConfig): Promise<void> {
    this._lifecycle.transition('INITIALIZING', 'SDK initialize called')

    this.events.publish(SDKEvents.SDKInitializing, { config: config ?? {} })

    try {
      this.validateConfig(config)

      if (config?.logLevel) {
        this.logger.setLevel(config.logLevel)
      }

      this.registry.register('mock', new MockTransport(config?.mock))

      const transportName = config?.transport ?? 'mock'
      const transport = this.registry.resolve(transportName)
      this._transport = transport

      this.logger.info(`SDK initializing with transport: ${transportName}`)

      if (config?.cache) {
        await this.cache.clear()
      }

      await transport.connect()

      this._lifecycle.transition('READY', 'SDK initialized successfully')

      const health = await this.health()
      this.events.publish(SDKEvents.SDKInitialized, { health })

      this.logger.info('SDK initialized successfully')
    } catch (error) {
      const err = error instanceof Error ? error : new Error(String(error))
      this.logger.error('SDK initialization failed', { error: err.message })
      this.events.publish(SDKEvents.SDKInitializationFailed, { error: err })

      if (this._lifecycle.canTransition('STOPPING')) {
        await this._lifecycle.transition('STOPPING', 'Initialization failed')
      }
      if (this._lifecycle.canTransition('STOPPED')) {
        await this._lifecycle.transition('STOPPED', 'Initialization failed')
      }

      throw err
    }
  }

  async shutdown(): Promise<void> {
    if (this._lifecycle.state === 'STOPPED') return
    if (this._lifecycle.state === 'CREATED') return

    this.events.publish(SDKEvents.SDKShuttingDown, { reason: 'shutdown called' })

    try {
      await this.events.drain()
      await this.cache.clear()
      await this.transport.disconnect()

      const fromState = this._lifecycle.state
      if (fromState !== 'STOPPING' && this._lifecycle.canTransition('STOPPING')) {
        await this._lifecycle.transition('STOPPING', 'SDK shutdown')
      }
      await this._lifecycle.transition('STOPPED', 'SDK shutdown complete')

      const uptime = this._lifecycle.startedAt !== null
        ? Date.now() - this._lifecycle.startedAt
        : 0

      this.events.publish(SDKEvents.SDKShutdown, { uptime })
      this.logger.info('SDK shutdown complete')
    } catch (error) {
      this.logger.error('SDK shutdown error', { error: String(error) })
    }
  }

  async health(): Promise<SDKHealthReport> {
    const transportInfo = await this.transport.health()
    const cacheSize = await this.cache.size()
    const cacheHits = await this.cache.hits()
    const cacheMisses = await this.cache.misses()
    const totalCacheCalls = cacheHits + cacheMisses
    const hitRate = totalCacheCalls > 0 ? cacheHits / totalCacheCalls : 0

    const warnings: string[] = []

    if (this._lifecycle.state === 'DEGRADED') {
      warnings.push('SDK running in degraded mode')
    }
    if (this._lifecycle.state === 'OFFLINE') {
      warnings.push('SDK running in offline mode')
    }
    if (this._lifecycle.state !== 'READY' && this._lifecycle.state !== 'DEGRADED' && this._lifecycle.state !== 'OFFLINE') {
      warnings.push(`SDK is not operational (state: ${this._lifecycle.state})`)
    }

    const state = this._lifecycle.state
    const overallStatus = state === 'READY'
      ? 'healthy' as const
      : state === 'DEGRADED' || state === 'OFFLINE'
        ? 'degraded' as const
        : 'unhealthy' as const

    return {
      status: overallStatus,
      sdkState: state,
      transport: {
        name: this.transport.name,
        status: transportInfo.status === 'healthy' ? 'connected' as const : 'error' as const,
        latency: transportInfo.latency,
      },
      cache: {
        size: cacheSize,
        hitRate,
      },
      latency: transportInfo.latency,
      version: SDK_VERSION,
      uptime: this._lifecycle.startedAt !== null ? Date.now() - this._lifecycle.startedAt : 0,
      activeTransport: this.transport.name,
      registeredTransports: this.registry.list(),
      warnings,
    }
  }

  version(): string {
    return SDK_VERSION
  }

  async switchTransport(name: string): Promise<void> {
    if (!(VALID_TRANSPORTS_FOR_SWITCH as readonly string[]).includes(this._lifecycle.state)) {
      throw new AscendError(
        `Cannot switch transport in state: ${this._lifecycle.state}`,
        { code: 'INVALID_STATE', statusCode: 500, details: { state: this._lifecycle.state } },
      )
    }

    const newTransport = this.registry.resolve(name)
    const oldName = this.transport.name

    await this.transport.disconnect()
    this._transport = newTransport
    await newTransport.connect()

    this.events.publish(SDKEvents.TransportChanged, { from: oldName, to: name })
    this.logger.info(`Transport switched: ${oldName} → ${name}`)
  }

  private validateConfig(config?: SDKConfig): void {
    if (!config) return

    if (config.transport && config.transport !== 'mock') {
      if (!this.registry.has(config.transport)) {
        throw new ValidationError(
          `Transport not registered: ${config.transport}`,
          { transport: config.transport, registered: this.registry.list() },
        )
      }
    }
  }
}
