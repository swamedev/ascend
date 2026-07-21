import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class ValidationError extends AscendError {
  constructor(
    message: string,
    options?: {
      details?: unknown
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: ErrorCodes.ValidationError,
      details: options?.details,
      recoverable: false,
      severity: 'warning' satisfies ErrorSeverity,
      source: options?.source ?? 'validation',
      correlationId: options?.correlationId,
    })
    this.name = 'ValidationError'
  }
}
