import { useEffect, useRef, useState } from 'react'

import { useFilterStore } from '../../stores/filterStore'
import { useDataStore } from '../../stores/dataStore'
import { useUIStore } from '../../stores/uiStore'
import { useStoreReset } from '../../utils/storeReset'
import { Bell, Sun, Moon, User, Menu, ChevronDown } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import MascotIcon from '../UI/MascotIcon'

export default function Navbar() {
  const [profileOpen, setProfileOpen] = useState(false)
  const [notifOpen, setNotifOpen] = useState(false)
  const profileRef = useRef(null)
  const notifRef = useRef(null)

  const resetStores = useStoreReset()
  const alerts = useDataStore((state) => state.alerts)
  const archiveCurrentDashboard = useDataStore((state) => state.archiveCurrentDashboard)
  const clearDashboardState = useDataStore((state) => state.clearDashboardState)

  const { darkMode, toggleDarkMode, toggleMobileMenu } = useUIStore()
  const filters = useFilterStore((state) => state.filters)
  const resetFilters = useFilterStore((state) => state.resetFilters)
  const activeFilterCount = Object.values(filters).filter(Boolean).length


  useEffect(() => {

    const handlePointerDown = (event) => {
      if (profileRef.current && !profileRef.current.contains(event.target)) {
        setProfileOpen(false)
      }
      if (notifRef.current && !notifRef.current.contains(event.target)) {
        setNotifOpen(false)
      }
    }

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        setProfileOpen(false)
        setNotifOpen(false)
      }
    }

    document.addEventListener('mousedown', handlePointerDown)
    document.addEventListener('keydown', handleEscape)
    return () => {
      document.removeEventListener('mousedown', handlePointerDown)
      document.removeEventListener('keydown', handleEscape)
    }
  }, [])

  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-background/75 backdrop-blur-2xl supports-[backdrop-filter:blur(20px)]:bg-background/60">
      <div className="flex min-h-20 items-center gap-4 px-4 sm:px-6 xl:px-8">
        <div className="flex min-w-0 items-center gap-4 lg:gap-6">
          <div className="flex items-center gap-2">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-[linear-gradient(135deg,hsl(var(--primary)/0.18),hsl(var(--secondary)/0.32))] p-1.5 ring-1 ring-white/10 shadow-lg shadow-slate-950/15">
              <MascotIcon className="h-6 w-6" />
            </div>

            <div>
              <h1 className="hidden text-xl font-bold tracking-tight lg:block">SentimentIQ</h1>
              <p className="hidden text-[11px] uppercase tracking-[0.32em] text-primary/75 lg:block">Signal Studio</p>
            </div>
          </div>

          <button
            type="button"
            onClick={toggleMobileMenu}
            className="rounded-xl border border-white/10 bg-white/5 p-2 hover:bg-accent lg:hidden"
            aria-label="Open navigation menu"
          >
            <Menu className="h-5 w-5" />
          </button>
        </div>


        <div className="ml-auto flex shrink-0 items-center gap-2 lg:gap-3">
          {activeFilterCount > 0 && (
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="hidden rounded-full border border-white/10 bg-destructive/10 px-3 py-1.5 text-xs font-medium text-destructive md:block"
            >
              {activeFilterCount} filters
            </motion.div>
          )}

          <div ref={notifRef} className="relative">
            <button
              type="button"
              onClick={() => setNotifOpen(!notifOpen)}
              className="relative rounded-xl border border-white/10 bg-white/5 p-2 hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring"
              aria-label="Toggle notifications"
              aria-expanded={notifOpen}
            >
              <Bell className="h-5 w-5" />
              {alerts.length > 0 && (
                <span className="absolute -top-1 -right-1 h-4 min-w-4 rounded-full bg-destructive px-1 text-xs flex items-center justify-center text-destructive-foreground">
                  {Math.min(alerts.length, 9)}
                </span>
              )}
            </button>
            <AnimatePresence>
              {notifOpen && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95, y: -8 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95, y: -8 }}
                  className="glass-panel absolute right-0 top-full z-50 mt-3 w-80 rounded-3xl border border-white/10 shadow-2xl"
                >
                  <div className="rounded-t-3xl border-b border-white/10 p-4">
                    <h3 className="font-semibold text-foreground">Notifications</h3>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {alerts.length ? (
                      alerts.slice(0, 4).map((alert) => (
                        <div key={alert.id} className="border-b border-white/5 p-4 hover:bg-white/5">
                          <p className="text-sm font-medium">{alert.title}</p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {alert.timestamp ? new Date(alert.timestamp).toLocaleString() : 'Unknown time'}
                          </p>
                        </div>
                      ))
                    ) : (
                      <div className="p-4 text-sm text-muted-foreground">
                        No notifications yet.
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <button
            type="button"
            onClick={toggleDarkMode}
            className="rounded-xl border border-white/10 bg-white/5 p-2 hover:bg-accent data-[state=checked]:bg-accent"
            title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>

          <div ref={profileRef} className="relative">
            <button
              type="button"
              onClick={() => setProfileOpen(!profileOpen)}
              className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-3 py-2 hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring"
              aria-expanded={profileOpen}
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[linear-gradient(135deg,hsl(var(--primary)),hsl(var(--secondary)))] text-slate-950">
                <User className="h-4 w-4" />
              </div>
              <div className="hidden text-left sm:block">
                <span className="block text-sm font-medium">SentimentIQ</span>
                <span className="block text-[11px] uppercase tracking-[0.25em] text-muted-foreground">Workspace</span>
              </div>

              <ChevronDown className="h-4 w-4" />
            </button>
            <AnimatePresence>
              {profileOpen && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95, y: -8 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95, y: -8 }}
                  className="glass-panel absolute right-0 top-full z-50 mt-3 w-52 rounded-3xl border border-white/10 py-2 shadow-2xl"
                >
                  <div className="border-b border-white/10 px-4 py-2 text-sm text-muted-foreground">
                    Workspace
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setProfileOpen(false)
                      resetFilters()
                    }}
                    className="w-full px-4 py-2 text-left text-sm hover:bg-white/5"
                  >
                    Clear filters
                  </button>

                  <button
                    type="button"
                    onClick={async () => {
                      setProfileOpen(false)

                      await archiveCurrentDashboard(useFilterStore.getState().filters)
                      clearDashboardState()
                      resetStores()
                    }}

                    className="w-full border-t border-white/10 px-4 py-2 text-left text-sm hover:bg-white/5"
                  >
                    Reset app
                  </button>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </header>
  )
}

