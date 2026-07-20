import type { TokenGroup } from '../types'

const tokens = [
  { name: 'space-0', value: '0', description: 'No spacing' },
  { name: 'space-1', value: '0.25rem', description: '4px — Micro spacing' },
  { name: 'space-2', value: '0.5rem', description: '8px — Tight spacing' },
  { name: 'space-3', value: '0.75rem', description: '12px — Small gap' },
  { name: 'space-4', value: '1rem', description: '16px — Standard gap' },
  { name: 'space-5', value: '1.25rem', description: '20px — Medium' },
  { name: 'space-6', value: '1.5rem', description: '24px — Section gap' },
  { name: 'space-8', value: '2rem', description: '32px — Large gap' },
  { name: 'space-10', value: '2.5rem', description: '40px — XL' },
  { name: 'space-12', value: '3rem', description: '48px — Section separator' },
  { name: 'space-16', value: '4rem', description: '64px — Page section' },
  { name: 'space-20', value: '5rem', description: '80px — Page section large' },
  { name: 'space-24', value: '6rem', description: '96px — Hero section' },
]

export const spacing: TokenGroup = {
  category: 'primitive',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'primitive' as const })),
}
