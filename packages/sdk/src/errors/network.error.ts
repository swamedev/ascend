import { AscendError } from './ascend.error'

export class NetworkError extends AscendError {
  constructor(message: string, details?: unknown) {
    super(message, {
      code: 'NETWORK_ERR',
      statusCode: 0,
      details,
      retryable: true,
    })
    this.name = 'NetworkError'
  }
}
