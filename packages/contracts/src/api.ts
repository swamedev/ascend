export interface ApiResponse<T> {
  success: true
  data: T
  timestamp: string
}

export interface ApiErrorResponse {
  success: false
  error: ApiErrorPayload
  timestamp: string
}

export interface ApiErrorPayload {
  code: string
  message: string
  details?: unknown
  correlationId: string
  timestamp: string
}
