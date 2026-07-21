'use client'

import { cn } from '@/lib/utils'
import { FileText } from 'lucide-react'

interface EvidenceBadgeProps {
  count: number
  label?: string
  size?: 'sm' | 'md'
  className?: string
}

const sizeStyles = {
  sm: 'text-xs gap-1',
  md: 'text-sm gap-1.5',
}

export function EvidenceBadge({ count, label = 'evidence', size = 'sm', className }: EvidenceBadgeProps) {
  return (
    <span className={cn('inline-flex items-center text-muted-foreground', sizeStyles[size], className)}>
      <FileText className={size === 'sm' ? 'h-3 w-3' : 'h-3.5 w-3.5'} />
      <span>
        {count} {label}{count !== 1 ? 's' : ''}
      </span>
    </span>
  )
}
