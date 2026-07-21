import { describe, it, expect, beforeEach } from 'vitest'
import { TransportRegistry } from '../src/registry/transport-registry'
import { AscendError } from '../src/errors/ascend.error'
import { MockTransport } from '../src/transports/mock-transport'

describe('TransportRegistry', () => {
  let registry: TransportRegistry

  beforeEach(() => {
    registry = new TransportRegistry()
  })

  it('registers and resolves transports', () => {
    const transport = new MockTransport()
    registry.register('mock', transport)
    expect(registry.resolve('mock')).toBe(transport)
  })

  it('throws on duplicate registration', () => {
    registry.register('mock', new MockTransport())
    expect(() => registry.register('mock', new MockTransport())).toThrow(AscendError)
  })

  it('throws on unknown transport', () => {
    expect(() => registry.resolve('unknown')).toThrow(AscendError)
  })

  it('unregisters transports', () => {
    registry.register('mock', new MockTransport())
    expect(registry.unregister('mock')).toBe(true)
    expect(registry.has('mock')).toBe(false)
  })

  it('returns false when unregistering unknown', () => {
    expect(registry.unregister('unknown')).toBe(false)
  })

  it('lists registered transports', () => {
    registry.register('mock', new MockTransport())
    registry.register('rest', new MockTransport())
    expect(registry.list()).toEqual(['mock', 'rest'])
  })

  it('checks transport existence', () => {
    expect(registry.has('mock')).toBe(false)
    registry.register('mock', new MockTransport())
    expect(registry.has('mock')).toBe(true)
  })

  it('clears all transports', () => {
    registry.register('a', new MockTransport())
    registry.register('b', new MockTransport())
    registry.clear()
    expect(registry.size).toBe(0)
  })

  it('reports correct size', () => {
    expect(registry.size).toBe(0)
    registry.register('a', new MockTransport())
    expect(registry.size).toBe(1)
    registry.register('b', new MockTransport())
    expect(registry.size).toBe(2)
  })
})
