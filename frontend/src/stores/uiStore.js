import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const defaultPreferences = {
  refreshInterval: 15,
  emailAlerts: false,
  browserAlerts: true,
}

export const useUIStore = create(
  persist(
    (set, get) => ({
      sidebarOpen: true,
      mobileMenuOpen: false,
      notifications: [],
      theme: 'system',
      darkMode: false,
      ...defaultPreferences,
      
      toggleSidebar: () => set({ sidebarOpen: !get().sidebarOpen }),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      toggleMobileMenu: () => set({ mobileMenuOpen: !get().mobileMenuOpen }),
      setMobileMenuOpen: (open) => set({ mobileMenuOpen: open }),
      
      toggleDarkMode: () => {
        const newDarkMode = !get().darkMode
        set({ darkMode: newDarkMode })
        if (newDarkMode) {
          document.documentElement.classList.add('dark')
          localStorage.theme = 'dark'
        } else {
          document.documentElement.classList.remove('dark')
          localStorage.theme = 'light'
        }
      },
      setDarkMode: (dark) => {
        set({ darkMode: dark })
        if (dark) {
          document.documentElement.classList.add('dark')
          localStorage.theme = 'dark'
        } else {
          document.documentElement.classList.remove('dark')
          localStorage.theme = 'light'
        }
      },
      
      initTheme: () => {
        const savedTheme = localStorage.theme || 'system'
        const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        
        if (savedTheme === 'dark' || (savedTheme === 'system' && isDark)) {
          document.documentElement.classList.add('dark')
          set({ darkMode: true, theme: savedTheme })
        } else {
          document.documentElement.classList.remove('dark')
          set({ darkMode: false, theme: savedTheme })
        }
      },

      setRefreshInterval: (value) => set({ refreshInterval: Number(value) || defaultPreferences.refreshInterval }),
      setEmailAlerts: (value) => set({ emailAlerts: Boolean(value) }),
      setBrowserAlerts: (value) => set({ browserAlerts: Boolean(value) }),
      applyPreferences: (preferences = {}) =>
        set((state) => ({
          ...state,
          ...Object.fromEntries(
            Object.entries(preferences).filter(([, value]) => value !== undefined && value !== null),
          ),
        })),
      
      addNotification: (notif) => set({ notifications: [...get().notifications, { id: Date.now(), ...notif }] }),
      dismissNotification: (id) => set({ notifications: get().notifications.filter(n => n.id !== id) }),
      
      resetUI: () => {
        set({ 
          sidebarOpen: true, 
          mobileMenuOpen: false,
          notifications: [],
          darkMode: false, 
          theme: 'system',
          ...defaultPreferences,
        })
        document.documentElement.classList.remove('dark')
        localStorage.removeItem('theme')
      },
    }),
    {
      name: 'ui-storage',
    }
  )
)
