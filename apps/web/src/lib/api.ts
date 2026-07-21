interface BuilderData { id: string; name: string; username: string; level: number; xp: number; maxXp: number; progress?: { stats?: Record<string, number> } }
interface JourneyData { id: string; title: string; description: string; missionCount: number; missions?: MissionData[]; status?: string }
interface MissionData { id: string; title: string; description: string; objective: string; instructions: string; xpReward: number; status: string; prerequisites?: string[] }
interface EvidenceData { id: string; content: string; status: string; submittedAt: string }
interface CompetencyData { id: string; name: string; score: number; maxScore: number }
interface AchievementData { id: string; name: string; label: string; description: string; unlocked: boolean; unlockedAt?: string }
interface BuilderCreateResponse { builder: BuilderData; token: string }
interface MissionResultData { missionId: string; passed: boolean; score: number; xpEarned: number; competenciesUnlocked: string[]; achievementsUnlocked: string[]; level: number; leveledUp: boolean; totalXp: number; xpToNextLevel: number }
interface PaginatedResponse<T> { data: T[]; total: number; limit: number; offset: number }
interface DemoStartResponse { demoId: string; builderId: string; journey: JourneyData }

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options,
  })
  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: { message: res.statusText } }))
    throw new Error(error?.error?.message || res.statusText)
  }
  if (res.status === 204) return undefined as T
  return res.json()
}

export const api = {
  login: (username: string) =>
    request<BuilderCreateResponse>('/auth/login', {
      method: 'POST', body: JSON.stringify({ username })
    }),

  getBuilder: (id: string) => request<BuilderData>(`/builders/${id}`),
  updateBuilder: (id: string, data: Partial<BuilderData>) =>
    request<BuilderData>(`/builders/${id}`, { method: 'PATCH', body: JSON.stringify(data) }),

  seedJourneys: () => request<JourneyData[]>('/journeys/seed', { method: 'POST' }),
  getJourneys: () => request<JourneyData[]>('/journeys'),
  getJourney: (id: string) => request<JourneyData>(`/journeys/${id}`),

  getMission: (id: string) => request<MissionData>(`/missions/${id}`),

  startMission: (missionId: string, builderId: string) =>
    request<{ status: string }>(`/missions/${missionId}/start`, {
      method: 'POST', body: JSON.stringify({ builderId })
    }),
  submitEvidence: (missionId: string, builderId: string, artifact: string, type?: string) =>
    request<EvidenceData>(`/missions/${missionId}/evidence`, {
      method: 'POST', body: JSON.stringify({ builderId, artifact, type: type || 'document' })
    }),
  completeMission: (missionId: string, builderId: string) =>
    request<MissionResultData>(`/missions/${missionId}/complete`, {
      method: 'POST', body: JSON.stringify({ builderId })
    }),

  startDemo: () => request<DemoStartResponse>('/demo/start', { method: 'POST' }),

  getCompetencies: (builderId: string) => request<CompetencyData[]>(`/builders/${builderId}/competencies`),

  getAchievements: (builderId: string) => request<AchievementData[]>(`/builders/${builderId}/achievements`),

  getCognitiveObservations: (builderId: string, limit = 50) =>
    request<PaginatedResponse<any>>(`/cognitive/observations?builder_id=${builderId}&limit=${limit}`),

  getCognitiveSignals: (builderId: string, signalType?: string, limit = 50) => {
    let path = `/cognitive/signals?builder_id=${builderId}&limit=${limit}`
    if (signalType) path += `&signal_type=${signalType}`
    return request<PaginatedResponse<any>>(path)
  },

  getCognitivePatterns: (builderId: string, patternType?: string, limit = 50) => {
    let path = `/cognitive/patterns?builder_id=${builderId}&limit=${limit}`
    if (patternType) path += `&pattern_type=${patternType}`
    return request<PaginatedResponse<any>>(path)
  },

  getCognitiveInsights: (builderId: string, insightType?: string, limit = 50) => {
    let path = `/cognitive/insights?builder_id=${builderId}&limit=${limit}`
    if (insightType) path += `&insight_type=${insightType}`
    return request<PaginatedResponse<any>>(path)
  },

  getCognitiveRecommendations: (builderId: string, recType?: string, limit = 50) => {
    let path = `/cognitive/recommendations?builder_id=${builderId}&limit=${limit}`
    if (recType) path += `&recommendation_type=${recType}`
    return request<PaginatedResponse<any>>(path)
  },

  getCognitiveTimeline: (builderId: string, startDate?: string, endDate?: string) => {
    let path = `/cognitive/timeline?builder_id=${builderId}`
    if (startDate) path += `&start_date=${startDate}`
    if (endDate) path += `&end_date=${endDate}`
    return request<any>(path)
  },
}
