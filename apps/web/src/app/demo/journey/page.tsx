'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Play, Clock, Compass, Home } from 'lucide-react'
import { Card, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { ErrorState } from '@/components/ui/state-components'
import { useDemoStore } from '@/store'
import { api } from '@/lib/api'

export default function DemoJourneyPage() {
  const router = useRouter()
  const { isDemo, currentJourney, builderId, setCurrentMission } = useDemoStore()
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!isDemo || !currentJourney) {
      router.replace('/')
    }
  }, [isDemo, currentJourney, router])

  if (!isDemo || !currentJourney) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background p-4">
        <Card variant="elevated" className="w-full max-w-md">
          <CardContent className="flex flex-col items-center gap-6 py-12">
            <Skeleton variant="circular" width={64} height={64} />
            <Skeleton variant="text" width="60%" />
            <Skeleton variant="rectangular" width="80%" height={40} />
          </CardContent>
        </Card>
      </main>
    )
  }

  const firstMission = currentJourney.missions?.[0]
  const missionCount = currentJourney.missionCount || currentJourney.missions?.length || 0

  async function handleStartFirstMission() {
    if (!firstMission || !builderId) return
    setStarting(true)
    setError(null)
    try {
      await api.startMission(firstMission.id, builderId)
      setCurrentMission(firstMission)
      router.push(`/demo/mission/${firstMission.id}`)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro ao iniciar missão')
    } finally {
      setStarting(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-background p-4">
      <Card variant="elevated" className="w-full max-w-lg">
        <CardContent className="flex flex-col items-center gap-6 pt-8 pb-6">
          <div className="inline-flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
            <Compass className="h-8 w-8 text-primary" />
          </div>

          <div className="text-center space-y-2">
            <h1 className="text-2xl font-bold text-foreground">{currentJourney.title}</h1>
            <p className="text-sm text-muted-foreground max-w-sm">
              {currentJourney.description}
            </p>
          </div>

          <div className="flex items-center gap-4">
            <Badge variant="info" size="md" className="gap-1.5">
              <Play className="h-3.5 w-3.5" />
              {missionCount} {missionCount === 1 ? 'missão' : 'missões'}
            </Badge>
            <Badge variant="default" size="md" className="gap-1.5">
              <Clock className="h-3.5 w-3.5" />
              ~20 minutos
            </Badge>
          </div>
        </CardContent>

        <CardFooter className="flex-col gap-3 pb-8">
          {error && (
            <p className="text-xs text-[var(--ascend-danger)]" role="alert">{error}</p>
          )}
          <Button
            size="lg"
            className="w-full"
            loading={starting}
            disabled={!firstMission || starting}
            onClick={handleStartFirstMission}
            icon={<Play className="h-5 w-5" />}
          >
            Começar Primeira Missão
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => router.push('/')}
            icon={<Home className="h-4 w-4" />}
          >
            Voltar ao início
          </Button>
        </CardFooter>
      </Card>
    </main>
  )
}
