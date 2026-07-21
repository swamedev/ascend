import { create } from 'zustand'

export interface DemoState {
  isDemo: boolean
  demoId: string | null
  builderId: string | null
  currentJourney: any | null
  currentMission: any | null
  missionResult: any | null
  setDemoData: (data: { id: string; builderId: string; journey: any }) => void
  setCurrentMission: (mission: any) => void
  setMissionResult: (result: any) => void
  clearDemo: () => void
}

export const useDemoStore = create<DemoState>((set) => ({
  isDemo: false,
  demoId: null,
  builderId: null,
  currentJourney: null,
  currentMission: null,
  missionResult: null,
  setDemoData: (data) => set({ isDemo: true, demoId: data.id, builderId: data.builderId, currentJourney: data.journey }),
  setCurrentMission: (mission) => set({ currentMission: mission }),
  setMissionResult: (result) => set({ missionResult: result }),
  clearDemo: () => set({ isDemo: false, demoId: null, builderId: null, currentJourney: null, currentMission: null, missionResult: null }),
}))
