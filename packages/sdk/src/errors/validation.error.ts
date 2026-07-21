import { AscendError } from './ascend.error'

export class ValidationError extends AscendError {
  constructor(message: string, details?: unknown) {
    super(message, {
      code: 'VALIDATION_ERR',
      statusCode: 422,
      details,
      retryable: false,
    })
    this.name = 'ValidationError'
  }
}
