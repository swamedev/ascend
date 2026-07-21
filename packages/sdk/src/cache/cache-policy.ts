import type { CachePolicy } from '../contracts/cache'

export const DEFAULT_CACHE_POLICY: CachePolicy = {
  ttl: 30_000,
  staleWhileRevalidate: true,
  maxEntries: 500,
}

export function mergePolicy(base: CachePolicy, override?: Partial<CachePolicy>): CachePolicy {
  if (!override) return { ...base }
  return { ...base, ...override }
}
