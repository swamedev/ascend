'use client'

import { cn } from '@/lib/utils'

interface LevelBadgeProps {
  level: number
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const sizeStyles = {
  sm: 'h-6 w-6 text-xs',
  md: 'h-8 w-8 text-sm',
  lg: 'h-10 w-10 text-base',
}

export function LevelBadge({ level, size = 'md', className }: LevelBadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex items-center justify-center rounded-full bg-primary font-bold text-primary-foreground',
        sizeStyles[size],
        className
      )}
      title={`Level ${level}`}
    >
      {level}
    </span>
  )
}
