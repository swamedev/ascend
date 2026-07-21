import { describe, it, expect, beforeEach } from 'vitest'
import { MockTransport } from '../src/transports/mock-transport'

describe('MockTransport', () => {
  let transport: MockTransport

  beforeEach(() => {
    transport = new MockTransport()
  })

  it('starts disconnected', () => {
    expect(transport.status).toBe('disconnected')
  })

  it('connects and changes status', async () => {
    await transport.connect()
    expect(transport.status).toBe('connected')
  })

  it('disconnects and clears history', async () => {
    await transport.connect()
    transport.register('/test', async () => ({ ok: true }))
    await transport.request({ method: 'GET', path: '/test' })
    await transport.disconnect()
    expect(transport.status).toBe('disconnected')
    expect(transport.getCallHistory()).toHaveLength(0)
  })

  it('rejects requests when disconnected', async () => {
    await expect(
      transport.request({ method: 'GET', path: '/' }),
    ).rejects.toThrow('not connected')
  })

  it('executes registered handlers', async () => {
    await transport.connect()
    transport.register('/builder', async () => ({ name: 'Test' }))

    const response = await transport.request<{ name: string }>({ method: 'GET', path: '/builder' })
    expect(response.data).toEqual({ name: 'Test' })
    expect(response.status).toBe(200)
  })

  it('handles path parameters', async () => {
    await transport.connect()
    transport.register('/missions/:id', async (config) => {
      const id = config.path.split('/').pop()
      return { id, title: 'Mission' }
    })

    const response = await transport.request<{ id: string }>({ method: 'GET', path: '/missions/123' })
    expect(response.data.id).toBe('123')
  })

  it('records call history', async () => {
    await transport.connect()
    transport.register('/test', async () => ({ ok: true }))
    await transport.request({ method: 'GET', path: '/test' })

    const history = transport.getCallHistory()
    expect(history).toHaveLength(1)
    expect(history[0]?.success).toBe(true)
    expect(history[0]?.config.path).toBe('/test')
  })

  it('returns health status', async () => {
    const health = await transport.health()
    expect(health.status).toBe('unhealthy')
    expect(health.latency).toBeGreaterThanOrEqual(0)
  })

  it('returns healthy after connect', async () => {
    await transport.connect()
    const health = await transport.health()
    expect(health.status).toBe('healthy')
  })

  it('notifies on status change', async () => {
    const changes: string[] = []
    transport.onStatusChange((status) => { changes.push(status) })

    await transport.connect()
    expect(changes).toContain('connecting')
    expect(changes).toContain('connected')
  })

  it('unsubscribes from status changes', async () => {
    const changes: string[] = []
    const unsub = transport.onStatusChange((status) => { changes.push(status) })
    unsub()

    await transport.connect()
    expect(changes).toHaveLength(0)
  })

  it('throws on unknown route', async () => {
    await transport.connect()
    await expect(
      transport.request({ method: 'GET', path: '/unknown' }),
    ).rejects.toThrow('No mock handler')
  })

  it('simulates latency', async () => {
    const slow = new MockTransport({ latency: 50 })
    await slow.connect()
    slow.register('/ping', async () => ({ pong: true }))

    const start = Date.now()
    await slow.request({ method: 'GET', path: '/ping' })
    const elapsed = Date.now() - start

    expect(elapsed).toBeGreaterThanOrEqual(45)
  })

  it('records failed calls in history', async () => {
    await transport.connect()
    transport.register('/fail', async () => {
      throw new Error('handler error')
    })

    await expect(transport.request({ method: 'GET', path: '/fail' })).rejects.toThrow('handler error')
    const history = transport.getCallHistory()
    expect(history[0]?.success).toBe(false)
    expect(history[0]?.status).toBe(500)
  })

  it('can simulate failures based on rate', async () => {
    const failing = new MockTransport({ failureRate: 1 })
    await failing.connect()
    failing.register('/maybe', async () => ({ ok: true }))

    await expect(failing.request({ method: 'GET', path: '/maybe' })).rejects.toThrow('Simulated failure')
  })

  it('returns undefined handler when pattern segment mismatch', async () => {
    await transport.connect()
    transport.register('/missions/active', async () => ({ list: [] }))

    await expect(transport.request({ method: 'GET', path: '/missions/completed' })).rejects.toThrow('No mock handler')
  })
})
