'use client'

import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { Card, CardHeader, CardContent } from '@/components/ui'
import { ProgressIndicator } from './progress-indicator'
import { MissionStatus } from './mission-status'

interface JourneyCardProps {
  title: string
  description?: string
  progress: number
  status?: 'pending' | 'active' | 'completed' | 'failed' | 'locked'
  icon?: ReactNode
  action?: ReactNode
  children?: ReactNode
  className?: string
}

export function JourneyCard({
  title,
  description,
  progress,
  status,
  icon,
  action,
  children,
  className,
}: JourneyCardProps) {
  return (
    <Card variant="bordered" className={cn(className)}>
      <CardHeader
        title={title}
        description={description}
        action={action}
      />
      {icon && <div className="mb-2">{icon}</div>}
      <CardContent padding="none">
        <ProgressIndicator value={progress} size="sm" showLabel />
        {status && (
          <div className="mt-2">
            <MissionStatus state={status} />
          </div>
        )}
        {children}
      </CardContent>
    </Card>
  )
}
