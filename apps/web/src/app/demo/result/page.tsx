'use client'

import { useEffect } from 'react'
import React from 'react'
import { useRouter } from 'next/navigation'
import { Trophy, Zap, Award, CheckCircle, Home, ArrowRight } from 'lucide-react'
import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { XPBar } from '@/components/shared/xp-bar'
import { LevelBadge } from '@/components/shared/level-badge'
import { useDemoStore } from '@/store'

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
}

const stagger = {
  animate: { transition: { staggerChildren: 0.1 } },
}

export default function DemoResultPage() {
  const router = useRouter()
  const { missionResult, clearDemo } = useDemoStore()

  useEffect(() => {
    if (!missionResult) {
      router.replace('/')
    }
  }, [missionResult, router])

  if (!missionResult) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-background p-4">
        <Card variant="elevated" className="w-full max-w-lg">
          <CardContent className="flex flex-col items-center gap-6 py-12">
            <Skeleton variant="circular" width={80} height={80} />
            <Skeleton variant="text" width="60%" />
            <Skeleton variant="rectangular" width="80%" height={12} />
            <Skeleton variant="rectangular" width="40%" height={40} />
          </CardContent>
        </Card>
      </main>
    )
  }

  const passed = missionResult.passed ?? true
  const hasCompetencies = missionResult.competenciesUnlocked?.length > 0
  const hasAchievements = missionResult.achievementsUnlocked?.length > 0

  return (
    <main className="min-h-screen bg-gradient-to-b from-background via-background to-[hsl(var(--primary)/0.03)]">
      <div className="mx-auto max-w-2xl px-4 py-12 sm:px-6 sm:py-16">
        <motion.div
          className="space-y-8"
          initial="initial"
          animate="animate"
          variants={stagger}
        >
          <motion.div variants={fadeIn} className="text-center space-y-4">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 15, delay: 0.2 }}
              className="flex justify-center"
            >
              <div className="inline-flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-yellow-400 to-amber-500 shadow-lg shadow-yellow-500/25">
                <Trophy className="h-12 w-12 text-white" />
              </div>
            </motion.div>

            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                🎉 Missão Concluída!
              </h1>
              <p className="text-lg text-muted-foreground">
                {passed
                  ? 'Você comprovou sua competência. Parabéns, Builder!'
                  : 'Continue evoluindo. Cada tentativa é progresso.'}
              </p>
            </div>
          </motion.div>

          <motion.div variants={fadeIn}>
            <Card variant="elevated">
              <CardContent className="p-6 sm:p-8 space-y-6">
                <h2 className="text-lg font-semibold text-foreground">Recompensas</h2>

                <div className="rounded-lg bg-gradient-to-r from-purple-500/10 to-blue-500/10 p-4">
                  <div className="flex items-center gap-3">
                    <div className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-purple-500/20">
                      <Zap className="h-5 w-5 text-purple-500" />
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-foreground">XP Ganho</p>
                        <motion.span
                          className="text-lg font-bold text-purple-500"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.8, duration: 0.5 }}
                        >
                          +{missionResult.xpEarned?.toLocaleString() ?? '0'} XP
                        </motion.span>
                      </div>
                      <XPBar
                        current={missionResult.totalXp}
                        max={missionResult.xpToNextLevel > 0 ? missionResult.xpToNextLevel : 100}
                        size="sm"
                        showValues
                      />
                    </div>
                  </div>
                </div>

                {missionResult.leveledUp && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1, type: 'spring', stiffness: 150 }}
                    className="rounded-lg bg-gradient-to-r from-amber-500/10 to-yellow-500/10 p-4"
                  >
                    <div className="flex items-center gap-3">
                      <LevelBadge level={missionResult.level} size="lg" />
                      <div>
                        <p className="text-sm font-semibold text-foreground">Subiu de Nível!</p>
                        <p className="text-xs text-muted-foreground">
                          Você alcançou o Nível {missionResult.level}
                        </p>
                      </div>
                    </div>
                  </motion.div>
                )}

                {hasCompetencies && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Award className="h-4 w-4 text-primary" />
                      <p className="text-sm font-medium text-foreground">
                        Competências Desbloqueadas
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {missionResult.competenciesUnlocked.map((name: string, i: number) => (
                        <motion.span
                          key={name}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 0.3 + i * 0.1 }}
                          className="inline-flex items-center gap-1 rounded-full border border-primary/20 bg-primary/5 px-3 py-1 text-xs font-medium text-primary"
                        >
                          <CheckCircle className="h-3 w-3" />
                          {name}
                        </motion.span>
                      ))}
                    </div>
                  </div>
                )}

                {hasAchievements && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Trophy className="h-4 w-4 text-amber-500" />
                      <p className="text-sm font-medium text-foreground">
                        Conquistas Obtidas
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {missionResult.achievementsUnlocked.map((name: string, i: number) => (
                        <motion.span
                          key={name}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.4 + i * 0.1 }}
                          className="inline-flex items-center gap-1 rounded-full border border-amber-500/20 bg-amber-500/5 px-3 py-1 text-xs font-medium text-amber-600"
                        >
                          <Trophy className="h-3 w-3" />
                          {name}
                        </motion.span>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          <motion.div variants={fadeIn} className="flex flex-col gap-3 sm:flex-row sm:justify-center">
            <Button
              variant="primary"
              size="lg"
              icon={<ArrowRight className="h-5 w-5" />}
              onClick={() => router.push('/auth')}
              className="w-full sm:w-auto"
            >
              Criar Conta Gratuita
            </Button>
            <Button
              variant="secondary"
              size="lg"
              icon={<Home className="h-5 w-5" />}
              onClick={() => {
                clearDemo()
                router.push('/demo/journey')
              }}
              className="w-full sm:w-auto"
            >
              Continuar Explorando
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </main>
  )
}
