import { create } from 'zustand'
import toast from 'react-hot-toast'
import { dashboardApi, getErrorMessage, reportsApi, reviewsApi, rootCauseApi } from '../api/client'

const serializeFilters = (filters) =>
  Object.fromEntries(Object.entries(filters).filter(([, value]) => value !== '' && value !== null))

const deriveAlertsFromRootCauses = (events) =>
  (events || []).map((event) => ({
    id: event.id,
    title: event.earliest_degrading_aspect
      ? `${event.earliest_degrading_aspect} sentiment drop detected`
      : 'Sentiment drop detected',
    message: `Sentiment changed by ${event.sentiment_delta?.toFixed?.(2) ?? event.sentiment_delta} across ${event.review_volume ?? 0} reviews.`,
    severity:
      event.sentiment_delta <= -0.35
        ? 'high'
        : event.sentiment_delta <= -0.2
          ? 'medium'
          : 'low',
    timestamp: event.event_date || event.created_at,
    source: event.amplification_chain?.[0] || event.earliest_degrading_aspect || 'Root cause engine',
  }))

export const useDataStore = create((set, get) => ({
  snapshot: null,
  reviews: [],
  reviewMeta: { total: 0, page: 1, page_size: 20 },
  rootCauses: [],
  alerts: [],
  loading: {
    snapshot: false,
    reviews: false,
    rootCauses: false,
    ingest: false,
    export: false,
  },
  error: null,
  fetchSnapshot: async (filters) => {
    set((state) => ({ loading: { ...state.loading, snapshot: true }, error: null }))
    try {
      const response = await dashboardApi.snapshot(serializeFilters(filters))
      set((state) => ({ snapshot: response.data, loading: { ...state.loading, snapshot: false } }))
    } catch (error) {
      set((state) => ({
        loading: { ...state.loading, snapshot: false },
        error: getErrorMessage(error) || 'Failed to load dashboard',
      }))
    }
  },
  fetchReviews: async (filters, page = 1, pageSize = 20) => {
    set((state) => ({ loading: { ...state.loading, reviews: true }, error: null }))
    try {
      const response = await reviewsApi.list({ ...serializeFilters(filters), page, page_size: pageSize })
      set((state) => ({
        reviews: response.data.items,
        reviewMeta: response.data,
        loading: { ...state.loading, reviews: false },
      }))
    } catch (error) {
      set((state) => ({
        loading: { ...state.loading, reviews: false },
        error: getErrorMessage(error) || 'Failed to load reviews',
      }))
    }
  },
  fetchRootCauses: async () => {
    set((state) => ({ loading: { ...state.loading, rootCauses: true }, error: null }))
    try {
      const response = await rootCauseApi.list()
      set((state) => ({
        rootCauses: response.data,
        alerts: deriveAlertsFromRootCauses(response.data),
        loading: { ...state.loading, rootCauses: false },
      }))
    } catch (error) {
      set((state) => ({
        loading: { ...state.loading, rootCauses: false },
        error: getErrorMessage(error) || 'Failed to load root-cause events',
      }))
    }
  },
  uploadCsv: async (file, filters) => {
    const formData = new FormData()
    formData.append('file', file)
    set((state) => ({ loading: { ...state.loading, ingest: true } }))
    try {
      const response = await reviewsApi.uploadCsv(formData)
      toast.success(`Imported ${response.data.created_count} reviews, skipped ${response.data.duplicate_count} duplicates`)
      set((state) => ({ loading: { ...state.loading, ingest: false } }))
      await get().fetchSnapshot(filters)
      await get().fetchReviews(filters)
      await get().fetchRootCauses()
    } catch (error) {
      set((state) => ({ loading: { ...state.loading, ingest: false } }))
      toast.error(getErrorMessage(error) || 'CSV upload failed')
    }
  },
  uploadJson: async (file, filters) => {
    const formData = new FormData()
    formData.append('file', file)
    set((state) => ({ loading: { ...state.loading, ingest: true } }))
    try {
      const response = await reviewsApi.uploadJson(formData)
      toast.success(`Imported ${response.data.created_count} reviews, skipped ${response.data.duplicate_count} duplicates`)
      set((state) => ({ loading: { ...state.loading, ingest: false } }))
      await get().fetchSnapshot(filters)
      await get().fetchReviews(filters)
      await get().fetchRootCauses()
    } catch (error) {
      set((state) => ({ loading: { ...state.loading, ingest: false } }))
      toast.error(getErrorMessage(error) || 'JSON upload failed')
    }
  },
  submitManual: async (payload, filters) => {
    set((state) => ({ loading: { ...state.loading, ingest: true } }))
    try {
      const response = await reviewsApi.manual({ reviews: payload })
      toast.success(`Processed ${response.data.processed_count} manual reviews`)
      set((state) => ({ loading: { ...state.loading, ingest: false } }))
      await get().fetchSnapshot(filters)
      await get().fetchReviews(filters)
      await get().fetchRootCauses()
    } catch (error) {
      set((state) => ({ loading: { ...state.loading, ingest: false } }))
      toast.error(getErrorMessage(error) || 'Manual ingestion failed')
    }
  },
  rebuildRootCauses: async () => {
    try {
      const response = await rootCauseApi.rebuild()
      await get().fetchRootCauses()
      toast.success(`Root-cause engine recomputed: ${response.data.recomputed} events`)
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Rebuild failed')
    }
  },
  exportReport: async (payload) => {
    set((state) => ({ loading: { ...state.loading, export: true } }))
    try {
      const response = await reportsApi.export(payload)
      const blob = new Blob([response.data], { type: response.headers['content-type'] })
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      const disposition = response.headers['content-disposition']
      const filenameMatch = disposition?.match(/filename="([^"]+)"/)
      anchor.href = url
      anchor.download = filenameMatch?.[1] || `sentimentiq-report.${payload.format}`
      anchor.click()
      URL.revokeObjectURL(url)
      toast.success('Report exported')
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Export failed')
    } finally {
      set((state) => ({ loading: { ...state.loading, export: false } }))
    }
  },
}))
