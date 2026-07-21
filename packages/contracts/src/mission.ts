import type { MissionId, JourneyId, BuilderId, EvidenceId } from './ids'
import type { EvidenceStatus } from './enums'

export interface MissionSummary {
  id: MissionId
  title: string
  description: string
  type: string
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  xpReward: number
  evidenceRequired: number
  evidenceSubmitted: number
  prerequisites: MissionId[]
}

export interface MissionDetail {
  id: MissionId
  journeyId: JourneyId
  title: string
  description: string
  type: string
  instructions: string
  xpReward: number
  evidenceRequired: number
  prerequisites: MissionId[]
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  startedAt?: string
  completedAt?: string
}

export interface EvidenceRecord {
  id: EvidenceId
  missionId: MissionId
  builderId: BuilderId
  type: string
  content: string
  status: EvidenceStatus
  submittedAt: string
  reviewedAt?: string
  feedback?: Feedback[]
  competencies: string[]
}

export interface Feedback {
  id: string
  evidenceId: EvidenceId
  reviewer: string
  message: string
  rating?: number
  createdAt: string
}

export interface MissionResult {
  missionId: MissionId
  builderId: BuilderId
  completed: boolean
  xpEarned: number
  evidenceAccepted: number
  evidenceRejected: number
  competenciesAdvanced: string[]
  completedAt: string
}
