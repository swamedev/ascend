import { AscendSDK } from '../core/ascend-sdk'
import { MockTransport } from '../transports/mock-transport'
import { SimpleEventBus } from '../events/event-bus'
import { InMemoryCacheStore } from '../cache/cache-store'
import { SilentLogger } from '../logger/silent-logger'
import { SystemClock } from '../clock/system-clock'
import type { SDKConfig } from '../core/types'

export interface TestSDKOptions {
  latency?: number
  failureRate?: number
  config?: Partial<SDKConfig>
}

export function createTestSDK(options?: TestSDKOptions): {
  sdk: AscendSDK
  transport: MockTransport
} {
  const events = new SimpleEventBus()
  const transport = new MockTransport({
    latency: options?.latency,
    failureRate: options?.failureRate,
  })

  const sdk = new AscendSDK({
    transport,
    cache: new InMemoryCacheStore(events),
    logger: new SilentLogger(),
    eventBus: events,
    clock: new SystemClock(),
  })

  return { sdk, transport }
}
