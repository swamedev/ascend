import { AscendError } from './ascend.error'

export class ConflictError extends AscendError {
  constructor(message: string, details?: unknown) {
    super(message, {
      code: 'CONFLICT_ERR',
      statusCode: 409,
      details,
      retryable: false,
    })
    this.name = 'ConflictError'
  }
}
