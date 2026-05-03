import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useFilterStore } from '../../stores/filterStore'
import { useDataStore } from '../../stores/dataStore'
import { useUIStore } from '../../stores/uiStore'
import { useStoreReset } from '../../utils/storeReset'
import { Bell, Search, Sun, Moon, User, Menu, ChevronDown } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

export default function Navbar() {
  const [profileOpen, setProfileOpen] = useState(false)
  const [notifOpen, setNotifOpen] = useState(false)
  const profileRef = useRef(null)
  const notifRef = useRef(null)
  const navigate = useNavigate()
  const resetStores = useStoreReset()
  
  const { darkMode, toggleDarkMode, toggleMobileMenu } = useUIStore()
  const filters = useFilterStore((state) => state.filters)
  const setFilter = useFilterStore((state) => state.setFilter)
  const resetFilters = useFilterStore((state) => state.resetFilters)
  const alerts = useDataStore((state) => state.alerts)
  const activeFilterCount = Object.values(filters).filter(Boolean).length

  const handleSearch = (e) => {
    const query = e.target.value
    setFilter('search', query)
  }

  useEffect(() => {
    // Close open popovers when focus shifts elsewhere so keyboard and mouse users are not trapped in stale menus.
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
    <header className="sticky top-0 z-40 border-b border-border/70 bg-background/95 backdrop-blur-xl supports-[backdrop-filter:blur(20px)]:bg-background/80">
      <div className="flex h-16 items-center gap-4 px-4 sm:px-6 xl:px-8">
        <div className="flex min-w-0 items-center gap-4 lg:gap-6">
          {/* Logo */}
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-gradient-to-r from-primary to-secondary p-1.5">
              <SentimentIQLogo className="h-6 w-6 text-primary-foreground" />
            </div>
            <div>
              <h1 className="text-xl font-bold tracking-tight lg:block hidden">SentimentIQ</h1>
              <p className="text-xs uppercase tracking-wide text-muted-foreground hidden lg:block">Live Dashboard</p>
            </div>
          </div>

          {/* Global Search */}
          <div className="hidden lg:block lg:w-72 xl:w-[26rem]">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search reviews, alerts..."
                value={filters.search}
                onChange={handleSearch}
                className="w-full rounded-xl border border-input bg-background px-10 py-2.5 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
              />
            </div>
          </div>

          {/* Mobile menu button */}
          <button
            type="button"
            onClick={toggleMobileMenu}
            className="rounded-lg p-2 hover:bg-accent lg:hidden"
            aria-label="Open navigation menu"
          >
            <Menu className="h-5 w-5" />
          </button>
        </div>

        {/* Right side actions */}
        <div className="ml-auto flex shrink-0 items-center gap-2 lg:gap-3">
          {/* Filters badge */}
          {activeFilterCount > 0 && (
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              className="hidden md:block rounded-full bg-destructive/10 px-3 py-1.5 text-xs font-medium text-destructive"
            >
              {activeFilterCount} filters
            </motion.div>
          )}

          {/* Notifications */}
          <div ref={notifRef} className="relative">
            <button
              type="button"
              onClick={() => setNotifOpen(!notifOpen)}
              className="relative p-2 rounded-lg hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring"
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
                  className="absolute right-0 top-full mt-2 w-80 bg-background border border-border rounded-xl shadow-2xl z-50"
                >
                  <div className="p-4 border-b border-border rounded-t-xl">
                    <h3 className="font-semibold text-foreground">Notifications</h3>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {alerts.length ? (
                      alerts.slice(0, 4).map((alert) => (
                        <div key={alert.id} className="p-4 border-b border-border hover:bg-accent">
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

          {/* Theme toggle */}
          <button
            type="button"
            onClick={toggleDarkMode}
            className="p-2 rounded-lg hover:bg-accent data-[state=checked]:bg-accent"
            title={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>

          {/* Profile */}
          <div ref={profileRef} className="relative">
            <button
              type="button"
              onClick={() => setProfileOpen(!profileOpen)}
              className="flex items-center gap-2 rounded-xl border border-border bg-card px-3 py-2 hover:bg-accent focus:outline-none focus:ring-2 focus:ring-ring"
              aria-expanded={profileOpen}
            >
              <div className="h-8 w-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center">
                <User className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="hidden sm:block text-sm font-medium">Admin</span>
              <ChevronDown className="h-4 w-4" />
            </button>
            <AnimatePresence>
              {profileOpen && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95, y: -8 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95, y: -8 }}
                  className="absolute right-0 top-full mt-2 w-48 bg-background border border-border rounded-xl shadow-2xl z-50 py-1"
                >
                  <div className="px-4 py-2 text-sm text-muted-foreground border-b border-border">
                    Admin User
                  </div>
                  {/* Wire the profile actions so the dropdown does not expose dead buttons. */}
                  <button
                    type="button"
                    onClick={() => {
                      setProfileOpen(false)
                      resetFilters()
                    }}
                    className="w-full px-4 py-2 text-sm text-left hover:bg-accent rounded-none"
                  >
                    Clear filters
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setProfileOpen(false)
                      navigate('/settings')
                    }}
                    className="w-full px-4 py-2 text-sm text-left hover:bg-accent rounded-none"
                  >
                    Settings
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setProfileOpen(false)
                      resetStores()
                    }}
                    className="w-full px-4 py-2 text-sm text-left hover:bg-accent rounded-none border-t border-border"
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

// Simple logo component
function SentimentIQLogo({ className }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
    </svg>
  )
}
