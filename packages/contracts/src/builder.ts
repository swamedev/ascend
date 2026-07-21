import type { BuilderId } from './ids'
import type { SocialPlatform, Theme, FontSize, DigestFrequency, ProfileVisibility } from './enums'

export interface Builder {
  id: BuilderId
  profile: Profile
  preferences: Preferences
  identity: LearningIdentity
  ledger: AchievementLedger
  progress: BuilderProgress
  createdAt: string
  updatedAt: string
  deletedAt?: string
}

export interface Profile {
  name: string
  avatar?: string
  bio?: string
  email?: string
  socialLinks?: SocialLink[]
}

export interface SocialLink {
  platform: SocialPlatform
  url: string
}

export interface Preferences {
  theme: Theme
  language: string
  reducedMotion: boolean
  fontSize: FontSize
  notifications: NotificationPreferences
  privacy: PrivacySettings
}

export interface NotificationPreferences {
  email: boolean
  push: boolean
  digest: DigestFrequency
  mentions: boolean
  achievements: boolean
}

export interface PrivacySettings {
  profileVisibility: ProfileVisibility
  showXP: boolean
  showStreak: boolean
  showCompetencies: boolean
  showAchievements: boolean
}

export interface LearningIdentity {
  builderId: BuilderId
  competencies: CompetencyGraph
  evidence: EvidencePortfolio
  assessments: AssessmentHistory
  learningPath: LearningPath
  exportedAt?: string
}

export interface CompetencyGraph {
  nodes: CompetencyNode[]
  edges: CompetencyEdge[]
  lastUpdated: string
}

export interface CompetencyNode {
  id: string
  name: string
  category: string
  currentLevel: number
  maxLevel: number
  progress: number
  unlockedAt?: string
  evidenceIds: string[]
}

export interface CompetencyEdge {
  source: string
  target: string
  relationship: 'prerequisite' | 'extends' | 'alternative'
}

export interface EvidencePortfolio {
  totalCount: number
  acceptedCount: number
  pendingCount: number
  items: EvidenceSummary[]
}

export interface EvidenceSummary {
  id: string
  missionId: string
  type: string
  status: 'pending' | 'accepted' | 'rejected'
  submittedAt: string
  competencies: string[]
}

export interface AssessmentHistory {
  totalTaken: number
  passed: number
  failed: number
  averageScore: number
  recentResults: AssessmentResult[]
}

export interface AssessmentResult {
  assessmentId: string
  title: string
  score: number
  total: number
  passed: boolean
  completedAt: string
}

export interface LearningPath {
  completedJourneys: string[]
  inProgressJourneys: string[]
  availableJourneys: string[]
  suggestedNext: string[]
}

export interface AchievementLedger {
  builderId: BuilderId
  entries: LedgerEntry[]
  totalAchievements: number
  totalCertificates: number
  lastUpdated: string
}

export interface LedgerEntry {
  id: string
  type: 'achievement' | 'certificate' | 'badge' | 'milestone'
  ref: string
  title: string
  description: string
  grantedAt: string
  source: 'journey' | 'mission' | 'streak' | 'special'
  expiresAt?: string
  metadata?: Record<string, unknown>
  verifiable: boolean
}

export interface BuilderProgress {
  builderId: BuilderId
  level: number
  xp: XPMetrics
  streak: StreakMetrics
  timeline: TimelineEntry[]
  stats: BuilderStats
}

export interface XPMetrics {
  current: number
  total: number
  nextLevelAt: number
  history: XPEvent[]
}

export interface XPEvent {
  amount: number
  source: string
  description: string
  timestamp: string
}

export interface StreakMetrics {
  current: number
  longest: number
  lastActivity: string
  frozen: boolean
  freezeAvailable: number
}

export interface TimelineEntry {
  id: string
  type: string
  title: string
  description: string
  timestamp: string
  icon?: string
}

export interface BuilderStats {
  missionsCompleted: number
  evidenceSubmitted: number
  evidenceAccepted: number
  achievementsUnlocked: number
  competenciesUnlocked: number
  journeysCompleted: number
  assessmentsPassed: number
  activeDays: number
  joinDate: string
}
