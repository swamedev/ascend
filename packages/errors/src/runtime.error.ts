import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class RuntimeError extends AscendError {
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
      code: options?.code ?? ErrorCodes.InternalError,
      details: options?.details,
      recoverable: true,
      severity: 'critical' satisfies ErrorSeverity,
      source: options?.source ?? 'runtime',
      correlationId: options?.correlationId,
    })
    this.name = 'RuntimeError'
  }
}
