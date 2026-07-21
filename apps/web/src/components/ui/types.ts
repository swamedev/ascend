import type { ReactNode } from 'react'

export interface BaseProps {
  className?: string
  children?: ReactNode
  'aria-label'?: string
}

export interface DataProps {
  loading?: boolean
  disabled?: boolean
}

export type ComponentSize = 'sm' | 'md' | 'lg'

export type ComponentVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'success' | 'warning' | 'info'
