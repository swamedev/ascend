import type { HealthStatus } from './enums'

export interface HealthReport {
  status: HealthStatus
  version: string
  uptime: number
  timestamp: string
  checks: {
    database: boolean
    runtime: boolean
    cache: boolean
  }
}
