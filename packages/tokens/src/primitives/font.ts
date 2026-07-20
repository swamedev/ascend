import type { TokenGroup } from '../types'

const tokens = [
  { name: 'font-sans', value: "'Inter', system-ui, sans-serif", description: 'Primary font family' },
  { name: 'font-mono', value: "'JetBrains Mono', monospace", description: 'Monospace font family' },
  { name: 'text-xs', value: '0.75rem', description: '12px — Caption, metadata' },
  { name: 'text-sm', value: '0.875rem', description: '14px — Body small' },
  { name: 'text-base', value: '1rem', description: '16px — Body' },
  { name: 'text-lg', value: '1.125rem', description: '18px — Lead, subtitles' },
  { name: 'text-xl', value: '1.25rem', description: '20px — Section titles' },
  { name: 'text-2xl', value: '1.5rem', description: '24px — Page titles' },
  { name: 'text-3xl', value: '1.875rem', description: '30px — Hero titles' },
  { name: 'text-4xl', value: '2.25rem', description: '36px — Display large' },
  { name: 'text-5xl', value: '3rem', description: '48px — Display hero' },
  { name: 'font-weight-regular', value: '400', description: 'Regular weight' },
  { name: 'font-weight-medium', value: '500', description: 'Medium weight' },
  { name: 'font-weight-semibold', value: '600', description: 'Semibold weight' },
  { name: 'font-weight-bold', value: '700', description: 'Bold weight' },
  { name: 'font-weight-extrabold', value: '800', description: 'ExtraBold weight' },
]

export const font: TokenGroup = {
  category: 'primitive',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'primitive' as const })),
}
