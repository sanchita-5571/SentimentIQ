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
      'bg-card rounded-lg border border-border p-6 transition-all hover:shadow-md',
      className
    )}>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {Icon && <Icon className="w-8 h-8 text-primary" />}
          <div>
            <p className="text-sm font-medium text-muted-foreground">{title}</p>
            <p className="text-2xl font-bold">{value}</p>
          </div>
        </div>
      </div>

      {change !== undefined && (
        <div className="flex items-center gap-1 mt-4">
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