'use client'

import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface AchievementBadgeProps {
  icon: ReactNode
  label: string
  unlocked?: boolean
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const sizeStyles = {
  sm: 'h-8 w-8',
  md: 'h-10 w-10',
  lg: 'h-14 w-14',
}

export function AchievementBadge({ icon, label, unlocked = true, size = 'md', className }: AchievementBadgeProps) {
  return (
    <div
      className={cn(
        'inline-flex flex-col items-center gap-1',
        !unlocked && 'opacity-40 grayscale',
        className
      )}
      title={label}
    >
      <div
        className={cn(
          'flex items-center justify-center rounded-full bg-accent text-accent-foreground',
          sizeStyles[size]
        )}
      >
        <span className={size === 'lg' ? 'h-6 w-6' : 'h-4 w-4'}>{icon}</span>
      </div>
      <span className="text-xs font-medium text-muted-foreground text-center max-w-20 truncate">
        {label}
      </span>
    </div>
  )
}
