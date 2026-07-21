import type { AssessmentId, BuilderId } from './ids'

export interface AssessmentSummary {
  id: AssessmentId
  title: string
  description: string
  type: 'quiz' | 'challenge' | 'project' | 'peer_review'
  difficulty: number
  duration: number
  passingScore: number
  status: 'not_started' | 'in_progress' | 'passed' | 'failed'
  questionsCount?: number
  attemptsCount: number
  maxAttempts: number
}

export interface AssessmentDetail {
  id: AssessmentId
  title: string
  description: string
  type: 'quiz' | 'challenge' | 'project' | 'peer_review'
  difficulty: number
  duration: number
  passingScore: number
  maxAttempts: number
  instructions: string
  rubric?: Rubric
}

export interface AssessmentSession {
  assessmentId: AssessmentId
  builderId: BuilderId
  startedAt: string
  expiresAt: string
  answers?: Record<string, unknown>
  status: 'in_progress' | 'completed' | 'expired'
}

export interface AssessmentResult {
  assessmentId: AssessmentId
  builderId: BuilderId
  score: number
  total: number
  passed: boolean
  attemptsUsed: number
  completedAt: string
  breakdown?: Record<string, number>
}

export interface Rubric {
  criteria: RubricCriterion[]
  maxScore: number
  passingScore: number
}

export interface RubricCriterion {
  id: string
  name: string
  description: string
  maxScore: number
  weight: number
}
