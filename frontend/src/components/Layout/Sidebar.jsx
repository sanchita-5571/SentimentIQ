import { NavLink } from 'react-router-dom'
import { Activity, BarChart3, Download, GitBranchPlus, MessageSquareQuote } from 'lucide-react'

const items = [
  { to: '/', label: 'Overview', icon: Activity },
  { to: '/trends', label: 'Trend Analytics', icon: BarChart3 },
  { to: '/root-causes', label: 'Root Cause', icon: GitBranchPlus },
  { to: '/verbatims', label: 'Verbatims', icon: MessageSquareQuote },
  { to: '/reports', label: 'Exports', icon: Download },
]

export default function Sidebar() {
  return (
    <aside className="hidden w-72 flex-col border-r border-white/10 bg-slate-950/70 p-6 backdrop-blur xl:flex">
      <div className="mb-10">
        <p className="text-xs uppercase tracking-[0.35em] text-cyan-300">SentimentIQ</p>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight text-white">Review intelligence</h1>
        <p className="mt-3 text-sm text-slate-300">
          Trace the earliest aspect drift, quantify the amplification chain, and ship fixes faster.
        </p>
      </div>
      <nav className="space-y-2">
        {items.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-2xl px-4 py-3 text-sm transition ${
                isActive
                  ? 'bg-cyan-400/15 text-cyan-200 shadow-[0_0_0_1px_rgba(34,211,238,0.2)]'
                  : 'text-slate-300 hover:bg-white/5 hover:text-white'
              }`
            }
          >
            <Icon className="h-4 w-4" />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
