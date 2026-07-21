'use client'

import { cn } from '@/lib/utils'

type MissionState = 'pending' | 'active' | 'completed' | 'failed' | 'locked'

interface MissionStatusProps {
  state: MissionState
  showLabel?: boolean
  size?: 'sm' | 'md'
  className?: string
}

const stateConfig: Record<MissionState, { dot: string; label: string }> = {
  pending: { dot: 'bg-warning', label: 'Pending' },
  active: { dot: 'bg-info', label: 'Active' },
  completed: { dot: 'bg-success', label: 'Completed' },
  failed: { dot: 'bg-destructive', label: 'Failed' },
  locked: { dot: 'bg-muted-foreground', label: 'Locked' },
}

const dotSizes = {
  sm: 'h-2 w-2',
  md: 'h-2.5 w-2.5',
}

export function MissionStatus({ state, showLabel = true, size = 'md', className }: MissionStatusProps) {
  const config = stateConfig[state]

  return (
    <span className={cn('inline-flex items-center gap-1.5', className)}>
      <span className={cn('rounded-full', dotSizes[size], config.dot)} />
      {showLabel && (
        <span className="text-xs font-medium text-muted-foreground">{config.label}</span>
      )}
    </span>
  )
}
