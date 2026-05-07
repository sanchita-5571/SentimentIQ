import { useEffect, useState } from 'react'
import { Download } from 'lucide-react'
import { Card, SectionTitle } from '../components/UI/Card'
import { Button } from '../components/UI/button'
import { Badge } from '../components/UI/badge'
import { Skeleton } from '../components/UI/Skeleton'
import { useDataStore } from '../stores/dataStore'

export default function HistoryPage() {
  const dashboardHistory = useDataStore((state) => state.dashboardHistory)
  const dashboardHistoryLoading = useDataStore((state) => state.dashboardHistoryLoading)
  const fetchDashboardHistory = useDataStore((state) => state.fetchDashboardHistory)
  const exportDashboardHistoryEntry = useDataStore((state) => state.exportDashboardHistoryEntry)

  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchDashboardHistory(searchTerm || undefined)
  }, [fetchDashboardHistory, searchTerm])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Reset App History</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          View and export dashboard snapshots that were saved when the app was reset.
        </p>
      </div>

      <Card className="p-6">
        <input
          type="text"
          placeholder="Search reset history..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
        />
      </Card>

      <Card className="p-6">
        <SectionTitle
          eyebrow="Dashboard snapshots"
          title="Reset app history"
          body={`${dashboardHistory.length} snapshot${dashboardHistory.length !== 1 ? 's' : ''} stored`}
        />

        <div className="space-y-3 max-h-[560px] overflow-y-auto">
          {dashboardHistoryLoading ? (
            <>
              <Skeleton className="h-20 rounded-lg" />
              <Skeleton className="h-20 rounded-lg" />
              <Skeleton className="h-20 rounded-lg" />
            </>
          ) : dashboardHistory.length ? (
            dashboardHistory.map((entry) => {
              const overview = entry.snapshot?.overview
              const totalReviews = overview?.total_reviews ?? 0
              const negRatio = Math.round((overview?.negative_ratio ?? 0) * 100)
              const avgSent = Number(overview?.average_sentiment ?? 0).toFixed(2)

              return (
                <div
                  key={entry.id}
                  className="rounded-lg border border-border p-4 text-left hover:bg-accent/40 transition"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="min-w-0 flex-1">
                      <p className="font-medium truncate">
                        {entry.batch_id ? `Batch ${entry.batch_id.slice(0, 8)}` : 'Current filters'}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {new Date(entry.created_at).toLocaleDateString()} {new Date(entry.created_at).toLocaleTimeString()}
                      </p>
                      <p className="mt-1 text-xs text-muted-foreground">
                        Filters: {Object.keys(entry.filters || {}).length ? Object.entries(entry.filters).map(([key, value]) => `${key}: ${value}`).join(', ') : 'None'}
                      </p>
                      <div className="mt-3 grid grid-cols-3 gap-2">
                        <div className="rounded-md border border-border px-2 py-1">
                          <p className="text-[11px] text-muted-foreground">Reviews</p>
                          <p className="text-sm font-semibold">{totalReviews}</p>
                        </div>
                        <div className="rounded-md border border-border px-2 py-1">
                          <p className="text-[11px] text-muted-foreground">Avg</p>
                          <p className="text-sm font-semibold">{avgSent}</p>
                        </div>
                        <div className="rounded-md border border-border px-2 py-1">
                          <p className="text-[11px] text-muted-foreground">Neg%</p>
                          <p className="text-sm font-semibold">{negRatio}%</p>
                        </div>
                      </div>
                      <div className="mt-3 flex flex-wrap gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => exportDashboardHistoryEntry(entry)}
                        >
                          <Download className="mr-2 h-4 w-4" />
                          Export PDF
                        </Button>
                      </div>
                    </div>
                    <Badge variant="secondary" className="shrink-0">
                      Saved
                    </Badge>
                  </div>
                </div>
              )
            })
          ) : (
            <div className="rounded-lg border border-dashed border-border p-8 text-center text-sm text-muted-foreground">
              No dashboard snapshots stored yet. Use <b>Reset app</b> to save the current dashboard to history.
            </div>
          )}
        </div>
      </Card>
    </div>
  )
}

