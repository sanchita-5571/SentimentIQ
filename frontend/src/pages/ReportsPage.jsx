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
              className={`rounded-full px-4 py-2 text-sm ${
                format === option ? 'bg-cyan-300 text-slate-950' : 'bg-white/5 text-slate-200'
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
              start_date: filters.start_date || null,
              end_date: filters.end_date || null,
              source: filters.source || null,
              sentiment_label: filters.sentiment_label || null,
              product: filters.product || null,
              category: filters.category || null,
            })
          }
          className="mt-6 rounded-2xl bg-orange-300 px-5 py-3 text-sm font-semibold text-slate-950"
        >
          {exporting ? 'Preparing export...' : 'Download report'}
        </button>
      </Card>

      <Card>
        <SectionTitle eyebrow="Snapshot" title="Current export context" />
        <div className="grid gap-4 md:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4">
            <p className="text-sm text-slate-300">Total reviews</p>
            <p className="mt-2 text-3xl font-semibold text-white">{snapshot?.overview?.total_reviews ?? 0}</p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4">
            <p className="text-sm text-slate-300">Average sentiment</p>
            <p className="mt-2 text-3xl font-semibold text-white">
              {Math.round((snapshot?.overview?.average_sentiment ?? 0) * 100)}%
            </p>
          </div>
          <div className="rounded-2xl border border-white/10 bg-slate-900/60 p-4">
            <p className="text-sm text-slate-300">Negative ratio</p>
            <p className="mt-2 text-3xl font-semibold text-white">
              {Math.round((snapshot?.overview?.negative_ratio ?? 0) * 100)}%
            </p>
          </div>
        </div>
      </Card>
    </div>
  )
}
