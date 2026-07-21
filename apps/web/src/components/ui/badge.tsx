'use client'

import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { cva, type VariantProps } from 'class-variance-authority'

const badgeVariants = cva('inline-flex items-center gap-1 rounded-[var(--ascend-badge-radius)] font-medium', {
  variants: {
    variant: {
      default: 'bg-muted text-muted-foreground',
      primary: 'bg-primary text-primary-foreground',
      success: 'bg-[var(--ascend-success-bg)] text-[var(--ascend-success)]',
      warning: 'bg-[var(--ascend-warning-bg)] text-[var(--ascend-warning)]',
      danger: 'bg-[var(--ascend-danger-bg)] text-[var(--ascend-danger)]',
      info: 'bg-[var(--ascend-info-bg)] text-[var(--ascend-info)]',
      xp: 'bg-secondary text-secondary-foreground',
    },
    size: {
      sm: 'px-1.5 py-0.5 text-[var(--ascend-text-xs)]',
      md: 'px-[var(--ascend-badge-padding-x)] py-[var(--ascend-badge-padding-y)] text-[var(--ascend-badge-font)]',
    },
  },
  defaultVariants: {
    variant: 'default',
    size: 'md',
  },
})

interface BadgeProps extends VariantProps<typeof badgeVariants> {
  children: ReactNode
  dot?: boolean
  className?: string
}

export function Badge({ children, variant, size, dot, className }: BadgeProps) {
  return (
    <span
      className={cn(badgeVariants({ variant, size }), className)}
    >
      {dot && (
        <span
          className="rounded-full"
          style={{ width: 'var(--ascend-badge-dot-size)', height: 'var(--ascend-badge-dot-size)', backgroundColor: 'currentColor' }}
        />
      )}
      {children}
    </span>
  )
}
