import { Suspense } from 'react'
import { Outlet } from 'react-router-dom'
import { motion } from 'framer-motion'
import Navbar from './Navbar'
import Sidebar from './Sidebar'
import { Bell } from 'lucide-react'
import { useUIStore } from '../../stores/uiStore'
import { useDataStore } from '../../stores/dataStore'
import { Skeleton } from '../UI/Skeleton'

export default function Layout() {
  const mobileMenuOpen = useUIStore((state) => state.mobileMenuOpen)
  const toggleMobileMenu = useUIStore((state) => state.toggleMobileMenu)
  const alerts = useDataStore((state) => state.alerts)

  const recentActivity = alerts.slice(0, 3)

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,hsl(var(--primary)/0.16),transparent_26%),radial-gradient(circle_at_78%_12%,hsl(var(--secondary)/0.14),transparent_20%),linear-gradient(180deg,hsl(var(--background)),hsl(var(--background)))]" />
        <div className="absolute inset-0 bg-sentiment-grid opacity-[0.08]" />
        <div className="absolute inset-0 bg-sentiment-noise opacity-[0.18]" />
      </div>

      <div className="relative flex min-h-screen flex-col">
        <Navbar />

        <div className="flex flex-1 overflow-hidden">
          <Sidebar />

          <div className="flex min-w-0 flex-1 flex-col">
            <motion.main
              key="main"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className="relative flex-1 overflow-y-auto p-4 sm:p-6 xl:p-8"
            >
              <Suspense
                fallback={
                  <div className="mx-auto flex max-w-7xl flex-col gap-6">
                    <Skeleton className="h-14 rounded-3xl" />
                    <Skeleton className="h-40 rounded-3xl" />
                    <Skeleton className="h-96 rounded-3xl" />
                  </div>
                }
              >
                <Outlet />
              </Suspense>
            </motion.main>
          </div>

          <aside className="hidden w-80 shrink-0 border-l border-white/10 bg-background/40 backdrop-blur-2xl 2xl:block">
            <div className="sticky top-0 p-6">
              <p className="mb-2 text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Live Feed</p>
              <h3 className="mb-4 text-lg font-semibold">Recent Activity</h3>
              <div className="space-y-3 text-sm">
                {recentActivity.length ? (
                  recentActivity.map((alert) => (
                    <div
                      key={alert.id}
                      className="glass-panel flex items-center gap-3 rounded-2xl border border-white/10 p-3 hover:border-primary/30"
                    >
                      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 ring-1 ring-primary/20">
                        <Bell className="h-5 w-5 text-primary" />
                      </div>
                      <div className="min-w-0">
                        <p className="truncate font-medium">{alert.title}</p>
                        <p className="text-xs text-muted-foreground">
                          {alert.timestamp ? new Date(alert.timestamp).toLocaleString() : 'Awaiting timestamp'}
                        </p>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="rounded-2xl border border-dashed border-white/10 p-4 text-muted-foreground">
                    Recent alerts and root-cause activity will appear here as the dataset changes.
                  </div>
                )}
              </div>
            </div>
          </aside>
        </div>
      </div>

      {mobileMenuOpen && (
        <div 
          className="fixed inset-0 z-40 bg-slate-950/30 backdrop-blur-sm lg:hidden"
          onClick={toggleMobileMenu}
        />
      )}
    </div>
  )
}
