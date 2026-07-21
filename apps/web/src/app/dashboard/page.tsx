'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useQuery } from '@tanstack/react-query'
import { Rocket, Target, Award, Zap, BookOpen, CheckCircle, Trophy } from 'lucide-react'
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
      </div>
    </main>
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
