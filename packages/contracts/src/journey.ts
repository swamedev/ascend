import type { JourneyId, BuilderId, CompetencyId, CertificateId } from './ids'
import type { MissionSummary } from './mission'

export interface JourneySummary {
  id: JourneyId
  title: string
  description: string
  category: string
  difficulty: number
  estimatedDuration: string
  missionCount: number
  completedCount: number
  status: 'not_started' | 'in_progress' | 'completed' | 'abandoned'
  xpReward: number
  prerequisites: JourneyId[]
}

export interface JourneyDetail {
  id: JourneyId
  title: string
  description: string
  category: string
  difficulty: number
  estimatedDuration: string
  xpReward: number
  certificateId?: CertificateId
  prerequisites: JourneyId[]
  missions: MissionSummary[]
  status: 'not_started' | 'in_progress' | 'completed' | 'abandoned'
  progress: JourneyProgress
  startedAt?: string
  completedAt?: string
}

export interface JourneyProgress {
  journeyId: JourneyId
  builderId: BuilderId
  missionsCompleted: number
  missionsTotal: number
  evidenceSubmitted: number
  evidenceAccepted: number
  xpEarned: number
  percentComplete: number
  startedAt: string
  completedAt?: string
  lastActivityAt: string
}

export interface JourneyNode {
  id: JourneyId
  title: string
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  prerequisites: JourneyId[]
  children: JourneyNode[]
}

export interface CompetencyRef {
  competencyId: CompetencyId
  name: string
  level: number
}
