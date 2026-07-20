import type { TokenGroup } from '../types'

const tokens = [
  { name: 'dur-instant', value: '0ms', description: 'Instant — state changes' },
  { name: 'dur-fast', value: '100ms', description: 'Fast — hover, micro-interactions' },
  { name: 'dur-normal', value: '200ms', description: 'Normal — standard transitions' },
  { name: 'dur-slow', value: '300ms', description: 'Slow — page transitions' },
  { name: 'dur-celebrate', value: '500ms', description: 'Celebrate — level up, achievements' },
  { name: 'ease-default', value: 'ease', description: 'Default easing' },
  { name: 'ease-in', value: 'cubic-bezier(0.4, 0, 1, 1)', description: 'In easing' },
  { name: 'ease-out', value: 'cubic-bezier(0, 0, 0.2, 1)', description: 'Out easing' },
  { name: 'ease-in-out', value: 'cubic-bezier(0.4, 0, 0.2, 1)', description: 'In-out easing' },
  { name: 'ease-spring', value: 'cubic-bezier(0.34, 1.56, 0.64, 1)', description: 'Spring — celebrations' },
]

export const duration: TokenGroup = {
  category: 'primitive',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'primitive' as const })),
}
