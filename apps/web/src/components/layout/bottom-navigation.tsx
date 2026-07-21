'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { type NavigationItem } from '@/types/navigation'

interface BottomNavigationProps {
  items: NavigationItem[]
  className?: string
}

export function BottomNavigation({ items, className }: BottomNavigationProps) {
  const pathname = usePathname()

  return (
    <nav
      className={cn(
        'fixed bottom-0 left-0 right-0 z-[var(--ascend-z-sticky)] flex items-center justify-around border-t bg-background px-2 pb-safe',
        className
      )}
    >
      {items.map((item) => {
        const Icon = item.icon
        const active = pathname === item.href || pathname.startsWith(item.href + '/')
        return (
          <Link
            key={item.id}
            href={item.href}
            className={cn(
              'relative flex flex-col items-center gap-0.5 px-3 py-1.5 text-xs transition-colors',
              active
                ? 'text-primary'
                : 'text-muted-foreground hover:text-foreground'
            )}
          >
            <Icon className="h-5 w-5" />
            <span className="truncate max-w-16">{item.label}</span>
            {item.badge !== undefined && (
              <span className="absolute right-1 top-0.5 flex h-4 min-w-4 items-center justify-center rounded-full bg-primary px-1 text-[10px] text-primary-foreground">
                {item.badge}
              </span>
            )}
          </Link>
        )
      })}
    </nav>
  )
}
