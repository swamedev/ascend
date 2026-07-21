'use client'

import { useState, useRef, useEffect, useId, type ReactNode } from 'react'
import { cn } from '@/lib/utils'

type TooltipPosition = 'top' | 'bottom' | 'left' | 'right'

interface TooltipProps {
  content: string
  children: ReactNode
  position?: TooltipPosition
  delay?: number
  className?: string
}

const positionStyles: Record<TooltipPosition, string> = {
  top: 'bottom-full left-1/2 -translate-x-1/2 mb-1.5',
  bottom: 'top-full left-1/2 -translate-x-1/2 mt-1.5',
  left: 'right-full top-1/2 -translate-y-1/2 mr-1.5',
  right: 'left-full top-1/2 -translate-y-1/2 ml-1.5',
}

export function Tooltip({ content, children, position = 'top', delay = 300, className }: TooltipProps) {
  const [visible, setVisible] = useState(false)
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)
  const tooltipId = useId()

  useEffect(() => {
    return () => { if (timer.current) clearTimeout(timer.current) }
  }, [])

  return (
    <div
      className="relative inline-flex"
      onMouseEnter={() => {
        timer.current = setTimeout(() => setVisible(true), delay)
      }}
      onMouseLeave={() => {
        if (timer.current) clearTimeout(timer.current)
        setVisible(false)
      }}
      onFocus={() => setVisible(true)}
      onBlur={() => setVisible(false)}
    >
      <div aria-describedby={visible ? tooltipId : undefined}>
        {children}
      </div>
      {visible && (
        <div
          id={tooltipId}
          role="tooltip"
          className={cn(
            'pointer-events-none absolute z-[var(--ascend-z-tooltip)] whitespace-nowrap rounded-md bg-foreground px-2.5 py-1.5 text-xs text-background shadow-md',
            positionStyles[position],
            className
          )}
        >
          {content}
        </div>
      )}
    </div>
  )
}
