import type { ProfileVisibility, Theme, FontSize, DigestFrequency } from './enums'

export interface UserSettings {
  profile: {
    name: string
    avatar?: string
    bio?: string
    email?: string
  }
  notifications: {
    email: boolean
    push: boolean
    digest: DigestFrequency
    mentions: boolean
    achievements: boolean
  }
  privacy: {
    profileVisibility: ProfileVisibility
    showXP: boolean
    showStreak: boolean
    showCompetencies: boolean
    showAchievements: boolean
  }
}

export interface UserPreferences {
  theme: Theme
  language: string
  reducedMotion: boolean
  fontSize: FontSize
}
