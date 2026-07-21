export const ErrorCodes = {
  NetworkError: 'NETWORK_ERROR',
  Timeout: 'TIMEOUT',
  Offline: 'OFFLINE',
  Unauthorized: 'UNAUTHORIZED',
  Forbidden: 'FORBIDDEN',
  TokenExpired: 'TOKEN_EXPIRED',
  NotFound: 'NOT_FOUND',
  Conflict: 'CONFLICT',
  MissionLocked: 'MISSION_LOCKED',
  MissionAlreadyStarted: 'MISSION_ALREADY_STARTED',
  InvalidTransition: 'INVALID_TRANSITION',
  PrerequisiteNotMet: 'PREREQUISITE_NOT_MET',
  ValidationError: 'VALIDATION_ERROR',
  RateLimited: 'RATE_LIMITED',
  InternalError: 'INTERNAL_ERROR',
  BadGateway: 'BAD_GATEWAY',
  ServiceUnavailable: 'SERVICE_UNAVAILABLE',
  RenderError: 'RENDER_ERROR',
} as const

export type ErrorCode = (typeof ErrorCodes)[keyof typeof ErrorCodes]
