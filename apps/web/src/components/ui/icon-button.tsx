'use client'

import { forwardRef } from 'react'
import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { Spinner } from './spinner'

type IconButtonSize = 'sm' | 'md' | 'lg'

interface IconButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  icon: ReactNode
  size?: IconButtonSize
  loading?: boolean
  label: string
}

const sizeStyles: Record<IconButtonSize, string> = {
  sm: 'h-8 w-8',
  md: 'h-9 w-9',
  lg: 'h-10 w-10',
}

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ icon, size = 'md', loading = false, label, className, ...props }, ref) => {
    return (
      <button
        ref={ref}
        aria-label={label}
        disabled={props.disabled || loading}
        className={cn(
          'inline-flex items-center justify-center rounded-md transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 hover:bg-accent active:bg-accent/80',
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {loading ? <Spinner size="sm" /> : <span className="h-4 w-4">{icon}</span>}
      </button>
    )
  }
)

IconButton.displayName = 'IconButton'
