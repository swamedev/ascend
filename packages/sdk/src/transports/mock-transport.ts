import type { Transport, TransportStatus, RequestConfig, TransportResponse, TransportHealth } from '../contracts/transport'

export interface MockTransportOptions {
  latency?: number
  failureRate?: number
  failureStatuses?: number[]
}

type MockHandler = (config: RequestConfig) => Promise<unknown>

export class MockTransport implements Transport {
  readonly name = 'mock'
  private _status: TransportStatus = 'disconnected'
  private statusHandlers = new Set<(status: TransportStatus) => void>()
  private latency: number
  private failureRate: number
  private failureStatuses: number[]
  private handlers = new Map<string, MockHandler>()
  private callHistory: Array<{ config: RequestConfig; timestamp: number; duration: number; success: boolean; status: number }> = []

  constructor(options?: MockTransportOptions) {
    this.latency = options?.latency ?? 0
    this.failureRate = options?.failureRate ?? 0
    this.failureStatuses = options?.failureStatuses ?? [500, 503]
  }

  get status(): TransportStatus {
    return this._status
  }

  register(pattern: string, handler: MockHandler): void {
    this.handlers.set(pattern, handler)
  }

  getCallHistory(): Array<{ config: RequestConfig; timestamp: number; duration: number; success: boolean; status: number }> {
    return [...this.callHistory]
  }

  clearCallHistory(): void {
    this.callHistory = []
  }

  async connect(): Promise<void> {
    this.setStatus('connecting')
    await this.simulateLatency()
    this.setStatus('connected')
  }

  async disconnect(): Promise<void> {
    this.setStatus('disconnected')
    this.clearCallHistory()
  }

  async request<T>(config: RequestConfig): Promise<TransportResponse<T>> {
    if (this._status !== 'connected') {
      throw new Error(`MockTransport not connected (status: ${this._status})`)
    }

    const start = Date.now()
    await this.simulateLatency()
    this.maybeFail()

    const handler = this.findHandler(config)
    if (!handler) {
      const duration = Date.now() - start
      this.callHistory.push({ config, timestamp: start, duration, success: false, status: 404 })
      throw new Error(`No mock handler for: ${config.method} ${config.path}`)
    }

    try {
      const data = await handler(config)
      const duration = Date.now() - start
      this.callHistory.push({ config, timestamp: start, duration, success: true, status: 200 })

      return {
        data: data as T,
        status: 200,
        headers: { 'content-type': 'application/json' },
        timestamp: Date.now(),
      }
    } catch (error) {
      const duration = Date.now() - start
      this.callHistory.push({ config, timestamp: start, duration, success: false, status: 500 })
      throw error
    }
  }

  async health(): Promise<TransportHealth> {
    const start = Date.now()
    await this.simulateLatency()
    const latency = Date.now() - start

    return {
      status: this._status === 'connected' ? 'healthy' : 'unhealthy',
      latency,
      message: this._status !== 'connected' ? `Transport status: ${this._status}` : undefined,
    }
  }

  onStatusChange(handler: (status: TransportStatus) => void): () => void {
    this.statusHandlers.add(handler)
    return () => {
      this.statusHandlers.delete(handler)
    }
  }

  private setStatus(status: TransportStatus): void {
    this._status = status
    for (const handler of this.statusHandlers) {
      handler(status)
    }
  }

  private async simulateLatency(): Promise<void> {
    if (this.latency > 0) {
      await new Promise(resolve => setTimeout(resolve, this.latency))
    }
  }

  private maybeFail(): void {
    if (this.failureRate > 0 && Math.random() < this.failureRate) {
      const status = this.failureStatuses[Math.floor(Math.random() * this.failureStatuses.length)]
      throw new Error(`Simulated failure (HTTP ${status})`)
    }
  }

  private findHandler(config: RequestConfig): MockHandler | undefined {
    const path = config.path

    for (const [pattern, handler] of this.handlers.entries()) {
      if (pattern === path) return handler

      const patternParts = pattern.split('/')
      const pathParts = path.split('/')

      if (patternParts.length === pathParts.length) {
        let match = true
        for (let i = 0; i < patternParts.length; i++) {
          const pp = patternParts[i]!
          const p = pathParts[i]!
          if (pp.startsWith(':')) continue
          if (pp !== p) { match = false; break }
        }
        if (match) return handler
      }
    }

    return undefined
  }
}
