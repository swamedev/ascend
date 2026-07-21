'use client'

import { type ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { IconButton } from '@/components/ui'
import { X } from 'lucide-react'

interface PanelProps {
  children: ReactNode
  header?: ReactNode
  onClose?: () => void
  className?: string
}

export function Panel({ children, header, onClose, className }: PanelProps) {
  return (
    <div className={cn('flex h-full flex-col', className)}>
      {(header || onClose) && (
        <div className="flex items-center justify-between border-b px-3 py-2">
          {header && <div className="font-medium text-sm">{header}</div>}
          {onClose && <IconButton icon={<X />} size="sm" label="Close panel" onClick={onClose} />}
        </div>
      )}
      <div className="flex-1 overflow-auto p-3">{children}</div>
    </div>
  )
}

interface PanelHeaderProps {
  title: string
  description?: string
  action?: ReactNode
  className?: string
}

export function PanelHeader({ title, description, action, className }: PanelHeaderProps) {
  return (
    <div className={cn('mb-4 space-y-1', className)}>
      <div className="flex items-center justify-between gap-2">
        <h3 className="font-semibold">{title}</h3>
        {action}
      </div>
      {description && <p className="text-sm text-muted-foreground">{description}</p>}
    </div>
  )
}
