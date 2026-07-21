import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class ConflictError extends AscendError {
  constructor(
    message: string,
    options?: {
      details?: unknown
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: ErrorCodes.Conflict,
      details: options?.details,
      recoverable: false,
      severity: 'warning' satisfies ErrorSeverity,
      source: options?.source ?? 'application',
      correlationId: options?.correlationId,
    })
    this.name = 'ConflictError'
  }
}
