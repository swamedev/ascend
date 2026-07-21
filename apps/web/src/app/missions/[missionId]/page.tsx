'use client'

import React, { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Play, ArrowRight, CheckCircle, FileText, Zap } from 'lucide-react'
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { ErrorState, SuccessState } from '@/components/ui/state-components'
import { useAuthStore, useResultStore, useLayoutStore } from '@/store'
import { api } from '@/lib/api'
import { useAuthGuard } from '@/hooks/use-auth-guard'

type Phase = 'briefing' | 'focus' | 'submitted'

export default function MissionWorkspacePage({ params }: { params: Promise<{ missionId: string }> }) {
  const { missionId } = React.use(params)
  const router = useRouter()
  const queryClient = useQueryClient()
  const isAuthenticated = useAuthGuard()
  const { builderId } = useAuthStore()
  const { setFocusMode, setBreadcrumbs } = useLayoutStore()
  const [phase, setPhase] = useState<Phase>('briefing')
  const [evidence, setEvidence] = useState('')
  const [evidenceError, setEvidenceError] = useState<string | null>(null)

  React.useEffect(() => {
    setBreadcrumbs([
      { label: 'Journeys', href: '/journeys' },
      { label: 'Mission', href: `/missions/${missionId}` },
    ])
  }, [missionId, setBreadcrumbs])

  React.useEffect(() => {
    if (phase === 'focus' || phase === 'submitted') {
      setFocusMode(true)
    }
    return () => setFocusMode(false)
  }, [phase, setFocusMode])

  const {
    data: mission,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ['mission', missionId],
    queryFn: () => api.getMission(missionId),
    enabled: isAuthenticated,
  })

  const startMissionMutation = useMutation({
    mutationFn: () => api.startMission(missionId, builderId!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mission', missionId] })
      setPhase('focus')
    },
  })

  const submitEvidenceMutation = useMutation({
    mutationFn: () => api.submitEvidence(missionId, builderId!, evidence),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['mission', missionId] })
      setPhase('submitted')
      setEvidence('')
      setEvidenceError(null)
    },
    onError: (err) => {
      setEvidenceError(err instanceof Error ? err.message : 'Failed to submit evidence')
    },
  })

  const completeMissionMutation = useMutation({
    mutationFn: () => api.completeMission(missionId, builderId!),
    onSuccess: (result) => {
      useResultStore.getState().setResult(result)
      router.push(`/missions/${missionId}/result`)
    },
  })

  function handleStartMission() {
    if (!builderId) return
    startMissionMutation.mutate()
  }

  function handleSubmitEvidence() {
    if (!builderId || !evidence.trim()) return
    setEvidenceError(null)
    submitEvidenceMutation.mutate()
  }

  function handleCompleteMission() {
    if (!builderId) return
    completeMissionMutation.mutate()
  }

  if (!isAuthenticated) {
    return null
  }

  if (isLoading) {
    return (
      <div className="mx-auto max-w-3xl space-y-6 py-8">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-4 w-96" />
        <Card className="mt-6">
          <CardContent className="space-y-4">
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-20 w-full" />
            <Skeleton className="h-10 w-32" />
          </CardContent>
        </Card>
      </div>
    )
  }

  if (isError) {
    return (
      <div className="mx-auto max-w-3xl py-8">
        <ErrorState
          title="Failed to load mission"
          message={error instanceof Error ? error.message : 'Could not fetch mission details.'}
          action={
            <Button variant="secondary" onClick={() => refetch()}>
              Retry
            </Button>
          }
        />
      </div>
    )
  }

  if (phase === 'briefing') {
    return (
      <div className="mx-auto max-w-3xl py-8">
        <Card variant="elevated">
          <CardHeader
            title={mission?.title || `Mission ${missionId}`}
            description={mission?.objective || 'Complete the objectives below to earn your reward.'}
          />
          <CardContent className="space-y-6">
            <div className="rounded-lg bg-muted/50 p-4">
              <h4 className="mb-2 text-sm font-semibold text-muted-foreground">INSTRUCTIONS</h4>
              <p className="text-sm leading-relaxed">
                {mission?.instructions || 'Follow the briefing to complete this mission.'}
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Badge variant="xp" size="md" className="gap-1.5">
                <Zap className="h-3.5 w-3.5" />
                {mission?.xpReward ?? 0} XP
              </Badge>
              {mission?.prerequisites && mission.prerequisites.length > 0 && (
                <Badge variant="warning" size="sm">
                  {mission.prerequisites.length} prerequisite{mission.prerequisites.length > 1 ? 's' : ''}
                </Badge>
              )}
            </div>

            {mission?.prerequisites && mission.prerequisites.length > 0 && (
              <div>
                <h4 className="mb-2 text-sm font-semibold text-muted-foreground">PREREQUISITES</h4>
                <ul className="list-inside list-disc space-y-1 text-sm text-muted-foreground">
                  {mission.prerequisites.map((prereq: string, i: number) => (
                    <li key={i}>{prereq}</li>
                  ))}
                </ul>
              </div>
            )}
          </CardContent>
          <CardFooter>
            <Button
              onClick={handleStartMission}
              loading={startMissionMutation.isPending}
              disabled={startMissionMutation.isPending}
              icon={<Play className="h-4 w-4" />}
            >
              Start Mission
            </Button>
          </CardFooter>
        </Card>
      </div>
    )
  }

  if (phase === 'focus') {
    return (
      <div className="mx-auto flex min-h-[70vh] w-full max-w-3xl flex-col justify-center gap-6 py-8">
        <div className="space-y-1 text-center">
          <h2 className="text-xl font-semibold">{mission?.title || 'Mission'}</h2>
          <p className="text-sm text-muted-foreground">Submit your evidence to complete this mission.</p>
        </div>

        <Textarea
          placeholder="Paste or write your evidence here..."
          value={evidence}
          onChange={(e) => {
            setEvidence(e.target.value)
            if (evidenceError) setEvidenceError(null)
          }}
          className="min-h-[300px] resize-y text-base"
          disabled={submitEvidenceMutation.isPending}
        />

        {evidenceError && (
          <p className="text-center text-xs text-[var(--ascend-danger)]" role="alert">
            {evidenceError}
          </p>
        )}

        <div className="flex justify-center">
          <Button
            onClick={handleSubmitEvidence}
            loading={submitEvidenceMutation.isPending}
            disabled={!evidence.trim() || submitEvidenceMutation.isPending}
            size="lg"
            icon={<FileText className="h-4 w-4" />}
          >
            Submit Evidence
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-3xl py-8">
      <SuccessState
        title="Evidence Submitted"
        message="Your evidence has been recorded. Complete the mission to finalize your progress."
        action={
          <Button
            onClick={handleCompleteMission}
            loading={completeMissionMutation.isPending}
            disabled={completeMissionMutation.isPending}
            icon={<CheckCircle className="h-4 w-4" />}
          >
            Complete Mission
          </Button>
        }
      />
    </div>
  )
}
