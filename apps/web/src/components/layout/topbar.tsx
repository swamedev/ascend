'use client'

import { type ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { useLayoutStore } from '@/store/layout-store'

interface TopBarProps {
  left?: ReactNode
  center?: ReactNode
  right?: ReactNode
  className?: string
}

export function TopBar({ left, center, right, className }: TopBarProps) {
  const transparent = useLayoutStore((s) => s.topbar.transparent)
  const hidden = useLayoutStore((s) => s.topbar.hidden)

  if (hidden) return null

  return (
    <header
      className={cn(
        'flex h-14 items-center gap-2 px-4',
        !transparent && 'bg-background',
        className
      )}
    >
      <div className="flex flex-1 items-center gap-2">{left}</div>
      {center && <div className="flex items-center gap-2">{center}</div>}
      <div className="flex flex-1 items-center justify-end gap-2">{right}</div>
    </header>
  )
}

interface TopBarActionProps {
  icon: ReactNode
  label: string
  onClick?: () => void
  active?: boolean
  badge?: number
  className?: string
}

export function TopBarAction({ icon, label, onClick, active, badge, className }: TopBarActionProps) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className={cn(
        'relative flex h-9 w-9 items-center justify-center rounded-md transition-colors',
        active
          ? 'bg-accent text-accent-foreground'
          : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
        className
      )}
    >
      <span className="h-4 w-4">{icon}</span>
      {badge !== undefined && badge > 0 && (
        <span className="absolute -right-0.5 -top-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-primary text-[10px] font-medium text-primary-foreground">
          {badge > 9 ? '9+' : badge}
        </span>
      )}
    </button>
  )
}
