import type { LucideIcon } from 'lucide-react'

export type CommandCategory = 'navigation' | 'actions' | 'pages' | 'recent'

export interface Command {
  id: string
  category: CommandCategory
  label: string
  description?: string
  icon?: LucideIcon
  shortcut?: string
  disabled?: boolean
  execute: () => void
}

export interface CommandGroup {
  category: CommandCategory
  label: string
  commands: Command[]
}

export type CommandRegistry = Map<string, Command>
