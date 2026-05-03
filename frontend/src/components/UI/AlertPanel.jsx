import { useState } from 'react'
import {
  AlertTriangle,
  X,
  CheckCircle,
  Clock,
  AlertCircle,
  Info
} from 'lucide-react'
import clsx from 'clsx'

export default function AlertPanel({
  alerts = [],
  onDismiss,
  onAcknowledge,
  onResolve,
  className = ''
}) {
  const [expandedAlert, setExpandedAlert] = useState(null)

  const getAlertIcon = (type) => {
    switch (type) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5 text-danger" />
      case 'high':
        return <AlertCircle className="w-5 h-5 text-warning" />
      case 'medium':
        return <Info className="w-5 h-5 text-info" />
      default:
        return <Info className="w-5 h-5 text-muted-foreground" />
    }
  }

  const getAlertColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'border-danger bg-danger/5'
      case 'high':
        return 'border-warning bg-warning/5'
      case 'medium':
        return 'border-info bg-info/5'
      default:
        return 'border-muted bg-muted/50'
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'resolved':
        return <CheckCircle className="w-4 h-4 text-success" />
      case 'acknowledged':
        return <Clock className="w-4 h-4 text-info" />
      default:
        return <AlertCircle className="w-4 h-4 text-muted-foreground" />
    }
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
  }

  if (alerts.length === 0) {
    return (
      <div className={clsx(
        'bg-card rounded-lg border border-border p-6 text-center',
        className
      )}>
        <Info className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
        <h3 className="text-lg font-medium mb-2">No Active Alerts</h3>
        <p className="text-muted-foreground">
          All systems are running smoothly. You&apos;ll see alerts here when issues are detected.
        </p>
      </div>
    )
  }

  return (
    <div className={clsx('space-y-4', className)}>
      {alerts.map((alert) => (
        <div
          key={alert.id}
          className={clsx(
            'border rounded-lg p-4 transition-all',
            getAlertColor(alert.severity),
            expandedAlert === alert.id && 'shadow-md'
          )}
        >
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3 flex-1">
              {getAlertIcon(alert.severity)}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-medium">{alert.title}</h4>
                  {getStatusIcon(alert.status)}
                  <span className="text-xs text-muted-foreground capitalize">
                    {alert.status}
                  </span>
                </div>

                <p className="text-sm text-muted-foreground mb-2">
                  {alert.message}
                </p>

                <div className="flex items-center gap-4 text-xs text-muted-foreground">
                  <span>Type: {alert.alert_type}</span>
                  <span>Severity: {alert.severity}</span>
                  <span>{formatDate(alert.created_at)}</span>
                </div>

                {expandedAlert === alert.id && (
                  <div className="mt-4 pt-4 border-t border-border">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium">Threshold:</span> {alert.threshold_value}
                      </div>
                      <div>
                        <span className="font-medium">Actual:</span> {alert.actual_value}
                      </div>
                      {alert.source_type && (
                        <div>
                          <span className="font-medium">Source:</span> {alert.source_type}
                        </div>
                      )}
                      {alert.source_id && (
                        <div>
                          <span className="font-medium">Source ID:</span> {alert.source_id}
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setExpandedAlert(
                  expandedAlert === alert.id ? null : alert.id
                )}
                className="p-1 rounded hover:bg-muted text-muted-foreground"
                title={expandedAlert === alert.id ? 'Collapse' : 'Expand'}
              >
                <Info className="w-4 h-4" />
              </button>

              {alert.status === 'active' && (
                <>
                  <button
                    onClick={() => onAcknowledge?.(alert)}
                    className="px-3 py-1 text-xs bg-info/10 text-info rounded hover:bg-info/20"
                  >
                    Acknowledge
                  </button>
                  <button
                    onClick={() => onResolve?.(alert)}
                    className="px-3 py-1 text-xs bg-success/10 text-success rounded hover:bg-success/20"
                  >
                    Resolve
                  </button>
                </>
              )}

              <button
                onClick={() => onDismiss?.(alert)}
                className="p-1 rounded hover:bg-muted text-muted-foreground hover:text-danger"
                title="Dismiss"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
