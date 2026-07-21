'use client'

import { type ReactNode } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { useLayoutStore } from '@/store/layout-store'
import type { NavigationItem } from '@/types/navigation'
import { ChevronDown } from 'lucide-react'
import { useState } from 'react'

interface SidebarProps {
  header?: ReactNode
  groups: { id: string; label?: string; items: NavigationItem[] }[]
  footer?: ReactNode
  className?: string
}

export function Sidebar({ header, groups, footer, className }: SidebarProps) {
  const collapsed = useLayoutStore((s) => s.sidebar.collapsed)

  if (collapsed) {
    return (
      <nav className={cn('flex flex-col items-center gap-1 py-2', className)}>
        {groups.flatMap((g) => g.items).map((item) => (
          <SidebarItem key={item.id} item={item} collapsed />
        ))}
      </nav>
    )
  }

  return (
    <nav className={cn('flex h-full flex-col', className)}>
      {header && <div className="flex-shrink-0 px-3 py-2">{header}</div>}
      <div className="flex-1 overflow-y-auto px-2 py-2">
        {groups.map((group) => (
          <div key={group.id} className="mb-4">
            {group.label && (
              <p className="mb-1 px-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">
                {group.label}
              </p>
            )}
            <div className="space-y-0.5">
              {group.items.map((item) => (
                <SidebarItem key={item.id} item={item} />
              ))}
            </div>
          </div>
        ))}
      </div>
      {footer && <div className="flex-shrink-0 border-t px-3 py-2">{footer}</div>}
    </nav>
  )
}

interface SidebarItemProps {
  item: NavigationItem
  collapsed?: boolean
  className?: string
}

export function SidebarItem({ item, collapsed, className }: SidebarItemProps) {
  const pathname = usePathname()
  const Icon = item.icon
  const active = pathname === item.href || pathname.startsWith(item.href + '/')
  const [expanded, setExpanded] = useState(active)

  if (collapsed) {
    return (
      <Link
        href={item.href}
        className={cn(
          'flex h-10 w-10 items-center justify-center rounded-md transition-colors',
          active
            ? 'bg-accent text-accent-foreground'
            : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
          className
        )}
        title={item.label}
      >
        <Icon className="h-[var(--ascend-icon-md)] w-[var(--ascend-icon-md)]" />
      </Link>
    )
  }

  return (
    <div>
      <Link
        href={item.href}
        className={cn(
          'flex items-center gap-3 rounded-md px-2 py-2 text-sm transition-colors',
          active
            ? 'bg-accent text-accent-foreground font-medium'
            : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
          className
        )}
      >
        <Icon className="h-[var(--ascend-icon-md)] w-[var(--ascend-icon-md)] shrink-0" />
        <span className="flex-1 truncate">{item.label}</span>
        {item.badge !== undefined && (
          <span className="flex h-5 min-w-5 items-center justify-center rounded-full bg-primary px-1 text-xs text-primary-foreground">
            {item.badge}
          </span>
        )}
        {item.children && (
          <button
            onClick={(e) => { e.preventDefault(); setExpanded(!expanded) }}
            className="p-0.5"
          >
            <ChevronDown
              className={cn(
                'h-3.5 w-3.5 transition-transform',
                expanded && 'rotate-180'
              )}
            />
          </button>
        )}
      </Link>
      {item.children && expanded && (
        <div className="ml-4 mt-0.5 space-y-0.5 border-l pl-2">
          {item.children.map((child) => (
            <SidebarItem key={child.id} item={child} />
          ))}
        </div>
      )}
    </div>
  )
}
