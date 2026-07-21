import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class AuthenticationError extends AscendError {
  constructor(
    message: string,
    options?: {
      code?: string
      details?: unknown
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: options?.code ?? ErrorCodes.Unauthorized,
      details: options?.details,
      recoverable: options?.code === ErrorCodes.TokenExpired,
      severity: 'error' satisfies ErrorSeverity,
      source: options?.source ?? 'auth',
      correlationId: options?.correlationId,
    })
    this.name = 'AuthenticationError'
  }
}
