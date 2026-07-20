'use client'

import { type ReactNode } from 'react'
import { useLayoutStore } from '@/store/layout-store'
import { useMotion } from '@/components/motion'
import { AnimatePresence, motion } from 'framer-motion'

interface AppShellSlots {
  topbar?: ReactNode
  sidebar?: ReactNode
  workspace: ReactNode
  rightPanel?: ReactNode
  overlay?: ReactNode
}

export function AppShell({ topbar, sidebar, workspace, rightPanel, overlay }: AppShellSlots) {
  const sidebarCollapsed = useLayoutStore((s) => s.sidebar.collapsed)
  const sidebarOpen = useLayoutStore((s) => s.sidebar.open)
  const rightPanelOpen = useLayoutStore((s) => s.rightPanel.open)
  const layoutMode = useLayoutStore((s) => s.layoutMode)
  const focusMode = useLayoutStore((s) => s.workspace.focusMode)
  const { reducedMotion } = useMotion()

  const isMobile = layoutMode === 'mobile'
  const sidebarVisible = sidebarOpen && !focusMode && !isMobile
  const sidebarWidth = sidebarCollapsed ? 'var(--ascend-sidebar-width-collapsed)' : 'var(--ascend-sidebar-width)'
  const topbarVisible = !focusMode

  return (
    <div className="flex h-screen w-full overflow-hidden">
      {/* Sidebar */}
      {sidebar && (
        <AnimatePresence mode="wait">
          {sidebarVisible && (
            <motion.aside
              initial={false}
              animate={{
                width: sidebarWidth,
              }}
              transition={{ duration: reducedMotion ? 0 : 0.2, ease: [0, 0, 0.2, 1] }}
              className="flex-shrink-0 overflow-hidden border-r"
              style={{ borderColor: 'var(--ascend-border)' }}
            >
              {sidebar}
            </motion.aside>
          )}
        </AnimatePresence>
      )}

      {/* Main area */}
      <div className="flex flex-1 flex-col overflow-hidden">
        {/* TopBar */}
        {topbar && topbarVisible && (
          <motion.header
            initial={false}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: reducedMotion ? 0 : 0.2 }}
            className="flex-shrink-0 border-b"
            style={{ borderColor: 'var(--ascend-border)' }}
          >
            {topbar}
          </motion.header>
        )}

        {/* Workspace */}
        <main className="flex-1 overflow-auto">
          {workspace}
        </main>
      </div>

      {/* Right Panel */}
      {rightPanel && (
        <AnimatePresence>
          {rightPanelOpen && (
            <motion.aside
              initial={{ width: 0, opacity: 0 }}
              animate={{ width: 'var(--ascend-panel-width, 320px)', opacity: 1 }}
              exit={{ width: 0, opacity: 0 }}
              transition={{ duration: reducedMotion ? 0 : 0.2, ease: [0, 0, 0.2, 1] }}
              className="flex-shrink-0 overflow-hidden border-l"
              style={{ borderColor: 'var(--ascend-border)' }}
            >
              {rightPanel}
            </motion.aside>
          )}
        </AnimatePresence>
      )}

      {/* Overlay */}
      {overlay}
    </div>
  )
}
