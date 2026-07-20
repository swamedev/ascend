import type { TokenGroup } from '../types'

const tokens = [
  { name: 'z-base', value: '0', description: 'Base layer' },
  { name: 'z-dropdown', value: '100', description: 'Dropdown menus' },
  { name: 'z-sticky', value: '200', description: 'Sticky elements' },
  { name: 'z-navbar', value: '300', description: 'Navigation bar' },
  { name: 'z-modal', value: '400', description: 'Modals' },
  { name: 'z-toast', value: '500', description: 'Toasts' },
  { name: 'z-tooltip', value: '600', description: 'Tooltips' },
  { name: 'z-overlay', value: '700', description: 'Overlays' },
  { name: 'z-max', value: '9999', description: 'Maximum' },
]

export const zIndex: TokenGroup = {
  category: 'primitive',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'primitive' as const })),
}
