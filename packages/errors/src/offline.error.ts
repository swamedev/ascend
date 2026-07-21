import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class OfflineError extends AscendError {
  readonly queued: boolean

  constructor(
    message: string,
    options?: {
      queued?: boolean
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: ErrorCodes.Offline,
      recoverable: true,
      severity: 'warning' satisfies ErrorSeverity,
      source: options?.source ?? 'network',
      correlationId: options?.correlationId,
    })
    this.name = 'OfflineError'
    this.queued = options?.queued ?? false
  }
}
