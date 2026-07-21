import type { BuilderId, JourneyId, MissionId, EvidenceId, AssessmentId, CompetencyId, AchievementId, CertificateId } from './ids'

export interface DomainEventEnvelope {
  id: string
  type: string
  version: number
  timestamp: string
  source: string
  correlationId: string
  causationId?: string
  actorId?: string
  payload: Record<string, unknown>
}

export const DomainEventTypes = {
  // Builder
  BuilderCreated: 'builder.created',
  BuilderUpdated: 'builder.updated',
  BuilderDeleted: 'builder.deleted',
  BuilderLeveledUp: 'builder.leveled_up',
  BuilderStreakUpdated: 'builder.streak_updated',
  BuilderPreferencesChanged: 'builder.preferences_changed',

  // Journey
  JourneyStarted: 'journey.started',
  JourneyCompleted: 'journey.completed',
  JourneyAbandoned: 'journey.abandoned',
  JourneyProgressUpdated: 'journey.progress_updated',

  // Mission
  MissionStarted: 'mission.started',
  MissionCompleted: 'mission.completed',
  MissionEvidenceSubmitted: 'mission.evidence_submitted',
  MissionEvidenceReviewed: 'mission.evidence_reviewed',
  MissionFeedbackReceived: 'mission.feedback_received',

  // Evidence
  EvidenceSubmitted: 'evidence.submitted',
  EvidenceAccepted: 'evidence.accepted',
  EvidenceRejected: 'evidence.rejected',

  // Assessment
  AssessmentStarted: 'assessment.started',
  AssessmentCompleted: 'assessment.completed',
  AssessmentScored: 'assessment.scored',

  // Competency
  CompetencyUnlocked: 'competency.unlocked',
  CompetencyLeveledUp: 'competency.leveled_up',
  CompetencyEvidenceLinked: 'competency.evidence_linked',

  // Achievement
  AchievementGranted: 'achievement.granted',
  CertificateIssued: 'certificate.issued',

  // Infrastructure
  SDKInitialized: 'sdk.initialized',
  SDKShutdown: 'sdk.shutdown',
  SDKTransportChanged: 'sdk.transport_changed',
  SDKTransportFailed: 'sdk.transport_failed',
  RuntimeStarted: 'runtime.started',
  RuntimeStopped: 'runtime.stopped',
  RuntimeError: 'runtime.error',
} as const

export type DomainEventType = (typeof DomainEventTypes)[keyof typeof DomainEventTypes]

export interface BuilderCreatedPayload {
  builderId: BuilderId
  name: string
  joinedAt: string
  initialLevel: number
}

export interface BuilderUpdatedPayload {
  builderId: BuilderId
  changedFields: string[]
}

export interface BuilderDeletedPayload {
  builderId: BuilderId
  deletedAt: string
}

export interface BuilderLeveledUpPayload {
  builderId: BuilderId
  previousLevel: number
  newLevel: number
  xpAtLevel: number
  unlockedAchievements: string[]
}

export interface BuilderStreakUpdatedPayload {
  builderId: BuilderId
  currentStreak: number
  longestStreak: number
  lastActivity: string
}

export interface BuilderPreferencesChangedPayload {
  builderId: BuilderId
  changedFields: string[]
}

export interface JourneyStartedPayload {
  journeyId: JourneyId
  builderId: BuilderId
  startedAt: string
  prerequisites: string[]
}

export interface JourneyCompletedPayload {
  journeyId: JourneyId
  builderId: BuilderId
  completedAt: string
  xpEarned: number
  competenciesAdvanced: Array<{ competencyId: CompetencyId; name: string; level: number }>
  certificateId?: CertificateId
}

export interface JourneyAbandonedPayload {
  journeyId: JourneyId
  builderId: BuilderId
  abandonedAt: string
  progress: number
}

export interface JourneyProgressUpdatedPayload {
  journeyId: JourneyId
  builderId: BuilderId
  percentComplete: number
  missionsCompleted: number
  xpEarned: number
}

export interface MissionStartedPayload {
  missionId: MissionId
  builderId: BuilderId
  journeyId?: JourneyId
  startedAt: string
}

export interface MissionCompletedPayload {
  missionId: MissionId
  builderId: BuilderId
  journeyId?: JourneyId
  completedAt: string
  xpEarned: number
  evidenceCount: number
  feedbackCount: number
}

export interface MissionEvidenceSubmittedPayload {
  missionId: MissionId
  builderId: BuilderId
  evidenceId: EvidenceId
  type: string
  submittedAt: string
}

export interface MissionEvidenceReviewedPayload {
  evidenceId: EvidenceId
  missionId: MissionId
  builderId: BuilderId
  status: 'accepted' | 'rejected'
  reviewedAt: string
}

export interface MissionFeedbackReceivedPayload {
  evidenceId: EvidenceId
  missionId: MissionId
  message: string
  rating?: number
}

export interface EvidenceSubmittedPayload {
  evidenceId: EvidenceId
  missionId: MissionId
  builderId: BuilderId
  type: string
  content: string
  submittedAt: string
}

export interface EvidenceAcceptedPayload {
  evidenceId: EvidenceId
  missionId: MissionId
  builderId: BuilderId
  acceptedAt: string
}

export interface EvidenceRejectedPayload {
  evidenceId: EvidenceId
  missionId: MissionId
  builderId: BuilderId
  reason: string
  rejectedAt: string
}

export interface AssessmentStartedPayload {
  assessmentId: AssessmentId
  builderId: BuilderId
  startedAt: string
}

export interface AssessmentCompletedPayload {
  assessmentId: AssessmentId
  builderId: BuilderId
  score: number
  total: number
  passed: boolean
  completedAt: string
}

export interface AssessmentScoredPayload {
  assessmentId: AssessmentId
  builderId: BuilderId
  score: number
  total: number
  passed: boolean
  breakdown?: Record<string, number>
}

export interface CompetencyUnlockedPayload {
  competencyId: CompetencyId
  builderId: BuilderId
  name: string
  level: number
  unlockedAt: string
  evidenceIds: string[]
}

export interface CompetencyLeveledUpPayload {
  competencyId: CompetencyId
  builderId: BuilderId
  previousLevel: number
  newLevel: number
  name: string
}

export interface CompetencyEvidenceLinkedPayload {
  competencyId: CompetencyId
  builderId: BuilderId
  evidenceId: EvidenceId
}

export interface AchievementGrantedPayload {
  achievementId: AchievementId
  builderId: BuilderId
  name: string
  category: string
  rarity: string
  grantedAt: string
}

export interface CertificateIssuedPayload {
  certificateId: CertificateId
  builderId: BuilderId
  title: string
  issuedAt: string
  expiresAt?: string
}

export interface RuntimeErrorPayload {
  code: string
  message: string
  recoverable: boolean
  timestamp: string
}

export interface SDKTransportChangedPayload {
  from: string
  to: string
  timestamp: string
}
