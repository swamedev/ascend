export type ErrorSeverity = 'critical' | 'error' | 'warning' | 'info'

export interface AscendErrorEnvelope {
  code: string
  message: string
  details?: unknown
  recoverable: boolean
  severity: ErrorSeverity
  source: string
  timestamp: string
  correlationId: string
}
