import type { TokenGroup } from '../types'
import { spacing, radius, font, duration, opacity, zIndex, shadow } from '../primitives'
import { semantic } from '../semantic'
import { brand } from '../brand'
import { component } from '../components'
import { motion } from '../motion'

export interface CssOutput {
  light: string
  dark: string
}

function primitiveValue(token: { name: string; value: string; darkValue?: string }, mode: 'light' | 'dark'): string {
  if ('darkValue' in token && mode === 'dark' && (token as any).darkValue) {
    return (token as any).darkValue
  }
  return token.value
}

function groupToCss(group: TokenGroup, mode: 'light' | 'dark'): string {
  return group.tokens
    .map((t) => {
      const varName = `--${group.prefix}-${t.name}`
      const val = primitiveValue(t as any, mode)
      return `  ${varName}: ${val};`
    })
    .join('\n')
}

function semanticToCss(mode: 'light' | 'dark'): string {
  const tokens = mode === 'light' ? semantic.light : semantic.dark
  return tokens.map((t) => `  --ascend-${t.name}: ${t.value};`).join('\n')
}

function allGroups(mode: 'light' | 'dark'): string[] {
  const groups = [spacing, radius, font, duration, opacity, zIndex, component, motion]
  return groups.map((g) => groupToCss(g, mode))
}

export function generateCss(): CssOutput {
  const lightGroups = allGroups('light')
  const darkGroups = allGroups('dark')

  // Shadow needs special handling (light/dark values)
  const shadowLight = shadow.tokens.map((t: any) => `  --ascend-${t.name}: ${t.light};`).join('\n')
  const shadowDark = shadow.tokens.map((t: any) => `  --ascend-${t.name}: ${t.dark};`).join('\n')

  // Brand uses darkValue
  const brandLight = brand.tokens.map((t: any) => `  --ascend-${t.name}: ${t.value};`).join('\n')
  const brandDark = brand.tokens.map((t: any) => `  --ascend-${t.name}: ${t.darkValue};`).join('\n')

  const light = `:root {
${lightGroups.join('\n')}

  /* Semantic */
${semanticToCss('light')}

  /* Brand */
${brandLight}

  /* Shadows */
${shadowLight}
}`

  const dark = `[data-theme='dark'] {
${darkGroups.join('\n')}

  /* Semantic */
${semanticToCss('dark')}

  /* Brand */
${brandDark}

  /* Shadows */
${shadowDark}
}`

  return { light, dark }
}

export function generateFullCss(): string {
  const { light, dark } = generateCss()
  return `${light}\n\n${dark}\n`
}
