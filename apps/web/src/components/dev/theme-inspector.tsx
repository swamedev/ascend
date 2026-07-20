'use client'

import { useEffect, useState, useCallback } from 'react'
import { useTheme } from 'next-themes'

function getCssVar(name: string): string {
  if (typeof document === 'undefined') return ''
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim()
}

function getBreakpoint(): string {
  if (typeof window === 'undefined') return '—'
  const w = window.innerWidth
  if (w < 640) return `sm (${w}px)`
  if (w < 768) return `md (${w}px)`
  if (w < 1024) return `lg (${w}px)`
  if (w < 1280) return `xl (${w}px)`
  return `2xl (${w}px)`
}

function prefersReducedMotion(): boolean {
  if (typeof window === 'undefined') return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

function prefersHighContrast(): boolean {
  if (typeof window === 'undefined') return false
  return window.matchMedia('(prefers-contrast: more)').matches
}

const WATCHED_TOKENS = [
  '--ascend-background',
  '--ascend-foreground',
  '--ascend-surface',
  '--ascend-border',
  '--ascend-brand-500',
  '--ascend-success',
  '--ascend-danger',
  '--ascend-warning',
  '--ascend-info',
  '--ascend-space-4',
  '--ascend-radius-md',
  '--ascend-text-base',
  '--ascend-shadow-sm',
  '--ascend-dur-normal',
  '--ascend-ease-out',
]

interface TokenEntry {
  name: string
  value: string
}

export function ThemeInspector() {
  const { theme, resolvedTheme } = useTheme()
  const [visible, setVisible] = useState(false)
  const [mounted, setMounted] = useState(false)
  const [tokens, setTokens] = useState<TokenEntry[]>([])
  const [breakpoint, setBreakpoint] = useState('—')

  const isDev = process.env.NODE_ENV === 'development'

  const refresh = useCallback(() => {
    setTokens(
      WATCHED_TOKENS.map((name) => ({
        name,
        value: getCssVar(name),
      }))
    )
    setBreakpoint(getBreakpoint())
  }, [])

  useEffect(() => {
    setMounted(true)
  }, [])

  useEffect(() => {
    refresh()
    const interval = setInterval(refresh, 1000)
    return () => clearInterval(interval)
  }, [refresh])

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.ctrlKey && e.altKey && e.key === 't') {
        e.preventDefault()
        setVisible((v) => !v)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  if (!isDev || !mounted) return null
  if (!visible) return null

  return (
    <div className="fixed bottom-4 right-4 z-[9999] w-80 rounded-lg border border-amber-200 bg-amber-50 p-4 font-mono text-xs shadow-lg dark:border-amber-800 dark:bg-amber-950">
      <div className="mb-3 flex items-center justify-between">
        <h3 className="font-semibold text-amber-800 dark:text-amber-200">
          🛠 Theme Inspector
        </h3>
        <div className="flex gap-2">
          <button
            onClick={refresh}
            className="rounded px-1.5 py-0.5 text-amber-600 hover:bg-amber-200 dark:text-amber-400 dark:hover:bg-amber-900"
            aria-label="Refresh"
          >
            ↻
          </button>
          <button
            onClick={() => setVisible(false)}
            className="rounded px-1.5 py-0.5 text-amber-600 hover:bg-amber-200 dark:text-amber-400 dark:hover:bg-amber-900"
            aria-label="Close"
          >
            ✕
          </button>
        </div>
      </div>

      <div className="mb-2 grid grid-cols-2 gap-1">
        <div className="rounded bg-amber-100/50 p-1 dark:bg-amber-900/50">
          <span className="text-amber-500">Theme</span>
          <div className="font-semibold text-amber-900 dark:text-amber-100">
            {theme}
          </div>
        </div>
        <div className="rounded bg-amber-100/50 p-1 dark:bg-amber-900/50">
          <span className="text-amber-500">Resolved</span>
          <div className="font-semibold text-amber-900 dark:text-amber-100">
            {resolvedTheme}
          </div>
        </div>
        <div className="rounded bg-amber-100/50 p-1 dark:bg-amber-900/50">
          <span className="text-amber-500">Breakpoint</span>
          <div className="font-semibold text-amber-900 dark:text-amber-100">
            {breakpoint}
          </div>
        </div>
        <div className="rounded bg-amber-100/50 p-1 dark:bg-amber-900/50">
          <span className="text-amber-500">Reduced motion</span>
          <div className="font-semibold text-amber-900 dark:text-amber-100">
            {prefersReducedMotion() ? 'Yes' : 'No'}
          </div>
        </div>
        <div className="rounded bg-amber-100/50 p-1 dark:bg-amber-900/50">
          <span className="text-amber-500">High contrast</span>
          <div className="font-semibold text-amber-900 dark:text-amber-100">
            {prefersHighContrast() ? 'Yes' : 'No'}
          </div>
        </div>
        <div className="rounded bg-amber-100/50 p-1 dark:bg-amber-900/50">
          <span className="text-amber-500">Density</span>
          <div className="font-semibold text-amber-900 dark:text-amber-100">
            Normal
          </div>
        </div>
      </div>

      <div className="max-h-48 overflow-y-auto">
        <table className="w-full text-amber-700 dark:text-amber-300">
          <thead>
            <tr className="text-amber-500">
              <th className="text-left">Token</th>
              <th className="text-right">Value</th>
            </tr>
          </thead>
          <tbody>
            {tokens.map(({ name, value }) => (
              <tr key={name} className="border-t border-amber-200/50 dark:border-amber-800/50">
                <td className="truncate py-0.5 pr-2">{name}</td>
                <td className="truncate py-0.5 text-right font-bold">{value || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-2 text-amber-400 dark:text-amber-500">
        Ctrl+Alt+T to toggle
      </div>
    </div>
  )
}
