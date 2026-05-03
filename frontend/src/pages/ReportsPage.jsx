import { useEffect, useState } from 'react'
import { Card, SectionTitle } from '../components/UI/Card'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'

export default function ReportsPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)
  const exportReport = useDataStore((state) => state.exportReport)
  const exporting = useDataStore((state) => state.loading.export)
  const [format, setFormat] = useState('csv')

  useEffect(() => {
    fetchSnapshot(filters)
  }, [fetchSnapshot, filters])

  return (
    <div className="space-y-6">
      <Card>
        <SectionTitle
          eyebrow="Report export"
          title="Export filtered review intelligence"
          body="Generate CSV, JSON, or Markdown report outputs from the live filtered dataset without leaving the local stack."
        />
        <div className="mt-6 flex flex-wrap gap-3">
          {['csv', 'json', 'markdown'].map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => setFormat(option)}
              className={`rounded-full border px-4 py-2 text-sm transition ${
                format === option
                  ? 'border-primary bg-primary text-primary-foreground'
                  : 'border-border bg-muted/50 text-foreground hover:bg-muted'
              }`}
            >
              {option.toUpperCase()}
            </button>
          ))}
        </div>
        <button
          type="button"
          disabled={exporting}
          onClick={() =>
            exportReport({
              format,
              search: filters.search || null,
              start_date: filters.start_date || null,
              end_date: filters.end_date || null,
              source: filters.source || null,
              sentiment_label: filters.sentiment_label || null,
              language: filters.language || null,
              product: filters.product || null,
              category: filters.category || null,
            })
          }
          className="mt-6 rounded-2xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground transition hover:bg-primary/90"
        >
          {exporting ? 'Preparing export...' : 'Download report'}
        </button>
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
