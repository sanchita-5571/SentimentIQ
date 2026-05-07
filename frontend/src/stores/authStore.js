import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const DUMMY_USER = {
  id: 'local-user',
  email: 'local@localhost',
  full_name: 'Local User',
}

export const useAuthStore = create(
  persist(
    (set) => ({
      user: DUMMY_USER,
      token: null,
      isAuthenticated: false,
      loading: false,
      error: null,
      login: async ({ email } = {}) => {
        // In this app, auth is handled via API calls in pages.
        // This method exists to keep a consistent store API.
        if (email) {
          set({ user: { ...DUMMY_USER, email } })
        }
        return true
      },
      logout: () => {
        set({ isAuthenticated: false, token: null })
      },
      setAuth: ({ token, user, isAuthenticated = true } = {}) => {
        set({ token, user: user || DUMMY_USER, isAuthenticated })
      },
      clearError: () => set({ error: null }),
      resetAuth: () => {
        set({
          user: DUMMY_USER,
          token: null,
          isAuthenticated: false,
          loading: false,
          error: null,
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

