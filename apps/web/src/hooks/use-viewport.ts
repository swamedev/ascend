'use client'

import { useState, useEffect } from 'react'

interface Viewport {
  width: number
  height: number
  scrollY: number
}

export function useViewport(): Viewport {
  const [viewport, setViewport] = useState<Viewport>({
    width: typeof window !== 'undefined' ? window.innerWidth : 0,
    height: typeof window !== 'undefined' ? window.innerHeight : 0,
    scrollY: typeof window !== 'undefined' ? window.scrollY : 0,
  })

  useEffect(() => {
    function handleResize() {
      setViewport({
        width: window.innerWidth,
        height: window.innerHeight,
        scrollY: window.scrollY,
      })
    }

    function handleScroll() {
      setViewport((prev) => ({ ...prev, scrollY: window.scrollY }))
    }

    window.addEventListener('resize', handleResize)
    window.addEventListener('scroll', handleScroll, { passive: true })

    return () => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('scroll', handleScroll)
    }
  }, [])

  return viewport
}
