import { motion } from 'framer-motion'
import { AlertCircle, AlertTriangle, Bell, Clock } from 'lucide-react'
import { Button } from './button'
import { Badge } from './badge'

const severityColors = {
  high: { bg: 'bg-negative', icon: AlertCircle },
  medium: { bg: 'bg-neutral', icon: AlertTriangle },
  low: { bg: 'bg-info', icon: Bell },
  critical: { bg: 'bg-critical', icon: AlertCircle },
}

export default function AlertCard({ alert, onResolve = () => {}, onIgnore = () => {} }) {
  const palette = severityColors[alert.severity || 'low'] || severityColors.low
  const Icon = palette.icon

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-panel group rounded-[28px] border border-white/10 p-6 shadow-sm transition-all duration-200 hover:border-white/20 hover:shadow-md"
    >
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <div className={`${palette.bg} rounded-2xl p-3 flex-shrink-0 ring-1 ring-white/10`}>
          <Icon className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="mb-2 flex items-start gap-2">
            <h3 className="text-lg font-semibold leading-tight">{alert.title}</h3>
            <Badge className={`${palette.bg} border-white/10`}>{alert.severity?.toUpperCase() || 'LOW'}</Badge>
          </div>
          <p className="mb-4 text-sm text-muted-foreground">{alert.message}</p>
          <div className="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
            <span className="inline-flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {alert.timestamp ? new Date(alert.timestamp).toLocaleString() : 'Unknown time'}
            </span>
            <span>&bull;</span>
            <span>{alert.source}</span>
          </div>
        </div>
        {}
        <div className="flex flex-wrap gap-2 sm:ml-4 sm:opacity-0 sm:transition-opacity sm:group-hover:opacity-100 sm:group-focus-within:opacity-100">
          <Button type="button" variant="outline" size="sm" onClick={() => onResolve(alert.id)}>
            Resolve
          </Button>
          <Button type="button" variant="ghost" size="sm" onClick={() => onIgnore(alert.id)}>
            Ignore
          </Button>
        </div>
      </div>
    </motion.div>
  )
}
