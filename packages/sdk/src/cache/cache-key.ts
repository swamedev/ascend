export function createCacheKey(method: string, path: string, params?: Record<string, string>): string {
  if (!params || Object.keys(params).length === 0) {
    return `${method}:${path}`
  }

  const sorted = Object.entries(params)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([k, v]) => `${k}=${v}`)
    .join('&')

  return `${method}:${path}?${sorted}`
}
