import type { TokenGroup } from '../types'

const tokens = [
  { name: 'brand-50', value: '#F0F4FF', darkValue: '#0D1428', description: 'Lightest brand' },
  { name: 'brand-100', value: '#D6E4FF', darkValue: '#1A2744', description: 'Hover background' },
  { name: 'brand-200', value: '#ADC8FF', darkValue: '#2A3F66', description: 'Subtle border' },
  { name: 'brand-300', value: '#84A9FF', darkValue: '#3D5A8C', description: 'Active border' },
  { name: 'brand-400', value: '#5B8AFF', darkValue: '#5375AD', description: 'Icon brand' },
  { name: 'brand-500', value: '#3366FF', darkValue: '#6699FF', description: 'Primary — Builder Blue' },
  { name: 'brand-600', value: '#2952CC', darkValue: '#80ADFF', description: 'Hover primary' },
  { name: 'brand-700', value: '#1F3D99', darkValue: '#99C0FF', description: 'Active primary' },
  { name: 'brand-800', value: '#142966', darkValue: '#B3D4FF', description: 'Text on dark' },
  { name: 'brand-900', value: '#0A1433', darkValue: '#CCE5FF', description: 'Deep brand' },
]

export const brand: TokenGroup = {
  category: 'brand',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({
    name: t.name,
    value: t.value,
    description: t.description,
    category: 'brand' as const,
    darkValue: t.darkValue,
  })),
}
