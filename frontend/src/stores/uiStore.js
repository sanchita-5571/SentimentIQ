import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useUIStore = create(
  persist(
    (set, get) => ({
      sidebarOpen: true,
      darkMode: false,
      theme: 'system',
      
      toggleSidebar: () => set({ sidebarOpen: !get().sidebarOpen }),
      setSidebarOpen: (open) => set({ sidebarOpen: open }),
      
      toggleDarkMode: () => set({ darkMode: !get().darkMode }),
      setDarkMode: (dark) => {
        set({ darkMode: dark })
        if (dark) {
          document.documentElement.classList.add('dark')
        } else {
          document.documentElement.classList.remove('dark')
        }
      },
      
      initTheme: () => {
        const savedTheme = get().theme
        if (savedTheme === 'dark' || (savedTheme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
          document.documentElement.classList.add('dark')
          set({ darkMode: true })
        }
      },
    }),
    {
      name: 'ui-storage',
    }
  )
)
