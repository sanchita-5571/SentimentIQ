import { useAuthStore } from '../stores/authStore'
import { useFilterStore } from '../stores/filterStore'
import { useUIStore } from '../stores/uiStore'

const STORAGE_KEYS = ['auth-storage', 'sentimentiq-filters', 'ui-storage', 'theme']

const clearAppStorage = () => {
  if (typeof window === 'undefined') return
  STORAGE_KEYS.forEach((key) => localStorage.removeItem(key))
}

export const resetAllStores = () => {
  if (typeof window !== 'undefined') {
    clearAppStorage()
    window.location.reload()
  }
}

export const useStoreReset = () => {
  const logout = useAuthStore((state) => state.logout)
  const resetFilters = useFilterStore((state) => state.resetFilters)
  const setSidebarOpen = useUIStore((state) => state.setSidebarOpen)
  const initTheme = useUIStore((state) => state.initTheme)

  return () => {
    logout()
    resetFilters()
    setSidebarOpen(true)
    initTheme()
    clearAppStorage()
    window.location.reload()
  }
}

