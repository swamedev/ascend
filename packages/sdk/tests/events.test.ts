import { describe, it, expect, vi } from 'vitest'
import { SimpleEventBus } from '../src/events/event-bus'
import { SDKEvents } from '../src/events/sdk-events'

describe('SimpleEventBus', () => {
  it('publishes and subscribes', () => {
    const bus = new SimpleEventBus()
    const handler = vi.fn()
    bus.subscribe('test:event', handler)
    bus.publish('test:event', { value: 42 })
    expect(handler).toHaveBeenCalledWith({ value: 42 })
  })

  it('publish to event with no handlers does nothing', () => {
    const bus = new SimpleEventBus()
    expect(() => bus.publish('empty', {})).not.toThrow()
  })

  it('publish works after drain completes', () => {
    const bus = new SimpleEventBus()
    bus.drain()
    const handler = vi.fn()
    bus.subscribe('post-drain', handler)
    bus.publish('post-drain', {})
    expect(handler).toHaveBeenCalled()
  })

  it('unsubscribes correctly', () => {
    const bus = new SimpleEventBus()
    const handler = vi.fn()
    const unsub = bus.subscribe('test:event', handler)
    unsub()
    bus.publish('test:event', {})
    expect(handler).not.toHaveBeenCalled()
  })

  it('supports multiple handlers', () => {
    const bus = new SimpleEventBus()
    const h1 = vi.fn()
    const h2 = vi.fn()
    bus.subscribe('test:event', h1)
    bus.subscribe('test:event', h2)
    bus.publish('test:event', {})
    expect(h1).toHaveBeenCalledTimes(1)
    expect(h2).toHaveBeenCalledTimes(1)
  })

  it('returns listener count', () => {
    const bus = new SimpleEventBus()
    expect(bus.listenerCount()).toBe(0)

    const h1 = vi.fn()
    const h2 = vi.fn()
    bus.subscribe('a', h1)
    bus.subscribe('b', h2)
    expect(bus.listenerCount()).toBe(2)
    expect(bus.listenerCount('a')).toBe(1)
  })

  it('listenerCount returns 0 for unknown event', () => {
    const bus = new SimpleEventBus()
    bus.subscribe('known', vi.fn())
    expect(bus.listenerCount('unknown')).toBe(0)
  })

  it('drains pending async handlers', async () => {
    const bus = new SimpleEventBus()
    let resolved = false

    bus.subscribe('test', async () => {
      await new Promise(r => setTimeout(r, 10))
      resolved = true
    })

    bus.publish('test', {})
    await bus.drain()
    expect(resolved).toBe(true)
  })

  it('clears all handlers', () => {
    const bus = new SimpleEventBus()
    const handler = vi.fn()
    bus.subscribe('test', handler)
    bus.clear()
    bus.publish('test', {})
    expect(handler).not.toHaveBeenCalled()
  })

  it('drains pending async handlers during drain', async () => {
    const bus = new SimpleEventBus()
    let resolved = false

    bus.subscribe('test', async () => {
      await new Promise(r => setTimeout(r, 5))
      resolved = true
    })

    bus.publish('test', {})
    expect(resolved).toBe(false)
    await bus.drain()
    expect(resolved).toBe(true)
  })

  it('unsubscribe removes only the specific handler', () => {
    const bus = new SimpleEventBus()
    const h1 = vi.fn()
    const h2 = vi.fn()
    bus.subscribe('e', h1)
    bus.subscribe('e', h2)
    bus.unsubscribe('e', h1)
    bus.publish('e', {})
    expect(h1).not.toHaveBeenCalled()
    expect(h2).toHaveBeenCalledTimes(1)
  })

  it('unsubscribe on non-existent event does nothing', () => {
    const bus = new SimpleEventBus()
    bus.unsubscribe('nonexistent', vi.fn())
    expect(bus.listenerCount()).toBe(0)
  })

  it('unsubscribe cleans up event entry when last handler removed', () => {
    const bus = new SimpleEventBus()
    const handler = vi.fn()
    bus.subscribe('temp', handler)
    bus.unsubscribe('temp', handler)
    expect(bus.listenerCount()).toBe(0)
  })
})

describe('SDKEvents', () => {
  it('has all expected event names', () => {
    expect(SDKEvents.SDKInitializing).toBe('sdk:initializing')
    expect(SDKEvents.SDKInitialized).toBe('sdk:initialized')
    expect(SDKEvents.SDKInitializationFailed).toBe('sdk:initialization:failed')
    expect(SDKEvents.SDKShuttingDown).toBe('sdk:shutting-down')
    expect(SDKEvents.SDKShutdown).toBe('sdk:shutdown')
    expect(SDKEvents.TransportChanged).toBe('sdk:transport:changed')
    expect(SDKEvents.TransportFailed).toBe('sdk:transport:failed')
    expect(SDKEvents.TransportRecovered).toBe('sdk:transport:recovered')
    expect(SDKEvents.StateChanged).toBe('sdk:state:changed')
    expect(SDKEvents.CacheCleared).toBe('sdk:cache:cleared')
    expect(SDKEvents.CacheMiss).toBe('sdk:cache:miss')
    expect(SDKEvents.CacheHit).toBe('sdk:cache:hit')
  })
})
