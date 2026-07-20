'use client'

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import {
  type Transition,
  type Spring,
  type Variants,
} from 'framer-motion'

export type MotionSpeed = 'instant' | 'fast' | 'normal' | 'slow' | 'hero'

interface MotionContextValue {
  speed: MotionSpeed
  reducedMotion: boolean
  pageTransition: Transition
  modalTransition: Transition
  springPreset: Spring
  variants: {
    fadeIn: Variants
    slideUp: Variants
    slideDown: Variants
    scaleIn: Variants
    shimmer: Variants
  }
}

function getDuration(speed: MotionSpeed, reduced: boolean): number {
  if (reduced) return 0
  const map: Record<MotionSpeed, number> = {
    instant: 0,
    fast: 0.1,
    normal: 0.2,
    slow: 0.3,
    hero: 0.5,
  }
  return map[speed]
}

function createMotionContext(speed: MotionSpeed, reducedMotion: boolean): MotionContextValue {
  const dur = getDuration(speed, reducedMotion)

  return {
    speed,
    reducedMotion,
    pageTransition: {
      duration: dur,
      ease: [0, 0, 0.2, 1],
    },
    modalTransition: {
      duration: Math.max(dur, 0.15),
      ease: [0.34, 1.56, 0.64, 1],
    },
    springPreset: {
      type: 'spring',
      stiffness: 400,
      damping: 30,
    },
    variants: {
      fadeIn: {
        initial: { opacity: 0 },
        animate: { opacity: 1, transition: { duration: dur, ease: [0, 0, 0.2, 1] } },
        exit: { opacity: 0, transition: { duration: dur * 0.5, ease: [0.4, 0, 1, 1] } },
      },
      slideUp: {
        initial: { opacity: 0, y: 10 },
        animate: { opacity: 1, y: 0, transition: { duration: dur, ease: [0, 0, 0.2, 1] } },
        exit: { opacity: 0, y: -10, transition: { duration: dur * 0.5, ease: [0.4, 0, 1, 1] } },
      },
      slideDown: {
        initial: { opacity: 0, y: -10 },
        animate: { opacity: 1, y: 0, transition: { duration: dur, ease: [0, 0, 0.2, 1] } },
        exit: { opacity: 0, y: 10, transition: { duration: dur * 0.5, ease: [0.4, 0, 1, 1] } },
      },
      scaleIn: {
        initial: { opacity: 0, scale: 0.95 },
        animate: { opacity: 1, scale: 1, transition: { duration: dur, ease: [0, 0, 0.2, 1] } },
        exit: { opacity: 0, scale: 0.95, transition: { duration: dur * 0.5, ease: [0.4, 0, 1, 1] } },
      },
      shimmer: {
        initial: { backgroundPosition: '-200% 0' },
        animate: {
          backgroundPosition: '200% 0',
          transition: { duration: 1.5, repeat: Infinity, ease: 'linear' },
        },
      },
    },
  }
}

const MotionContext = createContext<MotionContextValue | null>(null)

export function useMotion(): MotionContextValue {
  const ctx = useContext(MotionContext)
  if (!ctx) {
    return createMotionContext('normal', false)
  }
  return ctx
}

interface MotionProviderProps {
  children: ReactNode
  speed?: MotionSpeed
}

export function MotionProvider({ children, speed = 'normal' }: MotionProviderProps) {
  const [reducedMotion, setReducedMotion] = useState(false)

  useEffect(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
    setReducedMotion(mq.matches)
    const handler = (e: MediaQueryListEvent) => setReducedMotion(e.matches)
    mq.addEventListener('change', handler)
    return () => mq.removeEventListener('change', handler)
  }, [])

  const value = createMotionContext(speed, reducedMotion)

  return (
    <MotionContext.Provider value={value}>
      {children}
    </MotionContext.Provider>
  )
}
