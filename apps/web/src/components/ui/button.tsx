'use client'

import { forwardRef } from 'react'
import type { ButtonHTMLAttributes, ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { cva, type VariantProps } from 'class-variance-authority'
import { Spinner } from './spinner'

const buttonVariants = cva(
  'inline-flex items-center justify-center font-[var(--ascend-button-font)] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary: 'bg-primary text-primary-foreground hover:bg-primary/90 active:bg-primary/80',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80 active:bg-secondary/70',
        ghost: 'text-foreground hover:bg-accent hover:text-accent-foreground active:bg-accent/80',
        danger: 'bg-[var(--ascend-danger)] text-white hover:opacity-90 active:opacity-80',
      },
      size: {
        sm: 'h-8 gap-1.5 rounded-[var(--ascend-button-radius)] px-[var(--ascend-space-3)] text-[var(--ascend-text-sm)]',
        md: 'h-10 gap-2 rounded-[var(--ascend-button-radius)] px-[var(--ascend-button-padding-x)] text-[var(--ascend-text-sm)]',
        lg: 'h-12 gap-2 rounded-[var(--ascend-button-radius)] px-[var(--ascend-space-6)] text-[var(--ascend-text-base)]',
      },
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
    },
  }
)

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  loading?: boolean
  icon?: ReactNode
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      loading = false,
      disabled = false,
      icon,
      children,
      className,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(buttonVariants({ variant, size }), className)}
        {...props}
      >
        {loading ? (
          <Spinner size="sm" />
        ) : icon ? (
          <span className="h-4 w-4 shrink-0">{icon}</span>
        ) : null}
        {children && <span>{children}</span>}
      </button>
    )
  }
)

Button.displayName = 'Button'
