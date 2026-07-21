export interface Clock {
  now(): number
  setTimeout(handler: () => void, ms: number): number
  clearTimeout(id: number): void
}
