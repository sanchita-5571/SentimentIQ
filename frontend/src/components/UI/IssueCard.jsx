import { motion } from 'framer-motion'
import { TrendingUp, TrendingDown, AlertCircle } from 'lucide-react'
import { Badge } from './badge' // Shadcn badge

export default function IssueCard({ issue }) {
  const TrendIcon = issue.trend > 0 ? TrendingUp : TrendingDown
  const trendColor = issue.trend > 0 ? 'from-emerald-400/30 to-primary/30 text-emerald-300' : 'from-rose-500/30 to-orange-400/30 text-rose-200'

  return (
    <motion.div 
      whileHover={{ y: -2 }}
      className="glass-panel group rounded-[28px] border border-white/10 p-6 shadow-sm transition-all duration-200 hover:border-white/20 hover:shadow-lg"
    >
      <div className="flex items-start gap-4">
        <div className={`flex-shrink-0 rounded-2xl bg-gradient-to-br ${trendColor} p-3 shadow-sm ring-1 ring-white/10`}>
          <TrendIcon className="h-6 w-6" />
        </div>
        <div className="flex-1">
          <div className="flex items-start gap-2 mb-2">
            <h3 className="font-semibold text-lg">{issue.title}</h3>
            <Badge variant="secondary" className="border-white/10 bg-white/5 uppercase">{issue.severity}</Badge>
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
