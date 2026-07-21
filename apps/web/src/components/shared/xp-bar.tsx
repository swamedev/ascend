'use client'

import { cn } from '@/lib/utils'

interface XPBarProps {
  current: number
  max: number
  label?: string
  showValues?: boolean
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

const sizeStyles = {
  sm: 'h-1.5',
  md: 'h-2',
  lg: 'h-3',
}

export function XPBar({ current, max, label, showValues = true, size = 'md', className }: XPBarProps) {
  const percent = max > 0 ? Math.min(Math.round((current / max) * 100), 100) : 0

  return (
    <div className={cn('space-y-1', className)}>
      {(label || showValues) && (
        <div className="flex items-center justify-between">
          {label && <span className="text-xs font-medium text-muted-foreground">{label}</span>}
          {showValues && (
            <span className="text-xs text-muted-foreground">
              {current.toLocaleString()} / {max.toLocaleString()} XP
            </span>
          )}
        </div>
      )}
      <div className={cn('w-full overflow-hidden rounded-full bg-muted', sizeStyles[size])}>
        <div
          className={cn(
            'h-full rounded-full bg-gradient-to-r from-purple-500 to-blue-500 transition-all motion-reduce:transition-none duration-300',
            percent === 100 && 'from-green-500 to-emerald-500'
          )}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  )
}
