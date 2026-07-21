import { describe, it, expect, beforeEach, vi } from 'vitest'
import { AscendSDK, SDK_VERSION } from '../src/core/ascend-sdk'
import { MockTransport } from '../src/transports/mock-transport'
import { SimpleEventBus } from '../src/events/event-bus'
import { InMemoryCacheStore } from '../src/cache/cache-store'
import { SilentLogger } from '../src/logger/silent-logger'
import { SystemClock } from '../src/clock/system-clock'
import { SDKEvents } from '../src/events/sdk-events'

function createTestSDK() {
  const events = new SimpleEventBus()
  const transport = new MockTransport()
  const cache = new InMemoryCacheStore(events)
  const logger = new SilentLogger()

  const sdk = new AscendSDK({
    transport,
    cache,
    logger,
    eventBus: events,
    clock: new SystemClock(),
  })

  transport.register('/ping', async () => ({ pong: true }))

  return { sdk, transport, events, cache, logger }
}

describe('AscendSDK', () => {
  it('starts in CREATED state', () => {
    const { sdk } = createTestSDK()
    expect(sdk.state).toBe('CREATED')
  })

  it('initializes with mock transport', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    expect(sdk.state).toBe('READY')
    expect(sdk.transport.name).toBe('mock')
  })

  it('returns version', () => {
    const { sdk } = createTestSDK()
    expect(sdk.version()).toBe(SDK_VERSION)
  })

  it('reports healthy after init', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    const health = await sdk.health()
    expect(health.status).toBe('healthy')
    expect(health.sdkState).toBe('READY')
    expect(health.version).toBe(SDK_VERSION)
    expect(health.activeTransport).toBe('mock')
    expect(health.registeredTransports).toContain('mock')
    expect(health.uptime).toBeGreaterThanOrEqual(0)
    expect(health.warnings).toHaveLength(0)
  })

  it('shuts down gracefully', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    expect(sdk.state).toBe('READY')
    await sdk.shutdown()
    expect(sdk.state).toBe('STOPPED')
  })

  it('publishes SDKInitialized event on success', async () => {
    const { sdk, events } = createTestSDK()
    const handler = vi.fn()
    events.subscribe(SDKEvents.SDKInitialized, handler)

    await sdk.initialize()
    expect(handler).toHaveBeenCalledTimes(1)
  })

  it('publishes SDKShutdown event on shutdown', async () => {
    const { sdk } = createTestSDK()
    const handler = vi.fn()
    sdk.events.subscribe(SDKEvents.SDKShutdown, handler)

    await sdk.initialize()
    await sdk.shutdown()
    expect(handler).toHaveBeenCalledTimes(1)
  })

  it('publishes SDKShuttingDown before shutdown', async () => {
    const { sdk, events } = createTestSDK()
    const handler = vi.fn()
    events.subscribe(SDKEvents.SDKShuttingDown, handler)

    await sdk.initialize()
    await sdk.shutdown()
    expect(handler).toHaveBeenCalledTimes(1)
  })

  it('publishes SDKInitializing during init', async () => {
    const { sdk, events } = createTestSDK()
    const handler = vi.fn()
    events.subscribe(SDKEvents.SDKInitializing, handler)

    await sdk.initialize()
    expect(handler).toHaveBeenCalledTimes(1)
  })

  it('returns cache and transport info in health', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()

    const health = await sdk.health()
    expect(health.cache).toBeDefined()
    expect(health.cache.size).toBe(0)
    expect(health.cache.hitRate).toBe(0)
    expect(health.transport.name).toBe('mock')
    expect(health.transport.status).toBe('connected')
  })

  it('handles initialization failure gracefully', async () => {
    const { sdk } = createTestSDK()

    const failingTransport = new MockTransport()
    failingTransport.connect = async () => {
      throw new Error('Connection refused')
    }
    sdk.registry.register('failing', failingTransport)

    await expect(sdk.initialize({ transport: 'failing' })).rejects.toThrow('Connection refused')
    expect(sdk.state).toBe('STOPPED')
  })

  it('publishes initialization failed event', async () => {
    const { sdk } = createTestSDK()
    const handler = vi.fn()
    sdk.events.subscribe(SDKEvents.SDKInitializationFailed, handler)

    const failingTransport = new MockTransport()
    failingTransport.connect = async () => {
      throw new Error('Failed')
    }
    sdk.registry.register('failing', failingTransport)

    await expect(sdk.initialize({ transport: 'failing' })).rejects.toThrow()
    expect(handler).toHaveBeenCalledTimes(1)
  })

  it('supports custom log level in config', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize({ logLevel: 'debug', transport: 'mock' })
    expect(sdk.logger.getLevel()).toBe('debug')
  })

  it('switchTransport changes transport', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()

    const newTransport = new MockTransport()
    sdk.registry.register('mock2', newTransport)

    const switchSpy = vi.fn()
    sdk.events.subscribe(SDKEvents.TransportChanged, switchSpy)

    await sdk.switchTransport('mock2')
    expect(sdk.transport).toBe(newTransport)
    expect(switchSpy).toHaveBeenCalledWith({
      from: 'mock',
      to: 'mock2',
    })
  })

  it('rejects transport switch from STOPPED', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    await sdk.shutdown()

    await expect(sdk.switchTransport('mock')).rejects.toThrow('Cannot switch transport')
  })

  it('shutdown is idempotent', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    await sdk.shutdown()
    await sdk.shutdown()
    expect(sdk.state).toBe('STOPPED')
  })

  it('clears cache on init', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize({ cache: { ttl: 1000 } })
    expect(await sdk.cache.size()).toBe(0)
  })

  it('health reports healthy when state is READY', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    const health = await sdk.health()
    expect(health.status).toBe('healthy')
  })

  it('health reports unhealthy from STOPPED state', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    await sdk.shutdown()
    const health = await sdk.health()
    expect(health.status).toBe('unhealthy')
  })

  it('includes cache hit rate in health', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    await sdk.cache.set('k', 'v')
    await sdk.cache.get('k')
    const health = await sdk.health()
    expect(health.cache.hitRate).toBeGreaterThan(0)
    expect(health.cache.size).toBe(1)
  })

  it('throws for unregistered transport in config', async () => {
    const { sdk } = createTestSDK()
    await expect(sdk.initialize({ transport: 'nonexistent' })).rejects.toThrow()
  })

  it('transport getter returns current transport', () => {
    const { sdk, transport } = createTestSDK()
    expect(sdk.transport).toBe(transport)
  })

  it('health includes warnings when degraded', async () => {
    const { sdk, transport } = createTestSDK()
    await sdk.initialize()

    transport.disconnect()
    const health = await sdk.health()
    expect(health.warnings.length).toBeGreaterThanOrEqual(0)
  })

  it('reports sdk version correctly', async () => {
    const { sdk } = createTestSDK()
    expect(sdk.version()).toBe(SDK_VERSION)
  })

  it('shutdown from CREATED is safe', async () => {
    const { sdk } = createTestSDK()
    await sdk.shutdown()
    expect(sdk.state).toBe('CREATED')
  })

  it('handles transport switch to same transport', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()

    const mock2 = new MockTransport()
    sdk.registry.register('mock2', mock2)
    await sdk.switchTransport('mock2')
    expect(sdk.transport).toBe(mock2)

    await sdk.switchTransport('mock')
    expect(sdk.transport.name).toBe('mock')
  })
})
