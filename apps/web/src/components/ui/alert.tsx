'use client'

import type { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { CheckCircle, AlertCircle, AlertTriangle, Info, X } from 'lucide-react'
import { IconButton } from './icon-button'

type AlertVariant = 'success' | 'error' | 'warning' | 'info'

interface AlertProps {
  variant?: AlertVariant
  title?: string
  children: ReactNode
  onDismiss?: () => void
  className?: string
}

const config: Record<AlertVariant, { icon: ReactNode; styles: string }> = {
  success: {
    icon: <CheckCircle className="h-5 w-5 text-success" />,
    styles: 'border-success/20 bg-success/10 dark:border-success/50 dark:bg-success/20',
  },
  error: {
    icon: <AlertCircle className="h-5 w-5 text-destructive" />,
    styles: 'border-destructive/20 bg-destructive/10 dark:border-destructive/50 dark:bg-destructive/20',
  },
  warning: {
    icon: <AlertTriangle className="h-5 w-5 text-warning" />,
    styles: 'border-warning/20 bg-warning/10 dark:border-warning/50 dark:bg-warning/20',
  },
  info: {
    icon: <Info className="h-5 w-5 text-info" />,
    styles: 'border-info/20 bg-info/10 dark:border-info/50 dark:bg-info/20',
  },
}

export function Alert({ variant = 'info', title, children, onDismiss, className }: AlertProps) {
  const { icon, styles } = config[variant]

  return (
    <div
      className={cn(
        'flex items-start gap-3 rounded-lg border p-4',
        styles,
        className
      )}
      role="alert"
    >
      <span className="mt-0.5 shrink-0">{icon}</span>
      <div className="flex-1 space-y-1">
        {title && <p className="font-medium text-sm">{title}</p>}
        <div className="text-sm text-muted-foreground">{children}</div>
      </div>
      {onDismiss && <IconButton icon={<X />} size="sm" label="Dismiss" onClick={onDismiss} />}
    </div>
  )
}
