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
    <Card className="w-full p-6">
      <SectionTitle
        eyebrow="Ingestion"
        title="Load customer reviews from CSV, JSON, or manual entry"
        body="Flexible parsing: use 'content'/'review'/'text' columns. Or any text fields. No strict headers needed."
      />
      <div className="grid gap-4 lg:grid-cols-2 2xl:grid-cols-3">
        <label className="rounded-3xl border border-dashed border-info/30 bg-info/5 p-5">
          <span className="mb-3 block text-sm font-medium text-info">CSV upload</span>
          <input
            type="file"
            accept=".csv"
            className="block w-full text-sm text-muted-foreground"
            disabled={ingestLoading}
            onChange={(event) => event.target.files?.[0] && uploadCsv(event.target.files[0], filters)}
          />
        </label>
        <label className="rounded-3xl border border-dashed border-neutral/30 bg-neutral/5 p-5">
          <span className="mb-3 block text-sm font-medium text-neutral">JSON upload</span>
          <input
            type="file"
            accept=".json"
            className="block w-full text-sm text-muted-foreground"
            disabled={ingestLoading}
            onChange={(event) => event.target.files?.[0] && uploadJson(event.target.files[0], filters)}
          />
        </label>
        <form onSubmit={handleManualSubmit} className="space-y-3 rounded-3xl border border-border bg-muted/40 p-5 lg:col-span-2 2xl:col-span-1">
          <p className="text-sm font-medium text-foreground">Manual input</p>
          <input
            className="w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
            placeholder="Author"
            value={manual.author}
            onChange={(event) => setManual((state) => ({ ...state, author: event.target.value }))}
          />
          <input
            className="w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
            placeholder="Product"
            value={manual.product}
            onChange={(event) => setManual((state) => ({ ...state, product: event.target.value }))}
          />
          {/* Capture the optional metadata fields so manual ingestion is as complete as file-based ingestion. */}
          <div className="grid gap-3 sm:grid-cols-2">
            <input
              className="w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
              placeholder="Category"
              value={manual.category}
              onChange={(event) => setManual((state) => ({ ...state, category: event.target.value }))}
            />
            <input
              type="number"
              min="0"
              max="5"
              step="0.5"
              className="w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
              placeholder="Rating"
              value={manual.rating}
              onChange={(event) => setManual((state) => ({ ...state, rating: event.target.value }))}
            />
          </div>
          <textarea
            className="min-h-28 w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
            placeholder="Paste one review here"
            value={manual.content}
            onChange={(event) => setManual((state) => ({ ...state, content: event.target.value }))}
          />
          <button
            type="submit"
            disabled={ingestLoading || !manual.content.trim()}
            className="w-full rounded-2xl bg-primary/90 hover:bg-primary text-foreground font-semibold px-4 py-3 text-sm transition disabled:cursor-not-allowed disabled:opacity-50"
          >
            {ingestLoading ? 'Processing...' : 'Analyze review'}
          </button>
        </form>
      </div>
    </Card>
  )
}
