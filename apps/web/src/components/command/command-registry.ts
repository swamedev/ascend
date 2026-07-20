'use client'

import { create } from 'zustand'
import type { Command, CommandCategory, CommandGroup } from '@/types/commands'

interface CommandRegistryState {
  commands: Map<string, Command>
  register: (command: Command) => () => void
  registerMany: (commands: Command[]) => () => void
  getByCategory: (category: CommandCategory) => Command[]
  search: (query: string) => Command[]
  getAll: () => Command[]
  getGroups: () => CommandGroup[]
}

function createDefaultCommands(): Command[] {
  return [
    {
      id: 'nav-dashboard',
      category: 'navigation',
      label: 'Go to Dashboard',
      description: 'Navigate to the dashboard page',
      shortcut: 'G D',
      execute: () => window.location.href = '/dashboard',
    },
    {
      id: 'nav-journeys',
      category: 'navigation',
      label: 'Go to Journeys',
      description: 'Navigate to the journeys page',
      shortcut: 'G J',
      execute: () => window.location.href = '/journeys',
    },
    {
      id: 'nav-missions',
      category: 'navigation',
      label: 'Go to Missions',
      description: 'Navigate to the missions page',
      shortcut: 'G M',
      execute: () => window.location.href = '/missions',
    },
    {
      id: 'nav-competencies',
      category: 'navigation',
      label: 'Go to Competencies',
      description: 'Navigate to the competencies page',
      shortcut: 'G C',
      execute: () => window.location.href = '/competencies',
    },
    {
      id: 'nav-achievements',
      category: 'navigation',
      label: 'Go to Achievements',
      description: 'Navigate to the achievements page',
      shortcut: 'G A',
      execute: () => window.location.href = '/achievements',
    },
    {
      id: 'nav-profile',
      category: 'navigation',
      label: 'Go to Profile',
      description: 'Navigate to the builder profile page',
      shortcut: 'G P',
      execute: () => window.location.href = '/profile',
    },
  ]
}

const CATEGORY_ORDER: CommandCategory[] = ['navigation', 'pages', 'actions', 'recent']
const CATEGORY_LABELS: Record<CommandCategory, string> = {
  navigation: 'Navigation',
  pages: 'Pages',
  actions: 'Actions',
  recent: 'Recent',
}

export const useCommandRegistry = create<CommandRegistryState>()(
  (set, get) => {
    const defaults = createDefaultCommands()
    const initial = new Map<string, Command>()
    defaults.forEach((cmd) => initial.set(cmd.id, cmd))

    return {
      commands: initial,

      register: (command) => {
        set((s) => {
          const next = new Map(s.commands)
          next.set(command.id, command)
          return { commands: next }
        })
        return () => {
          set((s) => {
            const next = new Map(s.commands)
            next.delete(command.id)
            return { commands: next }
          })
        }
      },

      registerMany: (commands) => {
        set((s) => {
          const next = new Map(s.commands)
          commands.forEach((cmd) => next.set(cmd.id, cmd))
          return { commands: next }
        })
        return () => {
          set((s) => {
            const next = new Map(s.commands)
            commands.forEach((cmd) => next.delete(cmd.id))
            return { commands: next }
          })
        }
      },

      getByCategory: (category) => {
        const all = Array.from(get().commands.values())
        return all.filter((c) => c.category === category)
      },

      search: (query) => {
        const all = Array.from(get().commands.values())
        const lower = query.toLowerCase()
        return all.filter(
          (c) =>
            c.label.toLowerCase().includes(lower) ||
            c.description?.toLowerCase().includes(lower) ||
            c.id.toLowerCase().includes(lower)
        )
      },

      getAll: () => Array.from(get().commands.values()),

      getGroups: () => {
        const all = Array.from(get().commands.values())
        const groups = new Map<CommandCategory, Command[]>()

        for (const cmd of all) {
          const list = groups.get(cmd.category) || []
          list.push(cmd)
          groups.set(cmd.category, list)
        }

        return CATEGORY_ORDER
          .filter((cat) => (groups.get(cat)?.length ?? 0) > 0)
          .map((cat) => ({
            category: cat,
            label: CATEGORY_LABELS[cat],
            commands: groups.get(cat) || [],
          }))
      },
    }
  }
)
