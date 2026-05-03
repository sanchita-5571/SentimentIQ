import { useEffect, useMemo, useState } from 'react'
import { Bell } from 'lucide-react'
import { motion } from 'framer-motion'
import { Button } from '../components/UI/button'
import { Card, SectionTitle } from '../components/UI/Card'
import AlertCard from '../components/UI/AlertCard'
import { Skeleton } from '../components/UI/Skeleton'
import { Badge } from '../components/UI/badge'
import { useDataStore } from '../stores/dataStore'

export default function AlertsPage() {
  const alerts = useDataStore((state) => state.alerts)
  const loading = useDataStore((state) => state.loading.rootCauses)
  const fetchRootCauses = useDataStore((state) => state.fetchRootCauses)
  const [dismissedIds, setDismissedIds] = useState([])

  useEffect(() => {
    fetchRootCauses()
  }, [fetchRootCauses])

  const visibleAlerts = useMemo(
    () => alerts.filter((alert) => !dismissedIds.includes(alert.id)),
    [alerts, dismissedIds],
  )

  const dismissAlert = (id) => setDismissedIds((current) => [...current, id])
  const clearAll = () => setDismissedIds(alerts.map((alert) => alert.id))

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-bold">Alerts</h1>
          <Badge variant="secondary" className="text-sm">Derived from root-cause events</Badge>
        </div>
        <Button variant="outline" onClick={clearAll} disabled={!visibleAlerts.length}>
          Dismiss visible alerts
        </Button>
      </div>

      <Card className="p-8">
        <SectionTitle
          eyebrow="Monitoring"
          title="Recent alert feed"
          body="This feed is currently generated from the root-cause engine until dedicated alert endpoints are added."
        />
        <div className="space-y-4">
          {loading ? (
            Array.from({ length: 4 }).map((_, index) => (
              <Skeleton key={index} className="h-24 rounded-xl" />
            ))
          ) : visibleAlerts.length ? (
            visibleAlerts.map((alert) => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onResolve={dismissAlert}
                onIgnore={dismissAlert}
              />
            ))
          ) : (
            <motion.div
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex flex-col items-center justify-center py-20 text-center"
            >
              <Bell className="mb-6 h-16 w-16 text-muted-foreground" />
              <h3 className="text-2xl font-bold mb-3">No active alerts</h3>
              <p className="max-w-md text-muted-foreground">
                Your sentiment monitoring is quiet right now. New events will appear here after the next root-cause run.
              </p>
            </motion.div>
          )}
        </div>
      </Card>
    </div>
  )
}
