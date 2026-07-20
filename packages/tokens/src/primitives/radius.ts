import type { TokenGroup } from '../types'

const tokens = [
  { name: 'radius-none', value: '0', description: 'No radius' },
  { name: 'radius-sm', value: '0.25rem', description: '4px — Small elements' },
  { name: 'radius-md', value: '0.5rem', description: '8px — Cards, modals' },
  { name: 'radius-lg', value: '0.75rem', description: '12px — Large cards' },
  { name: 'radius-xl', value: '1rem', description: '16px — Dialogs' },
  { name: 'radius-full', value: '9999px', description: 'Badges, avatars' },
]

export const radius: TokenGroup = {
  category: 'primitive',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'primitive' as const })),
}
