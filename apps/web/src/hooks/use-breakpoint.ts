'use client'

import { useEffect, useCallback } from 'react'
import { useLayoutStore, type LayoutMode } from '@/store/layout-store'

const BREAKPOINTS: Record<LayoutMode, number> = {
  ultrawide: 1536,
  desktop: 1024,
  tablet: 768,
  mobile: 0,
}

function getLayoutMode(width: number): LayoutMode {
  if (width >= BREAKPOINTS.ultrawide) return 'ultrawide'
  if (width >= BREAKPOINTS.desktop) return 'desktop'
  if (width >= BREAKPOINTS.tablet) return 'tablet'
  return 'mobile'
}

export function useBreakpoint(): LayoutMode {
  const layoutMode = useLayoutStore((s) => s.layoutMode)
  return layoutMode
}

export function useBreakpointInit() {
  const setLayoutMode = useLayoutStore((s) => s.setLayoutMode)
  const setSidebarOpen = useLayoutStore((s) => s.setSidebarOpen)
  const setSidebarCollapsed = useLayoutStore((s) => s.setSidebarCollapsed)

  const handleResize = useCallback(() => {
    const mode = getLayoutMode(window.innerWidth)
    setLayoutMode(mode)

    if (mode === 'mobile') {
      setSidebarOpen(false)
      setSidebarCollapsed(false)
    } else if (mode === 'tablet') {
      setSidebarOpen(true)
      setSidebarCollapsed(true)
    } else {
      setSidebarOpen(true)
      setSidebarCollapsed(false)
    }
  }, [setLayoutMode, setSidebarOpen, setSidebarCollapsed])

  useEffect(() => {
    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [handleResize])
}
