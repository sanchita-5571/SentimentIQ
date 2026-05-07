import { useEffect, useState } from 'react'
import { Card, SectionTitle } from '../components/UI/Card'
import ReviewTable from '../components/UI/ReviewTable'
import FilterBar from '../components/UI/FilterBar'
import { Button } from '../components/UI/button'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'

export default function ReviewsExplorerPage() {
  const filters = useFilterStore((state) => state.filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const reviews = useDataStore((state) => state.reviews)
  const reviewMeta = useDataStore((state) => state.reviewMeta)
  const loading = useDataStore((state) => state.loading.reviews)
  const error = useDataStore((state) => state.error)
  const fetchReviews = useDataStore((state) => state.fetchReviews)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)
  const currentBatchId = useDataStore((state) => state.currentBatchId)
  const [page, setPage] = useState(1)

  useEffect(() => {
    setPage(1)
  }, [filters])

  useEffect(() => {
    fetchSnapshot(filters)
  }, [fetchSnapshot, filters, currentBatchId])

  useEffect(() => {
    fetchReviews(filters, page)
  }, [fetchReviews, filters, page, currentBatchId])

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-3xl font-bold">Reviews Explorer</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            Search through the ingested review set using the same filters that drive the dashboard.
          </p>
        </div>
        <Button variant="outline" onClick={() => fetchReviews(filters, page)}>
          Refresh results
        </Button>
      </div>

      <FilterBar options={snapshot?.filter_options} />

      <Card className="p-6">
        <SectionTitle
          eyebrow="Dataset"
          title="Filtered review results"
          body={`Showing ${reviewMeta.total || 0} reviews across page ${reviewMeta.page || 1}.`}
        />
        {error ? (
          <div className="mb-4 rounded-2xl border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
            {error}
          </div>
        ) : null}
        <ReviewTable
          reviews={reviews}
          loading={loading}
          reviewMeta={reviewMeta}
          onPageChange={setPage}
        />
      </Card>
    </div>
  )
}
