'use client'

import { useTheme } from 'next-themes'
import { Sun, Moon, Monitor, Check } from 'lucide-react'
import { useEffect, useState } from 'react'

const options = [
  { value: 'light', label: 'Light', icon: Sun },
  { value: 'dark', label: 'Dark', icon: Moon },
  { value: 'system', label: 'System', icon: Monitor },
] as const

export function ThemeSelector() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  return (
    <div className="flex flex-col gap-1 p-1" role="radiogroup" aria-label="Theme selector">
      {options.map(({ value, label, icon: Icon }) => (
        <button
          key={value}
          onClick={() => setTheme(value)}
          role="radio"
          aria-checked={mounted && theme === value}
          className="flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors hover:bg-accent aria-checked:bg-accent"
        >
          <Icon className="h-4 w-4" />
          <span className="flex-1 text-left">{label}</span>
          {mounted && theme === value && (
            <Check className="h-3.5 w-3.5 text-primary" />
          )}
        </button>
      ))}
    </div>
  )
}
