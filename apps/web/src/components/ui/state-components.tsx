'use client'

import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { Spinner } from './spinner'
import { XCircle, CheckCircle } from 'lucide-react'

interface LoadingStateProps {
  label?: string
  className?: string
}

export function LoadingState({ label = 'Loading...', className }: LoadingStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center gap-3 py-12', className)}>
      <Spinner size="lg" />
      <p className="text-sm text-muted-foreground">{label}</p>
    </div>
  )
}

interface ErrorStateProps {
  title?: string
  message?: string
  action?: ReactNode
  className?: string
}

export function ErrorState({
  title = 'Something went wrong',
  message = 'An unexpected error occurred. Please try again.',
  action,
  className,
}: ErrorStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-12 text-center', className)}>
      <XCircle className="mb-4 h-12 w-12 text-destructive" />
      <h3 className="text-lg font-semibold">{title}</h3>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">{message}</p>
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}

interface SuccessStateProps {
  title?: string
  message?: string
  action?: ReactNode
  className?: string
}

export function SuccessState({
  title = 'Success!',
  message,
  action,
  className,
}: SuccessStateProps) {
  return (
    <div className={cn('flex flex-col items-center justify-center py-12 text-center', className)}>
      <CheckCircle className="mb-4 h-12 w-12 text-success" />
      <h3 className="text-lg font-semibold">{title}</h3>
      {message && <p className="mt-1 max-w-sm text-sm text-muted-foreground">{message}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  )
}
