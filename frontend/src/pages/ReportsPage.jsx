import { useEffect, useMemo, useState } from 'react'
import { Card, SectionTitle } from '../components/UI/Card'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'
import ExportModal from '../components/UI/ExportModal'

export default function ReportsPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)
  const fetchRootCauses = useDataStore((state) => state.fetchRootCauses)
  const exportReport = useDataStore((state) => state.exportReport)
  const exporting = useDataStore((state) => state.loading.export)

  const [isExportModalOpen, setIsExportModalOpen] = useState(false)

  useEffect(() => {
    fetchSnapshot(filters)
    fetchRootCauses()
  }, [fetchSnapshot, fetchRootCauses, filters])

  const basePayload = useMemo(() => {
    return {
      search: filters.search || null,
      start_date: filters.start_date || null,
      end_date: filters.end_date || null,
      source: filters.source || null,
      sentiment_label: filters.sentiment_label || null,
      language: filters.language || null,
      product: filters.product || null,
      category: filters.category || null,
    }
  }, [filters])

  return (
    <div className="space-y-6">
      <Card>
        <SectionTitle
          eyebrow="Report export"
          title="Export dashboard analysis as PDF"
          body="Generate a PDF summary of the current dashboard analysis, including trend summaries, issues, alerts, and root-cause findings."
        />

        <div className="mt-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div className="text-sm text-muted-foreground">
            Current filters are applied to the PDF export.
          </div>
          <button
            type="button"
            disabled={exporting}
            onClick={() => setIsExportModalOpen(true)}
            className="rounded-2xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90 disabled:opacity-50"
          >
            {exporting ? 'Preparing PDF...' : 'Export PDF report'}
          </button>
        </div>

        <ExportModal
          isOpen={isExportModalOpen}
          onClose={() => setIsExportModalOpen(false)}
          title="Export PDF report"
          onExport={async () => {
            return exportReport({
              title: 'SentimentIQ Dashboard Analysis Report',
              filters: basePayload,
            })
          }}
        />
      </Card>

      <Card>
        <SectionTitle eyebrow="Snapshot" title="Current export context" />
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-border bg-muted/40 p-4">
            <p className="text-sm text-muted-foreground">Total reviews</p>
            <p className="mt-2 text-3xl font-semibold text-foreground">{snapshot?.overview?.total_reviews ?? 0}</p>
          </div>
          <div className="rounded-2xl border border-border bg-muted/40 p-4">
            <p className="text-sm text-muted-foreground">Average sentiment</p>
            <p className="mt-2 text-3xl font-semibold text-foreground">
              {Math.round((snapshot?.overview?.average_sentiment ?? 0) * 100)}%
            </p>
          </div>
          <div className="rounded-2xl border border-border bg-muted/40 p-4">
            <p className="text-sm text-muted-foreground">Negative ratio</p>
            <p className="mt-2 text-3xl font-semibold text-foreground">
              {Math.round((snapshot?.overview?.negative_ratio ?? 0) * 100)}%
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}
