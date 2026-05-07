import { useEffect, useState } from 'react'
import { Trash2, RotateCcw, Eye } from 'lucide-react'
import { Card, SectionTitle } from '../components/UI/Card'
import { Button } from '../components/UI/button'
import { Badge } from '../components/UI/badge'
import { Skeleton } from '../components/UI/Skeleton'
import { useDataStore } from '../stores/dataStore'

export default function HistoryPage() {
  const history = useDataStore((state) => state.history)
  const currentBatchId = useDataStore((state) => state.currentBatchId)
  const historyLoading = useDataStore((state) => state.historyLoading)
  const fetchBatches = useDataStore((state) => state.fetchBatches)
  const selectBatch = useDataStore((state) => state.selectBatch)
  const deleteBatch = useDataStore((state) => state.deleteBatch)
  const rerunBatch = useDataStore((state) => state.rerunBatch)
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    fetchBatches(searchTerm || undefined)
  }, [fetchBatches])

  const handleSearch = (term) => {
    setSearchTerm(term)
    fetchBatches(term || undefined)
  }

  const selectedBatch = history.find((b) => b.batch_id === currentBatchId)

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Analysis History</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          View, compare, and rerun previous file uploads and analyses.
        </p>
      </div>

      <Card className="p-6">
        <input
          type="text"
          placeholder="Search by file name or source..."
          value={searchTerm}
          onChange={(e) => handleSearch(e.target.value)}
          className="w-full rounded-2xl border border-input bg-background px-4 py-3 text-sm text-foreground"
        />
      </Card>

      <div className="grid gap-6 lg:grid-cols-[0.7fr,1.3fr]">
        <Card className="p-6">
          <SectionTitle
            eyebrow="Uploads"
            title="Previous batches"
            body={`${history.length} upload${history.length !== 1 ? 's' : ''} total`}
          />
          <div className="space-y-3 max-h-[600px] overflow-y-auto">
            {historyLoading ? (
              <>
                <Skeleton className="h-20 rounded-lg" />
                <Skeleton className="h-20 rounded-lg" />
                <Skeleton className="h-20 rounded-lg" />
              </>
            ) : history.length ? (
              history.map((batch) => (
                <button
                  key={batch.batch_id}
                  type="button"
                  onClick={() => selectBatch(batch.batch_id)}
                  className={`w-full rounded-lg border p-4 text-left text-sm transition ${
                    selectedBatch?.batch_id === batch.batch_id
                      ? 'border-primary bg-primary/5'
                      : 'border-border hover:bg-accent'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">{batch.file_name || `Batch ${batch.batch_id.slice(0, 8)}`}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {batch.created_count} reviews
                        {batch.duplicate_count > 0 && `, ${batch.duplicate_count} duplicates`}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(batch.created_at).toLocaleDateString()} {new Date(batch.created_at).toLocaleTimeString()}
                      </p>
                    </div>
                    <Badge variant="secondary" className="shrink-0">{batch.source}</Badge>
                  </div>
                </button>
              ))
            ) : (
              <div className="rounded-lg border border-dashed border-border p-8 text-center text-sm text-muted-foreground">
                No uploads yet. Start by uploading a CSV or JSON file.
              </div>
            )}
          </div>
        </Card>

        <Card className="p-6">
          <SectionTitle
            eyebrow="Details"
            title={selectedBatch?.file_name || 'Select a batch'}
            body={selectedBatch ? `Uploaded ${new Date(selectedBatch.created_at).toLocaleDateString()}` : 'Choose an upload to see details'}
          />
          {selectedBatch ? (
            <div className="space-y-6">
              <div className="grid gap-4 sm:grid-cols-2">
                <Metric label="Reviews created" value={String(selectedBatch.created_count)} />
                <Metric label="Duplicates skipped" value={String(selectedBatch.duplicate_count)} />
                <Metric label="Total processed" value={String(selectedBatch.processed_count)} />
                <Metric label="Source" value={selectedBatch.source} />
              </div>

              <div className="space-y-3">
                <h3 className="font-semibold">Actions</h3>
                <div className="flex flex-col gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="justify-start"
                    onClick={() => {

                      window.location.href = `/?batch_id=${selectedBatch.batch_id}`
                    }}
                  >
                    <Eye className="h-4 w-4 mr-2" />
                    View reviews from this upload
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="justify-start"
                    onClick={() => rerunBatch(selectedBatch.batch_id)}
                  >
                    <RotateCcw className="h-4 w-4 mr-2" />
                    Re-run analysis
                  </Button>
                  <Button
                    variant="destructive"
                    size="sm"
                    className="justify-start"
                    onClick={() => {
                      if (window.confirm('Delete this batch and all its reviews?')) {
                        deleteBatch(selectedBatch.batch_id)
                        selectBatch(null)
                      }
                    }}
                  >
                    <Trash2 className="h-4 w-4 mr-2" />
                    Delete batch
                  </Button>
                </div>
              </div>
            </div>
          ) : (
            <div className="rounded-lg border border-dashed border-border p-8 text-sm text-muted-foreground text-center">
              Select a batch from the list to view details and take actions.
            </div>
          )}
        </Card>
      </div>
    </div>
  )
}

function Metric({ label, value }) {
  return (
    <div className="rounded-lg border border-border p-3">
      <p className="text-xs text-muted-foreground">{label}</p>
      <p className="mt-1 font-semibold text-base">{value}</p>
    </div>
  )
}
