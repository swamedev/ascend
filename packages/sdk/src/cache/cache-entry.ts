import type { CacheEntry } from '../contracts/cache'

export function createCacheEntry<T>(value: T, ttl: number): CacheEntry<T> {
  const now = Date.now()
  return {
    value,
    expiresAt: now + ttl,
    createdAt: now,
    hitCount: 0,
  }
}

export function isExpired(entry: CacheEntry<unknown>): boolean {
  return Date.now() > entry.expiresAt
}
