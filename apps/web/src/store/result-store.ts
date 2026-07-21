import { create } from 'zustand'

export interface MissionResult {
  missionId: string
  passed: boolean
  score: number
  xpEarned: number
  competenciesUnlocked: string[]
  achievementsUnlocked: string[]
  level: number
  leveledUp: boolean
  totalXp: number
  xpToNextLevel: number
}

interface ResultStore {
  result: MissionResult | null
  setResult: (result: MissionResult) => void
  clearResult: () => void
}

export const useResultStore = create<ResultStore>((set) => ({
  result: null,
  setResult: (result) => set({ result }),
  clearResult: () => set({ result: null }),
}))
