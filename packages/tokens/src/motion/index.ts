import type { TokenGroup } from '../types'

const tokens = [
  // Speed categories
  { name: 'motion-instant', value: 'var(--ascend-dur-instant)', description: 'Instant — no animation' },
  { name: 'motion-fast', value: 'var(--ascend-dur-fast)', description: 'Fast — 100ms' },
  { name: 'motion-normal', value: 'var(--ascend-dur-normal)', description: 'Normal — 200ms' },
  { name: 'motion-slow', value: 'var(--ascend-dur-slow)', description: 'Slow — 300ms' },
  { name: 'motion-hero', value: 'var(--ascend-dur-celebrate)', description: 'Hero — 500ms' },
  { name: 'motion-spring', value: 'var(--ascend-ease-spring)', description: 'Spring easing' },

  // Transition properties
  { name: 'transition-default', value: 'all var(--ascend-dur-normal) var(--ascend-ease-out)', description: 'Default transition' },
  { name: 'transition-color', value: 'background-color var(--ascend-dur-normal) var(--ascend-ease-out), color var(--ascend-dur-normal) var(--ascend-ease-out)', description: 'Theme color transition' },
  { name: 'transition-transform', value: 'transform var(--ascend-dur-normal) var(--ascend-ease-out)', description: 'Transform transition' },
  { name: 'transition-opacity', value: 'opacity var(--ascend-dur-normal) var(--ascend-ease-out)', description: 'Opacity transition' },

  // Keyframes reference
  { name: 'key-fade-in', value: 'fade-in var(--ascend-dur-normal) var(--ascend-ease-out)', description: 'Fade in animation' },
  { name: 'key-slide-up', value: 'slide-up var(--ascend-dur-slow) var(--ascend-ease-out)', description: 'Slide up animation' },
  { name: 'key-scale-in', value: 'scale-in var(--ascend-dur-normal) var(--ascend-ease-out)', description: 'Scale in animation' },
  { name: 'key-shimmer', value: 'shimmer 1.5s linear infinite', description: 'Skeleton shimmer' },
]

export const motion: TokenGroup = {
  category: 'motion',
  prefix: 'ascend',
  tokens: tokens.map((t) => ({ ...t, category: 'motion' as const })),
}
