'use client'

import { useEffect, useRef, useCallback, type ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { IconButton } from './icon-button'
import { X } from 'lucide-react'
import { useMotion } from '@/components/motion'
import { motion, AnimatePresence } from 'framer-motion'

type DrawerSide = 'left' | 'right' | 'bottom'

interface DrawerProps {
  open: boolean
  onClose: () => void
  title?: string
  children: ReactNode
  side?: DrawerSide
  width?: number
  className?: string
}

const sideStyles: Record<DrawerSide, string> = {
  left: 'left-0 top-0 h-full',
  right: 'right-0 top-0 h-full',
  bottom: 'bottom-0 left-0 w-full',
}

const sideWidths: Record<DrawerSide, string> = {
  left: 'w-80',
  right: 'w-80',
  bottom: 'max-h-[60vh]',
}

const sideAnimations: Record<DrawerSide, { initial: Record<string, string>; animate: Record<string, string | number>; exit: Record<string, string> }> = {
  left: {
    initial: { x: '-100%' },
    animate: { x: 0 },
    exit: { x: '-100%' },
  },
  right: {
    initial: { x: '100%' },
    animate: { x: 0 },
    exit: { x: '100%' },
  },
  bottom: {
    initial: { y: '100%' },
    animate: { y: 0 },
    exit: { y: '100%' },
  },
}

export function Drawer({ open, onClose, title, children, side = 'right', className }: DrawerProps) {
  const { reducedMotion } = useMotion()
  const anim = sideAnimations[side]
  const focusTrapRef = useRef<HTMLDivElement>(null)
  const previousFocus = useRef<HTMLElement | null>(null)

  const handleEscape = useCallback((e: KeyboardEvent) => {
    if (e.key === 'Escape') onClose()
  }, [onClose])

  useEffect(() => {
    if (open) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
      previousFocus.current = document.activeElement as HTMLElement
      requestAnimationFrame(() => {
        const focusable = focusTrapRef.current?.querySelector<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        focusable?.focus()
      })
    }
    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = ''
      previousFocus.current?.focus()
    }
  }, [open, handleEscape])

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key !== 'Tab' || !focusTrapRef.current) return
    const focusable = focusTrapRef.current.querySelectorAll<HTMLElement>(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    if (!focusable.length) return
    const first = focusable[0]
    const last = focusable[focusable.length - 1]
    if (e.shiftKey) {
      if (document.activeElement === first) { e.preventDefault(); last.focus() }
    } else {
      if (document.activeElement === last) { e.preventDefault(); first.focus() }
    }
  }, [])

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-[var(--ascend-z-modal)]">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: reducedMotion ? 0 : 0.15 }}
            className="absolute inset-0 bg-black/50"
            onClick={onClose}
            aria-hidden="true"
          />
          <motion.div
            ref={focusTrapRef}
            initial={anim.initial}
            animate={anim.animate}
            exit={anim.exit}
            transition={{ duration: reducedMotion ? 0 : 0.25, ease: [0, 0, 0.2, 1] }}
            role="dialog"
            aria-modal="true"
            aria-label={title ?? undefined}
            onKeyDown={handleKeyDown}
            className={cn(
              'fixed flex flex-col bg-card shadow-xl',
              sideStyles[side],
              sideWidths[side],
              className
            )}
          >
            <div className="flex items-center justify-between border-b px-4 py-3">
              {title && <h2 className="font-semibold">{title}</h2>}
              <IconButton icon={<X />} size="sm" label="Close" onClick={onClose} />
            </div>
            <div className="flex-1 overflow-auto p-4">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
