import type { TokenGroup } from '../types'

const tokens = [
  // Button
  { name: 'button-radius', value: 'var(--ascend-radius-md)', description: 'Button border radius' },
  { name: 'button-padding-x', value: 'var(--ascend-space-4)', description: 'Button horizontal padding' },
  { name: 'button-padding-y', value: 'var(--ascend-space-2)', description: 'Button vertical padding' },
  { name: 'button-font', value: 'var(--ascend-font-weight-medium)', description: 'Button font weight' },
  { name: 'button-gap', value: 'var(--ascend-space-2)', description: 'Button icon gap' },

  // Card
  { name: 'card-radius', value: 'var(--ascend-radius-lg)', description: 'Card border radius' },
  { name: 'card-padding', value: 'var(--ascend-space-6)', description: 'Card padding' },
  { name: 'card-shadow', value: 'var(--ascend-shadow-sm)', description: 'Card shadow' },
  { name: 'card-gap', value: 'var(--ascend-space-4)', description: 'Card inner gap' },

  // Panel
  { name: 'panel-radius', value: 'var(--ascend-radius-md)', description: 'Panel border radius' },
  { name: 'panel-padding', value: 'var(--ascend-space-4)', description: 'Panel padding' },
  { name: 'panel-bg', value: 'var(--ascend-surface)', description: 'Panel background' },
  { name: 'panel-border', value: 'var(--ascend-border)', description: 'Panel border' },

  // Sidebar
  { name: 'sidebar-width', value: '240px', description: 'Sidebar expanded width' },
  { name: 'sidebar-width-collapsed', value: '64px', description: 'Sidebar collapsed width' },
  { name: 'sidebar-bg', value: 'var(--ascend-surface)', description: 'Sidebar background' },
  { name: 'sidebar-border', value: 'var(--ascend-border)', description: 'Sidebar border' },
  { name: 'sidebar-item-radius', value: 'var(--ascend-radius-md)', description: 'Sidebar item radius' },
  { name: 'sidebar-item-padding', value: 'var(--ascend-space-3)', description: 'Sidebar item padding' },

  // Input
  { name: 'input-radius', value: 'var(--ascend-radius-md)', description: 'Input border radius' },
  { name: 'input-padding-x', value: 'var(--ascend-space-3)', description: 'Input horizontal padding' },
  { name: 'input-padding-y', value: 'var(--ascend-space-2)', description: 'Input vertical padding' },
  { name: 'input-border', value: 'var(--ascend-border)', description: 'Input border' },
  { name: 'input-border-focus', value: 'var(--ascend-brand-500)', description: 'Input focus border' },

  // Badge
  { name: 'badge-radius', value: 'var(--ascend-radius-full)', description: 'Badge border radius' },
  { name: 'badge-padding-x', value: 'var(--ascend-space-2)', description: 'Badge horizontal padding' },
  { name: 'badge-padding-y', value: '0.125rem', description: 'Badge vertical padding' },
  { name: 'badge-font', value: 'var(--ascend-text-xs)', description: 'Badge font size' },
  { name: 'badge-dot-size', value: '8px', description: 'Badge dot size' },
]

export const component: TokenGroup = {
  category: 'component',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'component' as const })),
}
