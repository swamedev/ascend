import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class NetworkError extends AscendError {
  constructor(
    message: string,
    options?: {
      details?: unknown
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: ErrorCodes.NetworkError,
      details: options?.details,
      recoverable: true,
      severity: 'error' satisfies ErrorSeverity,
      source: options?.source ?? 'network',
      correlationId: options?.correlationId,
    })
    this.name = 'NetworkError'
  }
}
