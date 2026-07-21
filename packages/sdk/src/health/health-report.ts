import type { SDKState } from '../lifecycle/lifecycle'
import type { TransportStatus } from '../contracts/transport'

export interface TransportHealthInfo {
  name: string
  status: TransportStatus
  latency: number
}

export interface SDKHealthReport {
  status: 'healthy' | 'degraded' | 'unhealthy'
  sdkState: SDKState
  transport: TransportHealthInfo
  cache: {
    size: number
    hitRate: number
  }
  latency: number
  version: string
  uptime: number
  activeTransport: string
  registeredTransports: string[]
  warnings: string[]
}
