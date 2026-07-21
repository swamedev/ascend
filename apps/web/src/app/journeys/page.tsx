'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation } from '@tanstack/react-query'
import { Map, Lock, CheckCircle, Play, ArrowLeft, Compass } from 'lucide-react'
import { cn } from '@/lib/utils'
import { api } from '@/lib/api'
import { useAuthStore } from '@/store/auth-store'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { EmptyState } from '@/components/ui/empty-state'
import { ErrorState } from '@/components/ui/state-components'
import { JourneyCard } from '@/components/shared/journey-card'

const missionIcon = {
  locked: Lock,
  available: Play,
  in_progress: Map,
  completed: CheckCircle,
} as const

const SKELETON_CARD_COUNT = 4

const missionColor: Record<string, string> = {
  locked: 'text-muted-foreground',
  available: 'text-blue-500',
  in_progress: 'text-amber-500',
  completed: 'text-green-500',
}

export default function JourneysPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()
  const [selectedId, setSelectedId] = useState<string | null>(null)

  useEffect(() => {
    if (!isAuthenticated) {
      router.replace('/auth')
    }
  }, [isAuthenticated, router])

  const seedMutation = useMutation({
    mutationFn: () => api.seedJourneys(),
  })

  useEffect(() => {
    if (!seedMutation.isSuccess && !seedMutation.isPending) {
      seedMutation.mutate()
    }
  }, [seedMutation])

  const {
    data: journeys,
    isLoading,
    error,
    refetch,
  } = useQuery({
    queryKey: ['journeys'],
    queryFn: () => api.getJourneys(),
    enabled: seedMutation.isSuccess,
  })

  const { data: selectedJourney } = useQuery({
    queryKey: ['journey', selectedId],
    queryFn: () => api.getJourney(selectedId!),
    enabled: !!selectedId,
  })

  const firstAvailable = selectedJourney?.missions?.find(
    (m: any) => m.status === 'available'
  )

  function handleStartMission(missionId: string) {
    router.push(`/missions/${missionId}`)
  }

  if (!isAuthenticated) return null

  if (isLoading) {
    return (
      <main className="container mx-auto max-w-4xl px-4 py-8">
        <div className="mb-8 space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {Array.from({ length: SKELETON_CARD_COUNT }).map((_, i) => (
            <Card key={i} variant="bordered" padding="md">
              <Skeleton className="mb-3 h-5 w-3/4" />
              <Skeleton className="mb-2 h-3 w-full" />
              <Skeleton className="mb-4 h-3 w-1/2" />
              <Skeleton className="h-2 w-full" />
            </Card>
          ))}
        </div>
      </main>
    )
  }

  if (error) {
    return (
      <main className="container mx-auto max-w-4xl px-4 py-8">
        <ErrorState
          title="Failed to load journeys"
          message={error instanceof Error ? error.message : 'An unexpected error occurred'}
          action={<Button onClick={() => refetch()}>Retry</Button>}
        />
      </main>
    )
  }

  if (selectedId && selectedJourney) {
    return (
      <main className="container mx-auto max-w-4xl px-4 py-8">
        <button
          onClick={() => setSelectedId(null)}
          className="mb-6 inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Journeys
        </button>

        <div className="mb-8">
          <h1 className="text-2xl font-bold">{selectedJourney.title}</h1>
          <p className="mt-1 text-muted-foreground">{selectedJourney.description}</p>
        </div>

        <div className="space-y-3">
          <h2 className="text-lg font-semibold">
            Missions
            {selectedJourney.missions && (
              <span className="ml-2 text-sm font-normal text-muted-foreground">
                ({selectedJourney.missions.length})
              </span>
            )}
          </h2>

          {(!selectedJourney.missions || selectedJourney.missions.length === 0) ? (
            <EmptyState
              icon={<Compass className="h-8 w-8" />}
              title="No missions yet"
              description="This journey has no missions defined."
            />
          ) : (
            <div className="space-y-3">
              {selectedJourney.missions.map((mission: any) => {
                const Icon = missionIcon[mission.status as keyof typeof missionIcon] ?? Play
                return (
                  <Card key={mission.id} variant="bordered" padding="md">
                    <div className="flex items-center justify-between gap-4">
                      <div className="flex items-center gap-3 min-w-0">
                        <Icon
                          className={cn(
                            'h-5 w-5 shrink-0',
                            missionColor[mission.status] ?? 'text-muted-foreground'
                          )}
                        />
                        <div className="min-w-0">
                          <p className="font-medium truncate">{mission.title}</p>
                          <div className="flex items-center gap-3 text-xs text-muted-foreground">
                            <span className="capitalize">
                              {mission.status?.replace(/_/g, ' ') ?? 'unknown'}
                            </span>
                            {mission.xpReward != null && (
                              <span>{mission.xpReward} XP</span>
                            )}
                          </div>
                        </div>
                      </div>
                      {mission.status === 'available' && (
                        <Button
                          size="sm"
                          onClick={() => handleStartMission(mission.id)}
                          className="shrink-0"
                        >
                          {mission.id === firstAvailable?.id ? 'Start Journey' : 'Start Mission'}
                        </Button>
                      )}
                    </div>
                  </Card>
                )
              })}
            </div>
          )}
        </div>

        {firstAvailable && (
          <div className="mt-8 flex justify-center">
            <Button
              size="lg"
              icon={<Play className="h-5 w-5" />}
              onClick={() => handleStartMission(firstAvailable.id)}
            >
              Start Journey
            </Button>
          </div>
        )}
      </main>
    )
  }

  if (!journeys || journeys.length === 0) {
    return (
      <main className="container mx-auto max-w-4xl px-4 py-8">
        <div className="mb-8 space-y-2">
          <h1 className="text-2xl font-bold">Journey Explorer</h1>
          <p className="text-muted-foreground">Choose your path and start building competencies</p>
        </div>
        <EmptyState
          icon={<Compass className="h-12 w-12" />}
          title="No journeys available"
          description="There are no journeys to explore right now. Check back later."
          action={<Button onClick={() => refetch()}>Refresh</Button>}
        />
      </main>
    )
  }

  return (
    <main className="container mx-auto max-w-4xl px-4 py-8">
      <div className="mb-8 space-y-2">
        <h1 className="text-2xl font-bold">Journey Explorer</h1>
        <p className="text-muted-foreground">Choose your path and start building competencies</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {journeys.map((journey: any) => (
          <button
            key={journey.id}
            onClick={() => setSelectedId(journey.id)}
            className="text-left w-full transition-transform hover:scale-[1.02] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 rounded-[var(--ascend-card-radius)]"
          >
            <JourneyCard
              title={journey.title}
              description={`${journey.missions?.length ?? 0} missions`}
              progress={journey.progress ?? 0}
              status={journey.status}
              icon={<Map className="h-5 w-5 text-primary" />}
              action={
                <Button size="sm" variant="ghost">
                  View
                </Button>
              }
            />
          </button>
        ))}
      </div>
    </main>
  )
}
