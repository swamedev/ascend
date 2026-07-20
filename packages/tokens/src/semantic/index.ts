import type { TokenGroup } from '../types'

const light: Array<{ name: string; value: string; description: string }> = [
  { name: 'background', value: '#F8FAFC', description: 'Page background' },
  { name: 'surface', value: '#FFFFFF', description: 'Card, panel surface' },
  { name: 'surface-elevated', value: '#FFFFFF', description: 'Elevated surface (modals)' },
  { name: 'foreground', value: '#0F172A', description: 'Primary text' },
  { name: 'foreground-muted', value: '#64748B', description: 'Secondary text' },
  { name: 'foreground-subtle', value: '#94A3B8', description: 'Placeholder, caption' },
  { name: 'border', value: '#E2E8F0', description: 'Default border' },
  { name: 'border-strong', value: '#CBD5E1', description: 'Strong border (active)' },
  { name: 'muted', value: '#F1F5F9', description: 'Muted background' },
  { name: 'accent', value: '#D6E4FF', description: 'Accent background' },
  { name: 'accent-foreground', value: '#1F3D99', description: 'Accent text' },
  { name: 'success', value: '#22C55E', description: 'Success state' },
  { name: 'success-bg', value: '#F0FFF4', description: 'Success background' },
  { name: 'warning', value: '#F59E0B', description: 'Warning state' },
  { name: 'warning-bg', value: '#FFFBEB', description: 'Warning background' },
  { name: 'danger', value: '#EF4444', description: 'Danger state' },
  { name: 'danger-bg', value: '#FFF5F5', description: 'Danger background' },
  { name: 'info', value: '#3B82F6', description: 'Info state' },
  { name: 'info-bg', value: '#EFF6FF', description: 'Info background' },
]

const dark: Array<{ name: string; value: string; description: string }> = [
  { name: 'background', value: '#0F1115', description: 'Page background' },
  { name: 'surface', value: '#1A1D23', description: 'Card, panel surface' },
  { name: 'surface-elevated', value: '#262A33', description: 'Elevated surface (modals)' },
  { name: 'foreground', value: '#E1E5EB', description: 'Primary text' },
  { name: 'foreground-muted', value: '#838996', description: 'Secondary text' },
  { name: 'foreground-subtle', value: '#4A4F5C', description: 'Placeholder, caption' },
  { name: 'border', value: '#262A33', description: 'Default border' },
  { name: 'border-strong', value: '#333842', description: 'Strong border (active)' },
  { name: 'muted', value: '#1A1D23', description: 'Muted background' },
  { name: 'accent', value: '#1A2744', description: 'Accent background' },
  { name: 'accent-foreground', value: '#99C0FF', description: 'Accent text' },
  { name: 'success', value: '#4ADE80', description: 'Success state' },
  { name: 'success-bg', value: '#052E16', description: 'Success background' },
  { name: 'warning', value: '#FBBF24', description: 'Warning state' },
  { name: 'warning-bg', value: '#422006', description: 'Warning background' },
  { name: 'danger', value: '#F87171', description: 'Danger state' },
  { name: 'danger-bg', value: '#450A0A', description: 'Danger background' },
  { name: 'info', value: '#60A5FA', description: 'Info state' },
  { name: 'info-bg', value: '#0C1F3F', description: 'Info background' },
]

export const semantic = {
  light,
  dark,
}
