import { describe, it, expect, beforeEach, vi } from 'vitest'
import { InMemoryCacheStore } from '../src/cache/cache-store'
import { SimpleEventBus } from '../src/events/event-bus'
import { createCacheKey } from '../src/cache/cache-key'

describe('createCacheKey', () => {
  it('creates key from method and path', () => {
    expect(createCacheKey('GET', '/builder')).toBe('GET:/builder')
  })

  it('includes sorted params', () => {
    const key = createCacheKey('GET', '/missions', { status: 'active', limit: '10' })
    expect(key).toContain('limit=10')
    expect(key).toContain('status=active')
  })
})

describe('InMemoryCacheStore', () => {
  let cache: InMemoryCacheStore
  let events: SimpleEventBus

  beforeEach(() => {
    events = new SimpleEventBus()
    cache = new InMemoryCacheStore(events)
  })

  it('stores and retrieves values', async () => {
    await cache.set('key1', { name: 'test' })
    const entry = await cache.get<{ name: string }>('key1')
    expect(entry?.value).toEqual({ name: 'test' })
  })

  it('returns undefined for missing keys', async () => {
    const entry = await cache.get('nonexistent')
    expect(entry).toBeUndefined()
  })

  it('tracks hits and misses', async () => {
    await cache.set('k', 'v')
    await cache.get('k')
    await cache.get('missing')

    expect(await cache.hits()).toBe(1)
    expect(await cache.misses()).toBe(1)
  })

  it('checks key existence', async () => {
    await cache.set('exists', 'v')
    expect(await cache.has('exists')).toBe(true)
    expect(await cache.has('no')).toBe(false)
  })

  it('deletes keys', async () => {
    await cache.set('x', 'v')
    expect(await cache.delete('x')).toBe(true)
    expect(await cache.has('x')).toBe(false)
  })

  it('clears all entries', async () => {
    await cache.set('a', 1)
    await cache.set('b', 2)
    await cache.clear()
    expect(await cache.size()).toBe(0)
  })

  it('reports size', async () => {
    expect(await cache.size()).toBe(0)
    await cache.set('a', 1)
    expect(await cache.size()).toBe(1)
  })

  it('evicts oldest when over max entries', async () => {
    const smallCache = new InMemoryCacheStore(events, { maxEntries: 2, ttl: 60000 })
    await smallCache.set('a', 1)
    await smallCache.set('b', 2)
    await smallCache.set('c', 3)

    expect(await smallCache.size()).toBe(2)
    expect(await smallCache.has('a')).toBe(false)
  })

  it('publishes CacheHit event on hit', async () => {
    const handler = vi.fn()
    events.subscribe('sdk:cache:hit', handler)
    await cache.set('hit', 'value')
    await cache.get('hit')
    expect(handler).toHaveBeenCalled()
  })

  it('publishes CacheMiss event on miss', async () => {
    const handler = vi.fn()
    events.subscribe('sdk:cache:miss', handler)
    await cache.get('miss')
    expect(handler).toHaveBeenCalled()
  })

  it('publishes CacheCleared on clear', async () => {
    const handler = vi.fn()
    events.subscribe('sdk:cache:cleared', handler)
    await cache.set('a', 1)
    await cache.clear()
    expect(handler).toHaveBeenCalled()
  })

  it('returns stale data when staleWhileRevalidate is true', async () => {
    const staleCache = new InMemoryCacheStore(events, { ttl: -1000, staleWhileRevalidate: true })
    await staleCache.set('stale', 'old-value')
    const entry = await staleCache.get<string>('stale')
    expect(entry?.value).toBe('old-value')
  })

  it('returns undefined for expired entry without stale revalidation', async () => {
    const noStaleCache = new InMemoryCacheStore(events, { ttl: -1000, staleWhileRevalidate: false })
    await noStaleCache.set('expired', 'value')
    const entry = await noStaleCache.get('expired')
    expect(entry).toBeUndefined()
  })

  it('has returns false for expired entries', async () => {
    const expiredCache = new InMemoryCacheStore(events, { ttl: -1 })
    await expiredCache.set('expired-key', 'val')
    const exists = await expiredCache.has('expired-key')
    expect(exists).toBe(false)
  })
})
