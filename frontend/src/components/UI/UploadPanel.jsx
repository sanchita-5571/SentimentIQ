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
        title="Drop raw customer feedback and turn it into live signal"
        body="Bulk CSV and JSON uploads are parsed flexibly, so even messy exports can land cleanly in the dashboard."
      />
      <div className="grid gap-4 lg:grid-cols-2">
        <label className="rounded-[28px] border border-dashed border-primary/35 bg-primary/5 p-5 transition hover:bg-primary/10">
          <span className="mb-3 block text-sm font-semibold uppercase tracking-[0.22em] text-primary">CSV upload</span>
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
            <p className="mt-2 text-xs text-amber-400">
              Large CSV detected. First-time analysis can take a few minutes while reviews are parsed and scored.
            </p>
          ) : null}
          {ingestLoading ? (
            <p className="mt-2 text-xs text-primary">
              Uploading and analyzing reviews. Please keep this tab open until the import completes.
            </p>
          ) : null}
        </label>
        <label className="rounded-[28px] border border-dashed border-secondary/35 bg-secondary/5 p-5 transition hover:bg-secondary/10">
          <span className="mb-3 block text-sm font-semibold uppercase tracking-[0.22em] text-secondary">JSON upload</span>
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
