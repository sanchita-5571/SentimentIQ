import { useState } from 'react'
import { Card, SectionTitle } from './Card'
import { useDataStore } from '../../stores/dataStore'
import { useFilterStore } from '../../stores/filterStore'

const manualTemplate = {
  source: 'manual',
  author: '',
  product: '',
  category: '',
  rating: '',
  content: '',
}

export default function UploadPanel() {
  const filters = useFilterStore((state) => state.filters)
  const uploadCsv = useDataStore((state) => state.uploadCsv)
  const uploadJson = useDataStore((state) => state.uploadJson)
  const submitManual = useDataStore((state) => state.submitManual)
  const ingestLoading = useDataStore((state) => state.loading.ingest)
  const [manual, setManual] = useState(manualTemplate)

  const handleManualSubmit = async (event) => {
    event.preventDefault()
    await submitManual(
      [
        {
          ...manual,
          rating: manual.rating ? Number(manual.rating) : null,
        },
      ],
      filters,
    )
    setManual(manualTemplate)
  }

  return (
    <Card>
      <SectionTitle
        eyebrow="Ingestion"
        title="Load customer reviews from CSV, JSON, or a single manual entry"
        body="Every upload is cleaned, deduplicated, language-tagged, sentiment-scored, aspect-extracted, and topic-clustered."
      />
      <div className="grid gap-4 xl:grid-cols-3">
        <label className="rounded-3xl border border-dashed border-cyan-300/30 bg-cyan-400/5 p-5">
          <span className="mb-3 block text-sm font-medium text-cyan-100">CSV upload</span>
          <input
            type="file"
            accept=".csv"
            className="block w-full text-sm text-slate-300"
            disabled={ingestLoading}
            onChange={(event) => event.target.files?.[0] && uploadCsv(event.target.files[0], filters)}
          />
        </label>
        <label className="rounded-3xl border border-dashed border-orange-300/30 bg-orange-400/5 p-5">
          <span className="mb-3 block text-sm font-medium text-orange-100">JSON upload</span>
          <input
            type="file"
            accept=".json"
            className="block w-full text-sm text-slate-300"
            disabled={ingestLoading}
            onChange={(event) => event.target.files?.[0] && uploadJson(event.target.files[0], filters)}
          />
        </label>
        <form onSubmit={handleManualSubmit} className="space-y-3 rounded-3xl border border-white/10 bg-slate-900/60 p-5">
          <p className="text-sm font-medium text-white">Manual input</p>
          <input
            className="w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-white"
            placeholder="Author"
            value={manual.author}
            onChange={(event) => setManual((state) => ({ ...state, author: event.target.value }))}
          />
          <input
            className="w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-white"
            placeholder="Product"
            value={manual.product}
            onChange={(event) => setManual((state) => ({ ...state, product: event.target.value }))}
          />
          <textarea
            className="min-h-28 w-full rounded-2xl border border-white/10 bg-slate-950/70 px-4 py-3 text-sm text-white"
            placeholder="Paste one review here"
            value={manual.content}
            onChange={(event) => setManual((state) => ({ ...state, content: event.target.value }))}
          />
          <button
            type="submit"
            disabled={ingestLoading || !manual.content.trim()}
            className="w-full rounded-2xl bg-cyan-300 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {ingestLoading ? 'Processing...' : 'Analyze review'}
          </button>
        </form>
      </div>
    </Card>
  )
}
