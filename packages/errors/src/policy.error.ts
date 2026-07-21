import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class PolicyError extends AscendError {
  readonly prerequisite?: string

  constructor(
    message: string,
    options?: {
      prerequisite?: string
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: ErrorCodes.PrerequisiteNotMet,
      details: options?.prerequisite ? { prerequisite: options.prerequisite } : undefined,
      recoverable: false,
      severity: 'warning' satisfies ErrorSeverity,
      source: options?.source ?? 'policy',
      correlationId: options?.correlationId,
    })
    this.name = 'PolicyError'
    this.prerequisite = options?.prerequisite
  }
}
