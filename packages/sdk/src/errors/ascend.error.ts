export class AscendError extends Error {
  readonly code: string
  readonly statusCode: number
  readonly details: unknown
  readonly timestamp: number
  readonly retryable: boolean

  constructor(
    message: string,
    options?: {
      code?: string
      statusCode?: number
      details?: unknown
      retryable?: boolean
    },
  ) {
    super(message)
    this.name = 'AscendError'
    this.code = options?.code ?? 'ASCEND_ERR'
    this.statusCode = options?.statusCode ?? 500
    this.details = options?.details
    this.timestamp = Date.now()
    this.retryable = options?.retryable ?? false
  }
}
