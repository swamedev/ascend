'use client'

import { cn } from '@/lib/utils'

interface DividerProps {
  orientation?: 'horizontal' | 'vertical'
  label?: string
  className?: string
}

export function Divider({ orientation = 'horizontal', label, className }: DividerProps) {
  if (orientation === 'vertical') {
    return (
      <div
        className={cn('mx-2 h-full w-px bg-border', className)}
        role="separator"
        aria-orientation="vertical"
      />
    )
  }

  if (label) {
    return (
      <div className={cn('flex items-center gap-3', className)} role="separator" aria-orientation="horizontal">
        <div className="flex-1 border-t border-border" />
        <span className="text-xs text-muted-foreground">{label}</span>
        <div className="flex-1 border-t border-border" />
      </div>
    )
  }

  return (
    <div className={cn('my-2 border-t border-border', className)} role="separator" aria-orientation="horizontal" />
  )
}
