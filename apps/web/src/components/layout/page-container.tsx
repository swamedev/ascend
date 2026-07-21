'use client'

import { type ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface PageContainerProps {
  children: ReactNode
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  padding?: 'sm' | 'md' | 'lg'
  className?: string
}

const maxWidthStyles = {
  sm: 'max-w-2xl',
  md: 'max-w-4xl',
  lg: 'max-w-6xl',
  xl: 'max-w-7xl',
  full: 'max-w-full',
}

const paddingStyles = {
  sm: 'p-3',
  md: 'p-4',
  lg: 'p-6',
}

export function PageContainer({ children, maxWidth = 'lg', padding = 'md', className }: PageContainerProps) {
  return (
    <div className={cn('mx-auto', maxWidthStyles[maxWidth], paddingStyles[padding], className)}>
      {children}
    </div>
  )
}
