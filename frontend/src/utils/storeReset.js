import { useFilterStore } from '../stores/filterStore'
import { useUIStore } from '../stores/uiStore'

const STORAGE_KEYS = ['sentimentiq-filters', 'ui-storage', 'theme']


const clearAppStorage = () => {
  if (typeof window === 'undefined') return
  STORAGE_KEYS.forEach((key) => localStorage.removeItem(key))
}

const reloadWithoutQuery = () => {
  if (typeof window === 'undefined') return
  const cleanUrl = `${window.location.origin}${window.location.pathname}`
  window.location.replace(cleanUrl)
}

export const resetAllStores = () => {
  if (typeof window !== 'undefined') {
    clearAppStorage()
    reloadWithoutQuery()
  }
}

export const useStoreReset = () => {
  const resetFilters = useFilterStore((state) => state.resetFilters)

  const setSidebarOpen = useUIStore((state) => state.setSidebarOpen)
  const initTheme = useUIStore((state) => state.initTheme)

  // Keep: snapshot/history needs to be cleared from Dashboard view.
  // Navbar Reset app already clears dashboard state before calling this.
  return () => {
    resetFilters()

    setSidebarOpen(true)
    initTheme()
    clearAppStorage()
    reloadWithoutQuery()
  }
}

