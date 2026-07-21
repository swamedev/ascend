import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class DomainError extends AscendError {
  readonly currentState?: string
  readonly expectedState?: string

  constructor(
    message: string,
    options?: {
      code?: string
      currentState?: string
      expectedState?: string
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: options?.code ?? ErrorCodes.InvalidTransition,
      details: {
        currentState: options?.currentState,
        expectedState: options?.expectedState,
      },
      recoverable: false,
      severity: 'error' satisfies ErrorSeverity,
      source: options?.source ?? 'domain',
      correlationId: options?.correlationId,
    })
    this.name = 'DomainError'
    this.currentState = options?.currentState
    this.expectedState = options?.expectedState
  }
}
