import { create } from 'zustand'
import toast from 'react-hot-toast'
import { dashboardApi, dashboardHistoryApi, getErrorMessage, reviewsApi, rootCauseApi } from '../api/client'
import { downloadAnalysisPdf } from '../utils/analysisPdf'

const defaultReviewMeta = { total: 0, page: 1, page_size: 20 }
const DASHBOARD_CLEARED_KEY = 'sentimentiq-dashboard-cleared'

const serializeFilters = (filters) =>
  Object.fromEntries(Object.entries(filters).filter(([, value]) => value !== '' && value !== null))

const readDashboardCleared = () => {
  if (typeof window === 'undefined') return false
  return window.localStorage.getItem(DASHBOARD_CLEARED_KEY) === 'true'
}

const writeDashboardCleared = (value) => {
  if (typeof window === 'undefined') return
  if (value) {
    window.localStorage.setItem(DASHBOARD_CLEARED_KEY, 'true')
    return
  }
  window.localStorage.removeItem(DASHBOARD_CLEARED_KEY)
}

const makeExportFileName = (prefix, createdAt, extension) => {
  const safeStamp = new Date(createdAt || Date.now()).toISOString().replace(/[:.]/g, '-')
  return `${prefix}-${safeStamp}.${extension}`
}

const deriveAlertsFromRootCauses = (events) =>
  (events || []).map((event) => ({
    id: event.id,
    title: event.earliest_degrading_aspect
      ? `${event.earliest_degrading_aspect} sentiment drop detected`
      : 'Sentiment drop detected',
    message: `Sentiment changed by ${event.sentiment_delta?.toFixed?.(2) ?? event.sentiment_delta} across ${
      event.review_volume ?? 0
    } reviews.`,
    severity:
      event.sentiment_delta <= -0.35 ? 'high' : event.sentiment_delta <= -0.2 ? 'medium' : 'low',
    timestamp: event.event_date || event.created_at,
    source: event.amplification_chain?.[0] || event.earliest_degrading_aspect || 'Root cause engine',
  }))

export const useDataStore = create((set, get) => ({
  snapshot: null,
  reviews: [],
  reviewMeta: defaultReviewMeta,
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
  currentBatchId: null,
  currentBatch: null,
  dashboardCleared: readDashboardCleared(),
  history: [],
  historyLoading: false,
  historyError: null,

  dashboardHistory: [],
  dashboardHistoryLoading: false,
  dashboardHistoryError: null,

  clearDashboardState: () => {
    writeDashboardCleared(true)
    set({
      snapshot: null,
      reviews: [],
      reviewMeta: defaultReviewMeta,
      rootCauses: [],
      alerts: [],
      error: null,
      currentBatchId: null,
      currentBatch: null,
      dashboardCleared: true,
    })
  },

  archiveCurrentDashboard: async (filters) => {
    const { snapshot, rootCauses, currentBatchId } = get()

    if (!snapshot) {
      return false
    }

    try {
      await dashboardHistoryApi.store({
        batch_id: currentBatchId,
        filters,
        snapshot,
        root_causes: rootCauses,
      })
      return true
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Failed to save dashboard history')
      return false
    }
  },

  exportDashboardHistoryEntry: (entry) => {
    if (!entry) return

    const filename = makeExportFileName('sentimentiq-dashboard-history', entry.created_at, 'pdf')
    downloadAnalysisPdf({
      filename,
      title: 'SentimentIQ History Analysis Report',
      snapshot: entry.snapshot,
      rootCauses: entry.root_causes,
      filters: entry.filters,
      createdAt: entry.created_at,
    })
    toast.success('Dashboard history PDF exported')
  },

  fetchDashboardHistory: async (search) => {

    set({ dashboardHistoryLoading: true, dashboardHistoryError: null })
    try {
      const params = {}
      if (search) params.search = search
      const response = await dashboardHistoryApi.list(params)
      set({ dashboardHistory: response.data || [], dashboardHistoryLoading: false })
    } catch (error) {
      set({
        dashboardHistoryLoading: false,
        dashboardHistoryError: getErrorMessage(error) || 'Failed to load dashboard history',
      })
    }
  },

  fetchSnapshot: async (filters) => {
    if (get().dashboardCleared && !get().currentBatchId) {
      set({
        snapshot: null,
        loading: { ...get().loading, snapshot: false },
      })
      return
    }

    set({ loading: { ...get().loading, snapshot: true }, error: null })
    try {
      const snapshotParams = serializeFilters(filters)
      if (get().currentBatchId) {
        snapshotParams.batch_id = get().currentBatchId
      }

      const response = await dashboardApi.snapshot(snapshotParams)
      set({ snapshot: response.data, loading: { ...get().loading, snapshot: false } })
    } catch (error) {
      set({
        loading: { ...get().loading, snapshot: false },
        error: getErrorMessage(error) || 'Failed to load dashboard',
      })
    }
  },

  fetchReviews: async (filters, page = 1, pageSize = 20) => {
    if (get().dashboardCleared && !get().currentBatchId) {
      set({
        reviews: [],
        reviewMeta: defaultReviewMeta,
        loading: { ...get().loading, reviews: false },
      })
      return
    }

    set({ loading: { ...get().loading, reviews: true }, error: null })
    try {
      const reviewParams = { ...serializeFilters(filters), page, page_size: pageSize }
      if (get().currentBatchId) {
        reviewParams.batch_id = get().currentBatchId
      }

      const response = await reviewsApi.list(reviewParams)
      set({
        reviews: response.data.items,
        reviewMeta: response.data,
        loading: { ...get().loading, reviews: false },
      })
    } catch (error) {
      set({
        loading: { ...get().loading, reviews: false },
        error: getErrorMessage(error) || 'Failed to load reviews',
      })
    }
  },

  fetchRootCauses: async () => {
    if (get().dashboardCleared && !get().currentBatchId) {
      set({
        rootCauses: [],
        alerts: [],
        loading: { ...get().loading, rootCauses: false },
      })
      return
    }

    set({ loading: { ...get().loading, rootCauses: true }, error: null })
    try {
      const params = {}
      if (get().currentBatchId) {
        params.batch_id = get().currentBatchId
      }
      const response = await rootCauseApi.list(params)
      set({
        rootCauses: response.data,
        alerts: deriveAlertsFromRootCauses(response.data),
        loading: { ...get().loading, rootCauses: false },
      })
    } catch (error) {
      set({
        loading: { ...get().loading, rootCauses: false },
        error: getErrorMessage(error) || 'Failed to load root-cause events',
      })
    }
  },

  uploadCsv: async (file, filters) => {
    const formData = new FormData()
    formData.append('file', file)
    set({ loading: { ...get().loading, ingest: true }, error: null })

    try {
      const response = await reviewsApi.uploadCsv(formData)
      toast.success(
        `Imported ${response.data.created_count} reviews, skipped ${response.data.duplicate_count} duplicates`,
      )

      set({
        loading: { ...get().loading, ingest: false },
        snapshot: null,
        reviews: [],
        reviewMeta: defaultReviewMeta,
        rootCauses: [],
        alerts: [],
        currentBatchId: response.data.batch_id,
        dashboardCleared: false,
      })
      writeDashboardCleared(false)

      await Promise.all([
        get().fetchSnapshot(filters),
        get().fetchReviews(filters),
        get().fetchRootCauses(),
        get().fetchBatches(),
      ])
    } catch (error) {
      set({ loading: { ...get().loading, ingest: false } })
      toast.error(getErrorMessage(error) || 'CSV upload failed')
    }
  },

  uploadJson: async (file, filters) => {
    const formData = new FormData()
    formData.append('file', file)
    set({ loading: { ...get().loading, ingest: true }, error: null })

    try {
      const response = await reviewsApi.uploadJson(formData)
      toast.success(
        `Imported ${response.data.created_count} reviews, skipped ${response.data.duplicate_count} duplicates`,
      )

      set({
        loading: { ...get().loading, ingest: false },
        snapshot: null,
        reviews: [],
        reviewMeta: defaultReviewMeta,
        rootCauses: [],
        alerts: [],
        currentBatchId: response.data.batch_id,
        dashboardCleared: false,
      })
      writeDashboardCleared(false)

      await Promise.all([
        get().fetchSnapshot(filters),
        get().fetchReviews(filters),
        get().fetchRootCauses(),
        get().fetchBatches(),
      ])
    } catch (error) {
      set({ loading: { ...get().loading, ingest: false } })
      toast.error(getErrorMessage(error) || 'JSON upload failed')
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

  exportReport: async ({ title, filters }) => {
    set({ loading: { ...get().loading, export: true } })

    try {
      const { snapshot, rootCauses, alerts } = get()
      const filename = makeExportFileName('sentimentiq-analysis-report', Date.now(), 'pdf')
      downloadAnalysisPdf({
        filename,
        title: title || 'SentimentIQ Analysis Report',
        snapshot,
        rootCauses,
        alerts,
        filters,
        createdAt: Date.now(),
      })
      toast.success('Analysis PDF exported')
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Export failed')
    } finally {
      set({ loading: { ...get().loading, export: false } })
    }
  },

  fetchBatches: async (search) => {
    set({ historyLoading: true, historyError: null })
    try {
      const response = await reviewsApi.batches({ search })
      set({ history: response.data || [], historyLoading: false })
    } catch (error) {
      set({
        historyLoading: false,
        historyError: getErrorMessage(error) || 'Failed to load batch history',
      })
    }
  },

  selectBatch: (batchId) => {
    const cleared = !batchId ? get().dashboardCleared : false
    writeDashboardCleared(cleared)
    set({ currentBatchId: batchId, dashboardCleared: cleared })
  },

  deleteBatch: async (batchId) => {
    try {
      await reviewsApi.deleteBatch(batchId)
      toast.success('Batch deleted')
      await get().fetchBatches()
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Failed to delete batch')
    }
  },

  rerunBatch: async (batchId) => {
    try {
      await reviewsApi.rerunBatch(batchId)
      toast.success('Batch rerun completed')
      await get().fetchBatches()
    } catch (error) {
      toast.error(getErrorMessage(error) || 'Failed to rerun batch')
    }
  },
}))
