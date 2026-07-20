export interface Token {
  name: string
  value: string
  description: string
  category: TokenCategory
}

export type TokenCategory =
  | 'primitive'
  | 'semantic'
  | 'brand'
  | 'component'
  | 'motion'

export interface TokenGroup {
  category: TokenCategory
  prefix: string
  tokens: Token[]
}

export type ThemeMode = 'light' | 'dark'

export interface Theme {
  mode: ThemeMode
  tokens: Record<string, string>
}
