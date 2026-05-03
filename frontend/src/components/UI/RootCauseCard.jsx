import { useState } from 'react'
import {
  GitBranch,
  ChevronDown,
  ChevronRight,
  AlertTriangle,
  TrendingDown,
  Users,
  Calendar
} from 'lucide-react'
import clsx from 'clsx'

export default function RootCauseCard({
  rootCause,
  onViewDetails,
  className = ''
}) {
  const [isExpanded, setIsExpanded] = useState(false)

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'text-critical border-critical bg-critical/10'
      case 'high':
        return 'text-negative border-negative bg-negative/10'
      case 'medium':
        return 'text-neutral border-neutral bg-neutral/10'
      case 'low':
        return 'text-info border-info bg-info/10'
      default:
        return 'text-muted-foreground border-muted bg-muted/20'
    }
  }

  const getPriorityIcon = (priority) => {
    switch (priority) {
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-negative" />
      case 'medium':
        return <TrendingDown className="w-4 h-4 text-neutral" />
      default:
        return <GitBranch className="w-4 h-4 text-muted-foreground" />
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString()
  }

  return (
    <div className={clsx(
      'bg-card rounded-lg border border-border p-4 transition-all hover:shadow-md',
      getSeverityColor(rootCause.severity),
      className
    )}>
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-1">
          {getPriorityIcon(rootCause.priority)}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between mb-2">
            <h3 className="font-medium truncate">{rootCause.title}</h3>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-1 rounded hover:bg-muted"
            >
              {isExpanded ? (
                <ChevronDown className="w-4 h-4" />
              ) : (
                <ChevronRight className="w-4 h-4" />
              )}
            </button>
          </div>

          <p className="text-sm text-muted-foreground mb-3 line-clamp-2">
            {rootCause.description}
          </p>

          <div className="flex items-center gap-4 text-xs text-muted-foreground mb-3">
            <span className="flex items-center gap-1">
              <GitBranch className="w-3 h-3" />
              {rootCause.cause_type}
            </span>
            <span className="flex items-center gap-1">
              <Users className="w-3 h-3" />
              {rootCause.affected_reviews || 0} reviews
            </span>
            <span className="flex items-center gap-1">
              <Calendar className="w-3 h-3" />
              {formatDate(rootCause.identified_at)}
            </span>
          </div>

          {isExpanded && (
            <div className="border-t border-border pt-3 mt-3">
              <div className="grid grid-cols-2 gap-4 text-sm mb-3">
                <div>
                  <span className="font-medium">Confidence:</span>
                  <span className="ml-2">{rootCause.confidence_score || 'N/A'}</span>
                </div>
                <div>
                  <span className="font-medium">Impact:</span>
                  <span className="ml-2">{rootCause.impact_score || 'N/A'}</span>
                </div>
                <div>
                  <span className="font-medium">Status:</span>
                  <span className="ml-2 capitalize">{rootCause.status}</span>
                </div>
                <div>
                  <span className="font-medium">Priority:</span>
                  <span className="ml-2 capitalize">{rootCause.priority}</span>
                </div>
              </div>

              {rootCause.recommendations && rootCause.recommendations.length > 0 && (
                <div className="mb-3">
                  <h4 className="text-sm font-medium mb-2">Recommendations:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    {rootCause.recommendations.slice(0, 3).map((rec, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="w-1 h-1 rounded-full bg-primary mt-2 flex-shrink-0" />
                        <span className="line-clamp-1">{rec.title}</span>
                      </li>
                    ))}
                    {rootCause.recommendations.length > 3 && (
                      <li className="text-xs text-muted-foreground">
                        +{rootCause.recommendations.length - 3} more recommendations
                      </li>
                    )}
                  </ul>
                </div>
              )}

              <button
                onClick={() => onViewDetails?.(rootCause)}
                className="w-full px-3 py-2 text-sm bg-primary text-primary-foreground rounded hover:bg-primary/90"
              >
                View Details
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}