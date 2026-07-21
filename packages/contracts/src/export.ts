import type { Builder } from './builder'
import type { LearningIdentity } from './builder'
import type { AchievementLedger } from './builder'
import type { BuilderProgress } from './builder'
import type { DomainEventEnvelope } from './domain-events'

export interface BuilderExport {
  version: string
  exportedAt: string
  builder: Builder
  identity: LearningIdentity
  ledger: AchievementLedger
  progress: BuilderProgress
  events: DomainEventEnvelope[]
  metadata: {
    format: 'ascend-export-v1'
    totalSize: number
    eventCount: number
    includes: string[]
  }
}

export interface CloudSyncConfig {
  enabled: boolean
  provider?: 'ascend-cloud' | 'self-hosted'
  syncInterval: number
  conflictStrategy: 'lww' | 'manual'
  lastSyncAt?: string
  pendingChanges: number
}
