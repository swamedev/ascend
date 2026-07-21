export type EventHandler<T = unknown> = (payload: T) => void | Promise<void>

export interface EventBus {
  publish<T>(event: string, payload: T): void
  subscribe<T>(event: string, handler: EventHandler<T>): () => void
  unsubscribe(event: string, handler: EventHandler): void
  drain(): Promise<void>
  clear(): void
  listenerCount(event?: string): number
}
