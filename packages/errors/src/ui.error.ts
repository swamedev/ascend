import { AscendError } from './ascend-error'
import { ErrorCodes } from './error-codes'
import type { ErrorSeverity } from './envelope'

export class UIError extends AscendError {
  readonly component?: string

  constructor(
    message: string,
    options?: {
      code?: string
      component?: string
      source?: string
      correlationId?: string
    },
  ) {
    super(message, {
      code: options?.code ?? ErrorCodes.RenderError,
      details: options?.component ? { component: options.component } : undefined,
      recoverable: true,
      severity: 'error' satisfies ErrorSeverity,
      source: options?.source ?? 'ui',
      correlationId: options?.correlationId,
    })
    this.name = 'UIError'
    this.component = options?.component
  }
}
