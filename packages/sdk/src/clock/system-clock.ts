import type { Clock } from '../contracts/clock'

export class SystemClock implements Clock {
  now(): number {
    return Date.now()
  }

  setTimeout(handler: () => void, ms: number): number {
    return window.setTimeout(handler, ms)
  }

  clearTimeout(id: number): void {
    window.clearTimeout(id)
  }
}
