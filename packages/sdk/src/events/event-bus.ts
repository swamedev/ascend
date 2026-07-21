import type { EventBus, EventHandler } from '../contracts/event-bus'

export class SimpleEventBus implements EventBus {
  private handlers = new Map<string, Set<EventHandler>>()
  private draining = false
  private pending: Array<() => void> = []

  publish<T>(event: string, payload: T): void {
    if (this.draining) return

    const handlers = this.handlers.get(event)
    if (!handlers) return

    for (const handler of handlers) {
      const result = handler(payload)
      if (result instanceof Promise) {
        this.pending.push(() => result.catch(() => {}))
      }
    }
  }

  subscribe<T>(event: string, handler: EventHandler<T>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set())
    }

    const handlers = this.handlers.get(event)!
    handlers.add(handler as EventHandler)

    return () => {
      handlers.delete(handler as EventHandler)
      if (handlers.size === 0) {
        this.handlers.delete(event)
      }
    }
  }

  unsubscribe(event: string, handler: EventHandler): void {
    const handlers = this.handlers.get(event)
    if (!handlers) return

    handlers.delete(handler)
    if (handlers.size === 0) {
      this.handlers.delete(event)
    }
  }

  async drain(): Promise<void> {
    this.draining = true

    while (this.pending.length > 0) {
      const pending = this.pending.splice(0, this.pending.length)
      await Promise.allSettled(pending.map(fn => fn()))
    }

    this.draining = false
  }

  clear(): void {
    this.handlers.clear()
    this.pending = []
    this.draining = false
  }

  listenerCount(event?: string): number {
    if (event) {
      return this.handlers.get(event)?.size ?? 0
    }
    let count = 0
    for (const handlers of this.handlers.values()) {
      count += handlers.size
    }
    return count
  }
}
