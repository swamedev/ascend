'use client'

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Play, FileText, CheckCircle, Zap, ArrowLeft } from 'lucide-react'
import { Card, CardHeader, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { ErrorState, SuccessState } from '@/components/ui/state-components'
import { useDemoStore } from '@/store'
import { api } from '@/lib/api'

type Phase = 'briefing' | 'focus' | 'submitted'

export default function DemoMissionPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: missionId } = React.use(params)
  const router = useRouter()
  const { builderId, setCurrentMission, setMissionResult, currentMission } = useDemoStore()
  const [phase, setPhase] = useState<Phase>('briefing')
  const [evidence, setEvidence] = useState('')
  const [evidenceError, setEvidenceError] = useState<string | null>(null)
  const [mission, setMission] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState<string | null>(null)
  const [starting, setStarting] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [completing, setCompleting] = useState(false)

  useEffect(() => {
    if (!builderId) {
      router.replace('/')
      return
    }
    async function load() {
      try {
        const data = await api.getMission(missionId)
        setMission(data)
      } catch (err) {
        setLoadError(err instanceof Error ? err.message : 'Falha ao carregar missão')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [missionId, builderId, router])

  if (!builderId) return null

  if (loading) {
    return (
      <div className="mx-auto max-w-3xl space-y-6 py-8 px-4">
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

  if (loadError) {
    return (
      <div className="mx-auto max-w-3xl py-8 px-4">
        <ErrorState
          title="Falha ao carregar missão"
          message={loadError}
          action={
            <Button variant="secondary" onClick={() => router.push('/demo/journey')}>
              Voltar para Jornada
            </Button>
          }
        />
      </div>
    )
  }

  async function handleStartMission() {
    if (!builderId) return
    setStarting(true)
    try {
      await api.startMission(missionId, builderId)
      setCurrentMission(mission)
      setPhase('focus')
    } catch (err) {
      setEvidenceError(err instanceof Error ? err.message : 'Erro ao iniciar missão')
    } finally {
      setStarting(false)
    }
  }

  async function handleSubmitEvidence() {
    if (!builderId || !evidence.trim()) return
    setSubmitting(true)
    setEvidenceError(null)
    try {
      await api.submitEvidence(missionId, builderId, evidence)
      setPhase('submitted')
      setEvidence('')
    } catch (err) {
      setEvidenceError(err instanceof Error ? err.message : 'Falha ao enviar evidência')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleCompleteMission() {
    if (!builderId) return
    setCompleting(true)
    try {
      const result = await api.completeMission(missionId, builderId)
      setMissionResult(result)
      router.push('/demo/result')
    } catch (err) {
      setEvidenceError(err instanceof Error ? err.message : 'Falha ao completar missão')
    } finally {
      setCompleting(false)
    }
  }

  if (phase === 'briefing') {
    return (
      <div className="mx-auto max-w-3xl py-8 px-4">
        <button
          onClick={() => router.push('/demo/journey')}
          className="mb-6 inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          Voltar
        </button>

        <Card variant="elevated">
          <CardHeader
            title={mission?.title || `Missão ${missionId}`}
            description={mission?.objective || 'Complete os objetivos abaixo para ganhar sua recompensa.'}
          />
          <CardContent className="space-y-6">
            <div className="rounded-lg bg-muted/50 p-4">
              <h4 className="mb-2 text-sm font-semibold text-muted-foreground">INSTRUÇÕES</h4>
              <p className="text-sm leading-relaxed">
                {mission?.instructions || 'Siga as instruções para completar esta missão.'}
              </p>
            </div>

            <div className="flex items-center gap-3">
              <Badge variant="xp" size="md" className="gap-1.5">
                <Zap className="h-3.5 w-3.5" />
                {mission?.xpReward ?? 0} XP
              </Badge>
              {mission?.prerequisites && mission.prerequisites.length > 0 && (
                <Badge variant="warning" size="sm">
                  {mission.prerequisites.length} pré-requisito{mission.prerequisites.length > 1 ? 's' : ''}
                </Badge>
              )}
            </div>

            {mission?.prerequisites && mission.prerequisites.length > 0 && (
              <div>
                <h4 className="mb-2 text-sm font-semibold text-muted-foreground">PRÉ-REQUISITOS</h4>
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
              loading={starting}
              disabled={starting}
              icon={<Play className="h-4 w-4" />}
            >
              Começar Missão
            </Button>
          </CardFooter>
        </Card>
      </div>
    )
  }

  if (phase === 'focus') {
    return (
      <div className="mx-auto flex min-h-[70vh] w-full max-w-3xl flex-col justify-center gap-6 py-8 px-4">
        <div className="space-y-1 text-center">
          <h2 className="text-xl font-semibold">{mission?.title || 'Missão'}</h2>
          <p className="text-sm text-muted-foreground">
            Escreva sua evidência para completar esta missão.
          </p>
        </div>

        <Textarea
          placeholder="Descreva sua evidência aqui..."
          value={evidence}
          onChange={(e) => {
            setEvidence(e.target.value)
            if (evidenceError) setEvidenceError(null)
          }}
          className="min-h-[300px] resize-y text-base"
          disabled={submitting}
        />

        {evidenceError && (
          <p className="text-center text-xs text-[var(--ascend-danger)]" role="alert">
            {evidenceError}
          </p>
        )}

        <div className="flex justify-center">
          <Button
            onClick={handleSubmitEvidence}
            loading={submitting}
            disabled={!evidence.trim() || submitting}
            size="lg"
            icon={<FileText className="h-4 w-4" />}
          >
            Enviar Evidência
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto max-w-3xl py-8 px-4">
      <SuccessState
        title="Evidência Enviada"
        message="Sua evidência foi registrada. Complete a missão para finalizar seu progresso."
        action={
          <Button
            onClick={handleCompleteMission}
            loading={completing}
            disabled={completing}
            icon={<CheckCircle className="h-4 w-4" />}
          >
            Completar Missão
          </Button>
        }
      />
    </div>
  )
}
