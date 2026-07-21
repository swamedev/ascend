import { describe, it, expect } from 'vitest'
import { createTestSDK } from '../src/testing/create-sdk'

describe('createTestSDK', () => {
  it('creates an SDK with mock transport', () => {
    const { sdk, transport } = createTestSDK()
    expect(sdk).toBeDefined()
    expect(transport).toBeDefined()
    expect(transport.name).toBe('mock')
  })

  it('creates SDK in CREATED state', () => {
    const { sdk } = createTestSDK()
    expect(sdk.state).toBe('CREATED')
  })

  it('SDK can initialize with test harness', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    expect(sdk.state).toBe('READY')
  })

  it('SDK health works after init', async () => {
    const { sdk } = createTestSDK()
    await sdk.initialize()
    const health = await sdk.health()
    expect(health.status).toBe('healthy')
  })

  it('creates SDK with custom options', () => {
    const { sdk } = createTestSDK({ latency: 10, failureRate: 0.5 })
    expect(sdk).toBeDefined()
  })
})
