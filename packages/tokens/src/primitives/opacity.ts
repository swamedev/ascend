import type { TokenGroup } from '../types'

const tokens = [
  { name: 'opacity-0', value: '0', description: 'Hidden' },
  { name: 'opacity-5', value: '0.05', description: 'Subtle' },
  { name: 'opacity-10', value: '0.1', description: 'Very faint' },
  { name: 'opacity-20', value: '0.2', description: 'Faint' },
  { name: 'opacity-30', value: '0.3', description: 'Light overlay' },
  { name: 'opacity-40', value: '0.4', description: 'Medium overlay' },
  { name: 'opacity-50', value: '0.5', description: 'Disabled state' },
  { name: 'opacity-60', value: '0.6', description: 'Muted' },
  { name: 'opacity-70', value: '0.7', description: 'Subtle emphasis' },
  { name: 'opacity-80', value: '0.8', description: 'Emphasis' },
  { name: 'opacity-90', value: '0.9', description: 'Strong emphasis' },
  { name: 'opacity-100', value: '1', description: 'Full visibility' },
]

export const opacity: TokenGroup = {
  category: 'primitive',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'primitive' as const })),
}
