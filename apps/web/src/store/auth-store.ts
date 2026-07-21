import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface AuthState {
  builderId: string | null
  token: string | null
  username: string | null
  setAuth: (builderId: string, token: string, username: string) => void
  clearAuth: () => void
  isAuthenticated: boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      builderId: null,
      token: null,
      username: null,
      isAuthenticated: false,
      setAuth: (builderId, token, username) => set({ builderId, token, username, isAuthenticated: true }),
      clearAuth: () => set({ builderId: null, token: null, username: null, isAuthenticated: false }),
    }),
    { name: 'ascend-auth' }
  )
)
