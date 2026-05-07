import { useEffect, useMemo, useState } from 'react'
import { Area, ComposedChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis, Bar } from 'recharts'
import { motion, AnimatePresence } from 'framer-motion'
import { AlertCircle, CheckCircle2, Zap } from 'lucide-react'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'
import { useUIStore } from '../stores/uiStore'
import FilterBar from '../components/UI/FilterBar'
import UploadPanel from '../components/UI/UploadPanel'
import StatGrid from '../components/UI/StatGrid'
import SourcePieChart from '../components/charts/SourcePieChart'
import IssueCard from '../components/UI/IssueCard'
import AlertCard from '../components/UI/AlertCard'
import { Card } from '../components/UI/Card'
import { Badge } from '../components/UI/badge'
import { Skeleton } from '../components/UI/Skeleton'

export default function DashboardPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const rootCauses = useDataStore((state) => state.rootCauses)
  const alerts = useDataStore((state) => state.alerts)
  const loading = useDataStore((state) => state.loading)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)
  const fetchRootCauses = useDataStore((state) => state.fetchRootCauses)
  const currentBatchId = useDataStore((state) => state.currentBatchId)
  const dashboardCleared = useDataStore((state) => state.dashboardCleared)
  const selectBatch = useDataStore((state) => state.selectBatch)
  const refreshInterval = useUIStore((state) => state.refreshInterval)
  const [dismissedAlertIds, setDismissedAlertIds] = useState([])

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    const batchId = urlParams.get('batch_id')
    if (batchId && batchId !== currentBatchId) {
      selectBatch(batchId)
    }
  }, [selectBatch, currentBatchId])

  useEffect(() => {
    fetchSnapshot(filters)

    const safeInterval = Math.max(Number(refreshInterval) || 15, 5) * 1000
    const interval = window.setInterval(() => fetchSnapshot(filters), safeInterval)
    return () => window.clearInterval(interval)
  }, [fetchSnapshot, filters, refreshInterval, currentBatchId])

  useEffect(() => {
    fetchRootCauses()
  }, [fetchRootCauses, currentBatchId])

  const issueData = useMemo(
    () =>
      (snapshot?.aspect_trends || []).map((item) => ({
        id: item.aspect,
        title: item.aspect,
        description: `${item.mention_count} mentions with an average score of ${item.average_score?.toFixed?.(2) ?? item.average_score}.`,
        severity: item.delta <= -0.2 ? 'high' : item.delta <= -0.1 ? 'medium' : 'low',
        mentions: item.mention_count,
        trend: Math.round((item.delta || 0) * 100),
      })),
    [snapshot],
  )

  const aspectDistribution = useMemo(
    () =>
      (snapshot?.aspect_trends || []).slice(0, 5).map((item) => ({
        name: item.aspect,
        value: item.mention_count,
      })),
    [snapshot],
  )

  const visibleAlerts = useMemo(
    () => alerts.filter((alert) => !dismissedAlertIds.includes(alert.id)),
    [alerts, dismissedAlertIds],
  )

  const overview = snapshot?.overview
  const totalReviews = overview?.total_reviews?.toLocaleString?.() || '0'
  const negativeRatio = Math.round((overview?.negative_ratio || 0) * 100)
  const averageSentiment = Number(overview?.average_sentiment || 0).toFixed(2)

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      <Card className="overflow-hidden p-8 lg:p-10">
        <div className="grid gap-8 lg:grid-cols-[1.45fr_0.8fr] lg:items-end">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.32em] text-primary/80">Realtime Intelligence</p>
            <h2 className="mt-4 max-w-3xl text-4xl font-bold leading-tight lg:text-5xl">
              A sharper cockpit for tracking customer sentiment before it becomes churn.
            </h2>
            <p className="mt-4 max-w-2xl text-base text-muted-foreground lg:text-lg">
              Monitor review velocity, uncover rising issues, and isolate the signals that need action without digging through raw exports.
            </p>
            <div className="mt-8 flex flex-wrap gap-3 text-sm">
              <Badge className="border-white/10 bg-white/5 px-4 py-2 text-foreground">
                {dashboardCleared ? 'Dashboard cleared' : 'Live feed active'}
              </Badge>
              <Badge className="border-white/10 bg-primary/10 px-4 py-2 text-primary">{totalReviews} reviews indexed</Badge>
              <Badge className="border-white/10 bg-secondary/15 px-4 py-2 text-foreground">{negativeRatio}% negative share</Badge>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-3 lg:grid-cols-1">
            <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Avg Sentiment</p>
              <p className="mt-3 text-3xl font-bold">{averageSentiment}</p>
            </div>
            <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Root Causes</p>
              <p className="mt-3 text-3xl font-bold">{rootCauses.length}</p>
            </div>
            <div className="rounded-[28px] border border-white/10 bg-white/5 p-5">
              <p className="text-xs font-semibold uppercase tracking-[0.24em] text-muted-foreground">Open Alerts</p>
              <p className="mt-3 text-3xl font-bold">{visibleAlerts.length}</p>
            </div>
          </div>
        </div>
      </Card>

      <div className="flex flex-col lg:flex-row gap-6 lg:items-center">
        <FilterBar options={snapshot?.filter_options} />
        <UploadPanel />
      </div>

      {dashboardCleared && !currentBatchId && !loading.snapshot && (
        <Card className="p-8 text-center">
          <h3 className="text-xl font-semibold">Dashboard is cleared</h3>
          <p className="mt-2 text-sm text-muted-foreground">
            Upload a new CSV or JSON file to start a fresh analysis, or open a previous batch from History.
          </p>
        </Card>
      )}

      <StatGrid overview={snapshot?.overview} loading={loading.snapshot} />

      <div className="grid gap-8 lg:grid-cols-2">
        <Card className="p-8">
          <div className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Pulse</p>
            <h2 className="mt-2 text-2xl font-bold">Sentiment and Volume Trend</h2>
            <p className="text-muted-foreground">Daily average sentiment with review volume overlay</p>
          </div>
          <div className="h-96">
            {loading.snapshot ? (
              <Skeleton className="h-full rounded-lg" />
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <ComposedChart data={snapshot?.timeline || []}>
                  <CartesianGrid vertical={false} stroke="hsl(var(--muted-foreground)/0.12)" />
                  <XAxis dataKey="date" axisLine={false} tickLine={false} tickMargin={8} />
                  <YAxis yAxisId="left" axisLine={false} tickLine={false} tickMargin={8} />
                  <YAxis yAxisId="right" orientation="right" axisLine={false} tickLine={false} tickMargin={8} />
                  <Tooltip />
                  <Area
                    yAxisId="right"
                    type="monotone"
                    dataKey="review_count"
                    fill="#3b82f6"
                    fillOpacity={0.15}
                    stroke="#3b82f6"
                    name="Review volume"
                  />
                  <Bar
                    yAxisId="right"
                    dataKey="negative_reviews"
                    fill="#ef4444"
                    radius={[4, 4, 0, 0]}
                    name="Negative reviews"
                  />
                  <Area
                    yAxisId="left"
                    type="monotone"
                    dataKey="average_sentiment"
                    fill="#22c55e"
                    fillOpacity={0.08}
                    stroke="#22c55e"
                    strokeWidth={3}
                    name="Average sentiment"
                  />
                </ComposedChart>
              </ResponsiveContainer>
            )}
          </div>
        </Card>

        <Card className="p-8">
          <div className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Coverage</p>
            <h2 className="mb-2 mt-2 text-2xl font-bold">Aspect Distribution</h2>
            <p className="text-muted-foreground">Top mentioned aspects from the current filtered dataset</p>
          </div>
          <SourcePieChart data={aspectDistribution} loading={loading.snapshot} />
        </Card>
      </div>

      <Card className="p-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Friction Map</p>
            <h2 className="mt-2 text-2xl font-bold">Top Issues</h2>
            <p className="text-muted-foreground">Aspect trends with the strongest signal in the current review set</p>
          </div>
        </div>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {issueData.map((issue) => (
            <IssueCard key={issue.id} issue={issue} />
          ))}
          {loading.snapshot && (
            <>
              <Skeleton className="h-32 rounded-xl" />
              <Skeleton className="h-32 rounded-xl md:col-span-2 lg:col-span-1" />
            </>
          )}
          {!loading.snapshot && issueData.length === 0 && (
            <div className="col-span-full flex flex-col items-center justify-center py-16 text-center">
              <AlertCircle className="h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No issue trends yet</h3>
              <p className="text-muted-foreground max-w-md">
                Upload more reviews to generate aspect-level trend analysis.
              </p>
            </div>
          )}
        </div>
      </Card>

      <div className="grid gap-8 lg:grid-cols-2">
        <Card className="p-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Attention</p>
              <h2 className="mt-2 text-2xl font-bold">Recent Alerts</h2>
              <p className="text-muted-foreground">Notifications derived from root-cause events</p>
            </div>
            <Badge variant="secondary" className="border-white/10 bg-white/5 uppercase">Live</Badge>
          </div>
          <div className="space-y-4">
              <AnimatePresence>
              {visibleAlerts.slice(0, 3).map((alert) => (
                <AlertCard
                  key={alert.id}
                  alert={alert}
                  onResolve={(id) => setDismissedAlertIds((current) => [...current, id])}
                  onIgnore={(id) => setDismissedAlertIds((current) => [...current, id])}
                />
              ))}
            </AnimatePresence>
            {loading.rootCauses && (
              <>
                <Skeleton className="h-24 rounded-xl" />
                <Skeleton className="h-24 rounded-xl" />
              </>
            )}
            {!loading.rootCauses && visibleAlerts.length === 0 && (
              <div className="flex flex-col items-center justify-center py-16 text-center">
                <CheckCircle2 className="h-12 w-12 text-emerald-500 mb-4" />
                <h3 className="text-lg font-semibold mb-2">No active alerts</h3>
                <p className="text-muted-foreground">Everything looks good</p>
              </div>
            )}
          </div>
        </Card>

        <Card className="p-8">
          <div className="mb-6">
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-primary/80">Diagnosis</p>
            <h2 className="mt-2 text-2xl font-bold">Root Causes</h2>
            <p className="text-muted-foreground">Recent sentiment drop events</p>
          </div>
          <div className="space-y-4">
            {rootCauses.slice(0, 4).map((event, index) => (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="rounded-[28px] border border-white/10 bg-white/5 p-5 hover:bg-white/[0.07]"
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className="h-2 w-2 rounded-full bg-destructive" />
                  <span className="text-xs uppercase tracking-wider font-medium text-destructive">Detected</span>
                </div>
                <h4 className="font-semibold">{event.earliest_degrading_aspect || 'General'}</h4>
                <p className="text-sm text-muted-foreground mb-3">
                  {event.sentiment_delta > 0 ? '+' : ''}{event.sentiment_delta?.toFixed(2)} sentiment delta across {event.review_volume} reviews
                </p>
                <div className="text-xs text-muted-foreground">
                  {event.event_date ? new Date(event.event_date).toLocaleDateString() : 'Undated'}
                </div>
              </motion.div>
            ))}
            {!loading.rootCauses && !rootCauses.length && (
              <div className="flex flex-col items-center justify-center py-16 text-center">
                <Zap className="h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No root causes detected</h3>
                <p className="text-muted-foreground">Sentiment is stable across the filtered review set</p>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}
