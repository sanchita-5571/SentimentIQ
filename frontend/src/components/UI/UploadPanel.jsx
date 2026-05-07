import { useState } from 'react'
import { Card, SectionTitle } from './Card'
import { useDataStore } from '../../stores/dataStore'
import { useFilterStore } from '../../stores/filterStore'

export default function UploadPanel() {
  const filters = useFilterStore((state) => state.filters)
  const uploadCsv = useDataStore((state) => state.uploadCsv)
  const uploadJson = useDataStore((state) => state.uploadJson)
  const ingestLoading = useDataStore((state) => state.loading.ingest)
  const [selectedCsvName, setSelectedCsvName] = useState('')
  const [selectedCsvSizeMb, setSelectedCsvSizeMb] = useState(0)

  const handleCsvChange = (event) => {
    const file = event.target.files?.[0]
    if (!file) {
      return
    }
    setSelectedCsvName(file.name)
    setSelectedCsvSizeMb(Number((file.size / (1024 * 1024)).toFixed(1)))
    uploadCsv(file, filters)
  }

  return (
    <Card className="w-full p-6">
      <SectionTitle
        eyebrow="Ingestion"
        title="Load customer reviews from CSV or JSON files (bulk only)"
        body="Flexible parsing: use 'content'/'review'/'text' columns. Or any text fields. No strict headers needed."
      />
      <div className="grid gap-4 lg:grid-cols-2">
        <label className="rounded-3xl border border-dashed border-info/30 bg-info/5 p-5">
          <span className="mb-3 block text-sm font-medium text-info">CSV upload</span>
          <input
            type="file"
            accept=".csv"
            className="block w-full text-sm text-muted-foreground"
            disabled={ingestLoading}
            onChange={handleCsvChange}
          />
          {selectedCsvName ? (
            <p className="mt-3 text-xs text-muted-foreground">
              {selectedCsvName} ({selectedCsvSizeMb} MB)
            </p>
          ) : null}
          {selectedCsvSizeMb > 25 ? (
            <p className="mt-2 text-xs text-amber-300">
              Large CSV detected. First-time analysis can take a few minutes while reviews are parsed and scored.
            </p>
          ) : null}
          {ingestLoading ? (
            <p className="mt-2 text-xs text-info">
              Uploading and analyzing reviews. Please keep this tab open until the import completes.
            </p>
          ) : null}
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
      </div>
    </Card>
  )
}
