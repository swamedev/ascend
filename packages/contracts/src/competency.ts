import type { CompetencyId } from './ids'

export interface CompetencySummary {
  id: CompetencyId
  name: string
  category: string
  level: number
  maxLevel: number
  progress: number
  status: 'locked' | 'available' | 'in_progress' | 'completed'
}

export interface CompetencyDetail {
  id: CompetencyId
  name: string
  category: string
  description: string
  level: number
  maxLevel: number
  progress: number
  status: 'locked' | 'available' | 'in_progress' | 'completed'
  prerequisites: CompetencyId[]
  unlockedAt?: string
  evidenceIds: string[]
  children: CompetencyId[]
}
