import { describe, it, expect, vi } from 'vitest'
import { Lifecycle, SDKStates } from '../src/lifecycle/lifecycle'
import { SimpleEventBus } from '../src/events/event-bus'
import { SilentLogger } from '../src/logger/silent-logger'
import { AscendError } from '../src/errors/ascend.error'

function createLifecycle(): Lifecycle {
  return new Lifecycle(new SilentLogger(), new SimpleEventBus())
}

describe('Lifecycle', () => {
  it('starts in CREATED state', () => {
    const lc = createLifecycle()
    expect(lc.state).toBe('CREATED')
    expect(lc.previousState).toBeNull()
  })

  it('transitions to INITIALIZING', async () => {
    const lc = createLifecycle()
    await lc.transition('INITIALIZING')
    expect(lc.state).toBe('INITIALIZING')
    expect(lc.previousState).toBe('CREATED')
  })

  it('transitions through valid states', async () => {
    const lc = createLifecycle()
    await lc.transition('INITIALIZING')
    await lc.transition('READY')
    expect(lc.state).toBe('READY')
  })

  it('records startedAt on READY', async () => {
    const lc = createLifecycle()
    await lc.transition('INITIALIZING')
    await lc.transition('READY')
    expect(lc.startedAt).toBeGreaterThan(0)
  })

  it('rejects invalid transitions', async () => {
    const lc = createLifecycle()
    await expect(lc.transition('STOPPED')).rejects.toThrow(AscendError)
  })

  it('rejects transition from STOPPED to anything', async () => {
    const lc = createLifecycle()
    await lc.transition('INITIALIZING')
    await lc.transition('STOPPING')
    await lc.transition('STOPPED')
    await expect(lc.transition('CREATED')).rejects.toThrow(AscendError)
  })

  it('canTransition returns correct values', async () => {
    const lc = createLifecycle()
    expect(lc.canTransition('INITIALIZING')).toBe(true)
    expect(lc.canTransition('READY')).toBe(false)

    await lc.transition('INITIALIZING')
    expect(lc.canTransition('READY')).toBe(true)
    expect(lc.canTransition('CREATED')).toBe(false)
  })

  it('fires state change handlers', async () => {
    const lc = createLifecycle()
    const handler = vi.fn()
    lc.onStateChange(handler)

    await lc.transition('INITIALIZING')
    const event = handler.mock.calls[0]?.[0]
    expect(event.from).toBe('CREATED')
    expect(event.to).toBe('INITIALIZING')
  })

  it('unsubscribes handlers', async () => {
    const lc = createLifecycle()
    const handler = vi.fn()
    const unsub = lc.onStateChange(handler)
    unsub()

    await lc.transition('INITIALIZING')
    expect(handler).not.toHaveBeenCalled()
  })

  it('reset returns to CREATED', () => {
    const lc = createLifecycle()
    lc.reset()
    expect(lc.state).toBe('CREATED')
    expect(lc.previousState).toBeNull()
  })

  it('publishes state changed event', async () => {
    const events = new SimpleEventBus()
    const handler = vi.fn()
    events.subscribe('sdk:state:changed', handler)
    const lc = new Lifecycle(new SilentLogger(), events)

    await lc.transition('INITIALIZING')
    expect(handler).toHaveBeenCalledWith({
      from: 'CREATED',
      to: 'INITIALIZING',
      reason: undefined,
    })
  })

  it('transitions through full lifecycle', async () => {
    const lc = createLifecycle()

    await lc.transition('INITIALIZING')
    expect(lc.state).toBe('INITIALIZING')

    await lc.transition('READY')
    expect(lc.state).toBe('READY')

    await lc.transition('DEGRADED')
    expect(lc.state).toBe('DEGRADED')

    await lc.transition('READY')
    expect(lc.state).toBe('READY')

    await lc.transition('OFFLINE')
    expect(lc.state).toBe('OFFLINE')

    await lc.transition('READY')
    expect(lc.state).toBe('READY')

    await lc.transition('STOPPING')
    expect(lc.state).toBe('STOPPING')

    await lc.transition('STOPPED')
    expect(lc.state).toBe('STOPPED')
  })

  it('SDKStates array has all 7 states', () => {
    expect(SDKStates).toEqual([
      'CREATED', 'INITIALIZING', 'READY', 'DEGRADED', 'OFFLINE', 'STOPPING', 'STOPPED',
    ])
  })

  it('transition to same state is a no-op', async () => {
    const lc = createLifecycle()
    await lc.transition('INITIALIZING')
    await lc.transition('INITIALIZING')
    expect(lc.state).toBe('INITIALIZING')
  })

  it('canTransition returns false for unknown state', () => {
    const lc = createLifecycle()
    expect(lc.canTransition('UNKNOWN' as SDKState)).toBe(false)
  })
})
