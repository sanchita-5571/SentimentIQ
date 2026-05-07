import { lazy } from 'react'
import { Route, Routes } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout/Layout'
import ErrorBoundary from './components/UI/ErrorBoundary'
import { motion } from 'framer-motion'

const DashboardPage = lazy(() => import('./pages/DashboardPage'))
const RootCausePage = lazy(() => import('./pages/RootCausePage'))
const ReviewsExplorerPage = lazy(() => import('./pages/ReviewsExplorerPage'))
const ReportsPage = lazy(() => import('./pages/ReportsPage'))
const AlertsPage = lazy(() => import('./pages/AlertsPage'))
const SettingsPage = lazy(() => import('./pages/SettingsPage'))

const SentimentTrendsPage = lazy(() => import('./pages/SentimentTrendsPage'))
const HistoryPage = lazy(() => import('./pages/HistoryPage'))

export default function App() {
  return (
    <ErrorBoundary>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Layout />}>
          {}
          <Route
            index
            element={
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                <DashboardPage />
              </motion.div>
            }
          />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="root-cause-analysis" element={<RootCausePage />} />
          <Route path="reviews-explorer" element={<ReviewsExplorerPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="alerts" element={<AlertsPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="sentiment-trends" element={<SentimentTrendsPage />} />
          <Route path="history" element={<HistoryPage />} />
        </Route>
      </Routes>
    </ErrorBoundary>
  )
}
