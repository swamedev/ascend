'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useQuery } from '@tanstack/react-query'
import { Rocket, Target, Award, Zap, BookOpen, CheckCircle, Trophy, TrendingUp, TrendingDown, AlertTriangle, Lightbulb, BarChart3, Activity } from 'lucide-react'
import { cn } from '@/lib/utils'
import { api } from '@/lib/api'
import { useAuthStore } from '@/store/auth-store'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { Button } from '@/components/ui/button'
import { ErrorState, LoadingState } from '@/components/ui/state-components'
import { EmptyState } from '@/components/ui/empty-state'
import { LevelBadge } from '@/components/shared/level-badge'
import { XPBar } from '@/components/shared/xp-bar'
import { AscensionRing } from '@/components/shared/ascension-ring'
import { CompetencyBadge } from '@/components/shared/competency-badge'
import { AchievementBadge } from '@/components/shared/achievement-badge'

const SKELETON_STAT_COUNT = 4
const SKELETON_COMPETENCY_COUNT = 3
const TOP_COMPETENCIES = 3
const TOP_ACHIEVEMENTS = 4

export default function DashboardPage() {
  const router = useRouter()
  const { builderId, isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/auth')
    }
  }, [isAuthenticated, router])

  const builderQuery = useQuery({
    queryKey: ['builder', builderId],
    queryFn: () => api.getBuilder(builderId!),
    enabled: !!builderId,
  })

  const competenciesQuery = useQuery({
    queryKey: ['competencies', builderId],
    queryFn: () => api.getCompetencies(builderId!),
    enabled: !!builderId,
  })

  const achievementsQuery = useQuery({
    queryKey: ['achievements', builderId],
    queryFn: () => api.getAchievements(builderId!),
    enabled: !!builderId,
  })

  const patternsQuery = useQuery({
    queryKey: ['cognitive-patterns', builderId],
    queryFn: () => api.getCognitivePatterns(builderId!, undefined, 20),
    enabled: !!builderId,
  })

  const insightsQuery = useQuery({
    queryKey: ['cognitive-insights', builderId],
    queryFn: () => api.getCognitiveInsights(builderId!, undefined, 20),
    enabled: !!builderId,
  })

  const recommendationsQuery = useQuery({
    queryKey: ['cognitive-recommendations', builderId],
    queryFn: () => api.getCognitiveRecommendations(builderId!, undefined, 10),
    enabled: !!builderId,
  })

  const timelineQuery = useQuery({
    queryKey: ['cognitive-timeline', builderId],
    queryFn: () => api.getCognitiveTimeline(builderId!),
    enabled: !!builderId,
  })

  if (!isAuthenticated) return null

  const isLoading = builderQuery.isLoading || competenciesQuery.isLoading || achievementsQuery.isLoading
  const isError = builderQuery.isError || competenciesQuery.isError || achievementsQuery.isError

  if (isError) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background p-4">
        <ErrorState
          title="Could not load dashboard"
          message="An error occurred while loading your dashboard. Please try again."
          action={
            <Button
              variant="primary"
              onClick={() => {
                builderQuery.refetch()
                competenciesQuery.refetch()
                achievementsQuery.refetch()
              }}
            >
              Retry
            </Button>
          }
        />
      </main>
    )
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-background p-4 md:p-6 lg:p-8">
        <div className="mx-auto max-w-5xl space-y-8">
          <div className="flex items-center gap-6">
            <Skeleton variant="circular" width={80} height={80} />
            <div className="flex-1 space-y-3">
              <Skeleton variant="text" width="12rem" />
              <Skeleton variant="text" width="100%" />
            </div>
            <Skeleton variant="circular" width={80} height={80} />
          </div>

          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {Array.from({ length: SKELETON_STAT_COUNT }).map((_, i) => (
              <Card key={i} padding="md">
                <CardContent className="flex flex-col items-center gap-2 py-4 text-center">
                  <Skeleton variant="circular" width={32} height={32} />
                  <Skeleton variant="text" width="3rem" className="h-6" />
                  <Skeleton variant="text" width="5rem" />
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="space-y-4">
            <Skeleton variant="text" width="8rem" />
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              {Array.from({ length: SKELETON_COMPETENCY_COUNT }).map((_, i) => (
                <Card key={i} padding="md">
                  <CardContent className="space-y-2 py-4">
                    <Skeleton variant="text" width="60%" />
                    <Skeleton variant="text" width="40%" />
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </main>
    )
  }

  const builder = builderQuery.data
  const competencies = competenciesQuery.data ?? []
  const achievements = achievementsQuery.data ?? []

  const stats = builder?.progress?.stats ?? {}
  const level = builder?.level ?? 1
  const xp = builder?.xp ?? 0
  const maxXp = builder?.maxXp ?? 100

  const hasData = competencies.length > 0 || achievements.length > 0

  if (!hasData) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background p-4">
        <EmptyState
          icon={<Rocket className="h-12 w-12" />}
          title="Welcome to ASCEND"
          description="You're all set. Start your first journey to begin building competencies and earning achievements."
          action={
            <Link href="/journeys">
              <Button variant="primary" icon={<Rocket className="h-4 w-4" />}>
                Start Your First Journey
              </Button>
            </Link>
          }
        />
      </main>
    )
  }

  const topCompetencies = competencies.slice(0, TOP_COMPETENCIES)
  const topAchievements = achievements.slice(0, TOP_ACHIEVEMENTS)

  return (
    <main className="min-h-screen bg-background p-4 md:p-6 lg:p-8">
      <div className="mx-auto max-w-5xl space-y-8">
        <section className="flex items-center gap-6">
          <LevelBadge level={level} size="lg" />
          <div className="flex-1 space-y-2">
            <h1 className="text-xl font-bold">{builder?.name ?? 'Builder'}</h1>
            <XPBar current={xp} max={maxXp} label="Experience" size="md" />
          </div>
          <AscensionRing level={level} progress={maxXp > 0 ? Math.round((xp / maxXp) * 100) : 0} size={80} />
        </section>

        <section className="space-y-4">
          <h2 className="text-lg font-semibold">Quick Stats</h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            <StatCard icon={<Rocket className="h-5 w-5" />} label="Missions Completed" value={stats.missionsCompleted ?? 0} />
            <StatCard icon={<CheckCircle className="h-5 w-5" />} label="Evidence Accepted" value={stats.evidenceAccepted ?? 0} />
            <StatCard icon={<Award className="h-5 w-5" />} label="Competencies Unlocked" value={stats.competenciesUnlocked ?? 0} />
            <StatCard icon={<Trophy className="h-5 w-5" />} label="Achievements Earned" value={stats.achievementsEarned ?? 0} />
          </div>
        </section>

        <section className="space-y-4">
          <h2 className="text-lg font-semibold">Recent</h2>
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            {topCompetencies.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-muted-foreground">Competencies</h3>
                <div className="flex flex-wrap gap-2">
                  {topCompetencies.map((comp: any) => (
                    <CompetencyBadge
                      key={comp.id ?? comp.name}
                      name={comp.name}
                      score={comp.score}
                      maxScore={comp.maxScore}
                      size="md"
                    />
                  ))}
                </div>
              </div>
            )}
            {topAchievements.length > 0 && (
              <div className="space-y-3">
                <h3 className="text-sm font-medium text-muted-foreground">Achievements</h3>
                <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                  {topAchievements.map((ach: any) => (
                    <AchievementBadge
                      key={ach.id ?? ach.label}
                      icon={<Trophy className="h-5 w-5" />}
                      label={ach.label}
                      unlocked={ach.unlocked !== false}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>

        {insightsQuery.data?.data?.length > 0 && (
          <section className="space-y-4">
            <h2 className="text-lg font-semibold">Learning Trends</h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
              {insightsQuery.data.data.slice(0, 4).map((insight: any) => (
                <Card key={insight.id} variant="bordered" padding="md">
                  <CardContent className="space-y-2">
                    <div className="flex items-center gap-2">
                      <SeverityIcon severity={insight.severity} />
                      <span className="font-medium text-sm">{insight.title}</span>
                    </div>
                    <p className="text-xs text-muted-foreground">{insight.description}</p>
                    <div className="flex items-center gap-3 text-xs">
                      <span className={cn(
                        'px-1.5 py-0.5 rounded',
                        insight.severity === 'critical' && 'bg-red-100 text-red-700',
                        insight.severity === 'warning' && 'bg-yellow-100 text-yellow-700',
                        insight.severity === 'info' && 'bg-blue-100 text-blue-700',
                      )}>
                        {insight.severity}
                      </span>
                      <span>{(insight.confidence * 100).toFixed(0)}% confidence</span>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        )}

        {patternsQuery.data?.data?.length > 0 && (
          <section className="space-y-4">
            <h2 className="text-lg font-semibold">Consistency & Evolution</h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
              {patternsQuery.data.data.slice(0, 6).map((pattern: any) => (
                <Card key={pattern.id} variant="bordered" padding="sm">
                  <CardContent className="flex items-center gap-3 py-3">
                    <PatternIcon patternType={pattern.pattern_type} />
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium truncate">{pattern.label}</p>
                      <p className="text-[10px] text-muted-foreground">
                        value: {pattern.value} | confidence: {(pattern.confidence * 100).toFixed(0)}%
                      </p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        )}

        {recommendationsQuery.data?.data?.length > 0 && (
          <section className="space-y-4">
            <h2 className="text-lg font-semibold">Recommendations</h2>
            <div className="grid grid-cols-1 gap-3">
              {recommendationsQuery.data.data.slice(0, 5).map((rec: any) => (
                <Card key={rec.id} variant="bordered" padding="md">
                  <CardContent className="flex items-start gap-3">
                    <Lightbulb className="h-5 w-5 text-primary shrink-0 mt-0.5" />
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-sm">{rec.title}</span>
                        <PriorityBadge priority={rec.priority} />
                      </div>
                      <p className="text-xs text-muted-foreground mt-1">{rec.description}</p>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        )}
      </div>
    </main>
  )
}

function SeverityIcon({ severity }: { severity: string }) {
  if (severity === 'critical') return <AlertTriangle className="h-4 w-4 text-red-500" />
  if (severity === 'warning') return <AlertTriangle className="h-4 w-4 text-yellow-500" />
  return <Lightbulb className="h-4 w-4 text-blue-500" />
}

function PatternIcon({ patternType }: { patternType: string }) {
  if (patternType === 'trend_up') return <TrendingUp className="h-4 w-4 text-green-500" />
  if (patternType === 'trend_down') return <TrendingDown className="h-4 w-4 text-red-500" />
  if (patternType === 'spike') return <Activity className="h-4 w-4 text-orange-500" />
  if (patternType === 'consistency_score') return <BarChart3 className="h-4 w-4 text-blue-500" />
  if (patternType === 'stagnation') return <AlertTriangle className="h-4 w-4 text-yellow-500" />
  return <Activity className="h-4 w-4 text-muted-foreground" />
}

function PriorityBadge({ priority }: { priority: string }) {
  const colors: Record<string, string> = {
    critical: 'bg-red-100 text-red-700',
    high: 'bg-orange-100 text-orange-700',
    medium: 'bg-blue-100 text-blue-700',
    low: 'bg-gray-100 text-gray-600',
  }
  return (
    <span className={cn('px-1.5 py-0.5 rounded text-[10px] font-medium', colors[priority] || colors.low)}>
      {priority}
    </span>
  )
}

function StatCard({ icon, label, value }: { icon: React.ReactNode; label: string; value: number }) {
  return (
    <Card variant="bordered" padding="md">
      <CardContent className="flex flex-col items-center gap-2 py-4 text-center">
        <div className="text-primary">{icon}</div>
        <span className="text-2xl font-bold">{value}</span>
        <span className="text-xs text-muted-foreground">{label}</span>
      </CardContent>
    </Card>
  )
}
