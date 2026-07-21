'use client'

import { cn } from '@/lib/utils'
import { Badge } from '@/components/ui'
import type { ReactNode } from 'react'

interface CompetencyBadgeProps {
  name: string
  score?: number
  maxScore?: number
  icon?: ReactNode
  size?: 'sm' | 'md'
  className?: string
}

export function CompetencyBadge({ name, score, maxScore = 10, icon, size = 'md', className }: CompetencyBadgeProps) {
  const percent = score !== undefined ? Math.round((score / maxScore) * 100) : undefined

  return (
    <div className={cn('inline-flex items-center gap-2', className)}>
      {icon && <span className="text-muted-foreground">{icon}</span>}
      <Badge variant="primary" size={size}>
        {name}
      </Badge>
      {percent !== undefined && (
        <span className="text-xs font-medium text-muted-foreground">
          {percent}%
        </span>
      )}
    </div>
  )
}
