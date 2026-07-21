'use client'

import { type ReactNode } from 'react'
import { cn } from '@/lib/utils'

interface WorkspaceProps {
  children: ReactNode
  className?: string
}

export function Workspace({ children, className }: WorkspaceProps) {
  return (
    <div className={cn('h-full overflow-auto', className)}>
      {children}
    </div>
  )
}
