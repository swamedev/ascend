import type { AscendErrorEnvelope, ErrorSeverity } from './envelope'

let correlationCounter = 0

function generateCorrelationId(): string {
  correlationCounter++
  const ts = Date.now().toString(36)
  const rand = Math.random().toString(36).slice(2, 8)
  return `asc-${ts}-${rand}-${correlationCounter}`
}

export class AscendError extends Error implements AscendErrorEnvelope {
  readonly code: string
  readonly details: unknown
  readonly recoverable: boolean
  readonly severity: ErrorSeverity
  readonly source: string
  readonly timestamp: string
  readonly correlationId: string

  constructor(
    message: string,
    options?: {
      code?: string
      details?: unknown
      recoverable?: boolean
      severity?: ErrorSeverity
      source?: string
      correlationId?: string
    },
  ) {
    super(message)
    this.name = 'AscendError'
    this.code = options?.code ?? 'ASCEND_ERR'
    this.details = options?.details
    this.recoverable = options?.recoverable ?? false
    this.severity = options?.severity ?? 'error'
    this.source = options?.source ?? 'unknown'
    this.timestamp = new Date().toISOString()
    this.correlationId = options?.correlationId ?? generateCorrelationId()
  }

  toEnvelope(): AscendErrorEnvelope {
    return {
      code: this.code,
      message: this.message,
      details: this.details,
      recoverable: this.recoverable,
      severity: this.severity,
      source: this.source,
      timestamp: this.timestamp,
      correlationId: this.correlationId,
    }
  }
}
