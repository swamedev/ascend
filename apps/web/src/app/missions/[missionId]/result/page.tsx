'use client'

import { useEffect } from 'react'
import React from 'react'
import { useRouter } from 'next/navigation'
import { Trophy, Award, Star, Zap, CheckCircle, ArrowRight, Home } from 'lucide-react'
import { motion } from 'framer-motion'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { AscensionRing } from '@/components/shared/ascension-ring'
import { XPBar } from '@/components/shared/xp-bar'
import { LevelBadge } from '@/components/shared/level-badge'
import { AchievementBadge } from '@/components/shared/achievement-badge'
import { useResultStore, useAuthStore } from '@/store'
import { useAuthGuard } from '@/hooks/use-auth-guard'

const PASS_THRESHOLD = 60
const MAX_SCORE = 100

const fadeIn = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
}

const stagger = {
  animate: { transition: { staggerChildren: 0.1 } },
}

export default function MissionResultPage({ params }: { params: Promise<{ missionId: string }> }) {
  const { missionId } = React.use(params)
  const router = useRouter()
  const isAuthenticated = useAuthGuard()
  const { result, clearResult } = useResultStore()
  const { builderId } = useAuthStore()

  useEffect(() => {
    if (!result || result.missionId !== missionId) {
      router.replace('/dashboard')
    }
  }, [result, missionId, router])

  if (!isAuthenticated) return null
  if (!result || result.missionId !== missionId) {
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

  const scorePercent = MAX_SCORE > 0 ? Math.round((result.score / MAX_SCORE) * 100) : 0
  const passed = result.score >= PASS_THRESHOLD

  return (
    <main className="min-h-screen bg-gradient-to-b from-background via-background to-[hsl(var(--primary)/0.03)]">
      <div className="mx-auto max-w-2xl px-4 py-12 sm:px-6 sm:py-16">
        <motion.div
          className="space-y-8"
          initial="initial"
          animate="animate"
          variants={stagger}
        >
          {/* Hero Section */}
          <motion.div variants={fadeIn} className="text-center space-y-4">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200, damping: 15, delay: 0.2 }}
              className="flex justify-center"
            >
              <div className="inline-flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-yellow-400 to-amber-500 shadow-lg shadow-yellow-500/25">
                {passed ? (
                  <Trophy className="h-12 w-12 text-white" />
                ) : (
                  <Award className="h-12 w-12 text-white" />
                )}
              </div>
            </motion.div>

            <div className="space-y-2">
              <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                {passed ? 'Mission Complete!' : 'Assessment Complete'}
              </h1>
              <p className="text-lg text-muted-foreground">
                {passed
                  ? 'You have proven your competency. Well done, Builder.'
                  : 'Keep pushing forward. Every attempt is progress.'}
              </p>
            </div>
          </motion.div>

          {/* Score Card */}
          <motion.div variants={fadeIn}>
            <Card variant="elevated" className="overflow-hidden">
              <CardContent className="p-6 sm:p-8">
                <div className="flex flex-col items-center gap-4">
                  <AscensionRing
                    level={result.score}
                    progress={scorePercent}
                    size={120}
                    strokeWidth={8}
                    className="text-primary"
                  />
                  <div className="text-center">
                    <p className="text-4xl font-bold text-foreground">
                      {result.score}
                      <span className="text-xl text-muted-foreground">/100</span>
                    </p>
                    <p className="mt-1 text-sm text-muted-foreground">Assessment Score</p>
                  </div>
                  {passed && (
                    <div className="inline-flex items-center gap-1.5 rounded-full bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-500">
                      <CheckCircle className="h-4 w-4" />
                      Passed
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Rewards Section */}
          <motion.div variants={fadeIn}>
            <Card variant="elevated">
              <CardContent className="p-6 sm:p-8 space-y-6">
                <h2 className="text-lg font-semibold text-foreground">Rewards Earned</h2>

                {/* XP Earned */}
                <div className="rounded-lg bg-gradient-to-r from-purple-500/10 to-blue-500/10 p-4">
                  <div className="flex items-center gap-3">
                    <div className="inline-flex h-10 w-10 items-center justify-center rounded-full bg-purple-500/20">
                      <Zap className="h-5 w-5 text-purple-500" />
                    </div>
                    <div className="flex-1 space-y-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-foreground">XP Gained</p>
                        <motion.span
                          className="text-lg font-bold text-purple-500"
                          initial={{ opacity: 0 }}
                          animate={{ opacity: 1 }}
                          transition={{ delay: 0.8, duration: 0.5 }}
                        >
                          +{result.xpEarned?.toLocaleString() ?? '0'} XP
                        </motion.span>
                      </div>
                      <XPBar
                        current={result.totalXp}
                        max={result.xpToNextLevel > 0 ? result.xpToNextLevel : 100}
                        size="sm"
                        showValues
                      />
                    </div>
                  </div>
                </div>

                {/* Level Up */}
                {result.leveledUp && (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 1, type: 'spring', stiffness: 150 }}
                    className="rounded-lg bg-gradient-to-r from-amber-500/10 to-yellow-500/10 p-4"
                  >
                    <div className="flex items-center gap-3">
                      <LevelBadge level={result.level} size="lg" />
                      <div>
                        <p className="text-sm font-semibold text-foreground">Level Up!</p>
                        <p className="text-xs text-muted-foreground">
                          You have reached Level {result.level}
                        </p>
                      </div>
                      <motion.div
                        className="ml-auto"
                        animate={{ rotate: [0, -10, 10, -10, 0] }}
                        transition={{ delay: 1.5, duration: 0.5 }}
                      >
                        <Star className="h-6 w-6 text-amber-500" />
                      </motion.div>
                    </div>
                  </motion.div>
                )}

                {/* Competencies Unlocked */}
                {result.competenciesUnlocked.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Award className="h-4 w-4 text-primary" />
                      <p className="text-sm font-medium text-foreground">
                        Competencies Unlocked
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {result.competenciesUnlocked.map((name, i) => (
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

                {/* Achievements Earned */}
                {result.achievementsUnlocked.length > 0 && (
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <Trophy className="h-4 w-4 text-amber-500" />
                      <p className="text-sm font-medium text-foreground">
                        Achievements Earned
                      </p>
                    </div>
                    <div className="flex flex-wrap gap-3">
                      {result.achievementsUnlocked.map((name, i) => (
                        <motion.div
                          key={name}
                          initial={{ opacity: 0, y: 10 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.4 + i * 0.1 }}
                        >
                          <AchievementBadge
                            icon={<Trophy className="h-full w-full p-1" />}
                            label={name}
                            size="md"
                            unlocked
                          />
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          {/* Actions */}
          <motion.div variants={fadeIn} className="flex flex-col gap-3 sm:flex-row sm:justify-center">
            <Button
              variant="secondary"
              size="lg"
              icon={<Home className="h-5 w-5" />}
              onClick={() => {
                clearResult()
                router.push('/dashboard')
              }}
              className="w-full sm:w-auto"
            >
              Back to Dashboard
            </Button>
            <Button
              variant="primary"
              size="lg"
              icon={<ArrowRight className="h-5 w-5" />}
              onClick={() => {
                clearResult()
                router.push('/journeys')
              }}
              className="w-full sm:w-auto"
            >
              Continue Journey
            </Button>
          </motion.div>
        </motion.div>
      </div>
    </main>
  )
}
