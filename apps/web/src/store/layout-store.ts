import { create } from 'zustand'

export interface Breadcrumb {
  label: string
  href?: string
}

export type LayoutMode = 'ultrawide' | 'desktop' | 'tablet' | 'mobile'

export interface LayoutState {
  sidebar: { open: boolean; collapsed: boolean; pinned: boolean }
  topbar: { transparent: boolean; hidden: boolean }
  workspace: { fullscreen: boolean; focusMode: boolean }
  rightPanel: { open: boolean; width: number }
  breadcrumbs: Breadcrumb[]
  layoutMode: LayoutMode
  reducedMotion: boolean
}

export interface LayoutActions {
  toggleSidebar: () => void
  setSidebarOpen: (open: boolean) => void
  setSidebarCollapsed: (collapsed: boolean) => void
  setSidebarPinned: (pinned: boolean) => void
  setTopbarTransparent: (transparent: boolean) => void
  setTopbarHidden: (hidden: boolean) => void
  setFullscreen: (fullscreen: boolean) => void
  setFocusMode: (focusMode: boolean) => void
  toggleRightPanel: () => void
  setRightPanelOpen: (open: boolean) => void
  setRightPanelWidth: (width: number) => void
  setBreadcrumbs: (breadcrumbs: Breadcrumb[]) => void
  setLayoutMode: (mode: LayoutMode) => void
  setReducedMotion: (reduced: boolean) => void
  reset: () => void
}

const initialState: LayoutState = {
  sidebar: { open: true, collapsed: false, pinned: false },
  topbar: { transparent: false, hidden: false },
  workspace: { fullscreen: false, focusMode: false },
  rightPanel: { open: false, width: 320 },
  breadcrumbs: [],
  layoutMode: 'desktop',
  reducedMotion: false,
}

export const useLayoutStore = create<LayoutState & LayoutActions>()(
  (set) => ({
    ...initialState,

    toggleSidebar: () =>
      set((s) => ({
        sidebar: { ...s.sidebar, open: !s.sidebar.open },
      })),

    setSidebarOpen: (open) =>
      set((s) => ({ sidebar: { ...s.sidebar, open } })),

    setSidebarCollapsed: (collapsed) =>
      set((s) => ({ sidebar: { ...s.sidebar, collapsed } })),

    setSidebarPinned: (pinned) =>
      set((s) => ({ sidebar: { ...s.sidebar, pinned } })),

    setTopbarTransparent: (transparent) =>
      set((s) => ({ topbar: { ...s.topbar, transparent } })),

    setTopbarHidden: (hidden) =>
      set((s) => ({ topbar: { ...s.topbar, hidden } })),

    setFullscreen: (fullscreen) =>
      set((s) => ({ workspace: { ...s.workspace, fullscreen } })),

    setFocusMode: (focusMode) =>
      set((s) => ({ workspace: { ...s.workspace, focusMode } })),

    toggleRightPanel: () =>
      set((s) => ({
        rightPanel: { ...s.rightPanel, open: !s.rightPanel.open },
      })),

    setRightPanelOpen: (open) =>
      set((s) => ({ rightPanel: { ...s.rightPanel, open } })),

    setRightPanelWidth: (width) =>
      set((s) => ({ rightPanel: { ...s.rightPanel, width } })),

    setBreadcrumbs: (breadcrumbs) => set({ breadcrumbs }),

    setLayoutMode: (layoutMode) => set({ layoutMode }),

    setReducedMotion: (reducedMotion) => set({ reducedMotion }),

    reset: () => set(initialState),
  })
)
