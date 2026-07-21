import type { MockTransport } from '../transports/mock-transport'

export function simulateTransportFailure(transport: MockTransport, rate: number): void {
  const mockTransport = transport as MockTransport
  Object.defineProperty(mockTransport, 'failureRate', {
    value: rate,
    writable: true,
  })
}
