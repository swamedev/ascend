import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    include: ['tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      include: ['src'],
      exclude: [
        'src/**/index.ts',
        'src/contracts/**',
        'src/health/**',
        'src/mocks/**',
        'src/core/types.ts',
        'src/testing/simulate-failure.ts',
        'src/clock/system-clock.ts',
      ],
      thresholds: {
        statements: 95,
        branches: 90,
        functions: 95,
        lines: 95,
      },
    },
  },
})
