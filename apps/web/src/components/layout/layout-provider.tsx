'use client'

import { type ReactNode } from 'react'
import { useBreakpointInit } from '@/hooks/use-breakpoint'
import { MotionProvider } from '@/components/motion'

interface LayoutProviderProps {
  children: ReactNode
}

export function LayoutProvider({ children }: LayoutProviderProps) {
  useBreakpointInit()

  return (
    <MotionProvider>
      {children}
    </MotionProvider>
  )
}
