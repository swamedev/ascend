import type { TokenGroup } from '../types'

interface ShadowToken {
  name: string
  light: string
  dark: string
  description: string
  category: 'primitive'
}

const tokens: ShadowToken[] = [
  { name: 'shadow-sm', light: '0 1px 2px rgba(0,0,0,0.05)', dark: '0 1px 2px rgba(0,0,0,0.3)', description: 'Small shadow', category: 'primitive' },
  { name: 'shadow-md', light: '0 4px 6px rgba(0,0,0,0.07)', dark: '0 4px 6px rgba(0,0,0,0.4)', description: 'Medium shadow', category: 'primitive' },
  { name: 'shadow-lg', light: '0 10px 15px rgba(0,0,0,0.1)', dark: '0 10px 15px rgba(0,0,0,0.5)', description: 'Large shadow', category: 'primitive' },
  { name: 'shadow-xl', light: '0 20px 25px rgba(0,0,0,0.12)', dark: '0 20px 25px rgba(0,0,0,0.6)', description: 'Extra large shadow', category: 'primitive' },
  { name: 'shadow-glow', light: '0 0 20px rgba(51,102,255,0.15)', dark: '0 0 20px rgba(102,153,255,0.2)', description: 'Brand glow', category: 'primitive' },
]

export const shadow = {
  category: 'primitive' as const,
  prefix: 'ascend',
  tokens,
}
