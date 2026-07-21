'use client'

import { useEffect, useRef, useCallback, type ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { IconButton } from './icon-button'
import { X } from 'lucide-react'
import { useMotion } from '@/components/motion'
import { motion, AnimatePresence } from 'framer-motion'

interface ModalProps {
  open: boolean
  onClose: () => void
  title?: string
  description?: string
  children: ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full'
  className?: string
}

const sizeStyles = {
  sm: 'max-w-sm',
  md: 'max-w-md',
  lg: 'max-w-lg',
  xl: 'max-w-xl',
  full: 'max-w-[90vw]',
}

export function Modal({ open, onClose, title, description, children, size = 'md', className }: ModalProps) {
  const { reducedMotion } = useMotion()
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
        <div className="fixed inset-0 z-[var(--ascend-z-modal)] flex items-center justify-center p-4">
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
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={{ duration: reducedMotion ? 0 : 0.2, ease: [0, 0, 0.2, 1] }}
            role="dialog"
            aria-modal="true"
            aria-label={title ?? undefined}
            onKeyDown={handleKeyDown}
            className={cn(
              'relative w-full rounded-lg bg-card p-6 shadow-xl',
              sizeStyles[size],
              className
            )}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="space-y-1">
                {title && <h2 className="text-lg font-semibold">{title}</h2>}
                {description && <p className="text-sm text-muted-foreground">{description}</p>}
              </div>
              <IconButton icon={<X />} size="sm" label="Close" onClick={onClose} />
            </div>
            <div className="mt-4">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
