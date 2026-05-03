import { create } from 'zustand'
import { persist } from 'zustand/middleware'

// Dummy user for local-only access (no authentication required)
const DUMMY_USER = {
  id: 'local-user',
  email: 'local@localhost',
  full_name: 'Local User',
}

export const useAuthStore = create(
  persist(
    (set) => ({
      user: DUMMY_USER,
      token: 'dummy-token',
      isAuthenticated: true,
      loading: false,
      error: null,
      login: async () => {
        // No-op - always authenticated
        set({ isAuthenticated: true, user: DUMMY_USER })
        return true
      },
      logout: () => {
        // No-op - stay authenticated
        set({ isAuthenticated: true, user: DUMMY_USER })
      },
      clearError: () => set({ error: null }),
      resetAuth: () => {
        set({ 
          user: DUMMY_USER,
          token: 'dummy-token', 
          isAuthenticated: true,
          loading: false,
          error: null 
        })
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    },
  ),
)
