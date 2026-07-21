import type { CacheEntry, CachePolicy, CacheStore } from '../contracts/cache'
import { DEFAULT_CACHE_POLICY, mergePolicy } from './cache-policy'
import { createCacheEntry, isExpired } from './cache-entry'
import type { EventBus } from '../contracts/event-bus'
import { SDKEvents } from '../events/sdk-events'
import type { CacheClearedPayload, CacheHitPayload, CacheMissPayload } from '../events/sdk-events'

export class InMemoryCacheStore implements CacheStore {
  private store = new Map<string, CacheEntry<unknown>>()
  private _hits = 0
  private _misses = 0
  private policy: CachePolicy
  private events: EventBus

  constructor(events: EventBus, policy?: Partial<CachePolicy>) {
    this.events = events
    this.policy = mergePolicy(DEFAULT_CACHE_POLICY, policy)
  }

  async get<T>(key: string): Promise<CacheEntry<T> | undefined> {
    const entry = this.store.get(key) as CacheEntry<T> | undefined
    if (!entry) {
      this._misses++
      const payload: CacheMissPayload = { key }
      this.events.publish(SDKEvents.CacheMiss, payload)
      return undefined
    }

    if (isExpired(entry)) {
      this.store.delete(key)
      this._misses++
      const payload: CacheMissPayload = { key }
      this.events.publish(SDKEvents.CacheMiss, payload)

      if (this.policy.staleWhileRevalidate) {
        entry.hitCount++
        return entry
      }
      return undefined
    }

    this._hits++
    entry.hitCount++
    const payload: CacheHitPayload = { key, ttl: entry.expiresAt - Date.now() }
    this.events.publish(SDKEvents.CacheHit, payload)
    return entry
  }

  async set<T>(key: string, value: T, override?: Partial<CachePolicy>): Promise<void> {
    if (this.store.size >= this.policy.maxEntries) {
      this.evictOldest()
    }

    const merged = mergePolicy(this.policy, override)
    const entry = createCacheEntry(value, merged.ttl)
    this.store.set(key, entry)
  }

  async delete(key: string): Promise<boolean> {
    return this.store.delete(key)
  }

  async clear(): Promise<void> {
    const count = this.store.size
    this.store.clear()
    this._hits = 0
    this._misses = 0
    const payload: CacheClearedPayload = { entries: count }
    this.events.publish(SDKEvents.CacheCleared, payload)
  }

  async has(key: string): Promise<boolean> {
    const entry = this.store.get(key)
    if (!entry) return false
    if (isExpired(entry)) {
      this.store.delete(key)
      return false
    }
    return true
  }

  async size(): Promise<number> {
    return this.store.size
  }

  async hits(): Promise<number> {
    return this._hits
  }

  async misses(): Promise<number> {
    return this._misses
  }

  private evictOldest(): void {
    let oldest: string | undefined
    let oldestTime = Infinity

    for (const [key, entry] of this.store.entries()) {
      if (entry.createdAt < oldestTime) {
        oldestTime = entry.createdAt
        oldest = key
      }
    }

    if (oldest) {
      this.store.delete(oldest)
    }
  }
}
