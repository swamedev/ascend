export interface CacheEntry<T> {
  value: T
  expiresAt: number
  createdAt: number
  hitCount: number
}

export interface CachePolicy {
  ttl: number
  staleWhileRevalidate: boolean
  maxEntries: number
}

export interface CacheStore {
  get<T>(key: string): Promise<CacheEntry<T> | undefined>
  set<T>(key: string, value: T, policy?: Partial<CachePolicy>): Promise<void>
  delete(key: string): Promise<boolean>
  clear(): Promise<void>
  has(key: string): Promise<boolean>
  size(): Promise<number>
  hits(): Promise<number>
  misses(): Promise<number>
}
