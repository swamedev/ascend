'use client'

import type { ReactNode, HTMLAttributes } from 'react'
import { cn } from '@/lib/utils'
import { cva, type VariantProps } from 'class-variance-authority'

const cardVariants = cva('rounded-[var(--ascend-card-radius)]', {
  variants: {
    variant: {
      default: 'bg-card text-card-foreground',
      elevated: 'bg-card text-card-foreground shadow-md',
      bordered: 'bg-card text-card-foreground border',
    },
    padding: {
      none: '',
      sm: 'p-3',
      md: 'p-[var(--ascend-card-padding)]',
      lg: 'p-[var(--ascend-space-8)]',
    },
  },
  defaultVariants: {
    variant: 'default',
    padding: 'md',
  },
})

interface CardProps extends HTMLAttributes<HTMLDivElement>, VariantProps<typeof cardVariants> {
  variant?: 'default' | 'elevated' | 'bordered'
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

export function Card({ variant, padding, className, children, ...props }: CardProps) {
  return (
    <div
      className={cn(cardVariants({ variant, padding }), className)}
      {...props}
    >
      {children}
    </div>
  )
}

interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {
  title?: string
  description?: string
  action?: ReactNode
}

export function CardHeader({ title, description, action, className, children, ...props }: CardHeaderProps) {
  return (
    <div className={cn('flex items-start justify-between gap-4', className)} {...props}>
      <div className="space-y-1">
        {title && <h3 className="font-semibold leading-none tracking-tight">{title}</h3>}
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
        {children}
      </div>
      {action && <div className="flex-shrink-0">{action}</div>}
    </div>
  )
}

interface CardContentProps extends HTMLAttributes<HTMLDivElement> {
  padding?: 'none' | 'sm' | 'md' | 'lg'
}

const contentPaddingStyles = {
  none: '',
  sm: 'p-3',
  md: 'p-[var(--ascend-card-padding)]',
  lg: 'p-[var(--ascend-space-8)]',
}

export function CardContent({ padding, className, children, ...props }: CardContentProps) {
  return (
    <div
      className={cn(
        padding && contentPaddingStyles[padding],
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

interface CardFooterProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode
}

export function CardFooter({ className, children, ...props }: CardFooterProps) {
  return (
    <div className={cn('flex items-center gap-2 pt-4', className)} {...props}>
      {children}
    </div>
  )
}
