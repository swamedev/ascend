import { AscendError } from './ascend.error'

export class AuthenticationError extends AscendError {
  constructor(message: string, details?: unknown) {
    super(message, {
      code: 'AUTH_ERR',
      statusCode: 401,
      details,
      retryable: false,
    })
    this.name = 'AuthenticationError'
  }
}
