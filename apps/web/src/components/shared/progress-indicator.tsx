'use client'

import { cn } from '@/lib/utils'

interface ProgressIndicatorProps {
  value: number
  max?: number
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  variant?: 'default' | 'xp' | 'success' | 'warning'
  className?: string
}

const sizeStyles = {
  sm: 'h-1.5',
  md: 'h-2',
  lg: 'h-3',
}

const variantStyles = {
  default: 'bg-primary',
  xp: 'bg-gradient-to-r from-purple-500 to-blue-500',
  success: 'bg-success',
  warning: 'bg-warning',
}

export function ProgressIndicator({
  value,
  max = 100,
  size = 'md',
  showLabel = false,
  variant = 'default',
  className,
}: ProgressIndicatorProps) {
  const percent = max > 0 ? Math.min(Math.round((value / max) * 100), 100) : 0

  return (
    <div className={cn('space-y-1', className)}>
      {showLabel && (
        <div className="flex justify-end">
          <span className="text-xs text-muted-foreground">{percent}%</span>
        </div>
      )}
      <div className={cn('w-full overflow-hidden rounded-full bg-muted', sizeStyles[size])}>
        <div
          className={cn(
            'h-full rounded-full transition-all motion-reduce:transition-none duration-300',
            variantStyles[variant]
          )}
          style={{ width: `${percent}%` }}
          role="progressbar"
          aria-valuenow={value}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
    </div>
  )
}
