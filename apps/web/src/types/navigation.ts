import type { LucideIcon } from 'lucide-react'

export interface NavigationItem {
  id: string
  icon: LucideIcon
  label: string
  href: string
  permissions?: string[]
  badge?: number | string
  hidden?: boolean
  children?: NavigationItem[]
}

export interface NavigationGroup {
  id: string
  label?: string
  items: NavigationItem[]
}

export type NavigationRegistry = NavigationGroup[]
