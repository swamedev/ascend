import type { Transport } from '../contracts/transport'
import { AscendError } from '../errors/ascend.error'

export class TransportRegistry {
  private transports = new Map<string, Transport>()

  register(name: string, transport: Transport): void {
    if (this.transports.has(name)) {
      throw new AscendError(
        `Transport already registered: ${name}`,
        { code: 'TRANSPORT_ALREADY_REGISTERED', statusCode: 409, details: { name } },
      )
    }
    this.transports.set(name, transport)
  }

  resolve(name: string): Transport {
    const transport = this.transports.get(name)
    if (!transport) {
      throw new AscendError(
        `Transport not found: ${name}`,
        { code: 'TRANSPORT_NOT_FOUND', statusCode: 404, details: { name, registered: this.list() } },
      )
    }
    return transport
  }

  unregister(name: string): boolean {
    return this.transports.delete(name)
  }

  list(): string[] {
    return Array.from(this.transports.keys())
  }

  has(name: string): boolean {
    return this.transports.has(name)
  }

  clear(): void {
    this.transports.clear()
  }

  get size(): number {
    return this.transports.size
  }
}
