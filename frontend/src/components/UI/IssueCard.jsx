import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'
import { Badge } from './badge' // Shadcn badge

export default function IssueCard({ issue }) {
  const TrendIcon = issue.trend > 0 ? TrendingUp : TrendingDown
  const trendColor = issue.trend > 0 ? 'bg-positive' : 'bg-destructive'

  return (
    <motion.div 
      whileHover={{ y: -2 }}
      className="group border border-border bg-card hover:bg-accent p-6 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-200"
    >
      <div className="flex items-start gap-4">
        <div className={`${trendColor} p-3 rounded-xl flex-shrink-0 shadow-sm`}>
          <TrendIcon className="h-6 w-6 text-white" />
        </div>
        <div className="flex-1">
          <div className="flex items-start gap-2 mb-2">
            <h3 className="font-semibold text-lg">{issue.title}</h3>
            <Badge variant="secondary">{issue.severity}</Badge>
          </div>
          <p className="text-muted-foreground mb-4">{issue.description}</p>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <AlertCircle className="h-3 w-3" />
              <span>{issue.mentions} mentions</span>
            </div>
            <div className="flex items-center gap-1">
              <TrendIcon className="h-4 w-4 text-foreground" />
              <span>{issue.trend > 0 ? '+' : ''}{issue.trend}% trend</span>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}
