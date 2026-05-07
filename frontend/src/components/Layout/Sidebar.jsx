import { NavLink } from 'react-router-dom'
import { useUIStore } from '../../stores/uiStore'
import { cn } from '../../lib/utils'
import { Home, BarChart3, FileText, Settings, AlertTriangle, SearchCheck, FileBarChart2, Clock } from 'lucide-react'

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
    { to: '/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <aside className={cn(
      'fixed inset-y-16 left-0 z-30 w-64 border-r border-border bg-background transition-transform duration-200 ease-in-out lg:static lg:inset-auto lg:block lg:h-auto lg:translate-x-0 lg:shrink-0',
      
      mobileMenuOpen || sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
    )}>
      <div className="h-full overflow-y-auto lg:sticky lg:top-0">
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
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-muted hover:text-foreground'
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
      </div>
    </aside>
  )
}
