'use client'

import { useTheme } from 'next-themes'
import { Sun, Moon, Monitor } from 'lucide-react'
import { useEffect, useState } from 'react'

const icons = {
  light: Sun,
  dark: Moon,
  system: Monitor,
}

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <button
        className="inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-accent"
        aria-label="Toggle theme"
      >
        <Sun className="h-4 w-4" />
      </button>
    )
  }

  const Icon = icons[theme as keyof typeof icons] || Sun

  function cycleTheme() {
    const order = ['light', 'dark', 'system'] as const
    const currentIndex = order.indexOf(theme as typeof order[number])
    const nextIndex = (currentIndex + 1) % order.length
    setTheme(order[nextIndex])
  }

  return (
    <button
      onClick={cycleTheme}
      className="inline-flex h-9 w-9 items-center justify-center rounded-md transition-colors hover:bg-accent"
      aria-label={`Current theme: ${theme}. Click to change.`}
    >
      <Icon className="h-4 w-4" />
    </button>
  )
}
