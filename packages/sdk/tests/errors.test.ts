import { describe, it, expect } from 'vitest'
import { AscendError, ValidationError, NetworkError, AuthenticationError, ConflictError, OfflineError } from '../src/errors'

describe('AscendError', () => {
  it('creates with default values', () => {
    const error = new AscendError('test error')
    expect(error.message).toBe('test error')
    expect(error.code).toBe('ASCEND_ERR')
    expect(error.statusCode).toBe(500)
    expect(error.retryable).toBe(false)
    expect(error.timestamp).toBeGreaterThan(0)
  })

  it('creates with custom options', () => {
    const error = new AscendError('custom', {
      code: 'CUSTOM_ERR',
      statusCode: 400,
      details: { field: 'name' },
      retryable: true,
    })
    expect(error.code).toBe('CUSTOM_ERR')
    expect(error.statusCode).toBe(400)
    expect(error.details).toEqual({ field: 'name' })
    expect(error.retryable).toBe(true)
  })
})

describe('ValidationError', () => {
  it('creates with correct code and status', () => {
    const error = new ValidationError('invalid input', { field: 'email' })
    expect(error.code).toBe('VALIDATION_ERR')
    expect(error.statusCode).toBe(422)
    expect(error.retryable).toBe(false)
    expect(error.details).toEqual({ field: 'email' })
  })
})

describe('NetworkError', () => {
  it('creates with retryable = true', () => {
    const error = new NetworkError('connection lost')
    expect(error.code).toBe('NETWORK_ERR')
    expect(error.statusCode).toBe(0)
    expect(error.retryable).toBe(true)
  })
})

describe('AuthenticationError', () => {
  it('creates with 401 status', () => {
    const error = new AuthenticationError('unauthorized')
    expect(error.code).toBe('AUTH_ERR')
    expect(error.statusCode).toBe(401)
    expect(error.retryable).toBe(false)
  })
})

describe('ConflictError', () => {
  it('creates with 409 status', () => {
    const error = new ConflictError('duplicate')
    expect(error.code).toBe('CONFLICT_ERR')
    expect(error.statusCode).toBe(409)
  })
})

describe('OfflineError', () => {
  it('creates with retryable = true', () => {
    const error = new OfflineError('no network')
    expect(error.code).toBe('OFFLINE_ERR')
    expect(error.statusCode).toBe(503)
    expect(error.retryable).toBe(true)
  })
})
