import type { AchievementId, CertificateId } from './ids'

export interface AchievementList {
  achievements: Achievement[]
  badges: Badge[]
  certificates: Certificate[]
  totalCount: number
}

export interface Achievement {
  id: AchievementId
  name: string
  description: string
  category: string
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary'
  icon?: string
  grantedAt?: string
  progress?: number
  maxProgress?: number
}

export interface Badge {
  id: AchievementId
  name: string
  description: string
  imageUrl?: string
  grantedAt?: string
}

export interface Certificate {
  id: CertificateId
  title: string
  description: string
  issuer: string
  issuedAt: string
  expiresAt?: string
  credentialUrl?: string
  verifiable: boolean
}
