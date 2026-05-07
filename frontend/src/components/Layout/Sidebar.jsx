import { NavLink } from 'react-router-dom'
import { useUIStore } from '../../stores/uiStore'
import { cn } from '../../lib/utils'
import { Home, BarChart3, FileText, AlertTriangle, SearchCheck, FileBarChart2, Clock } from 'lucide-react'

export default function Sidebar() {
  const sidebarOpen = useUIStore((state) => state.sidebarOpen)
  const mobileMenuOpen = useUIStore((state) => state.mobileMenuOpen)
  const setSidebarOpen = useUIStore((state) => state.setSidebarOpen)
  const setMobileMenuOpen = useUIStore((state) => state.setMobileMenuOpen)

  const navItems = [
    { to: '/', icon: Home, label: 'Dashboard' },
    { to: '/reviews-explorer', icon: FileText, label: 'Reviews' },
    { to: '/sentiment-trends', icon: BarChart3, label: 'Trends' },
    { to: '/root-cause-analysis', icon: SearchCheck, label: 'Root Cause' },
    { to: '/history', icon: Clock, label: 'History' },
    { to: '/reports', icon: FileBarChart2, label: 'Reports' },
    { to: '/alerts', icon: AlertTriangle, label: 'Alerts' },
  ]

  return (
    <aside className={cn(
      'fixed inset-y-20 left-4 z-30 w-[272px] rounded-[28px] border border-white/10 bg-background/70 shadow-2xl shadow-slate-950/20 backdrop-blur-2xl transition-transform duration-200 ease-in-out lg:static lg:inset-auto lg:m-4 lg:mr-0 lg:block lg:h-[calc(100vh-6rem)] lg:translate-x-0 lg:shrink-0',
      
      mobileMenuOpen || sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    )}>
      <div className="h-full overflow-y-auto lg:sticky lg:top-0">
      <div className="border-b border-white/10 px-5 py-5">
        <p className="text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Navigation</p>
        <h2 className="mt-2 text-lg font-semibold">Command Center</h2>
      </div>
      <nav className="flex flex-col gap-2 p-4">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            onClick={() => {

              setMobileMenuOpen(false)
              setSidebarOpen(true)
            }}
            className={({ isActive }) => cn(
              'relative flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-medium transition-all',
              isActive
                ? 'bg-[linear-gradient(135deg,hsl(var(--primary)),hsl(var(--secondary)))] text-slate-950 shadow-[0_18px_50px_rgba(15,23,42,0.28)]'
                : 'text-muted-foreground hover:bg-white/5 hover:text-foreground'
            )}

          >
            <span className={cn(
              'flex h-9 w-9 items-center justify-center rounded-xl transition-colors',
              'bg-white/5 ring-1 ring-white/10',
            )}>
              <Icon className="h-4 w-4" />
            </span>
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>
      </div>
    </aside>
  )
}
