import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { QueryProvider } from '@/providers/query-provider'
import { ThemeProvider } from '@/components/theme/theme-provider'
import { LayoutProvider } from '@/components/layout/layout-provider'
import { AppShell } from '@/components/layout/app-shell'
import { ThemeInspector } from '@/components/dev/theme-inspector'
import '../../../../packages/tokens/src/generated/tokens.css'
import './globals.css'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

export const metadata: Metadata = {
  title: 'ASCEND',
  description: 'Competency Development Framework',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        <QueryProvider>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            <LayoutProvider>
              <AppShell
                workspace={children}
              />
              {process.env.NODE_ENV === 'development' && <ThemeInspector />}
            </LayoutProvider>
          </ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  )
}
