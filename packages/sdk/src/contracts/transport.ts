export type TransportStatus = 'disconnected' | 'connecting' | 'connected' | 'error'

export interface RequestConfig {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'
  path: string
  body?: unknown
  params?: Record<string, string>
  headers?: Record<string, string>
  timeout?: number
  retry?: RetryConfig
}

export interface TransportResponse<T> {
  data: T
  status: number
  headers: Record<string, string>
  timestamp: number
}

export interface TransportHealth {
  status: 'healthy' | 'degraded' | 'unhealthy'
  latency: number
  message?: string
}

export interface RetryConfig {
  maxRetries: number
  baseDelay: number
  maxDelay: number
  retryableStatuses: number[]
}

export interface Transport {
  readonly name: string
  readonly status: TransportStatus

  connect(): Promise<void>
  disconnect(): Promise<void>

  request<T>(config: RequestConfig): Promise<TransportResponse<T>>

  health(): Promise<TransportHealth>

  onStatusChange(handler: (status: TransportStatus) => void): () => void
}
