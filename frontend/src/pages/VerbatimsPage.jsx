import { useDeferredValue, useEffect } from 'react'
import FilterBar from '../components/UI/FilterBar'
import ReviewTable from '../components/UI/ReviewTable'
import { Card, SectionTitle } from '../components/UI/Card'
import { useDataStore } from '../stores/dataStore'
import { useFilterStore } from '../stores/filterStore'

export default function VerbatimsPage() {
  const filters = useFilterStore((state) => state.filters)
  const deferredFilters = useDeferredValue(filters)
  const snapshot = useDataStore((state) => state.snapshot)
  const reviews = useDataStore((state) => state.reviews)
  const loading = useDataStore((state) => state.loading.reviews)
  const reviewMeta = useDataStore((state) => state.reviewMeta)
  const fetchSnapshot = useDataStore((state) => state.fetchSnapshot)
  const fetchReviews = useDataStore((state) => state.fetchReviews)

  useEffect(() => {
    fetchSnapshot(deferredFilters)
    fetchReviews(deferredFilters, reviewMeta.page || 1, reviewMeta.page_size || 20)
  }, [deferredFilters, fetchReviews, fetchSnapshot, reviewMeta.page, reviewMeta.page_size])

  return (
    <div className="space-y-6">
      <FilterBar options={snapshot?.filter_options} />
      <Card>
        <SectionTitle
          eyebrow="Verbatims explorer"
          title="Dynamic review table"
          body="The table rendering is database-driven, tied to the same global filters as the charts, and tuned for fast scan-through of negative verbatims."
        />
        <p className="text-sm text-slate-300">
          Showing {reviews.length} of {reviewMeta.total} reviews.
        </p>
      </Card>
      <ReviewTable
        reviews={reviews}
        loading={loading}
        reviewMeta={reviewMeta}
        onPageChange={(nextPage) => fetchReviews(deferredFilters, nextPage, reviewMeta.page_size || 20)}
      />
    </div>
  )
}
