import { AscendError } from './ascend.error'

export class OfflineError extends AscendError {
  constructor(message: string, details?: unknown) {
    super(message, {
      code: 'OFFLINE_ERR',
      statusCode: 503,
      details,
      retryable: true,
    })
    this.name = 'OfflineError'
  }
}
