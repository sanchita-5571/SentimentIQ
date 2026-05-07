import axios from 'axios'
const api = axios.create({
  baseURL: '/api/v1',
})

function getErrorMessage(error) {

  const detail = error?.response?.data?.detail

  if (typeof detail === 'string') {
    return detail
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item
        if (!item) return ''
        if (typeof item === 'object') return item.msg || item.detail || JSON.stringify(item)
        return String(item)
      })
      .filter(Boolean)
      .join(', ')
  }

  if (detail && typeof detail === 'object') {
    return detail.msg || detail.detail || JSON.stringify(detail)
  }

  return error?.message || 'An unexpected error occurred'
}



api.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error)
  },
)



export const dashboardApi = {
  snapshot: (params) => api.get('/dashboard/snapshot', { params }),
}

export const dashboardHistoryApi = {
  store: (payload) => api.post('/dashboard/history/store', payload),
  list: (params) => api.get('/dashboard/history/list', { params }),
}


export const reviewsApi = {
  list: (params) => api.get('/reviews', { params }),
  uploadCsv: (formData) =>
    api.post('/reviews/upload/csv', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  uploadJson: (formData) =>
    api.post('/reviews/upload/json', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  get: (reviewId) => api.get(`/reviews/${reviewId}`),
  batches: (params) => api.get('/reviews/batches', { params }),
  getBatch: (batchId) => api.get(`/reviews/batches/${batchId}`),
  updateBatch: (batchId, payload) => api.put(`/reviews/batches/${batchId}`, payload),
  deleteBatch: (batchId) => api.delete(`/reviews/batches/${batchId}`),
  rerunBatch: (batchId) => api.post(`/reviews/batches/${batchId}/rerun`),
}

export const rootCauseApi = {
  list: (params) => api.get('/root-causes', { params }),
  rebuild: () => api.post('/root-causes/rebuild'),
}

export const reportsApi = {
  export: (payload) =>
    api.post('/reports/export', payload, {
      responseType: 'blob',
    }),
}

export const settingsApi = {
  get: () => api.get('/settings'),
  update: (payload) => api.put('/settings', payload),
}

export { getErrorMessage }
export default api



