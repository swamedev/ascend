'use client'

import { useEffect, type ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-react'
import { IconButton } from './icon-button'
import { motion, AnimatePresence } from 'framer-motion'
import { useMotion } from '@/components/motion'

type ToastVariant = 'success' | 'error' | 'warning' | 'info'

interface ToastData {
  id: string
  message: string
  variant?: ToastVariant
  duration?: number
}

interface ToastContainerProps {
  toasts: ToastData[]
  onDismiss: (id: string) => void
  className?: string
}

const iconMap: Record<ToastVariant, ReactNode> = {
  success: <CheckCircle className="h-4 w-4 text-green-500" />,
  error: <AlertCircle className="h-4 w-4 text-red-500" />,
  warning: <AlertTriangle className="h-4 w-4 text-yellow-500" />,
  info: <Info className="h-4 w-4 text-blue-500" />,
}

const variantStyles: Record<ToastVariant, string> = {
  success: 'border-green-200 dark:border-green-800',
  error: 'border-red-200 dark:border-red-800',
  warning: 'border-yellow-200 dark:border-yellow-800',
  info: 'border-blue-200 dark:border-blue-800',
}

function ToastItem({ toast, onDismiss }: { toast: ToastData; onDismiss: (id: string) => void }) {
  const variant = toast.variant ?? 'info'
  const { reducedMotion } = useMotion()

  useEffect(() => {
    if (toast.duration && toast.duration > 0) {
      const timer = setTimeout(() => onDismiss(toast.id), toast.duration)
      return () => clearTimeout(timer)
    }
  }, [toast.id, toast.duration, onDismiss])

  return (
    <motion.div
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: -20, scale: 0.95 }}
      transition={{ duration: reducedMotion ? 0 : 0.2 }}
      className={cn(
        'pointer-events-auto flex items-start gap-3 rounded-lg border bg-card px-4 py-3 shadow-lg',
        variantStyles[variant]
      )}
      role="status"
      aria-atomic="true"
    >
      {iconMap[variant]}
      <p className="flex-1 text-sm">{toast.message}</p>
      <IconButton icon={<X />} size="sm" label="Dismiss" onClick={() => onDismiss(toast.id)} />
    </motion.div>
  )
}

export function ToastContainer({ toasts, onDismiss, className }: ToastContainerProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      className={cn(
        'pointer-events-none fixed right-4 top-4 z-[var(--ascend-z-toast)] flex flex-col gap-2',
        className
      )}
    >
      <AnimatePresence>
        {toasts.map((toast) => (
          <ToastItem key={toast.id} toast={toast} onDismiss={onDismiss} />
        ))}
      </AnimatePresence>
    </div>
  )
}

export type { ToastData, ToastVariant }
