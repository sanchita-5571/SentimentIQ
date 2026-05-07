import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import clsx from 'clsx'

export default function KPICard({
  title,
  value,
  change,
  changeType = 'neutral', // 'positive', 'negative', 'neutral'
  icon: Icon,
  className = ''
}) {
  const getChangeIcon = () => {
    switch (changeType) {
      case 'positive':
        return <TrendingUp className="w-4 h-4 text-success" />
      case 'negative':
        return <TrendingDown className="w-4 h-4 text-danger" />
      default:
        return <Minus className="w-4 h-4 text-muted-foreground" />
    }
  }

  const getChangeColor = () => {
    switch (changeType) {
      case 'positive':
        return 'text-success'
      case 'negative':
        return 'text-danger'
      default:
        return 'text-muted-foreground'
    }
  }

  return (
    <div className={clsx(
      'glass-panel rounded-[28px] border border-white/10 p-6 transition-all hover:-translate-y-1 hover:border-primary/20 hover:shadow-2xl',
      className
    )}>
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          {Icon && (
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-[linear-gradient(135deg,hsl(var(--primary)/0.18),hsl(var(--secondary)/0.18))] ring-1 ring-white/10">
              <Icon className="h-6 w-6 text-primary" />
            </div>
          )}
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">{title}</p>
            <p className="mt-2 text-3xl font-bold">{value}</p>
          </div>
        </div>
      </div>

      {change !== undefined && (
        <div className="mt-5 flex items-center gap-1 text-sm">
          {getChangeIcon()}
          <span className={clsx('text-sm font-medium', getChangeColor())}>
            {changeType === 'positive' && '+'}
            {change} from last period
          </span>
        </div>
      )}
    </div>
  )
}
